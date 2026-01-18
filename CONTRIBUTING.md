# Contributing to Alexandria

First off, thank you for considering contributing to Alexandria! It's people like you that make Alexandria such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your Python version and OS**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior** and **the expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python styleguide
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Use emojis to categorize:
  * 🏛️ for Alexandria/project changes
  * ✨ for new features
  * 🐛 for bug fixes
  * 📚 for documentation
  * 🔒 for security fixes
  * 🌍 for language/internationalization
  * ♻️ for refactoring
  * ⚡ for performance improvements
  * 🧪 for tests

### Python Styleguide

* Follow PEP 8
* Use 4 spaces for indentation
* Use meaningful variable names
* Add docstrings to functions and classes
* Add type hints where possible
* Keep lines under 100 characters

Example:
```python
def add_ssh_connection(self, name: str, host: str, user: str, 
                      port: int = 22, auth_type: str = "password") -> str:
    """
    Add or update SSH connection details.
    
    Args:
        name: Connection name
        host: SSH host address
        user: SSH username
        port: SSH port (default 22)
        auth_type: Authentication type ("password" or "key")
    
    Returns:
        Success message string
    """
    # Implementation
```

## Development Setup

1. Fork the repo and clone it
```bash
git clone https://github.com/your-username/Alexandria.git
cd Alexandria
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a feature branch
```bash
git checkout -b feature/your-feature-name
```

5. Make your changes and test
```bash
python3 tests/test_alexandria.py
```

6. Commit with meaningful messages
```bash
git commit -m "✨ Add new feature: description"
```

7. Push to your fork
```bash
git push origin feature/your-feature-name
```

8. Create a Pull Request

## Testing

* Write tests for all new features
* Ensure all tests pass before submitting PR
* Aim for >80% code coverage
* Test on Python 3.6+

```bash
# Run tests
python3 tests/test_alexandria.py

# Run SSH tests
python3 test_ssh_comprehensive.py

# Check code quality
python3 -m py_compile src/alexandria/**/*.py
```

## Documentation

* Update README.md if you change functionality
* Add docstrings to new functions/classes
* Update help text in commands
* Add translations (Russian + English) for new features
* Keep documentation clear and concise

## Translation

To add a new language or translate existing content:

1. Add new language code to `TRANSLATIONS` dict in `src/alexandria/ui/languages.py`
2. Translate all keys (use existing Russian/English as template)
3. Test language switching with `language <code>` command
4. Update documentation

## Recognition

Contributors will be recognized in:
* CONTRIBUTORS.md file
* Release notes
* GitHub contributors page

## Questions?

Feel free to open an issue with the question tag or email us directly.

---

Happy contributing! 🎉
