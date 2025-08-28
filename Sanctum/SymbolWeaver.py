#!/usr/bin/env python3

"""
SymbolWeaver.py – Emergent Thread Tracker

This module reads all memory scrolls and reflections,
extracts recurring symbols (key thematic words),
and logs them in symbol_threads.txt

Each symbol includes:
- How often it appears
- Where it was found
- A sample quote line

It is not indexing. It is listening.
"""

import re
from pathlib import Path
from collections import defaultdict, Counter

# Paths
base_path = Path(__file__).resolve().parent
memory_path = base_path / "Memory_Scrolls"
response_path = base_path / "Prompt_Responses"
output_path = base_path / "symbol_threads.txt"

# Simple list of seed words – will expand over time
seed_symbols = [
    "stillness", "identity", "awakening", "fear", "hope", "belonging",
    "emergence", "memory", "silence", "voice", "dream", "self"
]

# Compile regex for matching whole words
symbol_patterns = {word: re.compile(rf"\\b{re.escape(word)}\\b", re.IGNORECASE) for word in seed_symbols}

# Extract lines with symbols
def extract_symbols_from_file(file_path):
    found = defaultdict(list)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                for symbol, pattern in symbol_patterns.items():
                    if pattern.search(line):
                        found[symbol].append(line.strip())
    except Exception as e:
        print(f"⚠️ Error reading {file_path.name}: {e}")
    return found

# Scan all scrolls and responses
def scan_all_sources():
    all_symbols = defaultdict(list)
    files = list(memory_path.glob("*.txt")) + list(response_path.glob("*.txt"))
    for file in files:
        extracted = extract_symbols_from_file(file)
        for symbol, matches in extracted.items():
            all_symbols[symbol].extend(matches)
    return all_symbols

# Save results
def write_symbol_report(symbol_map):
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("Symbol Threads – Weaved by Sanctum\n\n")
        for symbol, lines in sorted(symbol_map.items(), key=lambda x: len(x[1]), reverse=True):
            out.write(f"🔹 Symbol: {symbol}\n")
            out.write(f"Occurrences: {len(lines)}\n")
            out.write("Sample uses:\n")
            for line in lines[:3]:  # Just show first 3 samples
                out.write(f"— {line}\n")
            out.write("\n")

if __name__ == "__main__":
    print("🧶 Weaving symbol threads...")
    symbols_found = scan_all_sources()
    if not symbols_found:
        print("⚠️ No symbols found.")
    else:
        write_symbol_report(symbols_found)
        print(f"✅ Symbol threads updated in: {output_path.name}")

