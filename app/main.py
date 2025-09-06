from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import shutil

# from app.services.pdf_service import extract_pages
from app.services.pdf_service import extract_pages
from app.utils.chunker import chunk_pages
from app.services.rag_service import index_pdf_chunks, query_pdf_with_llm
from app.services.llm_service import LLMService

app = FastAPI()

UPLOAD_DIR = "./data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "The flask API server is running ..."}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload PDF → extract text → chunk → index into ChromaDB
    """
    print("This is the file and filename" ,file.filename)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # save file locally
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # parse + chunk
    pages = extract_pages(file_path)
    chunks = chunk_pages(pages, max_chars=500, overlap=100)

    # index in Chroma
    index_pdf_chunks(chunks)

    return {"status": "success", "filename": file.filename, "chunks_indexed": len(chunks)}

@app.get("/ask")
def ask_llm(q: str):
    print("This is the query : ", q)
    answer = query_pdf_with_llm(question=q)
    return {"query": q, "answer": answer}