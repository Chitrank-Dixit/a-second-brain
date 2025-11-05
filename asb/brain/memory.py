# asb/brain/memory.py
import os
import subprocess
import chromadb
from dotenv import load_dotenv
from asb.brain.embeddings import get_embedding_model

load_dotenv()

def is_ollama_running() -> bool:
    """Check if Ollama server is running locally."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


class Memory:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("asb_memory")
        self.data_dir = os.getenv("DATA_DIR", "./data/notes")

        self.embedding_model = get_embedding_model()

    def ingest_notes(self):
        for file in os.listdir(self.data_dir):
            if file.endswith(".md") or file.endswith(".txt"):
                path = os.path.join(self.data_dir, file)
                with open(path, "r") as f:
                    content = f.read()
                self.collection.add(
                    documents=[content],
                    ids=[file]
                )
        print("✅ Notes ingested into memory")

    def query(self, text, top_k=3):
        results = self.collection.query(
            query_texts=[text],
            n_results=top_k
        )
        return results["documents"][0]