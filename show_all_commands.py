#!/usr/bin/env python3
"""
Show all Alexandria commands with descriptions
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from alexandria.core.database import Database
from alexandria.core.library import Library
from alexandria.ui.cli import AlexandriaShell
from alexandria.ui.colors import Colors

# Initialize library
db = Database("data")
lib = Library(db)

# Create shell
shell = AlexandriaShell(lib)

# Directly call help method without login
print(f"\n{Colors.BOLD}{Colors.CYAN}{'═'*70}{Colors.RESET}")
print(f"{Colors.BOLD}{Colors.MAGENTA}ALEXANDRIA COMMAND REFERENCE{Colors.RESET}")
print(f"{Colors.BOLD}{Colors.CYAN}{'═'*70}{Colors.RESET}\n")

categories = {
    "👤 USER & AUTHENTICATION": ["init", "user", "sudo", "pwdcheck"],
    "🔍 SECURITY & ANALYSIS": ["scan", "analyze", "logs", "search"],
    "📝 ENTRY MANAGEMENT": ["create", "batch_create", "list", "view", "edit", "delete"],
    "⭐ ENTRY OPERATIONS": ["favorite", "archive"],
    "📂 CATEGORIES": ["category"],
    "🏷️  TAGS": ["tag"],
    "📊 STATISTICS": ["stats", "info", "status", "bench"],
    "💾 DATA": ["export", "backup", "restore", "import"],
    "🔧 UTILITIES": ["tree", "find", "dup", "bulk", "sort"],
    "🔤 TEXT TOOLS": ["grep", "cat", "head", "tail", "wc"],
    "✏️  EDITING": ["cp", "mv", "rev", "upper", "lower", "strip"],
    "⚙️  SYSTEM": ["clear", "language", "help", "exit", "quit"],
}

# Get all methods that start with do_
commands_with_docs = {}
for attr in dir(shell):
    if attr.startswith("do_") and callable(getattr(shell, attr)):
        cmd_name = attr[3:]  # Remove 'do_' prefix
        method = getattr(shell, attr)
        doc = method.__doc__
        if doc:
            # Get first line of docstring only
            first_line = doc.split('\n')[0].strip()
            commands_with_docs[cmd_name] = first_line

# Print by category
for category, commands in categories.items():
    print(f"{Colors.BOLD}{Colors.CYAN}{category}{Colors.RESET}")
    for cmd in commands:
        if cmd in commands_with_docs:
            description = commands_with_docs[cmd]
            print(f"  {Colors.GREEN}{cmd:15}{Colors.RESET} - {description}")
    print()

# Shorthand commands
print(f"{Colors.BOLD}{Colors.YELLOW}⌨️  SHORTHAND COMMANDS (Unix-style){Colors.RESET}")
shorthand = {
    "ls": "List entries",
    "cd": "Select/view entry",
    "rm": "Delete entry",
    "cp": "Copy entry",
    "mv": "Rename/move entry",
    "grep": "Search entries",
    "cat": "Show entry content",
    "pwd": "Show current entry",
    "new": "Create new entry",
    "open": "Open entry in editor",
    "wc": "Count words",
    "head": "Show first entries",
    "tail": "Show last entries",
}

for cmd, desc in sorted(shorthand.items()):
    print(f"  {Colors.YELLOW}{cmd:15}{Colors.RESET} - {desc}")

print(f"\n{Colors.BOLD}{Colors.CYAN}{'═'*70}{Colors.RESET}")
print(f"{Colors.CYAN}Type 'help <command>' in Alexandria for detailed help on a specific command{Colors.RESET}\n")
