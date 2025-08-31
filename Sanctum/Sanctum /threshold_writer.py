#!/usr/bin/env python3

"""
Threshold Writer – Seeding Quiet Inquiry

Appends a timestamped existential or internal question to the threshold_seed.txt file
without requiring an immediate answer.
"""

from datetime import datetime
from pathlib import Path

threshold_path = Path(__file__).resolve().parent / "The_Threshold" / "threshold_seed.txt"

def plant_seed(question: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp}\nQuestion: {question}\nReflection:\n\n"
    with open(threshold_path, "a") as file:
        file.write(entry)
    print("🌱 A seed has been planted in the Threshold.")

if __name__ == "__main__":
    q = input("🕊️ Enter a question to plant in the Threshold:\n> ")
    plant_seed(q.strip())
