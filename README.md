# Phreakwall - Modern Python Firewall Manager

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![Version](https://img.shields.io/badge/version-6.0.2-green.svg)](https://github.com/phreakwall/phreakwall)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Overview

Phreakwall is a modern Python-based firewall configuration and management system designed for new installations. It provides a high-level interface for configuring netfilter/nftables rules on Linux systems, making complex firewall configurations simple and maintainable.

**Version 6.0** represents a complete rewrite in Python 3.10+, bringing modern programming paradigms, improved performance, and enhanced maintainability to firewall management.

## Key Features

- 🔥 **High-level firewall configuration** - Abstract away iptables/nftables complexity
- 🌐 **Multi-zone networking** - Define zones and policies between them
- 🔀 **NAT/SNAT support** - Complete network address translation capabilities
- 📊 **Traffic shaping** - Built-in traffic control and QoS
- 🔍 **Connection tracking** - Advanced connection state management
- 📝 **Comprehensive logging** - Detailed firewall activity logs
- 🐍 **Pure Python** - Easy to extend and customize
- 🚀 **Modern codebase** - Python 3.10+ with type hints
- 📦 **Easy installation** - pip-based installation with minimal dependencies

## What's New in 6.0

Phreakwall 6.0 is a ground-up rewrite that modernizes the entire codebase:

- **Python 3.10+** - Migrated from Perl to modern Python
- **Type safety** - Full type hints throughout the codebase
- **Async support** - Asynchronous operations where beneficial
- **Better testing** - Comprehensive test suite with pytest
- **Modern CLI** - Click-based command-line interface
- **Plugin system** - Extensible architecture for custom rules
- **Configuration validation** - Schema-based config validation
- **Better documentation** - Sphinx-based documentation with examples

## Quick Start

### Prerequisites

- Linux kernel 5.0+ with netfilter support
- Python 3.10 or higher
- iptables or nftables
- Root/sudo access

### Installation

```bash
# Install from PyPI (when available)
pip install phreakwall

# Or install from source
git clone https://github.com/phreakwall/phreakwall.git
cd phreakwall
pip install -e .
```

### Basic Usage

```bash
# Initialize configuration
sudo phreakwall init

# Check configuration
sudo phreakwall check

# Start firewall
sudo phreakwall start

# View status
sudo phreakwall status

# Stop firewall
sudo phreakwall stop
```

## Configuration Example

Create `/etc/phreakwall/zones`:
```
#ZONE    TYPE
fw       firewall
net      ipv4
loc      ipv4
```

Create `/etc/phreakwall/policy`:
```
#SOURCE  DEST     POLICY
loc      net      ACCEPT
net      all      DROP
all      all      REJECT
```

Create `/etc/phreakwall/rules`:
```
#ACTION  SOURCE  DEST    PROTO   DPORT
ACCEPT   net     fw      tcp     ssh
ACCEPT   loc     fw      tcp     ssh
```

## Architecture

```
phreakwall/
├── core/           # Core firewall logic
│   ├── compiler.py # Configuration compiler
│   ├── chains.py   # Chain management
│   └── config.py   # Configuration parser
├── modules/        # Feature modules
│   ├── nat.py      # NAT/SNAT handling
│   ├── zones.py    # Zone management
│   └── rules.py    # Rule processing
├── cli/            # Command-line interface
└── utils/          # Utility functions
```


## Documentation

Full documentation is available at:
- **User Guide**: https://docs.phreakwall.org/guide
- **API Reference**: https://docs.phreakwall.org/api
- **Examples**: https://docs.phreakwall.org/examples

## Development

### Setting up development environment

```bash
# Clone repository
git clone https://github.com/phreakwall/phreakwall.git
cd phreakwall

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linters
black .
ruff check .
mypy phreakwall
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=phreakwall

# Run specific test file
pytest tests/test_compiler.py
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features and development timeline.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## License

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License version 2 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

## Credits

Phreakwall: Copyright (c) 2025 Phreakwall Contributors

## Support

- 📖 Documentation: https://docs.phreakwall.org
- 💬 Discussions: https://github.com/phreakwall/phreakwall/discussions
- 🐛 Bug Reports: https://github.com/phreakwall/phreakwall/issues
- 📧 Mailing List: phreakwall-users@lists.phreakwall.org

## Acknowledgments

Special thanks to:
- The Python community for excellent tooling
- All Phreakwall contributors and users

---

**Made with ❤️ by the Phreakwall community**
