import os
import glob
from datetime import datetime, timedelta
from asb.brain.agent import ASBAgent
from asb.brain.insight_db import InsightDB

class MemoryCompressor:
    def __init__(self,
                 reflections_dir="./data/reflections",
                 compressed_dir="./data/compressed"):
        self.reflections_dir = reflections_dir
        os.makedirs(compressed_dir, exist_ok=True)
        self.compressed_dir = compressed_dir
        self.agent = ASBAgent()

    def compress_old_reflections(self, days: int = 14):
        """Summarize and compress reflections older than N days."""
        cutoff = datetime.now() - timedelta(days=days)
        files = []
        for file in glob.glob(os.path.join(self.reflections_dir, "reflection_*.md")):
            date_str = file.split("_")[-1].split(".")[0]
            try:
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                continue
            if file_date < cutoff:
                files.append(file)

        if not files:
            print(f"🧹 No reflections older than {days} days to compress.")
            return None

        content = ""
        for f in files:
            with open(f) as fh:
                content += fh.read() + "\n"

        print(f"🧩 Compressing {len(files)} old reflections → summary.")
        summary = self.agent.ask(
            f"Summarize the following {len(files)} reflections into key insights, themes, and lessons:\n{content}"
        )

        out_file = os.path.join(self.compressed_dir, f"compressed_{datetime.now():%Y-%m-%d}.md")
        with open(out_file, "w") as f:
            f.write(summary)

        print(f"✅ Compressed reflections written → {out_file}")
        db = InsightDB()
        db.add_insight(
            topic="long_term_summary",
            question=f"Summary of reflections older than {days} days",
            answer=summary,
            tags=["compressed", "summary"]
        )
        for f in files:
            os.rename(f, f.replace("reflections/", "reflections/archived_"))
        return out_file