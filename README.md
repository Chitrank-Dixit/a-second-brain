# 🧠 Agentic Second Brain (ASB)

A fully-local, **autonomous cognitive system** that learns, reflects, evaluates, and researches — powered by **Ollama**, **LangChain**, **LangGraph**, and **Streamlit**.  
Your ASB evolves like a real mind: it thinks, improves, and visualizes its growth.

> “Your second brain should think *with* you, not *for* you.” — Chitrank Dixit

---

## 🧩 Overview

ASB is a modular **agentic framework** for personal knowledge management and reasoning.  
It can:

- 🧠 Ingest and embed notes or external context (Git, Notion, Markdown)  
- 🪞 Reflect on learning and generate new questions  
- 🔍 Conduct autonomous research via Ollama LLM  
- 📊 Evaluate reflection quality and cognitive trends  
- 🧩 Compress memory for long-term insight  
- 🕸 Visualize your thoughts and relationships in a Streamlit dashboard  
- 🔁 Automate the entire loop using **LangGraph** workflows

---

## 🏗️ Architecture

asb/
├── asb/
│   ├── brain/
│   │   ├── agent.py              # Cognition layer (LLM orchestration)
│   │   ├── cognition.py          # Ollama reasoning interface
│   │   ├── memory.py             # Vector store (Chroma)
│   │   ├── reflection.py         # Reflection + question generation
│   │   ├── research_agent.py     # Autonomous research (Ollama + web)
│   │   ├── self_evaluator.py     # Reflection scoring
│   │   ├── memory_compressor.py  # Long-term summarization
│   │   ├── insight_db.py         # SQLite insight store
│   │   ├── ingestion.py          # Context ingestion from sources
│   │   ├── automation_graph.py   # LangGraph workflow automation
│   │   └── sources/              # Git / Notion / Files adapters
│   ├── dashboard.py              # Streamlit visualization app
│   ├── main.py                   # Typer CLI entrypoint
│   └── init.py
├── data/
│   ├── notes/ reflections/ compressed/ questions/
│   ├── metrics/ logs/ vector_store/
│   └── insights.db
└── pyproject.toml

---

## ⚙️ Setup

### 1️⃣ Dependencies

