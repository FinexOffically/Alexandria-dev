"""
Library manager - High-level interface for Alexandria
"""

from typing import List, Optional, Dict, Any
import hashlib
import secrets
from datetime import datetime
from .database import Database
from .models import Entry, Category, Tag


class Library:
    """Main library interface for Alexandria"""

    def __init__(self, database: Database):
        """Initialize library with database"""
        self.db = database
        self.users = self.db.load_users()
        
    def _hash_password(self, password: str) -> str:
        """Hash password with SHA256"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${pwd_hash.hex()}"
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            salt, pwd_hash = hashed.split('$')
            new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return new_hash.hex() == pwd_hash
        except:
            return False
    
    # User management
    def create_user(self, username: str, password: str) -> Dict[str, Any]:
        """Create a new user account"""
        if username in self.users:
            return {"success": False, "error": "User already exists"}
        
        if len(username) < 3 or not username.isalnum():
            return {"success": False, "error": "Invalid username"}
        
        if len(password) < 4:
            return {"success": False, "error": "Password too short"}
        
        user = {
            "username": username,
            "password": self._hash_password(password),
            "created": datetime.now().isoformat(),
            "is_admin": username == "root",
        }
        self.users[username] = user
        self.db.save_users(self.users)
        return {"success": True, "user": username}
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user credentials"""
        if username not in self.users:
            self.log_access(username, "login", "FAILED - User not found")
            return {"success": False, "error": "User not found"}
        
        user = self.users[username]
        if self._verify_password(password, user["password"]):
            self.log_access(username, "login", "SUCCESS")
            return {"success": True, "user": username, "is_admin": user.get("is_admin", False)}
        
        self.log_access(username, "login", "FAILED - Invalid password")
        return {"success": False, "error": "Invalid password"}
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user info"""
        if username in self.users:
            user = self.users[username].copy()
            user.pop("password", None)  # Don't expose password hash
            return user
        return None
    
    def list_users(self) -> List[str]:
        """List all users"""
        return list(self.users.keys())
    
    def delete_user(self, username: str) -> bool:
        """Delete a user"""
        if username == "root":
            return False
        if username in self.users:
            del self.users[username]
            self.db.save_users(self.users)
            return True
        return False
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        return username in self.users

    # Entry management
    def create_entry(
        self,
        title: str,
        content: str,
        author: str = "Unknown",
        category_id: Optional[str] = None,
        source: Optional[str] = None,
        tags: Optional[List[Tag]] = None,
    ) -> Entry:
        """Create a new entry"""
        entry = Entry(
            title=title,
            content=content,
            author=author,
            category_id=category_id,
            source=source,
            tags=tags or [],
        )
        self.db.add_entry(entry)
        return entry

    def edit_entry(self, entry_id: str, title: str = None, content: str = None, author: str = None) -> Optional[Entry]:
        """Edit an existing entry"""
        entry = self.db.get_entry(entry_id)
        if entry:
            if title:
                entry.title = title
            if content:
                entry.update_content(content)
            if author:
                entry.author = author
            self.db.update_entry(entry)
        return entry

    def delete_entry(self, entry_id: str) -> bool:
        """Delete an entry"""
        return self.db.delete_entry(entry_id)

    def get_entry(self, entry_id: str) -> Optional[Entry]:
        """Get an entry"""
        return self.db.get_entry(entry_id)

    def list_entries(self) -> List[Entry]:
        """List all entries"""
        return self.db.get_all_entries()

    def search_entries(self, query: str) -> List[Entry]:
        """Search entries"""
        return self.db.search_entries(query)

    def get_entry_preview(self, entry_id: str, max_length: int = 200) -> Optional[str]:
        """Get a preview of entry content"""
        entry = self.db.get_entry(entry_id)
        if entry:
            preview = entry.content[:max_length]
            if len(entry.content) > max_length:
                preview += "..."
            return preview
        return None

    def toggle_favorite(self, entry_id: str) -> Optional[bool]:
        """Toggle favorite status"""
        entry = self.db.get_entry(entry_id)
        if entry:
            entry.is_favorite = not entry.is_favorite
            self.db.update_entry(entry)
            return entry.is_favorite
        return None

    def toggle_archive(self, entry_id: str) -> Optional[bool]:
        """Toggle archived status"""
        entry = self.db.get_entry(entry_id)
        if entry:
            entry.is_archived = not entry.is_archived
            self.db.update_entry(entry)
            return entry.is_archived
        return None

    # Category management
    def create_category(
        self,
        name: str,
        description: str = "",
        parent_id: Optional[str] = None,
    ) -> Category:
        """Create a new category"""
        category = Category(
            name=name,
            description=description,
            parent_id=parent_id,
        )
        self.db.add_category(category)
        return category

    def delete_category(self, category_id: str) -> bool:
        """Delete a category"""
        return self.db.delete_category(category_id)

    def get_category(self, category_id: str) -> Optional[Category]:
        """Get a category"""
        return self.db.get_category(category_id)

    def list_categories(self) -> List[Category]:
        """List all categories"""
        return self.db.get_all_categories()

    def get_entries_in_category(self, category_id: str) -> List[Entry]:
        """Get entries in a category"""
        return self.db.get_entries_by_category(category_id)

    # Tag management
    def create_tag(self, name: str, color: Optional[str] = None) -> Tag:
        """Create a new tag"""
        tag = Tag(name=name, color=color)
        self.db.add_tag(tag)
        return tag

    def delete_tag(self, tag_id: str) -> bool:
        """Delete a tag"""
        return self.db.delete_tag(tag_id)

    def get_tag(self, tag_id: str) -> Optional[Tag]:
        """Get a tag"""
        return self.db.get_tag(tag_id)

    def list_tags(self) -> List[Tag]:
        """List all tags"""
        return self.db.get_all_tags()

    def add_tag_to_entry(self, entry_id: str, tag_id: str) -> bool:
        """Add a tag to an entry"""
        entry = self.db.get_entry(entry_id)
        tag = self.db.get_tag(tag_id)
        if entry and tag:
            entry.add_tag(tag)
            self.db.update_entry(entry)
            return True
        return False

    def remove_tag_from_entry(self, entry_id: str, tag_id: str) -> bool:
        """Remove a tag from an entry"""
        entry = self.db.get_entry(entry_id)
        if entry:
            entry.remove_tag(tag_id)
            self.db.update_entry(entry)
            return True
        return False

    def get_entries_with_tag(self, tag_id: str) -> List[Entry]:
        """Get all entries with a specific tag"""
        return self.db.get_entries_by_tag(tag_id)

    # Statistics and info
    def get_statistics(self) -> Dict[str, Any]:
        """Get library statistics"""
        return self.db.get_statistics()

    def get_library_info(self) -> Dict[str, Any]:
        """Get comprehensive library information"""
        stats = self.get_statistics()
        return {
            **stats,
            "categories": self.list_categories(),
            "tags": self.list_tags(),
        }
    # Security & Analysis
    def check_password_strength(self, password: str) -> Dict[str, Any]:
        """Analyze password strength with detailed feedback"""
        import re
        
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Too short (min 8 chars)")
        
        if len(password) >= 12:
            score += 1
        
        # Character variety
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if re.search(r'[0-9]', password):
            score += 1
        else:
            feedback.append("Add numbers")
        
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:,.<>?]', password):
            score += 2
        else:
            feedback.append("Add special characters (!@#$%...)")
        
        # Determine strength level
        if score >= 8:
            strength = "VERY_STRONG"
            emoji = "🟢"
        elif score >= 6:
            strength = "STRONG"
            emoji = "🟢"
        elif score >= 4:
            strength = "MEDIUM"
            emoji = "🟡"
        elif score >= 2:
            strength = "WEAK"
            emoji = "🔴"
        else:
            strength = "VERY_WEAK"
            emoji = "🔴"
        
        return {
            "strength": strength,
            "score": score,
            "emoji": emoji,
            "feedback": feedback if feedback else ["Password looks good!"],
            "entropy": len(set(password))
        }
    
    def search_entries_advanced(self, query: str, regex: bool = False, case_sensitive: bool = False) -> List[Entry]:
        """Advanced search with regex support"""
        import re
        
        results = []
        entries = self.list_entries()
        
        if regex:
            try:
                flags = 0 if case_sensitive else re.IGNORECASE
                pattern = re.compile(query, flags)
                for entry in entries:
                    if (pattern.search(entry.title) or 
                        pattern.search(entry.content) or
                        pattern.search(entry.author)):
                        results.append(entry)
            except re.error as e:
                return []
        else:
            query_lower = query if case_sensitive else query.lower()
            for entry in entries:
                entry_text = f"{entry.title} {entry.content} {entry.author}"
                if case_sensitive:
                    if query in entry_text:
                        results.append(entry)
                else:
                    if query_lower in entry_text.lower():
                        results.append(entry)
        
        return results
    
    def find_vulnerabilities(self) -> Dict[str, Any]:
        """Scan library for security issues"""
        issues = []
        warnings = []
        
        # Check weak passwords
        for username in self.users:
            user = self.users[username]
            # Store a test to see if we can identify weak patterns
            if len(username) < 4:
                warnings.append(f"Short username: '{username}'")
        
        # Check entries without categories
        uncategorized = [e for e in self.list_entries() if not e.category_id]
        if len(uncategorized) > 0:
            warnings.append(f"{len(uncategorized)} entries without categories")
        
        # Check for duplicate content
        contents = {}
        for entry in self.list_entries():
            content_hash = hashlib.md5(entry.content.encode()).hexdigest()
            if content_hash in contents:
                issues.append(f"Duplicate content: '{entry.title}' vs '{contents[content_hash]}'")
            else:
                contents[content_hash] = entry.title
        
        # Check old entries (no updates)
        from datetime import datetime, timedelta
        old_date = datetime.now() - timedelta(days=90)
        old_entries = [e for e in self.list_entries() if e.created_at < old_date]
        if len(old_entries) > 0:
            warnings.append(f"{len(old_entries)} entries not updated in 90 days")
        
        return {
            "vulnerabilities": issues,
            "warnings": warnings,
            "total_issues": len(issues),
            "total_warnings": len(warnings),
            "security_score": max(0, 100 - len(issues)*10 - len(warnings)*5)
        }
    
    def analyze_content(self, entry_id: str) -> Dict[str, Any]:
        """Analyze single entry content for patterns"""
        import re
        
        entry = self.get_entry(entry_id)
        if not entry:
            return None
        
        content = entry.content
        
        # Find patterns
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
        urls = re.findall(r'https?://[^\s]+', content)
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)
        passwords = re.findall(r'(?:password|pwd|pass)[:=\s]+([^\s]+)', content, re.IGNORECASE)
        api_keys = re.findall(r'(?:api[_-]?key|token|secret)[:=\s]+([a-zA-Z0-9_-]+)', content, re.IGNORECASE)
        
        return {
            "entry_id": entry_id,
            "title": entry.title,
            "word_count": len(content.split()),
            "char_count": len(content),
            "emails_found": emails,
            "urls_found": urls,
            "ips_found": ips,
            "potential_passwords": passwords,
            "potential_api_keys": api_keys,
            "unique_words": len(set(content.lower().split())),
            "sentiment_hints": {
                "positive": len(re.findall(r'\b(good|great|excellent|amazing|perfect|love)\b', content, re.IGNORECASE)),
                "negative": len(re.findall(r'\b(bad|terrible|awful|hate|poor|worst)\b', content, re.IGNORECASE)),
            }
        }
    
    def get_access_log(self) -> List[Dict[str, Any]]:
        """Get login/access log"""
        log_file = self.db.data_dir / "access.log"
        logs = []
        
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    for line in f:
                        logs.append(line.strip())
            except:
                pass
        
        return logs
    
    def log_access(self, username: str, action: str, status: str) -> None:
        """Log user access"""
        log_file = self.db.data_dir / "access.log"
        timestamp = datetime.now().isoformat()
        
        try:
            with open(log_file, 'a') as f:
                f.write(f"[{timestamp}] {username} - {action} - {status}\n")
        except:
            pass
    
    # Global logging system
    def log_action(self, user: str, action: str, details: str = "", status: str = "OK") -> None:
        """Log any user action globally"""
        log_file = self.db.data_dir / "system.log"
        timestamp = datetime.now().isoformat()
        
        try:
            with open(log_file, 'a') as f:
                f.write(f"[{timestamp}] {user:15} | {action:20} | {details:40} | {status}\n")
        except:
            pass
    
    def get_system_logs(self, limit: int = 100) -> List[str]:
        """Get all system logs"""
        log_file = self.db.data_dir / "system.log"
        logs = []
        
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    all_lines = f.readlines()
                    # Return last 'limit' lines
                    for line in all_lines[-limit:]:
                        logs.append(line.strip())
            except:
                pass
        
        return logs
    
    def search_logs(self, query: str, limit: int = 100) -> List[str]:
        """Search system logs"""
        all_logs = self.get_system_logs(limit=limit*2)  # Get more to search through
        results = []
        
        query_lower = query.lower()
        for log in all_logs:
            if query_lower in log.lower():
                results.append(log)
        
        return results[-limit:]  # Return last 'limit' matches
    
    def get_user_activity(self, username: str, limit: int = 100) -> List[str]:
        """Get activity log for specific user"""
        logs = self.get_system_logs(limit=limit*2)
        results = []
        
        for log in logs:
            if username in log:
                results.append(log)
        
        return results[-limit:]
    
    # Temporary email generation
    def generate_temp_email(self) -> str:
        """Generate a temporary email address"""
        import random
        import string
        
        # Generate random string
        random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        
        # Temporary email domains
        temp_domains = [
            "tempmail.com",
            "throwaway.email",
            "guerrillamail.com",
            "10minutemail.com",
            "mailinator.com",
            "temp-mail.org"
        ]
        
        domain = random.choice(temp_domains)
        return f"{random_part}@{domain}"
    
    def generate_temp_email_with_name(self, name: str = None) -> str:
        """Generate temporary email with optional name prefix"""
        import random
        import string
        
        if name:
            username_part = name.lower().replace(" ", "")[:8]
        else:
            username_part = ''.join(random.choices(string.ascii_lowercase, k=6))
        
        timestamp = str(int(datetime.now().timestamp()))[-4:]
        
        temp_domains = [
            "tempmail.com",
            "throwaway.email",
            "guerrillamail.com"
        ]
        
        domain = random.choice(temp_domains)
        return f"{username_part}{timestamp}@{domain}"
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        import platform
        import os
        
        log_dir = self.db.data_dir
        system_log = log_dir / "system.log"
        access_log = log_dir / "access.log"
        
        return {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "log_directory": str(log_dir),
            "system_log": str(system_log),
            "access_log": str(access_log),
            "system_log_size": system_log.stat().st_size if system_log.exists() else 0,
            "access_log_size": access_log.stat().st_size if access_log.exists() else 0,
            "total_users": len(self.users),
            "total_entries": len(self.list_entries()),
        }

    # SSH Connection Management
    def add_ssh_connection(self, name, host, user, port=22, auth_type="password", password=None, key_path=None):
        """Add or update SSH connection details."""
        ssh_connections = self.db.load_ssh_connections()
        
        ssh_connections[name] = {
            "host": host,
            "user": user,
            "port": port,
            "auth_type": auth_type,  # "password" or "key"
            "password": password,
            "key_path": key_path,
            "created": str(datetime.now()),
            "last_used": None
        }
        self.db.save_ssh_connections(ssh_connections)
        return f"SSH connection '{name}' saved successfully"

    def get_ssh_connection(self, name):
        """Get SSH connection details by name."""
        ssh_connections = self.db.load_ssh_connections()
        if name in ssh_connections:
            return ssh_connections[name]
        return None

    def list_ssh_connections(self):
        """List all saved SSH connections."""
        ssh_connections = self.db.load_ssh_connections()
        return list(ssh_connections.keys())

    def delete_ssh_connection(self, name):
        """Delete SSH connection by name."""
        ssh_connections = self.db.load_ssh_connections()
        if name in ssh_connections:
            del ssh_connections[name]
            self.db.save_ssh_connections(ssh_connections)
            return f"SSH connection '{name}' deleted successfully"
        return None

    def test_ssh_connection(self, name):
        """Test SSH connection (requires paramiko library)."""
        try:
            import paramiko
            conn = self.get_ssh_connection(name)
            if not conn:
                return False, f"Connection '{name}' not found"
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            try:
                if conn['auth_type'] == 'key':
                    ssh.connect(conn['host'], port=conn['port'], username=conn['user'], 
                              key_filename=conn['key_path'], timeout=5)
                else:
                    ssh.connect(conn['host'], port=conn['port'], username=conn['user'], 
                              password=conn['password'], timeout=5)
                
                # Update last_used timestamp
                ssh_connections = self.db.load_ssh_connections()
                ssh_connections[name]['last_used'] = str(datetime.now())
                self.db.save_ssh_connections(ssh_connections)
                ssh.close()
                return True, f"Connection to {conn['host']} successful"
            except paramiko.AuthenticationException:
                return False, "Authentication failed"
            except paramiko.SSHException as e:
                return False, f"SSH error: {str(e)}"
            except Exception as e:
                return False, f"Connection error: {str(e)}"
        except ImportError:
            return False, "paramiko library not installed. Install with: pip install paramiko"

    def update_ssh_connection_timestamp(self, name):
        """Update the last_used timestamp for an SSH connection."""
        ssh_connections = self.db.load_ssh_connections()
        if name in ssh_connections:
            ssh_connections[name]['last_used'] = str(datetime.now())
            self.db.save_ssh_connections(ssh_connections)
