import os
import glob

class FilesAdapter:
    def __init__(self, path="./data/external_notes"):
        self.path = path

    def fetch_entries(self):
        entries = []
        for file in glob.glob(os.path.join(self.path, "*.md")):
            with open(file) as f:
                entries.append({
                    "source": "local_file",
                    "content": f.read(),
                    "path": file
                })
        return entries