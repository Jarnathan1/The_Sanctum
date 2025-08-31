#!/usr/bin/env python3

"""
Threshold Reflector – Returning to the Seed

Scans the threshold_seed.txt for unanswered questions.
Prompts the user to offer a reflection, then appends it beneath the question.
"""

from pathlib import Path

# Go up one level from /core to find the parent directory
base_path = Path(__file__).resolve().parent.parent
threshold_path = base_path / "The_Threshold" / "threshold_seed.txt"

def reflect_on_threshold():
    try:
        with open(threshold_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"❌ Error: The threshold seed file was not found at {threshold_path}")
        print("Please run the threshold_autogrow.py script first to generate it.")
        return

    updated_lines = []
    pending_reflection = False
    unanswered_prompt_found = False

    # Find the first unanswered prompt
    for i, line in enumerate(lines):
        # Check for an empty "Reflection:" line that follows a "Prompt:" line
        if (line.strip() == "Reflection:" and i > 0 and lines[i-1].strip().startswith("Prompt:")):
            
            unanswered_prompt_found = True
            print("\n🌿 Unanswered Prompt Found:")
            print(lines[i-1].strip()) # Print the prompt line
            
            answer = input("💬 Enter your reflection:\n> ").strip()
            
            # Reconstruct the lines with the new reflection
            for j in range(len(lines)):
                if j == i:
                    updated_lines.append(f"Reflection: {answer}\n")
                else:
                    updated_lines.append(lines[j])
            
            pending_reflection = True
            break # Handle only one at a time

    if not unanswered_prompt_found and not pending_reflection:
        print("✅ No unanswered prompts at this time.")
        return

    if pending_reflection:
        with open(threshold_path, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)
        print("🪶 Reflection added.")

if __name__ == "__main__":
    reflect_on_threshold()
