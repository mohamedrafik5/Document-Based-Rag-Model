# import os
# import yaml
# from sentence_transformers import SentenceTransformer
# import faiss
# from pypdf import PdfReader
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq

# from dotenv import load_dotenv
# load_dotenv()
# from langchain_community.embeddings import HuggingFaceEmbeddings
# class LoadConfig:
#     def __init__(self):
#         self.root_dir = os.path.abspath(
#             os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
#         )

#         self.config_path = os.path.join(self.root_dir, "RagModel", "config", "config.yaml")

#         with open(self.config_path, "r") as file:
#             self.config = yaml.safe_load(file)

#         # Load YAML values
#         self._load_config()
#         load_dotenv()
#         # Load components: embedder, FAISS, PDFs
#         self.embed_model = self._load_embedding_model()
#         self.llm = self._load_openai_model()

#     # ------------------------------------
#     # YAML Config Loader  
#     # ------------------------------------
#     def _load_config(self):

#         self.llm_model_name = self.config["gemini"]["model_name"]
#         self.embedding_model_name = self.config["embedding"]["model_name"]

#         self.faiss_dir = self.config["faiss"]["faiss_path"]

#         self.pdf_path = self.config["files"]["pdf_path"]
#         self.hash_file_path = self.config["files"]["hash_file_path"]

#         chunk = self.config["chunking"]
#         self.chunking_enabled = chunk["enabled"]
#         self.chunk_size = chunk["chunk_size"]
#         self.chunk_overlap = chunk["overlap"]

#         self.prompt = self.config["prompt"]

#     # ------------------------------------
#     # Load Embedding Model
#     # ------------------------------------
#     def _load_embedding_model(self):
#         return HuggingFaceEmbeddings(
#     model_name=self.embedding_model_name,
#     model_kwargs={"device": "cpu"}  # or "cuda"
# )


#     def _load_openai_model(self):
#         """
#         Loads an OpenAI model using LangChain's ChatOpenAI wrapper.
#         Verifies API key + model availability by running a 1-token test call.
#         """
#         try:
#             llm = ChatGroq(
#                 model=self.llm_model_name,
#                 temperature=0.0,
#                 max_retries=1,
#                 api_key=os.getenv("GROQ_API_KEY"),
#             )

#             # ---- SELF TEST CALL ----
#             # try:
#             #     test_response = llm.invoke("ping")
#             #     if not test_response:
#             #         raise RuntimeError("Empty response received from test LLM call.")

#             # except Exception as inner:
#             #     raise RuntimeError(
#             #         f"OpenAI model loaded but failed test call. "
#             #         f"Check API key, model name, or usage limits. Details: {inner}"
#             #     )

#             return llm

#         except Exception as e:

#             raise RuntimeError(f"Failed to initialize model: {e}")

    # ------------------------------------
    # Load PDFs as text chunks
    # ------------------------------------
    # def _load_pdf_chunks(self):
    #     chunks = []
    #     for filename in os.listdir(self.pdf_folder):
    #         if filename.endswith(".pdf"):
    #             reader = PdfReader(os.path.join(self.pdf_folder, filename))
    #             text = "\n".join(page.extract_text() for page in reader.pages)
    #             chunks.append(text)
    #     return chunks

    








import os
import yaml
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.embeddings import SentenceTransformerEmbeddings

load_dotenv()


class LoadConfig:
    _instance = None   # <-- SINGLETON INSTANCE

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoadConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Prevent reinitialization on multiple imports
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.root_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
        )

        self.config_path = os.path.join(self.root_dir, "RagModel", "config", "config.yaml")

        with open(self.config_path, "r") as file:
            self.config = yaml.safe_load(file)

        # Load YAML keys
        self._load_config()

        # Load models only ONCE
        self.embed_model = self._load_embedding_model()
        self.llm = self._load_llm()

        self._initialized = True  # <-- mark as initialized


    # ---------- CONFIG LOADING ----------
    def _load_config(self):
        print("-----LOADING CONFIG-----")
        # IMPORTANT: Make this "groq"
        self.llm_model_name = self.config["gemini"]["model_name"]
        self.embedding_model_name = self.config["embedding"]["model_name"]

        self.faiss_dir = self.config["faiss"]["faiss_path"]
        self.pdf_path = self.config["files"]["pdf_path"]
        self.hash_file_path = self.config["files"]["hash_file_path"]

        chunk = self.config["chunking"]
        self.chunk_size = chunk["chunk_size"]
        self.chunk_overlap = chunk["overlap"]

        prompt = self.config["prompts"]
        self.main_prompt = prompt["main_prompt"]
        self.refiner_prompt = prompt["refiner_prompt"]

    # ---------- EMBEDDINGS ----------
    def _load_embedding_model(self):
        return SentenceTransformerEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={"device": "cpu"}
        )


    # ---------- LLM ----------
    def _load_llm(self):
        try:
            llm = ChatGroq(
                model=self.llm_model_name,
                temperature=0,
                max_retries=1,
                api_key=os.getenv("GROQ_API_KEY")
            )
            # ---- SELF TEST CALL ----
            try:
                test_response = llm.invoke("ping")
                if not test_response:
                    raise RuntimeError("Empty response received from test LLM call.")

            except Exception as inner:
                raise RuntimeError(
                    f"OpenAI model loaded but failed test call. "
                    f"Check API key, model name, or usage limits. Details: {inner}"
                )


            return llm
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {e}")
