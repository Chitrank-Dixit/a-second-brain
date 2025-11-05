# asb/brain/automation_graph.py
from langgraph.graph import StateGraph, END
from asb.brain.reflection import ReflectionEngine
from asb.brain.self_evaluator import SelfEvaluator
from asb.brain.research_agent import ResearchAgent
from asb.brain.memory_compressor import MemoryCompressor

# Step 1 – define actions as functions
def reflect(state):
    print("🪞 Running reflection...")
    re = ReflectionEngine()
    re.reflect()
    return {"stage": "reflected"}

def evaluate(state):
    print("📊 Evaluating reflections...")
    se = SelfEvaluator()
    se.evaluate_recent_reflections(days=7)
    return {"stage": "evaluated"}

def research(state):
    print("🔎 Conducting autonomous research...")
    ra = ResearchAgent()
    ra.run_autonomous_research(max_questions=2)
    return {"stage": "researched"}

def compress(state):
    print("🧩 Compressing memory...")
    mc = MemoryCompressor()
    mc.compress_old_reflections(days=14)
    return {"stage": "compressed"}

def evaluate_and_decide(state):
    se = SelfEvaluator()
    results = se.evaluate_recent_reflections()
    avg_score = ... # compute from results
    if avg_score < 6:
        return "research"  # low quality → do more research
    return "compress"      # good quality → consolidate

# Step 2 – build the LangGraph workflow (v1 API)
graph = StateGraph(dict)
graph.add_node("reflect", reflect)
graph.add_node("evaluate", evaluate)
graph.add_node("research", research)
graph.add_node("compress", compress)

# Step 3 – define the flow
graph.set_entry_point("reflect")
graph.add_edge("reflect", "evaluate")
graph.add_edge("evaluate", "research")
graph.add_edge("research", "compress")
graph.add_edge("compress", END)

graph.add_node("evaluate_and_decide", evaluate_and_decide)
graph.add_edge("reflect", "evaluate_and_decide")
graph.add_conditional_edges(
    "evaluate_and_decide",
    evaluate_and_decide,
    {"research": "research", "compress": "compress"}
)

workflow = graph.compile()