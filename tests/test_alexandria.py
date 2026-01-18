"""
Unit tests for Alexandria
Run with: python -m pytest tests/
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from alexandria.core.database import Database
from alexandria.core.library import Library
from alexandria.core.models import Entry, Category, Tag


class TestModels:
    """Test data models"""
    
    def test_tag_creation(self):
        """Test tag creation and conversion"""
        tag = Tag(name="Important", color="#FF0000")
        assert tag.name == "Important"
        assert tag.color == "#FF0000"
        assert tag.id is not None
    
    def test_tag_serialization(self):
        """Test tag to_dict and from_dict"""
        tag = Tag(name="Python", color="#0066FF")
        tag_dict = tag.to_dict()
        
        assert tag_dict["name"] == "Python"
        assert tag_dict["color"] == "#0066FF"
        
        restored = Tag.from_dict(tag_dict)
        assert restored.name == tag.name
        assert restored.color == tag.color
    
    def test_category_creation(self):
        """Test category creation"""
        cat = Category(name="Technology", description="Tech entries")
        assert cat.name == "Technology"
        assert cat.description == "Tech entries"
        assert cat.id is not None
    
    def test_entry_creation(self):
        """Test entry creation"""
        entry = Entry(
            title="Test Entry",
            content="This is a test entry",
            author="Test User"
        )
        assert entry.title == "Test Entry"
        assert entry.author == "Test User"
        assert not entry.is_favorite
        assert not entry.is_archived
    
    def test_entry_update_content(self):
        """Test entry content update"""
        entry = Entry(title="Test", content="Original")
        original_time = entry.updated_at
        
        entry.update_content("Updated content")
        assert entry.content == "Updated content"
        assert entry.updated_at > original_time
    
    def test_entry_tag_operations(self):
        """Test adding and removing tags"""
        entry = Entry(title="Test", content="Content")
        tag1 = Tag(name="Tag1")
        tag2 = Tag(name="Tag2")
        
        entry.add_tag(tag1)
        assert len(entry.tags) == 1
        
        entry.add_tag(tag2)
        assert len(entry.tags) == 2
        
        entry.remove_tag(tag1.id)
        assert len(entry.tags) == 1
        assert entry.tags[0].name == "Tag2"


class TestDatabase:
    """Test database operations"""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        temp_dir = tempfile.mkdtemp()
        db = Database(temp_dir)
        yield db
        shutil.rmtree(temp_dir)
    
    def test_entry_crud(self, temp_db):
        """Test entry CRUD operations"""
        entry = Entry(title="Test", content="Content")
        entry_id = temp_db.add_entry(entry)
        
        assert entry_id is not None
        retrieved = temp_db.get_entry(entry_id)
        assert retrieved is not None
        assert retrieved.title == "Test"
        
        assert temp_db.delete_entry(entry_id)
        assert temp_db.get_entry(entry_id) is None
    
    def test_search_entries(self, temp_db):
        """Test search functionality"""
        e1 = Entry(title="Python Guide", content="Learn Python")
        e2 = Entry(title="JavaScript", content="Web programming")
        
        temp_db.add_entry(e1)
        temp_db.add_entry(e2)
        
        results = temp_db.search_entries("Python")
        assert len(results) == 1
        assert results[0].title == "Python Guide"
    
    def test_category_operations(self, temp_db):
        """Test category operations"""
        cat = Category(name="Test Category")
        cat_id = temp_db.add_category(cat)
        
        retrieved = temp_db.get_category(cat_id)
        assert retrieved.name == "Test Category"
        
        assert temp_db.delete_category(cat_id)
    
    def test_tag_operations(self, temp_db):
        """Test tag operations"""
        tag = Tag(name="Important")
        tag_id = temp_db.add_tag(tag)
        
        retrieved = temp_db.get_tag(tag_id)
        assert retrieved.name == "Important"
        
        assert temp_db.delete_tag(tag_id)


class TestLibrary:
    """Test library operations"""
    
    @pytest.fixture
    def lib(self):
        """Create temporary library"""
        temp_dir = tempfile.mkdtemp()
        db = Database(temp_dir)
        library = Library(db)
        yield library
        shutil.rmtree(temp_dir)
    
    def test_create_entry(self, lib):
        """Test entry creation"""
        entry = lib.create_entry(
            title="Test",
            content="Content",
            author="Author"
        )
        assert entry is not None
        assert entry.author == "Author"
    
    def test_toggle_favorite(self, lib):
        """Test favorite toggle"""
        entry = lib.create_entry("Test", "Content")
        
        assert not entry.is_favorite
        result = lib.toggle_favorite(entry.id)
        assert result is True
        
        result = lib.toggle_favorite(entry.id)
        assert result is False
    
    def test_create_category_and_filter(self, lib):
        """Test category creation and filtering"""
        cat = lib.create_category("Technology")
        entry = lib.create_entry(
            "Python",
            "Content",
            category_id=cat.id
        )
        
        results = lib.get_entries_in_category(cat.id)
        assert len(results) == 1
        assert results[0].title == "Python"
    
    def test_create_tag_and_filter(self, lib):
        """Test tag creation and filtering"""
        tag = lib.create_tag("Important")
        entry = lib.create_entry("Test", "Content")
        
        lib.add_tag_to_entry(entry.id, tag.id)
        results = lib.get_entries_with_tag(tag.id)
        assert len(results) == 1
    
    def test_statistics(self, lib):
        """Test statistics"""
        lib.create_entry("Entry 1", "Content 1")
        lib.create_entry("Entry 2", "Content 2")
        lib.create_category("Cat 1")
        lib.create_tag("Tag 1")
        
        stats = lib.get_statistics()
        assert stats["total_entries"] == 2
        assert stats["total_categories"] == 1
        assert stats["total_tags"] == 1


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
