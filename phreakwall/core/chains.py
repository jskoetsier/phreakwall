#!/usr/bin/env python3
"""
Phreakwall Chain Management

Manages iptables/nftables chains for firewall rules.

Copyright (c) 2025 Phreakwall Contributors
"""

import logging
from enum import Enum
from typing import Dict, List, Optional, Set


class ChainType(Enum):
    """Types of firewall chains."""

    FILTER = "filter"
    NAT = "nat"
    MANGLE = "mangle"
    RAW = "raw"


class Chain:
    """Represents a firewall chain."""

    def __init__(
        self,
        name: str,
        chain_type: ChainType = ChainType.FILTER,
        policy: str = "ACCEPT",
    ):
        """
        Initialize a chain.

        Args:
            name: Chain name
            chain_type: Type of chain
            policy: Default policy
        """
        self.name = name
        self.chain_type = chain_type
        self.policy = policy
        self.rules: List[str] = []

    def add_rule(self, rule: str):
        """Add a rule to the chain."""
        self.rules.append(rule)

    def clear_rules(self):
        """Clear all rules from the chain."""
        self.rules.clear()


class ChainManager:
    """
    Manages firewall chains and rules.

    Handles creation, management, and generation of firewall chains.
    """

    def __init__(self, family: int = 4, export: bool = False):
        """
        Initialize chain manager.

        Args:
            family: IP family (4 or 6)
            export: Export mode flag
        """
        self.family = family
        self.export = export
        self.logger = logging.getLogger(__name__)

        self.chains: Dict[str, Chain] = {}
        self._initialize_standard_chains()

    def _initialize_standard_chains(self):
        """Initialize standard firewall chains."""
        # Standard filter chains
        self.create_chain("INPUT", ChainType.FILTER, "DROP")
        self.create_chain("OUTPUT", ChainType.FILTER, "ACCEPT")
        self.create_chain("FORWARD", ChainType.FILTER, "DROP")

        # Standard NAT chains
        self.create_chain("PREROUTING", ChainType.NAT, "ACCEPT")
        self.create_chain("POSTROUTING", ChainType.NAT, "ACCEPT")

        # Custom chains
        self.create_chain("phreakwall_input", ChainType.FILTER)
        self.create_chain("phreakwall_output", ChainType.FILTER)
        self.create_chain("phreakwall_forward", ChainType.FILTER)

    def create_chain(
        self,
        name: str,
        chain_type: ChainType = ChainType.FILTER,
        policy: Optional[str] = None,
    ) -> Chain:
        """
        Create a new chain.

        Args:
            name: Chain name
            chain_type: Type of chain
            policy: Chain policy (optional)

        Returns:
            Created chain object
        """
        if name in self.chains:
            self.logger.warning(f"Chain {name} already exists")
            return self.chains[name]

        policy = policy or "ACCEPT"
        chain = Chain(name, chain_type, policy)
        self.chains[name] = chain

        self.logger.debug(f"Created chain: {name} ({chain_type.value})")
        return chain

    def get_chain(self, name: str) -> Optional[Chain]:
        """
        Get a chain by name.

        Args:
            name: Chain name

        Returns:
            Chain object or None
        """
        return self.chains.get(name)

    def add_rule(self, chain_name: str, rule: str):
        """
        Add a rule to a chain.

        Args:
            chain_name: Name of the chain
            rule: Rule specification
        """
        chain = self.get_chain(chain_name)
        if not chain:
            raise ValueError(f"Chain not found: {chain_name}")

        chain.add_rule(rule)

    def generate_chains(self) -> List[str]:
        """
        Generate iptables commands for all chains.

        Returns:
            List of iptables command lines
        """
        lines = ["# Create and configure chains", ""]

        iptables_cmd = "ip6tables" if self.family == 6 else "iptables"

        # Group chains by type
        for chain_type in ChainType:
            type_chains = [
                c for c in self.chains.values() if c.chain_type == chain_type
            ]

            if not type_chains:
                continue

            lines.append(f"# {chain_type.value.upper()} table chains")

            for chain in type_chains:
                # Create custom chains
                if chain.name not in [
                    "INPUT",
                    "OUTPUT",
                    "FORWARD",
                    "PREROUTING",
                    "POSTROUTING",
                ]:
                    lines.append(
                        f"run_iptables -t {chain_type.value} -N {chain.name} "
                        f"2>/dev/null || true"
                    )
                    lines.append(f"run_iptables -t {chain_type.value} -F {chain.name}")
                else:
                    # Set policy for built-in chains
                    lines.append(
                        f"run_iptables -t {chain_type.value} "
                        f"-P {chain.name} {chain.policy}"
                    )

            lines.append("")

        # Add rules to chains
        lines.append("# Add rules to chains")
        lines.append("")

        for chain in self.chains.values():
            if chain.rules:
                lines.append(f"# Rules for {chain.name}")
                for rule in chain.rules:
                    lines.append(
                        f"run_iptables -t {chain.chain_type.value} "
                        f"-A {chain.name} {rule}"
                    )
                lines.append("")

        return lines

    def validate(self):
        """Validate chain configuration."""
        self.logger.debug("Validating chains")

        # Check that standard chains exist
        required_chains = ["INPUT", "OUTPUT", "FORWARD"]
        for chain_name in required_chains:
            if chain_name not in self.chains:
                raise ValueError(f"Required chain missing: {chain_name}")

        self.logger.debug("Chain validation passed")
