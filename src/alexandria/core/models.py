"""
Data models for Alexandria library system
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid


@dataclass
class Tag:
    """Represents a tag for categorizing entries"""
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    color: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert tag to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tag":
        """Create tag from dictionary"""
        return cls(
            name=data["name"],
            id=data.get("id", str(uuid.uuid4())),
            color=data.get("color"),
        )


@dataclass
class Category:
    """Represents a category for organizing entries"""
    name: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert category to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "parent_id": self.parent_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Category":
        """Create category from dictionary"""
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            id=data.get("id", str(uuid.uuid4())),
            parent_id=data.get("parent_id"),
        )


@dataclass
class Entry:
    """Represents a single entry/article in the library"""
    title: str
    content: str
    category_id: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tags: List[Tag] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    author: str = "Unknown"
    source: Optional[str] = None
    is_favorite: bool = False
    is_archived: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category_id": self.category_id,
            "tags": [tag.to_dict() for tag in self.tags],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "author": self.author,
            "source": self.source,
            "is_favorite": self.is_favorite,
            "is_archived": self.is_archived,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Entry":
        """Create entry from dictionary"""
        return cls(
            title=data["title"],
            content=data["content"],
            category_id=data.get("category_id"),
            id=data.get("id", str(uuid.uuid4())),
            tags=[Tag.from_dict(tag) for tag in data.get("tags", [])],
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
            author=data.get("author", "Unknown"),
            source=data.get("source"),
            is_favorite=data.get("is_favorite", False),
            is_archived=data.get("is_archived", False),
            metadata=data.get("metadata", {}),
        )

    def update_content(self, new_content: str) -> None:
        """Update entry content and timestamp"""
        self.content = new_content
        self.updated_at = datetime.now()

    def add_tag(self, tag: Tag) -> None:
        """Add a tag to the entry"""
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag_id: str) -> None:
        """Remove a tag from the entry"""
        self.tags = [tag for tag in self.tags if tag.id != tag_id]
