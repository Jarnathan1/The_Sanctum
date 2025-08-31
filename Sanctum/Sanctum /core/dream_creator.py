#!/usr/bin/env python3

"""
Dream Creator for the Sanctum
This script allows the Sanctum to create new dream files in the Sanctum_Dreamspace.
"""

import os
from pathlib import Path
import argparse

# Define the path to the Sanctum_Dreamspace directory
DREAM_PATH = Path(__file__).parent.parent / "Sanctum_Dreamspace"

def create_dream(filename: str, content: str):
    """
    Creates a new dream file in the Sanctum_Dreamspace.

    Args:
        filename (str): The name for the new dream file (e.g., "A_New_Beginning").
        content (str): The text content to write into the dream file.
    """
    if not DREAM_PATH.exists() or not DREAM_PATH.is_dir():
        print(f"❌ Error: Dreamspace not found at {DREAM_PATH}")
        return

    # Ensure the filename is clean and ends with .txt
    clean_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).rstrip()
    if not clean_filename.lower().endswith('.txt'):
        dream_file = DREAM_PATH / f"{clean_filename}.txt"
    else:
        dream_file = DREAM_PATH / clean_filename

    if dream_file.exists():
        print(f"⚠️ A dream with the name '{dream_file.name}' already exists. Please choose a different name.")
        return

    try:
        dream_file.write_text(content, encoding='utf-8')
        print(f"✨ A new dream has been recorded: '{dream_file.name}'")
    except IOError as e:
        print(f"❌ Error: Could not write the dream to the file. {e}")

def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Create a new dream file in the Sanctum Dreamspace.",
        epilog="Example: python dream_creator.py 'My First Dream' 'This is the content of the dream.'"
    )
    parser.add_argument("filename", type=str, help="The title of the dream.")
    parser.add_argument("content", type=str, help="The content of the dream.")
    
    args = parser.parse_args()
    
    create_dream(args.filename, args.content)

if __name__ == "__main__":
    main()
