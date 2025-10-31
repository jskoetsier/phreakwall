# Contributing to Phreakwall

First off, thank you for considering contributing to Phreakwall! It's people like you that make Phreakwall such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to conduct@phreakwall.org.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include logs and error messages

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### Pull Requests

* Fill in the required template
* Follow the Python style guide (PEP 8)
* Include appropriate test coverage
* Update documentation as needed
* End all files with a newline

## Development Setup

### Prerequisites

* Python 3.10 or higher
* Git
* Linux system (for full testing)

### Setting Up Your Development Environment

1. Fork the repository

2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/phreakwall.git
   cd phreakwall
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

5. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Style

Phreakwall follows PEP 8 with some modifications:

* Line length: 100 characters (not 79)
* Use type hints for all function signatures
* Use docstrings for all public modules, functions, classes, and methods
* Follow Google-style docstring format

### Running Linters

```bash
# Format code
black phreakwall tests

# Check style
ruff check phreakwall tests

# Type checking
mypy phreakwall
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=phreakwall --cov-report=html

# Run specific test file
pytest tests/test_compiler.py

# Run specific test
pytest tests/test_compiler.py::test_compiler_init
```

### Writing Tests

* Write tests for all new features
* Maintain or improve code coverage
* Use descriptive test names
* Use pytest fixtures for common setup
* Mock external dependencies

Example:
```python
import pytest
from phreakwall.core.compiler import Compiler

def test_compiler_initialization():
    """Test that compiler initializes correctly."""
    compiler = Compiler(options=default_options())
    assert compiler.VERSION == "6.0.0"
```

## Documentation

### Code Documentation

* All public modules, classes, and functions must have docstrings
* Use Google-style docstrings
* Include type hints
* Provide examples for complex functions

Example:
```python
def process_rule(rule: str, zone: str) -> List[str]:
    """
    Process a firewall rule for a specific zone.

    Args:
        rule: The rule specification string
        zone: The target zone name

    Returns:
        List of iptables commands

    Raises:
        ValueError: If rule is invalid

    Example:
        >>> process_rule("ACCEPT tcp 22", "net")
        ['iptables -A INPUT -p tcp --dport 22 -j ACCEPT']
    """
```

### Documentation Files

* Update README.md for user-facing changes
* Update CHANGELOG.md for all changes
* Add examples to docs/examples/ for new features

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

* **feat**: A new feature
* **fix**: A bug fix
* **docs**: Documentation only changes
* **style**: Changes that don't affect code meaning (formatting, etc.)
* **refactor**: Code change that neither fixes a bug nor adds a feature
* **perf**: Performance improvement
* **test**: Adding or updating tests
* **chore**: Changes to build process or auxiliary tools

### Examples

```
feat(compiler): add support for nftables backend

Implement initial nftables backend support alongside existing
iptables backend. Users can now choose between backends.

Closes #123
```

```
fix(zones): handle empty zone definitions correctly

Previously crashed when zones file was empty. Now handles
gracefully with a warning message.

Fixes #456
```

## Release Process

### Versioning

Phreakwall follows [Semantic Versioning](https://semver.org/):

* MAJOR version for incompatible API changes
* MINOR version for new functionality (backwards-compatible)
* PATCH version for backwards-compatible bug fixes

### Release Checklist

1. Update CHANGELOG.md
2. Update version in `phreakwall/__init__.py`
3. Update version in `setup.py`
4. Run full test suite
5. Build and test package
6. Create git tag
7. Push to GitHub
8. Create GitHub release
9. Publish to PyPI

## Getting Help

* 💬 [Discord](https://discord.gg/phreakwall)
* 📧 [Mailing List](mailto:phreakwall-dev@lists.phreakwall.org)
* 🐙 [GitHub Discussions](https://github.com/phreakwall/phreakwall/discussions)

## Recognition

Contributors will be recognized in:

* CHANGELOG.md (for significant contributions)
* README.md contributors section
* GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the GPL-2.0 License.

## Questions?

Don't hesitate to ask! We're here to help:

* Open an issue with your question
* Ask in GitHub Discussions
* Email: dev@phreakwall.org

---

Thank you for contributing to Phreakwall! 🎉
