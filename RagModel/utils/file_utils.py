import os
import hashlib
from fastapi import UploadFile

from RagModel.utils.load_config import LoadConfig
from RagModel.utils.db_manager import VectorDBManager


class PDFManager:
    def __init__(self):
        self.config = LoadConfig()

        # Paths from config.yaml
        self.pdf_path = self.config.pdf_path
        self.hash_file_path = self.config.hash_file_path

        # FAISS DB manager
        self.db = VectorDBManager()

        # Ensure folder exists
        os.makedirs(os.path.dirname(self.pdf_path), exist_ok=True)

    @staticmethod
    def compute_hash(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def save_and_trigger_db(self, file: UploadFile) -> dict:
        """
        Saves PDF if changed and rebuilds FAISS DB if needed.
        Returns a dict with details.
        """

        if not file.filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are supported.")

        file_bytes = file.file.read()
        new_hash = self.compute_hash(file_bytes)

        # Check if same file was already uploaded
        if os.path.exists(self.hash_file_path):
            with open(self.hash_file_path, "r") as f:
                old_hash = f.read().strip()

            if new_hash == old_hash:
                return {
                    "status": "no_change",
                    "message": "Same PDF. No reindexing.",
                    "pdf_path": self.pdf_path,
                }

        # Save PDF
        with open(self.pdf_path, "wb") as f:
            f.write(file_bytes)

        # Save new hash
        with open(self.hash_file_path, "w") as f:
            f.write(new_hash)

        # Auto-rebuild FAISS index
        self.db.build_vectorstore(self.pdf_path)

        return {
            "status": "updated",
            "message": "New PDF uploaded. FAISS index rebuilt.",
            "pdf_path": self.pdf_path
        }
