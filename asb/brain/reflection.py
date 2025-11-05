# asb/brain/reflection.py
import datetime
import os
import random
from asb.brain.agent import ASBAgent
from asb.brain.insight_db import InsightDB
from asb.brain.logger import setup_logger
from asb.brain.self_evaluator import SelfEvaluator
log = setup_logger()


class ReflectionEngine:
    def __init__(self,
                 reflections_dir: str = "./data/reflections",
                 questions_file: str = "./data/questions/open_questions.md"):
        os.makedirs(reflections_dir, exist_ok=True)
        os.makedirs(os.path.dirname(questions_file), exist_ok=True)
        self.reflections_dir = reflections_dir
        self.questions_file = questions_file
        self.agent = ASBAgent()
        self.db = InsightDB()

    # --- helper functions ----------------------------------------------------
    def _load_open_questions(self):
        if not os.path.exists(self.questions_file):
            return []
        with open(self.questions_file, "r") as f:
            lines = [line.strip("- ").strip() for line in f if line.strip()]
        return [q for q in lines if q]

    def _save_new_questions(self, questions: list[str]):
        with open(self.questions_file, "a") as f:
            for q in questions:
                f.write(f"- {q}\n")

    def _select_question(self, questions: list[str]):
        return random.choice(questions) if questions else None

    # --- main reflection -----------------------------------------------------
    def reflect(self):
        # 1️⃣ Try answering one old question first
        evaluator = SelfEvaluator()
        metrics = evaluator.summarize_scores()  # optional print

        summary = self.agent.ask(
            "Summarize what I've learned recently and avoid repeating prior reflections with high redundancy scores."
        )
        open_qs = self._load_open_questions()
        chosen_q = self._select_question(open_qs)
        old_answer = None

        if chosen_q:
            log.info(f"🤔 Revisiting previous question: {chosen_q}")
            old_answer = self.agent.ask(f"Answer this question based on my knowledge: {chosen_q}")

            # remove answered question from list
            remaining = [q for q in open_qs if q != chosen_q]
            with open(self.questions_file, "w") as f:
                for q in remaining:
                    f.write(f"- {q}\n")

        if chosen_q and old_answer:
            # Store in insight DB
            topic_guess = self.agent.ask(
                f"Categorize this question into 1-2 topic keywords: {chosen_q}"
            )
            tags_guess = self.agent.ask(
                f"Suggest 3 short tags for this content: {chosen_q} {old_answer}"
            )
            self.db.add_insight(topic_guess, chosen_q, old_answer, tags_guess.split(","))

        summary = self.agent.ask(
            "Reflect on what I have done across all sources (git commits, notes, reflections). Identify recurring themes and possible next improvements."
        )

        # 2️⃣ Generate a new reflection summary
        summary = self.agent.ask(
            "Summarize what I've learned recently and identify recurring themes."
        )

        # 3️⃣ Generate new follow-up questions
        new_qs_text = self.agent.ask(
            "Based on this reflection, list 3 new thoughtful questions to explore next."
        )
        # extract bullet points (simple heuristic)
        new_qs = [line.strip("- ").strip()
                  for line in new_qs_text.splitlines() if line.strip()]
        self._save_new_questions(new_qs)

        # 4️⃣ Write full reflection file
        date = datetime.date.today().strftime("%Y-%m-%d")
        output_file = os.path.join(self.reflections_dir, f"reflection_{date}.md")

        with open(output_file, "w") as f:
            f.write(f"# Reflection — {date}\n\n")
            if chosen_q and old_answer:
                f.write("## Revisited Question\n")
                f.write(f"**{chosen_q}**\n\n{old_answer}\n\n")
            f.write("## Summary\n")
            f.write(summary + "\n\n")
            f.write("## New Questions\n")
            for q in new_qs:
                f.write(f"- {q}\n")

        log.info(f"🪞 Reflection complete → {output_file}")
        return {"summary": summary, "answered": chosen_q, "new_questions": new_qs}