from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uvicorn

# from app.services.pdf_service import extract_pages
from app.services.pdf_service import extract_pages
from app.utils.chunker import chunk_pages
from app.services.rag_service import index_pdf_chunks, query_pdf_with_llm
from app.services.llm_service import LLMService

app = FastAPI()

# allow your React frontend (Vite dev server runs on 5173)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # frontend URLs
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods (including OPTIONS)
    allow_headers=["*"],         # allow all headers
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

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