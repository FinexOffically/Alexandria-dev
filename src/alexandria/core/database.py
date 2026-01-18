"""
Database operations for Alexandria
Handles persistence of library data
"""

import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from .models import Entry, Category, Tag


logger = logging.getLogger(__name__)


class Database:
    """Manages persistent storage for Alexandria library"""

    def __init__(self, data_dir: str = "data"):
        """Initialize database with data directory"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.entries_file = self.data_dir / "entries.json"
        self.categories_file = self.data_dir / "categories.json"
        self.tags_file = self.data_dir / "tags.json"
        
        self._entries: Dict[str, Entry] = {}
        self._categories: Dict[str, Category] = {}
        self._tags: Dict[str, Tag] = {}
        
        self._load_all()

    def _load_all(self) -> None:
        """Load all data from files"""
        logger.info("Loading database...")
        self._load_entries()
        self._load_categories()
        self._load_tags()
        logger.info("Database loaded successfully")

    def _load_entries(self) -> None:
        """Load entries from file"""
        if self.entries_file.exists():
            try:
                with open(self.entries_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._entries = {
                        entry_id: Entry.from_dict(entry_data)
                        for entry_id, entry_data in data.items()
                    }
            except Exception as e:
                logger.error(f"Error loading entries: {e}")
                self._entries = {}

    def _load_categories(self) -> None:
        """Load categories from file"""
        if self.categories_file.exists():
            try:
                with open(self.categories_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._categories = {
                        cat_id: Category.from_dict(cat_data)
                        for cat_id, cat_data in data.items()
                    }
            except Exception as e:
                logger.error(f"Error loading categories: {e}")
                self._categories = {}

    def _load_tags(self) -> None:
        """Load tags from file"""
        if self.tags_file.exists():
            try:
                with open(self.tags_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._tags = {
                        tag_id: Tag.from_dict(tag_data)
                        for tag_id, tag_data in data.items()
                    }
            except Exception as e:
                logger.error(f"Error loading tags: {e}")
                self._tags = {}

    def save_entries(self) -> None:
        """Save all entries to file"""
        try:
            with open(self.entries_file, "w", encoding="utf-8") as f:
                json.dump(
                    {entry_id: entry.to_dict() for entry_id, entry in self._entries.items()},
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
            logger.info("Entries saved successfully")
        except Exception as e:
            logger.error(f"Error saving entries: {e}")

    def save_categories(self) -> None:
        """Save all categories to file"""
        try:
            with open(self.categories_file, "w", encoding="utf-8") as f:
                json.dump(
                    {cat_id: cat.to_dict() for cat_id, cat in self._categories.items()},
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
            logger.info("Categories saved successfully")
        except Exception as e:
            logger.error(f"Error saving categories: {e}")

    def save_tags(self) -> None:
        """Save all tags to file"""
        try:
            with open(self.tags_file, "w", encoding="utf-8") as f:
                json.dump(
                    {tag_id: tag.to_dict() for tag_id, tag in self._tags.items()},
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
            logger.info("Tags saved successfully")
        except Exception as e:
            logger.error(f"Error saving tags: {e}")

    def save_all(self) -> None:
        """Save all data to files"""
        self.save_entries()
        self.save_categories()
        self.save_tags()

    # Entry operations
    def add_entry(self, entry: Entry) -> str:
        """Add an entry to the database"""
        self._entries[entry.id] = entry
        self.save_entries()
        logger.info(f"Entry added: {entry.title} ({entry.id})")
        return entry.id

    def get_entry(self, entry_id: str) -> Optional[Entry]:
        """Get an entry by ID"""
        return self._entries.get(entry_id)

    def get_all_entries(self) -> List[Entry]:
        """Get all entries"""
        return list(self._entries.values())

    def update_entry(self, entry: Entry) -> None:
        """Update an existing entry"""
        if entry.id in self._entries:
            self._entries[entry.id] = entry
            self.save_entries()
            logger.info(f"Entry updated: {entry.title}")
        else:
            logger.warning(f"Entry not found: {entry.id}")

    def delete_entry(self, entry_id: str) -> bool:
        """Delete an entry by ID"""
        if entry_id in self._entries:
            del self._entries[entry_id]
            self.save_entries()
            logger.info(f"Entry deleted: {entry_id}")
            return True
        logger.warning(f"Entry not found: {entry_id}")
        return False

    def search_entries(self, query: str) -> List[Entry]:
        """Search entries by title or content"""
        query_lower = query.lower()
        results = []
        for entry in self._entries.values():
            if (query_lower in entry.title.lower() or 
                query_lower in entry.content.lower()):
                results.append(entry)
        return results

    def get_entries_by_category(self, category_id: str) -> List[Entry]:
        """Get all entries in a category"""
        return [e for e in self._entries.values() if e.category_id == category_id]

    def get_entries_by_tag(self, tag_id: str) -> List[Entry]:
        """Get all entries with a specific tag"""
        return [e for e in self._entries.values() if any(t.id == tag_id for t in e.tags)]

    def get_favorite_entries(self) -> List[Entry]:
        """Get all favorite entries"""
        return [e for e in self._entries.values() if e.is_favorite]

    # Category operations
    def add_category(self, category: Category) -> str:
        """Add a category to the database"""
        self._categories[category.id] = category
        self.save_categories()
        logger.info(f"Category added: {category.name}")
        return category.id

    def get_category(self, category_id: str) -> Optional[Category]:
        """Get a category by ID"""
        return self._categories.get(category_id)

    def get_all_categories(self) -> List[Category]:
        """Get all categories"""
        return list(self._categories.values())

    def update_category(self, category: Category) -> None:
        """Update a category"""
        if category.id in self._categories:
            self._categories[category.id] = category
            self.save_categories()
            logger.info(f"Category updated: {category.name}")

    def delete_category(self, category_id: str) -> bool:
        """Delete a category"""
        if category_id in self._categories:
            del self._categories[category_id]
            self.save_categories()
            logger.info(f"Category deleted: {category_id}")
            return True
        return False

    # Tag operations
    def add_tag(self, tag: Tag) -> str:
        """Add a tag to the database"""
        self._tags[tag.id] = tag
        self.save_tags()
        logger.info(f"Tag added: {tag.name}")
        return tag.id

    def get_tag(self, tag_id: str) -> Optional[Tag]:
        """Get a tag by ID"""
        return self._tags.get(tag_id)

    def get_all_tags(self) -> List[Tag]:
        """Get all tags"""
        return list(self._tags.values())

    def update_tag(self, tag: Tag) -> None:
        """Update a tag"""
        if tag.id in self._tags:
            self._tags[tag.id] = tag
            self.save_tags()
            logger.info(f"Tag updated: {tag.name}")

    def delete_tag(self, tag_id: str) -> bool:
        """Delete a tag"""
        if tag_id in self._tags:
            del self._tags[tag_id]
            self.save_tags()
            logger.info(f"Tag deleted: {tag_id}")
            return True
        return False

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            "total_entries": len(self._entries),
            "total_categories": len(self._categories),
            "total_tags": len(self._tags),
            "favorite_entries": len(self.get_favorite_entries()),
            "archived_entries": len([e for e in self._entries.values() if e.is_archived]),
        }

    # User management
    def load_users(self) -> Dict[str, Any]:
        """Load users from file"""
        users_file = self.data_dir / "users.json"
        if users_file.exists():
            try:
                with open(users_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading users: {e}")
        return {}
    
    def save_users(self, users: Dict[str, Any]) -> None:
        """Save users to file"""
        users_file = self.data_dir / "users.json"
        try:
            with open(users_file, "w", encoding="utf-8") as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
            logger.info("Users saved successfully")
        except Exception as e:
            logger.error(f"Error saving users: {e}")

    def save(self) -> None:
        """Save all data"""
        self.save_entries()
        self.save_categories()
        self.save_tags()

    # SSH Connection management
    def load_ssh_connections(self) -> Dict[str, Any]:
        """Load SSH connections from file"""
        ssh_file = self.data_dir / "ssh_connections.json"
        if ssh_file.exists():
            try:
                with open(ssh_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading SSH connections: {e}")
        return {}
    
    def save_ssh_connections(self, connections: Dict[str, Any]) -> None:
        """Save SSH connections to file"""
        ssh_file = self.data_dir / "ssh_connections.json"
        try:
            with open(ssh_file, "w", encoding="utf-8") as f:
                json.dump(connections, f, indent=2, ensure_ascii=False)
            logger.info("SSH connections saved successfully")
        except Exception as e:
            logger.error(f"Error saving SSH connections: {e}")
