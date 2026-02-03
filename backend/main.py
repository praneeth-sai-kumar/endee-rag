from fastapi import FastAPI
from fastapi import UploadFile, File
import shutil
import os

from pydantic import BaseModel
from typing import List

from backend.rag import RAGRetriever

app = FastAPI(
    title="Endee RAG API",
    description="Semantic Search / RAG backend using Endee Vector Database",
    version="1.0.0"
)

rag = RAGRetriever()


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


class RetrievedChunk(BaseModel):
    score: float | None
    text: str | None
    source: str | None


class QueryResponse(BaseModel):
    results: List[RetrievedChunk]


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Endee RAG API is running"}


@app.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    results = rag.retrieve(request.question)

    return {
        "results": results[: request.top_k]
    }
DATA_DIR = "data"


@app.post("/ingest")
def ingest_file(file: UploadFile = File(...)):
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Save uploaded file
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Trigger ingestion
    from backend.ingest import ingest_documents
    ingest_documents()

    return {
        "status": "success",
        "message": f"File '{file.filename}' ingested successfully"
    }