```bash
uv sync

2️⃣ Install & run Ollama

brew install ollama
ollama pull llama3.1:8b
ollama serve

3️⃣ Environment

Create .env:

DATA_DIR=./data/notes
VECTOR_DIR=./data/vector_store
OLLAMA_MODEL=llama3.1:8b
OLLAMA_EMBED_MODEL=nomic-embed-text
SERPER_API_KEY=optional_web_api_key
NOTION_API_KEY=optional_notion_key


⸻

🧠 CLI Commands

Command	Description
uv run asb ingest	Ingest local notes
uv run asb reflect	Generate reflection + new questions
uv run asb evaluate -d 7	Evaluate reflection quality
uv run asb metrics	Display average scores
uv run asb compress -d 14	Summarize old reflections
uv run asb ingest-all	Ingest from Git, Notion, files
uv run asb research -m 3	Auto-research 3 questions (Ollama)
uv run asb logs -d 1	View last day of logs
uv run asb focus	Suggest next learning directions
uv run asb automate	Run full LangGraph cognitive loop
uv run streamlit run asb/dashboard.py	Launch dashboard


⸻

🔢 Phases Implemented

Phase 1 – Core MVP

Typer CLI · Chroma memory · Ollama LLM reasoning.

Phase 2 – Living Memory

Automatic ingestion · Reflection scheduling.

Phase 3 – Self-Reflective Intelligence

Daily reflections + follow-up question generation.

Phase 4 – System Awareness

Persistent logs · log-reflect for meta-insight.

Phase 5 – Contextual Autonomy

Adapters for Git / Notion / Files → ingest-all.

Phase 6 – Memory Compression

Summarizes 14-day-old reflections to /data/compressed.

Phase 7 – Cognitive Feedback

Self-evaluation (clarity / novelty / redundancy) + focus suggestions.

Phase 8 – Autonomous Research

Ollama-based research agent with optional web search.
Stores results in Insight DB + vector memory + triggers post-research reflection.

Phase 9 – Visual Insight Dashboard

Streamlit UI for reflections, metrics, tags, semantic search, and knowledge graph.

⸻

🧩 LangGraph Integration (Automation Loop)

🚀 Goal

Automate your cognitive pipeline:

reflect → evaluate → research → compress → repeat

🧠 Workflow

asb/brain/automation_graph.py

from langgraph.graph import Graph, END
from asb.brain.reflection import ReflectionEngine
from asb.brain.self_evaluator import SelfEvaluator
from asb.brain.research_agent import ResearchAgent
from asb.brain.memory_compressor import MemoryCompressor

def reflect(_): ReflectionEngine().reflect(); return {"stage": "reflected"}
def evaluate(_): SelfEvaluator().evaluate_recent_reflections(7); return {"stage": "evaluated"}
def research(_): ResearchAgent().run_autonomous_research(2); return {"stage": "researched"}
def compress(_): MemoryCompressor().compress_old_reflections(14); return {"stage": "compressed"}

graph = Graph()
graph.add_node("reflect", reflect)
graph.add_node("evaluate", evaluate)
graph.add_node("research", research)
graph.add_node("compress", compress)
graph.set_entry_point("reflect")
graph.add_edge("reflect", "evaluate")
graph.add_edge("evaluate", "research")
graph.add_edge("research", "compress")
graph.add_edge("compress", END)
workflow = graph.compile()

Run:

uv run asb automate

Output:

🪞 Running reflection...
📊 Evaluating reflections...
🔎 Conducting autonomous research...
🧩 Compressing memory...
✅ ASB cognitive loop complete!

⏰ Optional Scheduling

Integrate with apscheduler for daily or weekly self-runs:

scheduler.add_job(lambda: workflow.invoke({}), 'interval', days=1)


⸻

🧠 Dashboard Highlights (Phase 9)

Run:

uv run streamlit run asb/dashboard.py

Features:
	•	🧩 Recent Insights panel
	•	📊 Reflection quality trends
	•	🕰 Reflection timeline reader
	•	🏷 Tag frequency bars
	•	🔍 Semantic search (via Chroma)
	•	🕸 Interactive knowledge graph (NetworkX + PyVis)
	•	📈 Insight analytics (topics & frequency)

⸻

🧬 Intelligence Stack

Layer	Implementation
Reasoning	Ollama LLM (llama3.1:8b, phi3, etc.)
Memory	Chroma vector store + SQLite Insight DB
Reflection	Autonomous summarization + question generation
Evaluation	SelfEvaluator (clarity / novelty / redundancy)
Compression	Memory Compressor (long-term summaries)
Research	Ollama ResearchAgent + optional SERPER API
Visualization	Streamlit Dashboard + Plotly + PyVis
Automation	LangGraph workflow orchestrator


⸻

🧩 Example End-to-End Run

uv run asb ingest
uv run asb reflect
uv run asb evaluate -d 7
uv run asb research -m 3
uv run asb compress
uv run asb automate        # Full LangGraph loop
uv run streamlit run asb/dashboard.py


⸻

🚀 Future Phases

Phase 10 – Emotional & Context Modeling

Sentiment + tone analysis of reflections; emotional trend visualization.

Phase 11 – Multi-Agent Coordination

Specialized sub-agents (Reflector, Researcher, Evaluator, Archivist) communicating via LangGraph shared memory.

⸻

🧑‍💻 Author

Chitrank Dixit — Building an evolving, privacy-first AI that learns alongside its creator.

⸻

🧾 License

MIT License © 2025 Chitrank Dixit

⸻

🧠 “From notes to knowledge to wisdom — autonomously.”

---

Would you like me to add **GitHub-ready badges + screenshots section** (Python | Ollama | LangChain | Streamlit | LangGraph) so your README looks polished for public release?