import os
import shutil
from typing import Optional

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from RagModel.utils.load_config import LoadConfig 

class VectorDBManager:
    _instance = None  # <-- Singleton storage

    def __new__(cls, *args, **kwargs):
        # Always return the same instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Avoid running __init__ multiple times
        if hasattr(self, "_initialized") and self._initialized:
            return

        self._initialized = True

        # Load config + components
        self.config = LoadConfig()
        self.embed_model = self.config.embed_model

        # Paths from YAML
        self.index_dir = self.config.faiss_dir
        self.pdf_path = self.config.pdf_path

        # Chunk config
        self.chunk_size = self.config.chunk_size
        self.chunk_overlap = self.config.chunk_overlap

        # Local state
        self.vectorstore: Optional[FAISS] = None

    # ------------------------------------------------
    # Build or rebuild vectors from PDF
    # ------------------------------------------------
    def build_vectorstore(self, pdf_path: Optional[str] = None) -> FAISS:
        # Flush in-memory vectorstore
        self.vectorstore = None

        pdf_file = pdf_path or self.pdf_path

        if not os.path.exists(pdf_file):
            raise FileNotFoundError(f"PDF not found: {pdf_file}")

        loader = PyPDFLoader(pdf_file)
        docs = loader.load()

        if not docs:
            raise ValueError("PDF contains no readable text.")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_documents(docs)

        if not chunks:
            raise ValueError("Text split failed — empty chunks generated.")

        texts = [c.page_content for c in chunks]

        embeddings = self.embed_model.embed_documents(texts)

        # Remove old DB
        if os.path.exists(self.index_dir):
            shutil.rmtree(self.index_dir)

        # Build new FAISS store
        vectorstore = FAISS.from_embeddings(
            text_embeddings=list(zip(texts, embeddings)),
            embedding=self.embed_model
        )

        vectorstore.save_local(self.index_dir)

        # Keep only disk version; do not load into RAM yet
        self.vectorstore = None

        return vectorstore

    # ------------------------------------------------
    # Load existing FAISS DB
    # ------------------------------------------------
    def load_vectorstore(self) -> Optional[FAISS]:
        if not os.path.exists(self.index_dir):
            return None

        try:
            self.vectorstore = FAISS.load_local(
                self.index_dir,
                self.embed_model,
                allow_dangerous_deserialization=True
            )
            return self.vectorstore

        except Exception as e:
            print(f"❌ Failed to load FAISS index: {e}")
            return None

    # ------------------------------------------------
    # Query stored DB
    # ------------------------------------------------
    def query(self, query_text: str, k: int = 3):
        if self.vectorstore is None:
            print("^^^^^^^^^^^^ LOADING VECTORSTORE FROM DISK ^^^^^^^^^^^^")
            self.load_vectorstore()

        if self.vectorstore is None:
            raise RuntimeError("Vector store is not ready. Build or load index first.")

        return self.vectorstore.similarity_search(query_text, k=k)

