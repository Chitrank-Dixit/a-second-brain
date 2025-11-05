# main.py
import typer
from rich.console import Console
from asb.brain.agent import ASBAgent
from asb.brain.reflection import ReflectionEngine
from asb.brain.graph import KnowledgeGraph
from asb.brain.scheduler import start_daily_reflection
from asb.brain.insight_db import InsightDB
from asb.brain.logger import setup_logger
from datetime import datetime, timedelta
from asb.brain.sources.git_adapter import GitAdapter
from asb.brain.sources.files_adapter import FilesAdapter
from asb.brain.sources.notion_adapter import NotionAdapter
from asb.brain.ingestion import ContextIngestor
from asb.brain.memory_compressor import MemoryCompressor
import glob
from asb.brain.scheduler import start_weekly_compression
from asb.brain.self_evaluator import SelfEvaluator
from asb.brain.research_agent import ResearchAgent
from asb.brain.automation_graph import workflow
log = setup_logger()

app = typer.Typer()
console = Console()
agent = ASBAgent()

@app.command()
def ingest():
    console.print("[green]Ingesting notes into memory...[/green]")
    agent.memory.ingest_notes()
    console.print("[cyan]Done![/cyan]")

@app.command()
def ask(query: str):
    console.print(f"[bold blue]You:[/bold blue] {query}")
    response = agent.ask(query)
    console.print(f"[bold green]ASB:[/bold green] {response}")

@app.command()
def reflect():
    """Generate a reflection summary of your notes."""
    engine = ReflectionEngine()
    summary = engine.reflect()
    console.print(f"[bold green]{summary}[/bold green]")

@app.command()
def related(concept: str):
    """Find concepts related to a keyword."""
    graph = KnowledgeGraph()
    graph.build()
    related = graph.related(concept)
    console.print(f"[yellow]{concept}[/yellow] → {related}")

@app.command()
def schedule(timeout_hours: float = typer.Option(1.0, "--timeout-hours", "-t", help="How many hours to run before stopping")):
    """Start the daily reflection job with an optional timeout (in hours)."""
    start_daily_reflection(timeout_hours)

@app.command()
def insights(topic: str):
    """Query past insights related to a topic."""
    db = InsightDB()
    rows = db.query_by_topic(topic)
    if not rows:
        console.print(f"[red]No insights found on topic '{topic}'.[/red]")
        return
    console.print(f"[bold cyan]Insights about {topic}[/bold cyan]")
    for date, q, a, tags in rows:
        console.print(f"[yellow]{date}[/yellow]: {q}")
        console.print(f"[green]{a}[/green]\nTags: {tags}\n")

@app.command()
def logs(days: int = typer.Option(1, "--days", "-d", help="Days of logs to view")):
    """View or summarize recent ASB logs."""
    console = Console()
    cutoff = datetime.now() - timedelta(days=days)
    files = sorted(glob.glob("./data/logs/asb_*.log"))
    if not files:
        console.print("[red]No log files found.[/red]")
        return
    for file in files[-days:]:
        console.print(f"[bold cyan]{file}[/bold cyan]")
        with open(file) as f:
            console.print(f.read())

@app.command()
def log_reflect(days: int = typer.Option(1, "--days", "-d", help="Days of logs to analyze")):
    """Ask ASB to analyze its recent log activity."""
    from asb.brain.agent import ASBAgent
    import glob
    cutoff_logs = sorted(glob.glob("./data/logs/asb_*.log"))[-days:]
    text = ""
    for file in cutoff_logs:
        with open(file) as f:
            text += f.read() + "\n"
    agent = ASBAgent()
    summary = agent.ask(f"Summarize key activities, successes, and issues in these logs:\n{text}")
    console.print(f"[green]{summary}[/green]")

@app.command()
def ingest_git(repo_path: str = typer.Option("./data/external_notes", "--repo-path", "-r", help="Path to Git repository")):
    """Ingest from Git commits."""
    adapter = GitAdapter(repo_path)
    entries = adapter.fetch_entries()
    console.print(f"[green]Ingested {len(entries)} entries from Git.[/green]")

@app.command()
def ingest_files(repo_path: str = typer.Option("./data/external_notes", "--repo-path", "-r", help="Path to Git repository")):
    """Ingest from local files."""
    adapter = FilesAdapter(repo_path)
    entries = adapter.fetch_entries()
    console.print(f"[green]Ingested {len(entries)} entries from files.[/green]")

@app.command()
def ingest_notion():
    """Ingest from Notion."""
    adapter = NotionAdapter()
    entries = adapter.fetch_entries()
    console.print(f"[green]Ingested {len(entries)} entries from Notion.[/green]")

@app.command()
def ingest_all():
    """Ingest from all connected sources (Git, local notes, etc.)."""
    ingestor = ContextIngestor()
    ingestor.ingest_all()


@app.command()
def compress(days: int = typer.Option(14, "--days", "-d", help="Compress reflections older than N days")):
    """Summarize and compress old reflections into key insights."""
    compressor = MemoryCompressor()
    compressor.compress_old_reflections(days)

@app.command()
def schedule_compression():
    """Start the weekly compression job."""
    start_weekly_compression()

@app.command()
def evaluate(days: int = typer.Option(7, "--days", "-d", help="Days of reflections to evaluate")):
    """Evaluate recent reflections for quality & novelty."""
    evaluator = SelfEvaluator()
    evaluator.evaluate_recent_reflections(days)

@app.command()
def metrics():
    """Show average self-evaluation metrics."""
    evaluator = SelfEvaluator()
    evaluator.summarize_scores()

@app.command()
def focus():
    """Suggest next learning focus areas."""
    agent = ASBAgent()
    evaluator = SelfEvaluator()
    with open(evaluator.scores_file) as f:
        logs = f.read()
    suggestion = agent.ask(
        f"Based on these self-evaluation logs, suggest 3 learning areas I should focus on next:\n{logs}"
    )
    console.print(f"[green]{suggestion}[/green]")

@app.command()
def research(max_questions: int = typer.Option(3, "--max", "-m", help="Number of open questions to research")):
    """Autonomously research unanswered questions."""
    ra = ResearchAgent()
    ra.run_autonomous_research(max_questions)

@app.command()
def schedule_research():
    """Start weekly autonomous research."""
    from asb.brain.scheduler_research import start_weekly_research
    start_weekly_research()

@app.command()
def automate():
    """Run the full ASB cognitive automation loop."""
    print("🚀 Starting autonomous ASB loop via LangGraph")
    state = {}
    workflow.invoke(state)
    print("✅ ASB cognitive loop complete!")

@app.command()
def schedule_automate():
    """Schedule daily ASB automation loop."""
    start_autonomous_loop()


if __name__ == "__main__":
    app()