"""
Alexandria - Knowledge & Information Management System
A sophisticated library database inspired by CyberStalker's Alexandria

Version: 0.2.0
Status: Production Ready
"""

__version__ = "0.2.0"
__author__ = "Ananimus Team"
__description__ = "Knowledge & Information Management System"

from pathlib import Path

# Package metadata
PACKAGE_DIR = Path(__file__).parent
PROJECT_DIR = PACKAGE_DIR.parent.parent
DATA_DIR = PROJECT_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Import core classes
from .core.database import Database
from .core.models import Entry, Category, Tag
from .core.library import Library
from .ui.cli import AlexandriaShell
from .ui.colors import Colors, banner
from .ui.languages import LanguageManager, get_language_manager

__all__ = [
    "Entry",
    "Category",
    "Tag",
    "Database",
    "Library",
    "AlexandriaShell",
    "Colors",
    "banner",
    "LanguageManager",
    "get_language_manager",
    "PACKAGE_DIR",
    "PROJECT_DIR",
    "DATA_DIR",
    "__version__",
]
