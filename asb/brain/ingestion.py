from asb.brain.sources.git_adapter import GitAdapter
from asb.brain.sources.files_adapter import FilesAdapter
from asb.brain.sources.notion_adapter import NotionAdapter
from asb.brain.memory import Memory

class ContextIngestor:
    def __init__(self):
        self.memory = Memory()

    def ingest_all(self):
        entries = []
        adapters = [
            GitAdapter(),
            FilesAdapter(),
        ]
        for adapter in adapters:
            entries.extend(adapter.fetch_entries())

        print(f"📚 Ingested {len(entries)} entries from sources.")

        for e in entries:
            self.memory.collection.add(
                documents=[e["content"]],
                metadatas=[{"source": e["source"]}],
                ids=[f"{e['source']}_{hash(e['content'])}"],
            )