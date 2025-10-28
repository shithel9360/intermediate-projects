#!/usr/bin/env python3
"""
Quiz Application (Console)

Features:
- Multiple-choice questions with shuffled options
- Score tracking and percentage calculation
- Per-question timers (optional) with graceful timeout handling
- Review mode showing correct answers and explanations
- Clean, modular design for easy extension

Run:
    python3 quiz_app.py
"""

from dataclasses import dataclass
from typing import List, Optional
import random
import time


@dataclass
class Question:
    prompt: str
    options: List[str]
    answer_index: int
    explanation: Optional[str] = None

    def shuffled(self):
        """Return a new Question with options shuffled and adjusted answer index."""
        indices = list(range(len(self.options)))
        random.shuffle(indices)
        new_options = [self.options[i] for i in indices]
        new_answer_index = indices.index(self.answer_index)
        return Question(self.prompt, new_options, new_answer_index, self.explanation)


class Quiz:
    def __init__(self, questions: List[Question], per_question_seconds: Optional[int] = None):
        self.original_questions = questions
        self.questions = [q.shuffled() for q in questions]
        self.per_question_seconds = per_question_seconds
        self.correct = 0
        self.responses: List[Optional[int]] = []  # None for timeout/no answer

    def ask(self):
        print("\n" + "=" * 80)
        print("QUIZ START")
        print("=" * 80)
        for idx, q in enumerate(self.questions, 1):
            print(f"\nQ{idx}. {q.prompt}")
            for i, opt in enumerate(q.options):
                print(f"  {chr(65+i)}. {opt}")

            user_choice = self._get_user_choice(len(q.options))
            self.responses.append(user_choice)
            if user_choice is None:
                print("Time's up or no input. Moving on.")
            elif user_choice == q.answer_index:
                self.correct += 1
                print("Correct!\n")
            else:
                print("Incorrect.\n")

        self._show_results()

    def _get_user_choice(self, num_options: int) -> Optional[int]:
        start = time.time()
        while True:
            remaining = None
            if self.per_question_seconds is not None:
                elapsed = time.time() - start
                remaining = int(self.per_question_seconds - elapsed)
                if remaining <= 0:
                    return None
                print(f"Enter your choice (A-{chr(64+num_options)}) [{remaining}s]: ", end="", flush=True)
            else:
                print(f"Enter your choice (A-{chr(64+num_options)}): ", end="", flush=True)

            try:
                # Note: True per-keystroke timing requires threads/async; here we check between inputs
                choice = input().strip().upper()
            except EOFError:
                return None

            if self.per_question_seconds is not None and (time.time() - start) > self.per_question_seconds:
                return None

            if len(choice) == 1 and 'A' <= choice <= chr(64 + num_options):
                return ord(choice) - 65
            else:
                print("Invalid input. Please enter a valid option letter.")

    def _show_results(self):
        total = len(self.questions)
        percent = (self.correct / total * 100) if total else 0
        print("\n" + "=" * 80)
        print("RESULTS")
        print("=" * 80)
        print(f"Score: {self.correct}/{total} ({percent:.1f}%)")

        print("\nREVIEW:")
        for idx, (q, resp) in enumerate(zip(self.questions, self.responses), 1):
            correct_letter = chr(65 + q.answer_index)
            your_letter = '-' if resp is None else chr(65 + resp)
            status = '✓' if resp == q.answer_index else '✗'
            print(f"Q{idx}: {status} Your: {your_letter}, Correct: {correct_letter}")
            if q.explanation:
                print(f"   Explanation: {q.explanation}")


SAMPLE_QUESTIONS = [
    Question(
        prompt="Which data structure uses FIFO order?",
        options=["Stack", "Queue", "Tree", "Graph"],
        answer_index=1,
        explanation="Queues remove the earliest enqueued element first (First-In-First-Out).",
    ),
    Question(
        prompt="What is the average time complexity of Quick Sort?",
        options=["O(n^2)", "O(n log n)", "O(log n)", "O(n)"],
        answer_index=1,
        explanation="Average-case is O(n log n), worst-case O(n^2) without randomized pivots.",
    ),
    Question(
        prompt="Which file format is best for hierarchical data serialization?",
        options=["CSV", "JSON", "INI", "TXT"],
        answer_index=1,
        explanation="JSON supports nested objects/arrays naturally.",
    ),
]


def main():
    print("Welcome to the Quiz App!\n")
    use_timer = input("Enable per-question timer? (y/N): ").strip().lower() == 'y'
    seconds = None
    if use_timer:
        try:
            seconds = int(input("Enter seconds per question (e.g., 20): ").strip())
        except ValueError:
            print("Invalid number. Proceeding without timer.")
            seconds = None

    quiz = Quiz(SAMPLE_QUESTIONS, per_question_seconds=seconds)
    quiz.ask()


if __name__ == "__main__":
    main()
