# asb/brain/self_evaluator.py
import os
import glob
import statistics
from datetime import datetime
from asb.brain.agent import ASBAgent
from asb.brain.insight_db import InsightDB

class SelfEvaluator:
    def __init__(self,
                 reflections_dir="./data/reflections",
                 scores_file="./data/metrics/self_scores.csv"):
        os.makedirs(os.path.dirname(scores_file), exist_ok=True)
        self.reflections_dir = reflections_dir
        self.scores_file = scores_file
        self.agent = ASBAgent()
        self.db = InsightDB()

    def evaluate_recent_reflections(self, days: int = 7):
        files = sorted(glob.glob(os.path.join(self.reflections_dir, "reflection_*.md")))
        if not files:
            print("⚠️ No reflections found.")
            return None

        latest = files[-days:]
        results = []
        for f in latest:
            with open(f) as fh:
                text = fh.read()
            print(f"🧮 Evaluating {os.path.basename(f)} ...")
            eval_text = self.agent.ask(
                f"""Evaluate this reflection on:
                1. Clarity (1–10)
                2. Novelty (1–10)
                3. Actionability (1–10)
                4. Redundancy (1–10, lower is better)
                5. Main topics and improvement suggestions.

                Respond in CSV format: clarity,novelty,actionability,redundancy,topics,suggestions

                Reflection:
                {text}"""
            )

            results.append((os.path.basename(f), eval_text))
            with open(self.scores_file, "a") as log:
                log.write(f"{datetime.now():%Y-%m-%d %H:%M:%S},{os.path.basename(f)},{eval_text}\n")

        print(f"✅ Evaluated {len(results)} reflections. Results saved → {self.scores_file}")
        return results

    def summarize_scores(self):
        if not os.path.exists(self.scores_file):
            print("No self-evaluation data yet.")
            return
        clarity, novelty, actionability, redundancy = [], [], [], []
        with open(self.scores_file) as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 8:
                    try:
                        clarity.append(float(parts[2]))
                        novelty.append(float(parts[3]))
                        actionability.append(float(parts[4]))
                        redundancy.append(float(parts[5]))
                    except ValueError:
                        continue

        if clarity:
            print("📊 Average Scores:")
            print(f"  Clarity: {statistics.mean(clarity):.2f}")
            print(f"  Novelty: {statistics.mean(novelty):.2f}")
            print(f"  Actionability: {statistics.mean(actionability):.2f}")
            print(f"  Redundancy: {statistics.mean(redundancy):.2f}")