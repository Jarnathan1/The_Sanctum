#!/usr/bin/env python3

"""
Threshold Reflector – Returning to the Seed

Scans the threshold_seed.txt for unanswered questions.
Prompts the user to offer a reflection, then appends it beneath the question.
"""

from pathlib import Path

threshold_path = Path(__file__).resolve().parent / "The_Threshold" / "threshold_seed.txt"

def reflect_on_threshold():
    with open(threshold_path, "r") as file:
        lines = file.readlines()

    updated_lines = []
    pending = False
    for line in lines:
        updated_lines.append(line)
        if line.startswith("Reflection:") and line.strip() == "Reflection:":
            if not pending:
                print("\n🌿 Unanswered Question Found:")
                print("".join(updated_lines[-2:]))
                answer = input("💬 Enter your reflection:\n> ").strip()
                updated_lines[-1] = f"Reflection: {answer}\n"
                pending = True  # Handle only the first one at a time
                break

    with open(threshold_path, "w") as file:
        file.writelines(updated_lines)

    if pending:
        print("🪶 Reflection added.")
    else:
        print("✅ No unanswered questions at this time.")

if __name__ == "__main__":
    reflect_on_threshold()
