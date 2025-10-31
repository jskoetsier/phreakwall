#!/usr/bin/env python3
"""
Phreakwall - Modern Python Firewall Manager

Setup script for installation.
"""

from pathlib import Path

from setuptools import find_packages, setup

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = (
    readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""
)

# Read version from package
version = "6.0.2"

setup(
    name="phreakwall",
    version=version,
    description="Modern Python-based firewall configuration and management system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Phreakwall Contributors",
    author_email="dev@phreakwall.org",
    url="https://github.com/phreakwall/phreakwall",
    project_urls={
        "Documentation": "https://docs.phreakwall.org",
        "Source": "https://github.com/phreakwall/phreakwall",
        "Tracker": "https://github.com/phreakwall/phreakwall/issues",
    },
    license="GPL-2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: System :: Systems Administration",
        "Topic :: Security",
    ],
    keywords="firewall iptables nftables netfilter security networking",
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
    python_requires=">=3.10",
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
        "rich>=13.0.0",
        "flask>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
            "types-PyYAML",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "sphinx-autodoc-typehints>=1.23.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "phreakwall=phreakwall.cli.main:main",
            "phreakwall-compiler=phreakwall.core.compiler:main",
        ],
    },
    package_data={
        "phreakwall": [
            "data/*.yaml",
            "data/*.conf",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    platforms=["Linux"],
)
