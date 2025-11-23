# from fastapi import FastAPI
# from pydantic import BaseModel

# from utils.load_config import LoadConfig
# from core.model_invoking import ModelInvoker

# # Load config & models at startup
# cfg = LoadConfig()
# llm = ModelInvoker(cfg)

# app = FastAPI(title="RAG LLM API", version="1.0")


# # Request body structure
# class QueryRequest(BaseModel):
#     query: str


# @app.post("/generate")
# def generate_text(request: QueryRequest):
#     response = llm.generate(request.query)
#     return {"response": response}


# @app.get("/")
# def home():
#     return {
#         "status": "running",
#         "app": cfg.app_name,
#         "model": cfg.llm_model_name
#     }


from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from RagModel.utils.file_utils import PDFManager
from RagModel.core.model_invoking import ModelInvoker

router = APIRouter()
pdf_mgr = PDFManager()
model = ModelInvoker()


class QueryRequest(BaseModel):
    question: str


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    result = pdf_mgr.save_and_trigger_db(file)
    return result


@router.post("/query")
async def query_rag(req: QueryRequest):
    try:
        print("-----USER QUESTION-----")
        print(req.question)
        answer = model.query(user_prompt=req.question)
        return {"question": req.question, "answer": answer}
    except Exception as e:
        return {
            "error": str(e),
            "message": "Upload a PDF first."
        }
