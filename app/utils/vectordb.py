import chromadb
from chromadb.config import Settings
from typing import List, Dict

class VectorDB:
    def __init__(self, persist_dir: str = "./data/chroma"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection("pdf_chunks")

    def add_chunks(self, chunks: List[Dict]):
        """
        Add chunks with embeddings & metadata into ChromaDB
        """
        ids = [c["id"] for c in chunks]
        texts = [c["text"] for c in chunks]
        metadatas = [{"page_number": c["page_number"]} for c in chunks]

        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )

    def query(self, embedding_fn, query: str, top_k: int = 3):
        """
        Query the collection using an embedding function
        """
        query_vec = embedding_fn([query])[0]

        results = self.collection.query(
            query_embeddings=[query_vec],
            n_results=top_k
        )

        # Format results
        retrieved = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            retrieved.append({
                "page_number": meta["page_number"],
                "text": doc
            })
        return retrieved
