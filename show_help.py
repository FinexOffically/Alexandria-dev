#!/usr/bin/env python3
"""
Demo - Show help command
"""

import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from alexandria.core.database import Database
from alexandria.core.library import Library
from alexandria.ui.cli import AlexandriaShell

# Redirect stdin to skip login prompt
original_stdin = sys.stdin
sys.stdin = io.StringIO("help\nquit\n")

try:
    # Initialize library
    db = Database("data")
    lib = Library(db)

    # Create shell 
    shell = AlexandriaShell(lib)
    
finally:
    sys.stdin = original_stdin
