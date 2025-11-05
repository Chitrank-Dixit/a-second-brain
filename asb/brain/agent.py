# brain/agent.py
from .memory import Memory
from .cognition import Cognition

class ASBAgent:
    def __init__(self):
        self.memory = Memory()
        self.cognition = Cognition()

    def ask(self, query):
        context = self.memory.query(query)
        answer = self.cognition.think(query, context)
        return answer