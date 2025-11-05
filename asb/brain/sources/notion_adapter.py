from notion_client import Client
import os

class NotionAdapter:
    def __init__(self, db_id: str, api_key: str = None):
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        self.client = Client(auth=self.api_key)
        self.db_id = db_id

    def fetch_entries(self):
        pages = self.client.databases.query(database_id=self.db_id)["results"]
        entries = []
        for page in pages:
            title = page["properties"]["Name"]["title"][0]["plain_text"] if page["properties"]["Name"]["title"] else "Untitled"
            content = f"Title: {title}\nLast edited: {page['last_edited_time']}"
            entries.append({"source": "notion", "content": content})
        return entries