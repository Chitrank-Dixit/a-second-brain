# asb/brain/research_agent.py
import os
import requests
from dotenv import load_dotenv
from asb.brain.agent import ASBAgent
from asb.brain.memory import Memory
from asb.brain.reflection import ReflectionEngine
from asb.brain.insight_db import InsightDB
from langchain_ollama import OllamaLLM
import subprocess
load_dotenv()

def is_ollama_available():
    try:
        subprocess.run(["ollama", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
        return True
    except Exception:
        return False


class ResearchAgent:
    def __init__(self, model_name: str = None):
        if not is_ollama_available():
            raise RuntimeError("⚠️ Ollama not running. Start with `ollama serve` before using ResearchAgent.")
        self.model_name = model_name or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.llm = OllamaLLM(model=self.model_name)
        self.agent = ASBAgent()
        self.db = InsightDB()
        self.memory = Memory()
        self.reflection_engine = ReflectionEngine()

        

    def _summarize_with_llm(self, text: str) -> str:
        """Summarize content using Ollama LLM."""
        prompt = f"Summarize the following information into concise factual insights:\n{text}"
        return self.llm.invoke(prompt)

    def research_question(self, question: str):
        """Search, summarize, and store new findings using Ollama."""
        print(f"🔎 Researching: {question}")

        # Try web search first
        serper_key = os.getenv("SERPER_API_KEY")
        if serper_key:
            try:
                url = f"https://serpapi.com/search.json?q={question.replace(' ', '+')}&api_key={serper_key}"
                response = requests.get(url, timeout=10)
                data = response.json()
                snippets = " ".join([r.get("snippet", "") for r in data.get("organic_results", [])[:5]])
                if snippets.strip():
                    results = self._summarize_with_llm(snippets)
                else:
                    results = self._summarize_with_llm(f"No results found for {question}")
            except Exception as e:
                print(f"⚠️ Web search failed ({e}). Falling back to internal reasoning.")
                results = self.llm.invoke(f"Generate a short factual summary about: {question}")
        else:
            # No web access → reasoning-only research
            results = self.llm.invoke(f"Explain the key concepts behind: {question}")

        # Store to Insight DB
        self.db.add_insight(topic="research", question=question, answer=results, tags=["research", "auto"])

        # Add to semantic memory
        self.memory.collection.add(
            documents=[results],
            metadatas=[{"source": "auto_research", "question": question}],
            ids=[f"research_{hash(question)}"]
        )

        print("🧠 New insight added to long-term memory.")
        return results

    def run_autonomous_research(self, max_questions: int = 3):
        """Auto-select unanswered questions, research them, and trigger reflection."""
        open_q_file = "./data/questions/open_questions.md"
        if not os.path.exists(open_q_file):
            print("No open questions found.")
            return

        with open(open_q_file) as f:
            questions = [q.strip("- ").strip() for q in f if q.strip()]

        researched = []
        for q in questions[:max_questions]:
            ans = self.research_question(q)
            researched.append((q, ans[:200] + "..."))

        print(f"✅ Research cycle complete — {len(researched)} questions processed.")
        print("🪞 Initiating post-research reflection...")
        self.reflection_engine.reflect()
        print("✨ Reflection after research completed.")