from app.utils.vectordb import VectorDB
from app.utils.embeddings import Embedder
from app.services.llm_service import LLMService

vector_db = VectorDB()
embedder = Embedder()
llm = LLMService()

def index_pdf_chunks(chunks):
    """Add chunks (with id, text, page_number) to Chroma"""
    # Drop the collection entirely
    vector_db.client.delete_collection("pdf_chunks")

    # Recreate the collection
    vector_db.collection = vector_db.client.get_or_create_collection("pdf_chunks")

    vector_db.add_chunks(chunks)

def query_pdf_with_llm(question: str, top_k: int = 3):
    """
    1. Retrieve top chunks
    2. Send to LLM with context
    3. Return answer + citations
    """
    # Retrieve top chunks from Chroma
    retrieved_chunks = vector_db.query(embedder.embed, question, top_k=top_k)

    # Prepare context with page numbers
    context = "\n".join([f"(Page {c['page_number']}): {c['text']}" for c in retrieved_chunks])

    # Send to LLM
    prompt = f"Answer the following question using the context below. Include citations for each part of your answer:\n\nContext:\n{context}\n\nQuestion: {question}"
    answer = llm.generate(prompt)

    # Return answer + citations for frontend
    return {
        "question": question,
        "answer": answer,
        "citations": [{"page_number": c["page_number"], "text": c["text"][:200]} for c in retrieved_chunks]
    }
