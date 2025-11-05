# 🧠 Agentic Second Brain (ASB)

A fully-local, **autonomous personal intelligence system** built in Python.  
Your ASB learns from your notes, projects, reflections, and research — thinking, summarizing, and improving just like a human brain.

> ⚙️ Powered by **Ollama**, **LangChain**, **Chroma**, and **Typer CLI**

---

## 📚 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Setup](#setup)
4. [Environment Variables](#environment-variables)
5. [CLI Usage](#cli-usage)
6. [Phases Implemented](#phases-implemented)
7. [Intelligence Stack](#intelligence-stack)
8. [Autonomous Research (Phase 8)](#autonomous-research-phase8)
9. [Example Flow](#example-flow)
10. [Future Roadmap](#future-roadmap)
11. [Author & License](#author--license)

---

## 🧩 Overview

ASB is your **Agentic Second Brain** — an evolving system that:
- 🧠 Stores and embeds your notes for semantic recall  
- 🪞 Reflects on what you’ve learned  
- 🔄 Self-evaluates and improves its reasoning  
- 🌐 Performs autonomous research  
- 🧩 Compresses and organizes knowledge over time  

Everything runs **locally via Ollama**, ensuring privacy and full offline operation.

---

## 🏗️ Architecture

asb/
├── asb/
│   ├── brain/
│   │   ├── agent.py              # Orchestrates cognition + reasoning
│   │   ├── cognition.py          # Ollama-based thinking module
│   │   ├── memory.py             # Vector memory via Chroma + embeddings
│   │   ├── reflection.py         # Reflection engine (summary + follow-up)
│   │   ├── insight_db.py         # SQLite database for insights
│   │   ├── scheduler.py          # Time-based jobs with timeout
│   │   ├── logger.py             # Persistent daily logs
│   │   ├── self_evaluator.py     # Reflection scoring & feedback
│   │   ├── memory_compressor.py  # Long-term memory consolidation
│   │   ├── ingestion.py          # Context ingestion from Git/Notion/files
│   │   ├── research_agent.py     # Autonomous research & summarization
│   │   └── sources/              # Modular adapters (Git, Notion, Local)
│   ├── main.py                   # Typer CLI entrypoint
│   └── init.py
├── data/
│   ├── notes/
│   ├── reflections/
│   ├── compressed/
│   ├── questions/
│   ├── metrics/
│   ├── logs/
│   └── vector_store/
└── pyproject.toml

---

## ⚙️ Setup

### 1️⃣ Install dependencies
```bash
uv sync

2️⃣ Install & run Ollama

# macOS / Linux
brew install ollama
ollama pull llama3.1:8b
ollama serve

3️⃣ Environment Variables

Create a .env file in your root folder:

DATA_DIR=./data/notes
VECTOR_DIR=./data/vector_store
OLLAMA_MODEL=llama3.1:8b
OLLAMA_EMBED_MODEL=nomic-embed-text
SERPER_API_KEY=your_serper_api_key_here   # optional web search
NOTION_API_KEY=your_notion_api_key_here   # optional


⸻

🧠 CLI Usage

Command	Description
uv run asb ingest	Ingest notes into semantic memory
uv run asb ask "What did I learn about RabbitMQ persistence?"	Query your brain
uv run asb reflect	Generate reflection & follow-up questions
uv run asb schedule -t 1	Run reflection scheduler for 1 hour
uv run asb ingest-all	Ingest from Git, Notion, and markdown sources
uv run asb insights retry	Query stored insights by topic
uv run asb compress -d 14	Compress reflections older than 14 days
uv run asb evaluate -d 7	Score last 7 reflections for quality
uv run asb metrics	Show average reflection scores
uv run asb focus	Suggest next learning directions
uv run asb research -m 3	Auto-research 3 open questions via Ollama
uv run asb logs -d 1	View last day of activity logs


⸻

🔢 Phases Implemented

Phase 1 — Core MVP
	•	Typer CLI + Rich output
	•	ChromaDB vector memory
	•	LLM cognition via Ollama (local) or OpenAI fallback

Phase 2 — Living Memory
	•	Auto-ingestion and reflection system
	•	Knowledge graph creation
	•	Timed jobs via APScheduler

Phase 3 — Self-Reflective Intelligence
	•	Writes reflection files (reflection_YYYY-MM-DD.md)
	•	Generates follow-up questions automatically

Phase 4 — System Awareness
	•	Persistent action logs (data/logs/)
	•	ASB reflects on its own performance

Phase 5 — Contextual Autonomy
	•	Modular source adapters: Git, Notion, Local Files
	•	Unified ingestion: uv run asb ingest-all

Phase 6 — Memory Compression
	•	Summarizes older reflections into key insights
	•	Stores compressed results in DB + /data/compressed

Phase 7 — Cognitive Feedback
	•	Scores reflections (clarity, novelty, redundancy)
	•	Tracks metrics in /data/metrics/self_scores.csv
	•	Suggests new focus areas via uv run asb focus

Phase 8 — Autonomous Research (Ollama-powered)
	•	Reads open questions from /data/questions/open_questions.md
	•	Uses Ollama for reasoning and summarization
	•	Optional web-search snippets via SERPER_API_KEY
	•	Stores findings in both Insight DB and vector memory
	•	Triggers automatic post-research reflection

⸻

🧬 Autonomous Research (Phase 8)

🔧 Configuration

.env

OLLAMA_MODEL=llama3.1:8b
SERPER_API_KEY=optional

🔍 Run Research

uv run asb research -m 2

Output:

🔎 Researching: How does CPU affinity impact RPC performance?
🧠 New insight added to long-term memory.
🔎 Researching: What retry strategies improve persistence?
🧠 New insight added to long-term memory.
✅ Research cycle complete — 2 questions processed.
🪞 Initiating post-research reflection...
✨ Reflection after research completed.

💡 What Happens
	1.	Pulls open questions → performs web search (optional).
	2.	Summarizes findings locally using Ollama LLM.
	3.	Writes them into:
	•	insight_db (structured memory)
	•	Chroma vector store (semantic recall)
	4.	Triggers reflection to integrate new learnings.

⸻

🧠 Intelligence Stack

Layer	Implementation
Reasoning	Ollama LLM (llama3.1:8b, phi3, etc.)
Embeddings	Local HuggingFace or Ollama embeddings
Memory	ChromaDB vector store
Long-term storage	SQLite (insight_db.py)
Reflection	ReflectionEngine (summarization + questioning)
Evaluation	SelfEvaluator (clarity, novelty, redundancy)
Compression	MemoryCompressor (long-term summarization)
Research	ResearchAgent (Ollama-based summarization + web search)


⸻

🧩 Example Flow

# 1. Ingest notes
uv run asb ingest

# 2. Reflect on learnings
uv run asb reflect

# 3. Compress old reflections
uv run asb compress -d 14

# 4. Self-evaluate reflections
uv run asb evaluate -d 7
uv run asb metrics

# 5. Auto-research open questions
uv run asb research -m 3

# 6. Review new insights
uv run asb insights research


⸻

🚀 Future Roadmap

Phase 9 — Insight Dashboard
	•	Streamlit-based visualization
	•	Reflection timelines, scores, and knowledge graph

Phase 10 — Emotional Context Modeling
	•	Track tone, stress, and motivation in reflections

Phase 11 — Continuous Learning
	•	Real-time integration with GitHub activity, papers, and notes

⸻

🧑‍💻 Author

Chitrank Dixit
Building an evolving, privacy-first AI system that learns alongside its creator.

⸻

🧾 License

MIT License © 2025 Chitrank Dixit

“Your second brain should think with you, not for you.”

---

Would you like me to add optional **badges** (Python | Ollama | LangChain | Made with uv) and a **project banner header** so the README looks fully production-ready for GitHub?