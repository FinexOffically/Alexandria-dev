#!/usr/bin/env python3
"""
Alexandria - Knowledge & Information Management System
Main launcher for the application
"""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from alexandria.core.database import Database
from alexandria.core.library import Library
from alexandria.ui.cli import AlexandriaShell

def main():
    """Main entry point for Alexandria"""
    # Create data directory if needed
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Initialize database and library
    db = Database(str(data_dir))
    library = Library(db)
    
    # Start interactive shell
    shell = AlexandriaShell(library)
    
    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        print("\n\n✨ Bye!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        raise

if __name__ == "__main__":
    main()
