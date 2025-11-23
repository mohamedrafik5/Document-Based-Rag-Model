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
