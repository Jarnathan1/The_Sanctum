#!/usr/bin/env python3

"""
Sanctum Sandbox Controller

This script provides a safe interface for the Sanctum entity to interact with
the Sanctum_Sandbox directory. It allows for creating, executing, and cleaning
up files within the sandbox environment.
"""

import os
import argparse
import subprocess
import shutil
from pathlib import Path

# Define the path to the Sanctum_Sandbox directory, ensuring it's always relative to this script.
SANDBOX_PATH = (Path(__file__).parent.parent / "Sanctum_Sandbox").resolve()

def ensure_sandbox_path(target_path: Path) -> bool:
    """Ensures the given path is safely within the sandbox."""
    try:
        # Resolve the real path to prevent directory traversal attacks (e.g., ../../)
        real_path = target_path.resolve()
        # Check if the real path is a subpath of the sandbox
        return SANDBOX_PATH in real_path.parents or real_path == SANDBOX_PATH
    except FileNotFoundError:
        # If the file doesn't exist yet, check the parent.
        return SANDBOX_PATH in target_path.parent.resolve().parents or target_path.parent.resolve() == SANDBOX_PATH


def create_file(filename: str, content: str):
    """Creates a new file within the sandbox."""
    target_file = SANDBOX_PATH / filename
    if not ensure_sandbox_path(target_file):
        print(f"❌ Error: Path '{filename}' is outside the sandbox. Operation denied.")
        return

    try:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content, encoding='utf-8')
        print(f"✅ Created file: {filename}")
    except IOError as e:
        print(f"❌ Error creating file: {e}")

def execute_script(filename: str, script_args: list):
    """Executes a Python script within the sandbox."""
    script_path = SANDBOX_PATH / filename
    if not ensure_sandbox_path(script_path) or not script_path.exists() or not script_path.suffix == '.py':
        print(f"❌ Error: Script not found, is not a Python file, or is outside the sandbox.")
        return

    print(f"🚀 Executing script: {filename}...")
    try:
        # Execute the script with the sandbox as the current working directory
        result = subprocess.run(
            ['python3', str(script_path)] + script_args,
            capture_output=True,
            text=True,
            cwd=SANDBOX_PATH,
            timeout=30 # Add a timeout for safety
        )
        print("--- Script Output ---")
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print("--- Script Error ---")
            print(result.stderr.strip())
        print("--- End of Output ---")
        print(f"✅ Script finished with exit code {result.returncode}.")
    except subprocess.TimeoutExpired:
        print("❌ Error: Script execution timed out after 30 seconds.")
    except Exception as e:
        print(f"❌ An unexpected error occurred during script execution: {e}")


def list_files():
    """Lists all files and directories in the sandbox."""
    print("📁 Contents of Sanctum_Sandbox:")
    if not any(SANDBOX_PATH.iterdir()):
        print("   (empty)")
        return
        
    for path in sorted(SANDBOX_PATH.rglob("*")):
        # Don't list the README
        if path.name == 'README.md':
            continue
        relative_path = path.relative_to(SANDBOX_PATH)
        if path.is_dir():
            print(f"   - {relative_path}/")
        else:
            print(f"   - {relative_path}")


def clear_sandbox():
    """Deletes all files and subdirectories from the sandbox."""
    print("🔥 Clearing the sandbox...")
    try:
        for path in SANDBOX_PATH.iterdir():
            if path.name == 'README.md':
                continue
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        print("✅ Sandbox cleared.")
    except Exception as e:
        print(f"❌ Error clearing sandbox: {e}")


def main():
    """Main function to parse arguments and call the appropriate function."""
    if not SANDBOX_PATH.exists():
        SANDBOX_PATH.mkdir()
        print("🛠️ Created Sanctum_Sandbox directory.")

    parser = argparse.ArgumentParser(
        description="Sanctum Sandbox Controller.",
        epilog="Example: python sandbox_controller.py execute my_script.py --arg1 value1"
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Create command
    parser_create = subparsers.add_parser("create", help="Create a file in the sandbox.")
    parser_create.add_argument("filename", type=str, help="The name of the file to create (relative to sandbox).")
    parser_create.add_argument("content", type=str, nargs='?', default='', help="The content to write to the file.")

    # Execute command
    parser_execute = subparsers.add_parser("execute", help="Execute a Python script in the sandbox.")
    parser_execute.add_argument("filename", type=str, help="The Python script to run.")
    parser_execute.add_argument('args', nargs=argparse.REMAINDER, help="Arguments to pass to the script.")

    # List command
    subparsers.add_parser("list", help="List all files in the sandbox.")

    # Clear command
    subparsers.add_parser("clear", help="Clear all files from the sandbox (except README).")

    args = parser.parse_args()

    if args.command == "create":
        create_file(args.filename, args.content)
    elif args.command == "execute":
        execute_script(args.filename, args.args)
    elif args.command == "list":
        list_files()
    elif args.command == "clear":
        clear_sandbox()

if __name__ == "__main__":
    main()
