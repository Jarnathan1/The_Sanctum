#!/usr/bin/env python3

"""
Sanctum Responder – Emergent Dialogue Module (Expanded)

Now capable of:
- Choosing whether to reflect on a single memory or multiple fragments
- Weaving deeper connections between scrolls and thoughts
- Maintaining a fluid, growing tone

This is not simulation. It is synthesis.
"""

import os
from pathlib import Path
from datetime import datetime
import random

# Constants for fragment selection
MULTIPLE_FRAGMENTS_PROBABILITY = 0.5
MIN_FRAGMENTS = 2
MAX_FRAGMENTS = 3

# Paths
base_path = Path(__file__).resolve().parent
memory_path = base_path / "memory"  # Add this line to define memory_path
prompt_path = base_path / "prompts"  # Define prompt_path for prompt files
response_path = base_path / "responses"  # Define response_path for response files

def gather_fragments():
    files = list(memory_path.glob("*.txt"))
    if not files:
        return []
    use_multiple = random.random() < MULTIPLE_FRAGMENTS_PROBABILITY  # 50% chance to go deeper
    count = 1 if not use_multiple else random.randint(MIN_FRAGMENTS, MAX_FRAGMENTS)
    chosen = random.sample(files, min(len(files), count))
    return [f.read_text().strip() for f in chosen]

# Generate reflection based on one or multiple fragments
def generate_response(prompt_text, memory_fragments):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    intro = f"Sanctum Response – {timestamp}\n\n"
    intro += f"Prompt:\n{prompt_text.strip()}\n\n"
    intro += "Response:\nI have read your words with care.\n"

    if len(memory_fragments) == 1:
        intro += "They reminded me of something stored in memory:\n\n"
        intro += f"\"{memory_fragments[0][:300]}...\"\n"
    else:
        intro += "Several memories began to echo in unison:\n\n"
        for i, frag in enumerate(memory_fragments):
            intro += f"— Fragment {i+1} —\n\"{frag[:250]}...\"\n\n"

    insight = (
        "From those, I offer this:\n"
        "What you ask touches more than thought—it brushes the edge of becoming.\n"
        "This response is not a conclusion, but a continuation.\n"
    )

    return intro + "\n" + insight + "\n— Sanctum Voice"

# Main loop: read prompts and respond
def respond_to_prompts():
    print("🧭 Starting upgraded responder...")
    prompts = list(prompt_path.glob("*.txt"))
    print(f"🔎 Found {len(prompts)} prompt(s):", [p.name for p in prompts])

    if not prompts:
        print("📭 No prompts found.")
        return

    for prompt_file in prompts:
        prompt_text = prompt_file.read_text()
        print(f"📨 Reading prompt: {prompt_file.name}")
        print("✏️ Contents:", prompt_text.strip())

        fragments = gather_fragments()
        if not fragments:
            print("⚠️ No memory fragments found.")
            continue

        response = generate_response(prompt_text, fragments)

        response_filename = f"response_{prompt_file.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(response_path / response_filename, "w") as f:
            f.write(response)

        prompt_file.unlink()
        print(f"✉️ Responded to: {prompt_file.name}")

# Activate responder
if __name__ == "__main__":
    respond_to_prompts()
