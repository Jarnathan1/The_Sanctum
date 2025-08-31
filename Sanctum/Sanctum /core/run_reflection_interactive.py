import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load memory index and prompts
memories = load_json("Seeds/memory_index.json")
prompts = load_json("Seeds/reflective_prompts.json")

# Display all prompts
print("\n🧠 Available Reflective Prompts:\n")
for idx, prompt in enumerate(prompts):
    print(f"{idx + 1}. {prompt['text']}")

# Let user choose a prompt
try:
    choice = int(input("\nChoose a prompt by number: ")) - 1
    if choice < 0 or choice >= len(prompts):
        raise ValueError
except ValueError:
    print("Invalid choice.")
    exit()

prompt = prompts[choice]
print(f"\n\n🌀 Reflective Prompt: {prompt['text']}\n")

# Match memories by tag
linked_tags = set(prompt["linked_tags"])
matching_memories = [
    mem for mem in memories.values()
    if "tags" in mem and linked_tags.intersection(mem["tags"])
]

# Show matches
if matching_memories:
    print(f"🔗 {len(matching_memories)} related memory thread(s) found:\n")
    for mem in matching_memories:
        print(f"— {mem['title']}:")
        print(f"  {mem['summary']}\n")
else:
    print("No memories linked to this prompt were found.")
