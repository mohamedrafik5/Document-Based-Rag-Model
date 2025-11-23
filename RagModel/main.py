from fastapi import FastAPI
from RagModel.api.endpoint import router
import uvicorn

main_app = FastAPI(
    title="RagChat bot",
    description="A FastAPI service that generate text with rag using a Transformer model.",
    version="1.0.0"
)

# include router instead of mount
main_app.include_router(router, prefix="/rag")

# Uvicorn entry point
if __name__ == "__main__":
    uvicorn.run( "RagModel.main:main_app", host="127.0.0.1", port=8000)

    # python -m RagModel.main