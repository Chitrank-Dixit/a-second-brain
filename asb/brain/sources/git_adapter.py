import subprocess
import os
from datetime import datetime, timedelta

class GitAdapter:
    def __init__(self, repo_path: str = ".", since_hours: int = 24):
        self.repo_path = repo_path
        self.since = datetime.now() - timedelta(hours=since_hours)

    def fetch_entries(self):
        os.chdir(self.repo_path)
        result = subprocess.run(
            ["git", "log", f'--since="{self.since.isoformat()}"', "--pretty=format:%h|%s|%an|%ad", "--date=iso"],
            capture_output=True,
            text=True,
        )
        entries = []
        for line in result.stdout.splitlines():
            parts = line.split("|")
            if len(parts) >= 4:
                entries.append({
                    "id": parts[0],
                    "summary": parts[1],
                    "author": parts[2],
                    "date": parts[3],
                    "source": "git"
                })
        return entries