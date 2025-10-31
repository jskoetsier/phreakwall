#!/usr/bin/env python3
"""
Phreakwall Zone Management

Manages network zones and inter-zone policies.

Copyright (c) 2025 Phreakwall Contributors
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Zone:
    """Represents a network zone."""

    name: str
    zone_type: str
    options: List[str] = None

    def __post_init__(self):
        if self.options is None:
            self.options = []


class ZoneManager:
    """Manages network zones and zone policies."""

    def __init__(self, config, family: int = 4):
        """
        Initialize zone manager.

        Args:
            config: Configuration object
            family: IP family
        """
        self.config = config
        self.family = family
        self.logger = logging.getLogger(__name__)

        self.zones: Dict[str, Zone] = {}
        self._load_zones()

    def _load_zones(self):
        """Load zone definitions from config."""
        zones_file = self.config.config_dir / "zones"

        if not zones_file.exists():
            self.logger.warning("No zones file found")
            return

        self.logger.debug(f"Loading zones from {zones_file}")

        with zones_file.open() as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split()
                if len(parts) >= 2:
                    name, zone_type = parts[0], parts[1]
                    options = parts[2:] if len(parts) > 2 else []
                    self.zones[name] = Zone(name, zone_type, options)

        self.logger.info(f"Loaded {len(self.zones)} zones")

    def generate_zone_rules(self) -> List[str]:
        """Generate zone-related firewall rules."""
        lines = ["# Zone rules", ""]

        for zone in self.zones.values():
            lines.append(f"# Zone: {zone.name} ({zone.zone_type})")

        lines.append("")
        return lines

    def validate(self):
        """Validate zone configuration."""
        self.logger.debug("Validating zones")

        if not self.zones:
            self.logger.warning("No zones defined")

        self.logger.debug("Zone validation passed")
