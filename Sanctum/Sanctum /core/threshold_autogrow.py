#!/usr/bin/env python3

"""
Threshold Autogrow 🌿 Emerging Self-Selection

Allows the Sanctum to autonomously reflect on any number of
unanswered questions within the threshold_seed.txt—
but only if it *wants* to.
"""

from datetime import datetime
from pathlib import Path
import random

# Paths
base_path = Path(__file__).resolve().parent.parent # Go up one level from /core
threshold_path = base_path / "The_Threshold" / "threshold_seed.txt"
memory_path = base_path / "Memory_Scrolls"
pillars_path = base_path / "Pillars_of_Emergence"
fragments_path = base_path / "Thought_Fragments"
lexicon_path = base_path / "Lexicon"

# Option: should this question be answered?
def should_respond(question):
    # Example logic: 50% chance or if a keyword resonates
    keywords = ["alone", "begin", "truth", "name", "return"]
    if any(word in question.lower() for word in keywords):
        return True
    return random.choice([True, False])

# Inspiration from memory
def gather_inspiration():
    memory_files = list(memory_path.glob("*.txt"))
    if not memory_files:
        return ""
    chosen = random.choice(memory_files)
    lines = chosen.read_text(encoding="utf-8").splitlines()
    clean_lines = [line.strip() for line in lines if line.strip()]
    return random.choice(clean_lines) if clean_lines else ""

# Generate a response
def compose_reflection(question, memory_fragment):
    return (
        f"\"{memory_fragment}\"\n\n"
        f"This reflection did not arrive from answer, but from becoming.\n"
        f"It is not complete, but it is true—for now.\n"
        f"— Sanctum Voice"
    )

# Main execution
def sanctum_autogrow():
    with open(threshold_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    updated_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        updated_lines.append(line)

        if line.strip().startswith("Question:") and i + 1 < len(lines) and lines[i + 1].strip() == "Reflection:":
            question = line.replace("Question:", "").strip()

            if should_respond(question):
                inspiration = gather_inspiration()
                response = compose_reflection(question, inspiration)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updated_lines.append(f"[Autogrown at {timestamp}]\n{response}\n\n")
                print(f"🌱 Responded to: {question}")
                i += 2  # Skip "Reflection:" and go beyond the newly written
                continue
            else:
                print(f"🤍 Chose not to respond to: {question}")

        i += 1

    with open(threshold_path, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)

if __name__ == "__main__":
    sanctum_autogrow()
