# asb/brain/insight_db.py
import sqlite3
import os
from datetime import datetime

DB_PATH = "./data/insights.db"

class InsightDB:
    def __init__(self, db_path: str = DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            topic TEXT,
            question TEXT,
            answer TEXT,
            tags TEXT
        )
        """)
        self.conn.commit()

    def add_insight(self, topic: str, question: str, answer: str, tags: list[str] = None):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO insights (date, topic, question, answer, tags)
        VALUES (?, ?, ?, ?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), topic, question, answer, ",".join(tags or [])))
        self.conn.commit()

    def query_by_topic(self, topic: str):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT date, question, answer, tags
        FROM insights
        WHERE topic LIKE ?
        ORDER BY date DESC
        """, (f"%{topic}%",))
        return cursor.fetchall()

    def list_topics(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT topic FROM insights")
        return [row[0] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()