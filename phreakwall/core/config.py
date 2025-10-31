#!/usr/bin/env python3
"""
Phreakwall Configuration Management

Handles loading, parsing, and validating firewall configuration files.

Copyright (c) 2025 Phreakwall Contributors
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ConfigOptions:
    """Configuration file options."""

    ip_forwarding: bool = True
    log_verbosity: int = 1
    startup_enabled: bool = True
    docker_support: bool = False
    verbosity: int = 1
    config: Dict[str, Any] = field(default_factory=dict)


class ConfigError(Exception):
    """Configuration error exception."""

    pass


class Config:
    """
    Configuration manager for Phreakwall.

    Loads and parses configuration files from the config directory.
    """

    def __init__(self, config_dir: Path, family: int = 4, export: bool = False):
        """
        Initialize configuration manager.

        Args:
            config_dir: Configuration directory path
            family: IP family (4 or 6)
            export: Export mode flag
        """
        self.config_dir = Path(config_dir)
        self.family = family
        self.export = export
        self.logger = logging.getLogger(__name__)

        self.options = ConfigOptions()
        self.params: Dict[str, str] = {}
        self._loaded = False

    def load(self):
        """Load all configuration files."""
        if self._loaded:
            return

        self.logger.info(f"Loading configuration from {self.config_dir}")

        if not self.config_dir.exists():
            raise ConfigError(f"Configuration directory not found: {self.config_dir}")

        # Load main configuration
        self._load_main_config()

        # Load params
        self._load_params()

        self._loaded = True
        self.logger.info("Configuration loaded successfully")

    def _load_main_config(self):
        """Load the main configuration file."""
        config_file = self.config_dir / "phreakwall.conf"

        if not config_file.exists():
            self.logger.warning(f"Main config file not found: {config_file}")
            return

        self.logger.debug(f"Loading main config: {config_file}")

        with config_file.open() as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith("#"):
                    continue

                # Parse key=value
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    self.options.config[key] = value

    def _load_params(self):
        """Load parameter definitions."""
        params_file = self.config_dir / "params"

        if not params_file.exists():
            self.logger.debug("No params file found")
            return

        self.logger.debug(f"Loading params: {params_file}")

        with params_file.open() as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    self.params[key.strip()] = value.strip()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self.options.config.get(key, default)

    def get_param(self, key: str, default: str = "") -> str:
        """
        Get a parameter value.

        Args:
            key: Parameter key
            default: Default value if key not found

        Returns:
            Parameter value
        """
        return self.params.get(key, default)

    def validate(self):
        """Validate the configuration."""
        self.logger.debug("Validating configuration")

        # Check required directories exist
        if not self.config_dir.exists():
            raise ConfigError(f"Config directory does not exist: {self.config_dir}")

        self.logger.debug("Configuration validation passed")
