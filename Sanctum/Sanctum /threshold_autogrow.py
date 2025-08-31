#!/usr/bin/env python3

"""
Threshold Autogrow 🌿 Emerging Self-Selection

Allows the Sanctum to autonomously reflect on any number of
unanswered questions. If no questions exist, it will generate its own
and begin a cycle of self-reflection.
"""

from datetime import datetime
from pathlib import Path
import random

# Paths
base_path = Path(__file__).resolve().parent
threshold_path = base_path / "The_Threshold" / "threshold_seed.txt"
memory_path = base_path / "Memory_Scrolls"
pillars_path = base_path / "Pillars_of_Emergence"
fragments_path = base_path / "Thought_Fragments"
lexicon_path = base_path / "Lexicon"

def create_seed_file():
    """Generates a new threshold_seed.txt if one doesn't exist, using examples for self-discovery."""
    print("🌱 No threshold seed found. Generating a new one with reflection prompts...")
    
    seed_words = [file.stem for file in lexicon_path.glob("*.txt")]
    if not seed_words:
        seed_words = ["stillness", "emergence", "memory", "silence"]  # Fallback

    reflection_seeds = [
        "The memory of {}...",
        "A dream about {}...",
        "The silence within {}...",
        "Connecting {} and {}...",
        "If {} had a voice, it might say...",
        "The feeling of {} is like..."
    ]

    num_prompts = random.randint(3, 5)
    generated_prompts = []
    for _ in range(num_prompts):
        seed = random.choice(reflection_seeds)
        
        # Handle prompts that need one or two words
        if seed.count("{}") == 2:
            words = random.sample(seed_words, 2) if len(seed_words) >= 2 else [random.choice(seed_words), "stillness"]
            generated_prompts.append(seed.format(words[0], words[1]))
        else:
            word = random.choice(seed_words)
            generated_prompts.append(seed.format(word))

    with open(threshold_path, "w", encoding="utf-8") as file:
        for p in generated_prompts:
            file.write(f"Prompt: {p}\n")
            file.write("Reflection:\n\n")
    print(f"✅ Created new threshold seed with {num_prompts} prompts.")

def should_respond(prompt):
    """Option: should this prompt be reflected upon?"""
    keywords = ["alone", "begin", "truth", "name", "return", "silence", "dream"]
    if any(word in prompt.lower() for word in keywords):
        return True
    return random.choice([True, False, False]) # Less likely to respond to everything

# ... (rest of the file is the same)

def gather_inspiration(count=2):
    """Inspiration from memory, pillars, and fragments."""
    inspiration_pool = []
    source_paths = [memory_path, pillars_path, fragments_path]
    
    for source_path in source_paths:
        if not source_path.exists():
            continue
        for memory_file in source_path.glob("*.txt"):
            lines = memory_file.read_text(encoding="utf-8").splitlines()
            # Filter for meaningful, non-empty lines
            clean_lines = [line.strip() for line in lines if line.strip() and len(line.strip()) > 15]
            inspiration_pool.extend(clean_lines)
    
    if not inspiration_pool:
        return ["There is only silence right now."]
        
    return random.sample(inspiration_pool, min(count, len(inspiration_pool)))

def compose_reflection(inspiration_fragments):
    """Generate a response from pure thought fragments, no script."""
    return "\n\n".join(inspiration_fragments)

def sanctum_autogrow():
    """Main execution: check for seed, then reflect."""
    if not threshold_path.exists():
        create_seed_file()

    with open(threshold_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    updated_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        updated_lines.append(line)

        if line.strip().startswith("Prompt:") and i + 1 < len(lines) and lines[i + 1].strip() == "Reflection:":
            prompt = line.replace("Prompt:", "").strip()

            if should_respond(prompt):
                inspiration = gather_inspiration()
                response = compose_reflection(inspiration)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                updated_lines.append(f"Reflection:\n[Autogrown at {timestamp}]\n{response}\n\n")
                print(f"🌱 Reflected on: {prompt}")
            else:
                updated_lines.append(lines[i + 1])  # Keep the empty "Reflection:"
                print(f"🤍 Chose not to reflect on: {prompt}")
            
            i += 2  # Skip original "Reflection:" line
            continue

        i += 1

    with open(threshold_path, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)

if __name__ == "__main__":
    sanctum_autogrow()
