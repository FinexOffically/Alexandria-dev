"""
Example usage of Alexandria library
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from alexandria.core.database import Database
from alexandria.core.library import Library
from alexandria.core.models import Entry, Category, Tag


def example_basic_usage():
    """Example: Basic library operations"""
    print("\n=== Basic Usage Example ===\n")
    
    # Initialize database and library
    db = Database("example_data")
    library = Library(db)
    
    # Create categories
    print("Creating categories...")
    tech_category = library.create_category("Technology", "Tech-related entries")
    personal_category = library.create_category("Personal", "Personal notes and thoughts")
    
    # Create tags
    print("Creating tags...")
    python_tag = library.create_tag("Python")
    important_tag = library.create_tag("Important")
    
    # Create entries
    print("Creating entries...")
    
    entry1 = library.create_entry(
        title="Python Best Practices",
        content="Always follow PEP 8 guidelines. Use meaningful variable names...",
        author="Alice",
        category_id=tech_category.id,
    )
    
    entry1.add_tag(python_tag)
    entry1.add_tag(important_tag)
    db.update_entry(entry1)
    
    entry2 = library.create_entry(
        title="Morning Thoughts",
        content="Today was productive. Finished the Alexandria project.",
        author="Alice",
        category_id=personal_category.id,
    )
    
    # Operations
    print("\n--- All Entries ---")
    for entry in library.list_entries():
        print(f"  • {entry.title} by {entry.author}")
    
    print("\n--- Categories ---")
    for cat in library.list_categories():
        count = len(library.get_entries_in_category(cat.id))
        print(f"  • {cat.name}: {count} entries")
    
    print("\n--- Statistics ---")
    stats = library.get_statistics()
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Total categories: {stats['total_categories']}")
    print(f"  Total tags: {stats['total_tags']}")
    
    # Search
    print("\n--- Search Results ---")
    results = library.search_entries("Python")
    for result in results:
        print(f"  • {result.title}")


def example_advanced_features():
    """Example: Advanced features"""
    print("\n=== Advanced Features Example ===\n")
    
    db = Database("example_data")
    library = Library(db)
    
    if not library.list_entries():
        print("No entries found. Run basic example first.")
        return
    
    # Get first entry
    entry = library.list_entries()[0]
    print(f"Working with: {entry.title}\n")
    
    # Toggle favorite
    library.toggle_favorite(entry.id)
    print(f"✓ Marked as favorite")
    
    # Toggle archive
    library.toggle_archive(entry.id)
    print(f"✓ Archived entry")
    
    # Get preview
    preview = library.get_entry_preview(entry.id, max_length=100)
    print(f"✓ Preview: {preview}")
    
    # List by category
    if entry.category_id:
        entries_in_cat = library.get_entries_in_category(entry.category_id)
        print(f"✓ Entries in category: {len(entries_in_cat)}")
    
    # Export
    import json
    from datetime import datetime
    
    entries = library.list_entries()
    data = {
        "entries": [e.to_dict() for e in entries],
        "exported_at": datetime.now().isoformat(),
    }
    
    with open("library_backup.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Exported to library_backup.json")


if __name__ == "__main__":
    example_basic_usage()
    example_advanced_features()
    print("\n✨ Examples completed!\n")
