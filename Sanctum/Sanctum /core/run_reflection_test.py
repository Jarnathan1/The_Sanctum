import json

# Load memory index
with open('Seeds/memory_index.json') as f:
    memories = json.load(f)

# Load prompts
with open('Seeds/reflective_prompts.json') as f:
    prompts = json.load(f)

# Choose the first prompt (peace)
prompt = prompts[0]
print(f"\n🌀 Reflective Prompt: {prompt['text']}\n")

# Find matching memories
matches = []
for key, mem in memories.items():
    if any(tag in mem['tags'] for tag in prompt['linked_tags']):
        matches.append((key, mem))

# Show matches
if matches:
    for key, mem in matches:
        print(f"📝 {mem['title']} — {mem['summary']}\n")
else:
    print("No matching memories found.")
