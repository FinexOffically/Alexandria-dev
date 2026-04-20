# 🏛️ Alexandria - Knowledge Management System

A powerful, feature-rich knowledge management and information organization system with SSH connection management, built in Python.

![Version](https://img.shields.io/badge/version-0.5.1-blue)
![Status](https://img.shields.io/badge/status-Production%20Ready-green)
![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

### 🌍 Multi-Language Support
- **Russian** (276+ translations) - Default language
- **English** (122+ translations)
- Easy language switching with `language` command

### 📚 Knowledge Management
- Create, edit, delete entries
- Organize with categories and tags
- Search and filter capabilities
- Favorites and archive system
- Export/import functionality

### 🔐 Security & Authentication
- User authentication with role-based access
- Root (admin) and user roles
- PBKDF2-SHA256 password hashing
- Access logging and audit trail
- Sudo command support for elevated operations

### 🖥️ SSH Connection Management (NEW!)
- Store and manage SSH connections
- Support for password and key-based authentication
- Connection testing and validation
- Automatic timestamp tracking
- 5 dedicated SSH management commands

### ⚙️ Advanced Features
- 80+ commands for various operations
- Color-coded terminal interface
- System information display
- Temporary email generation
- Global security scanning
- Pattern detection (emails, IPs, API keys, passwords)
- Comprehensive logging system

## Installation

### Requirements
- Python 3.6 or higher
- pip (Python package manager)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/FinexOffically/Alexandria.git
cd Alexandria

# Install dependencies (optional)
pip install -r requirements.txt

# Run Alexandria
python3 runalexa.py
```

### First Time Setup

```bash
# Default root password is 'root'
# Change it immediately for security!
$ python3 runalexa.py
🏛️ Alexandria - Knowledge Management System

Username: root
Password: root

[root] ➜ user create myuser newpassword
✅ User created successfully
```

## Usage

### SSH Connection Management

```bash
# Add SSH connection with password
ssh_add production web.example.com admin

# Add SSH connection with key
ssh_add staging app.example.com deploy --key ~/.ssh/app_key

# List all SSH connections
ssh_list

# Show connection details
ssh_info production

# Test SSH connection (requires paramiko)
ssh_test production

# Delete SSH connection
ssh_delete staging
```

### Basic Entry Management

```bash
# Create a new entry
create

# List all entries
list

# View entry content
view 1

# Edit entry
edit 1

# Delete entry
delete 1

# Search entries
search "keyword"
```

### User Management

```bash
# Create a new user
user create username password

# List all users
user list

# Delete user
user delete username

# Change password
pwdcheck

# Run command as admin
sudo <command>
```

### System Commands

```bash
# Show all available commands
help

# Change language
language ru

# Clear screen
clear or cc or cls

# View system information
sysinfo

# Generate temporary email
tempmail

# Exit application
exit or quit
```

## Project Structure

```
Alexandria/
├── src/
│   └── alexandria/
│       ├── core/
│       │   ├── database.py      # Database operations
│       │   ├── library.py       # Core library functions
│       │   ├── models.py        # Data models
│       │   └── __init__.py
│       └── ui/
│           ├── cli.py           # Command-line interface (3280+ lines)
│           ├── colors.py        # Color support
│           ├── languages.py     # Multi-language support
│           └── __init__.py
├── data/                         # Database storage (JSON)
│   ├── entries.json
│   ├── categories.json
│   ├── tags.json
│   ├── users.json
│   └── ssh_connections.json
├── tests/                        # Test suite
│   └── test_alexandria.py
├── config/                       # Configuration files
│   └── settings.py
├── runalexa.py                   # Main entry point
├── setup.py                      # Package setup
└── README.md                      # This file
```

## Commands Reference

### User & Authentication (3 commands)
- `init` - Initialize database
- `user` - User management
- `sudo` - Execute as administrator

### Entry Management (3 commands)
- `create` - Create new entry
- `edit` - Edit existing entry
- `delete` - Delete entry

### Viewing & Search (3 commands)
- `list` - List all entries
- `view` - View entry details
- `search` - Search entries

### Categories & Tags (2 commands)
- `category` - Manage categories
- `tag` - Manage tags

### Organization (2 commands)
- `favorite` - Mark as favorite
- `archive` - Archive entries

### Information & Export (4 commands)
- `stats` - Show statistics
- `export` - Export library
- `import` - Import library
- `backup` - Backup database

### SSH Connections (5 commands) ⭐ NEW
- `ssh_add` - Add SSH connection
- `ssh_list` - List connections
- `ssh_info` - Connection details
- `ssh_test` - Test connectivity
- `ssh_delete` - Delete connection

### System & Utilities (14+ commands)
- `sysinfo` - System information
- `logs` - View activity logs
- `scan` - Security scan
- `analyze` - Analyze entries
- `tempmail` - Generate temporary email
- `clear/cc/cls` - Clear screen
- `language` - Change language
- `help` - Show help
- `exit/quit` - Exit application

### Unix-Style Shortcuts (13 commands)
- `ls`, `cd`, `pwd`, `cat`, `rm`, `cp`, `mv`, `grep`, `wc`, `head`, `tail`, `open`, `new`

**Total: 80+ commands**

## Configuration

### Language Settings
Edit `src/alexandria/ui/languages.py` to add or modify translations.

### Database Settings
Edit `config/settings.py` for database configuration.

### Color Scheme
Modify `src/alexandria/ui/colors.py` for custom colors.

## Testing

```bash
# Run comprehensive tests
python3 tests/test_alexandria.py

# Run SSH functionality tests
python3 test_ssh_comprehensive.py

# Show all commands
python3 show_all_commands.py
```

## Optional Dependencies

### SSH Connection Testing
For SSH connection testing functionality, install paramiko:

```bash
pip install paramiko
```

Without paramiko, SSH storage and management work normally, but `ssh_test` command will inform you to install it.

## Security Considerations

1. **Change Default Password**: Root account uses 'root' by default - change immediately
2. **SSH Keys**: Store SSH keys securely, not in Alexandria data
3. **Password Storage**: Passwords are hashed with PBKDF2-SHA256
4. **Access Logs**: Check logs regularly with `logs` command
5. **Backups**: Use `backup` command regularly
6. **Database Access**: Keep `data/` directory secure

## Performance

- **Memory**: Minimal footprint (~50MB with data)
- **Storage**: Efficient JSON-based storage
- **Speed**: Instant command execution
- **Scalability**: Handles 1000s of entries smoothly

## Troubleshooting

### Module Not Found Error
```bash
# Ensure src directory is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python3 runalexa.py
```

### Permission Denied
```bash
chmod +x runalexa.py
python3 runalexa.py
```

### Database Corruption
```bash
# Use backup and restore
backup  # Create backup first
restore # Restore from backup
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Development

### Adding New Commands
1. Create `do_<command>` method in `AlexandriaShell` class (cli.py)
2. Add help text to method docstring
3. Add translations to languages.py
4. Test with comprehensive unit tests

### Adding New Languages
1. Add language code to `TRANSLATIONS` dict in languages.py
2. Translate all keys from English/Russian templates
3. Test language switching

## License

MIT License - see LICENSE file for details

## Author

**Gabrielle** - Alexandria Developer
- GitHub: [@gabrielle](https://github.com)

## Changelog

### v0.5.1 (Current)
- ✨ SSH connection management system (5 new commands)
- 🌍 276+ Russian translations (default language)
- 🔐 Enhanced security with SSH support
- 📝 Comprehensive documentation
- ✅ Full test coverage

### v0.5.0
- 🏛️ Initial release
- 📚 Knowledge management features
- 🔐 User authentication
- 🌍 Multi-language support
- 80+ commands

## Roadmap

- [ ] Web interface (Flask/FastAPI)
- [ ] Cloud synchronization
- [ ] Mobile app
- [ ] Advanced search with Elasticsearch
- [ ] Team collaboration features
- [ ] Version control for entries
- [ ] API server

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check documentation in `SSH_IMPLEMENTATION.md`
- Review help with `help` command in Alexandria

## Statistics

- **Lines of Code**: 6500+
- **Commands**: 80+
- **Translations**: 398+ (276 Russian, 122 English)
- **Database Files**: 5 (entries, categories, tags, users, SSH connections)
- **Test Coverage**: 20+ unit tests
- **Documentation**: 6000+ lines

---

**Made with ❤️ for knowledge management**

![Alexandria Logo](./logo.txt)

🏛️ Alexandria - Your Personal Knowledge Management System
