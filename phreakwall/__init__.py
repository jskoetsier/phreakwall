#!/usr/bin/env python3
"""
Phreakwall - Modern Python Firewall Manager

A high-level firewall configuration and management system for Linux
designed for modern Python architecture.

Copyright (c) 2025 Phreakwall Contributors

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.
"""

__version__ = "6.0.2"
__author__ = "Phreakwall Contributors"
__license__ = "GPL-2.0"
__copyright__ = "Copyright (c) 2025 Phreakwall Contributors"

from phreakwall.core.chains import ChainManager
from phreakwall.core.compiler import Compiler
from phreakwall.core.config import Config

__all__ = [
    "Compiler",
    "Config",
    "ChainManager",
    "__version__",
]
