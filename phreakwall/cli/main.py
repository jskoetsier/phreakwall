#!/usr/bin/env python3
"""
Phreakwall Main CLI

Main command-line interface for Phreakwall firewall manager.

Copyright (c) 2025 Phreakwall Contributors
"""

import sys
from pathlib import Path

import click

from phreakwall import __version__
from phreakwall.core.compiler import Compiler, CompilerOptions
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="phreakwall")
@click.option("-v", "--verbose", count=True, help="Increase verbosity")
@click.option(
    "-d",
    "--directory",
    type=Path,
    default=Path("/etc/phreakwall"),
    help="Configuration directory",
)
@click.pass_context
def cli(ctx, verbose, directory):
    """Phreakwall - Modern Python Firewall Manager"""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["directory"] = directory


@cli.command()
@click.pass_context
def check(ctx):
    """Validate firewall configuration"""
    console.print("[bold blue]Checking configuration...[/bold blue]")

    options = CompilerOptions(
        directory=ctx.obj["directory"], verbosity=ctx.obj["verbose"]
    )

    compiler = Compiler(options)
    result = compiler.compile()

    if result == 0:
        console.print("[bold green]✓[/bold green] Configuration is valid")
    else:
        console.print("[bold red]✗[/bold red] Configuration has errors")
        sys.exit(1)


@cli.command()
@click.option("-o", "--output", type=Path, help="Output script file")
@click.option("--preview", is_flag=True, help="Preview the generated script")
@click.pass_context
def compile(ctx, output, preview):
    """Compile firewall configuration to script"""
    console.print("[bold blue]Compiling firewall configuration...[/bold blue]")

    if not output:
        output = Path("/var/lib/phreakwall/firewall.sh")

    options = CompilerOptions(
        script=output,
        directory=ctx.obj["directory"],
        verbosity=ctx.obj["verbose"],
        preview=preview,
    )

    compiler = Compiler(options)
    result = compiler.compile()

    if result == 0:
        console.print(f"[bold green]✓[/bold green] Script generated: {output}")
    else:
        console.print("[bold red]✗[/bold red] Compilation failed")
        sys.exit(1)


@cli.command()
@click.pass_context
def start(ctx):
    """Start the firewall"""
    console.print("[bold blue]Starting firewall...[/bold blue]")
    console.print("[yellow]Note:[/yellow] This requires root privileges")
    console.print("[dim]Implementation pending - use phreakwall-compiler for now[/dim]")


@cli.command()
@click.pass_context
def stop(ctx):
    """Stop the firewall"""
    console.print("[bold blue]Stopping firewall...[/bold blue]")
    console.print("[yellow]Note:[/yellow] This requires root privileges")
    console.print("[dim]Implementation pending[/dim]")


@cli.command()
@click.pass_context
def restart(ctx):
    """Restart the firewall"""
    console.print("[bold blue]Restarting firewall...[/bold blue]")
    console.print("[yellow]Note:[/yellow] This requires root privileges")
    console.print("[dim]Implementation pending[/dim]")


@cli.command()
@click.pass_context
def status(ctx):
    """Show firewall status"""
    console.print("[bold blue]Firewall Status[/bold blue]\n")

    table = Table(title="Phreakwall Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details")

    table.add_row("Version", __version__, "")
    table.add_row("Config Dir", str(ctx.obj["directory"]), "")
    table.add_row("State", "Unknown", "Use systemctl status phreakwall")

    console.print(table)


@cli.command()
@click.pass_context
def init(ctx):
    """Initialize a new configuration"""
    config_dir = ctx.obj["directory"]

    console.print(
        f"[bold blue]Initializing configuration in {config_dir}[/bold blue]\n"
    )

    if config_dir.exists():
        console.print(
            f"[yellow]Warning:[/yellow] Directory already exists: {config_dir}"
        )
        if not click.confirm("Continue anyway?"):
            return

    # Create directory structure
    config_dir.mkdir(parents=True, exist_ok=True)

    # Create basic configuration files
    files_created = []

    # zones file
    zones_file = config_dir / "zones"
    zones_file.write_text(
        """# Phreakwall Zones Configuration
#ZONE    TYPE        OPTIONS
fw       firewall
net      ipv4
"""
    )
    files_created.append("zones")

    # interfaces file
    interfaces_file = config_dir / "interfaces"
    interfaces_file.write_text(
        """# Phreakwall Interfaces Configuration
#ZONE    INTERFACE       OPTIONS
net      eth0            dhcp,routefilter
"""
    )
    files_created.append("interfaces")

    # policy file
    policy_file = config_dir / "policy"
    policy_file.write_text(
        """# Phreakwall Policy Configuration
#SOURCE  DEST    POLICY      LOG
fw       all     ACCEPT
net      all     DROP        info
all      all     REJECT      info
"""
    )
    files_created.append("policy")

    # rules file
    rules_file = config_dir / "rules"
    rules_file.write_text(
        """# Phreakwall Rules Configuration
#ACTION     SOURCE  DEST    PROTO   DPORT
ACCEPT      net     fw      tcp     ssh
"""
    )
    files_created.append("rules")

    # Main config
    config_file = config_dir / "phreakwall.conf"
    config_file.write_text(
        """# Phreakwall Main Configuration
VERBOSITY=1
IP_FORWARDING=No
STARTUP_ENABLED=Yes
"""
    )
    files_created.append("phreakwall.conf")

    console.print(f"[bold green]✓[/bold green] Created configuration files:")
    for filename in files_created:
        console.print(f"  • {filename}")

    console.print(f"\n[bold]Next steps:[/bold]")
    console.print("  1. Edit the configuration files in", config_dir)
    console.print("  2. Run 'phreakwall check' to validate")
    console.print("  3. Run 'phreakwall compile' to generate firewall script")


@cli.command()
def version():
    """Show version information"""
    console.print(f"[bold]Phreakwall[/bold] version {__version__}")
    console.print("Copyright (c) 2025 Phreakwall Contributors")
    console.print("Based on Shorewall (c) 1999-2019 Tom Eastep")
    console.print("\nLicense: GPL-2.0")
    console.print("Python: " + sys.version.split()[0])


def main():
    """Main entry point"""
    cli(obj={})


if __name__ == "__main__":
    main()
