# brain/cognition.py
import os
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv

load_dotenv()

class Cognition:
    def __init__(self):
        model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.llm = OllamaLLM(model=model)

    def think(self, query, context):
        context_str = "\n".join(context)
        prompt = f"""You are Chitrank's Second Brain.

Context:
{context_str}

Question:
{query}

Give a concise, insightful answer, referring only to the context."""
        response = self.llm.invoke(prompt)
        return response