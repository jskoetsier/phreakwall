#!/usr/bin/env python3
"""
Phreakwall Installation Script

Modern Python-based installation for Phreakwall firewall manager.

Copyright (c) 2025 Phreakwall Contributors

Usage:
    sudo python3 install.py [options]
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


class PhreakwallInstaller:
    """Phreakwall installation manager."""

    VERSION = "6.0.2"

    def __init__(self, prefix="/usr", sysconfdir="/etc", destdir=""):
        """
        Initialize installer.

        Args:
            prefix: Installation prefix (default: /usr)
            sysconfdir: System config directory (default: /etc)
            destdir: Destination root for staged installs
        """
        self.prefix = Path(prefix)
        self.sysconfdir = Path(sysconfdir)
        self.destdir = Path(destdir) if destdir else Path("/")

        self.bindir = self.destdir / self.prefix.relative_to("/") / "bin"
        self.libdir = self.destdir / self.prefix.relative_to("/") / "lib" / "phreakwall"
        self.confdir = self.destdir / self.sysconfdir.relative_to("/") / "phreakwall"
        self.systemd_dir = self.destdir / Path("lib/systemd/system")

    def check_root(self):
        """Check if running as root."""
        if os.geteuid() != 0:
            print("ERROR: This script must be run as root")
            print("Try: sudo python3 install.py")
            sys.exit(1)

    def check_python_version(self):
        """Check Python version."""
        if sys.version_info < (3, 10):
            print(
                f"ERROR: Python 3.10+ required (found {sys.version_info.major}.{sys.version_info.minor})"
            )
            sys.exit(1)

    def install_python_package(self):
        """Install Python package using pip."""
        print("Installing Python package...")

        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", "."], check=True
            )
            print("✓ Python package installed")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install Python package: {e}")
            sys.exit(1)

    def create_directories(self):
        """Create necessary directories."""
        print("Creating directories...")

        directories = [
            self.bindir,
            self.libdir,
            self.confdir,
            self.confdir / "samples",
            Path("/var/lib/phreakwall"),
            Path("/var/log/phreakwall"),
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {directory}")

    def install_config_samples(self):
        """Install sample configuration files."""
        print("Installing configuration samples...")

        if not self.confdir.exists():
            self.confdir.mkdir(parents=True)

        # Create basic sample configs
        samples = {
            "phreakwall.conf.sample": """# Phreakwall Configuration
# Version 6.0.0

VERBOSITY=1
IP_FORWARDING=No
STARTUP_ENABLED=Yes
LOG_LEVEL=info
""",
            "zones.sample": """# Zone Definitions
#ZONE    TYPE        OPTIONS
fw       firewall
net      ipv4
loc      ipv4
""",
            "interfaces.sample": """# Interface Definitions
#ZONE    INTERFACE   OPTIONS
net      eth0        dhcp,tcpflags,routefilter,nosmurfs,logmartians
loc      eth1        dhcp,routefilter
""",
            "policy.sample": """# Zone Policies
#SOURCE  DEST    POLICY      LOG
$FW      net     ACCEPT
loc      net     ACCEPT
net      all     DROP        info
all      all     REJECT      info
""",
            "rules.sample": """# Firewall Rules
#ACTION     SOURCE  DEST    PROTO   DPORT   SPORT   ORIGDEST
ACCEPT      net     $FW     tcp     ssh
ACCEPT      loc     $FW     tcp     ssh
""",
        }

        sample_dir = self.confdir / "samples"
        sample_dir.mkdir(exist_ok=True)

        for filename, content in samples.items():
            sample_file = sample_dir / filename
            sample_file.write_text(content)
            print(f"  Created: {sample_file}")

    def install_systemd_service(self):
        """Install systemd service file."""
        print("Installing systemd service...")

        service_content = """[Unit]
Description=Phreakwall Firewall
Documentation=https://docs.phreakwall.org
After=network-pre.target
Before=network.target
Wants=network-pre.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/phreakwall start
ExecStop=/usr/bin/phreakwall stop
ExecReload=/usr/bin/phreakwall reload
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""

        if self.systemd_dir.exists() or self.systemd_dir.parent.exists():
            self.systemd_dir.mkdir(parents=True, exist_ok=True)
            service_file = self.systemd_dir / "phreakwall.service"
            service_file.write_text(service_content)
            print(f"  Created: {service_file}")

            # Reload systemd
            try:
                subprocess.run(["systemctl", "daemon-reload"], check=False)
                print("  Reloaded systemd")
            except FileNotFoundError:
                print("  (systemctl not found, skipping daemon-reload)")
        else:
            print("  Systemd not found, skipping service installation")

    def install(self):
        """Run full installation."""
        print(f"Installing Phreakwall {self.VERSION}")
        print("=" * 50)

        self.check_root()
        self.check_python_version()

        self.create_directories()
        self.install_python_package()
        self.install_config_samples()
        self.install_systemd_service()

        print("\n" + "=" * 50)
        print("Installation completed successfully!")
        print("\nNext steps:")
        print("  1. Copy sample configs:")
        print(f"     cp {self.confdir}/samples/*.sample {self.confdir}/")
        print("     (Remove .sample extension)")
        print("  2. Edit configuration files")
        print("  3. Test: phreakwall check")
        print("  4. Enable: systemctl enable phreakwall")
        print("  5. Start: systemctl start phreakwall")

    def uninstall(self):
        """Uninstall Phreakwall."""
        print(f"Uninstalling Phreakwall {self.VERSION}")
        print("=" * 50)

        self.check_root()

        # Stop and disable service
        try:
            subprocess.run(["systemctl", "stop", "phreakwall"], check=False)
            subprocess.run(["systemctl", "disable", "phreakwall"], check=False)
        except FileNotFoundError:
            pass

        # Uninstall Python package
        print("Uninstalling Python package...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "uninstall", "-y", "phreakwall"],
                check=True,
            )
        except subprocess.CalledProcessError:
            pass

        # Remove systemd service
        service_file = Path("/lib/systemd/system/phreakwall.service")
        if service_file.exists():
            service_file.unlink()
            print(f"Removed: {service_file}")

        print("\nUninstallation completed!")
        print(f"\nNote: Configuration files in {self.confdir} were preserved.")
        print("Remove manually if desired.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Phreakwall Installation Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--prefix", default="/usr", help="Installation prefix (default: /usr)"
    )

    parser.add_argument(
        "--sysconfdir",
        default="/etc",
        help="System configuration directory (default: /etc)",
    )

    parser.add_argument(
        "--destdir", default="", help="Destination root for staged installs"
    )

    parser.add_argument("--uninstall", action="store_true", help="Uninstall Phreakwall")

    parser.add_argument(
        "--version",
        action="version",
        version=f"Phreakwall Installer {PhreakwallInstaller.VERSION}",
    )

    args = parser.parse_args()

    installer = PhreakwallInstaller(
        prefix=args.prefix, sysconfdir=args.sysconfdir, destdir=args.destdir
    )

    if args.uninstall:
        installer.uninstall()
    else:
        installer.install()


if __name__ == "__main__":
    main()
