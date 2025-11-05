import re, os, networkx as nx
from asb.brain.logger import setup_logger
log = setup_logger()


class KnowledgeGraph:
    def __init__(self, notes_dir="./data/notes"):
        self.notes_dir = notes_dir
        self.graph = nx.Graph()

    def build(self):
        for file in os.listdir(self.notes_dir):
            if file.endswith((".md", ".txt")):
                text = open(os.path.join(self.notes_dir, file)).read()
                words = re.findall(r'\b[A-Za-z]{5,}\b', text)
                for i in range(len(words) - 1):
                    self.graph.add_edge(words[i].lower(), words[i + 1].lower())

        log.info(f"🕸 Built knowledge graph with {len(self.graph.nodes())} nodes")

    def related(self, concept: str):
        concept = concept.lower()
        if concept in self.graph:
            return list(self.graph.neighbors(concept))
        else:
            return []