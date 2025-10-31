#!/usr/bin/env python3
"""
Phreakwall Web Application

Flask-based web interface for managing Phreakwall firewall.

Copyright (c) 2025 Phreakwall Contributors
"""

import os
from pathlib import Path

from flask import flash, Flask, jsonify, redirect, render_template, request, url_for
from phreakwall import __version__
from phreakwall.core.compiler import Compiler, CompilerOptions
from phreakwall.core.config import Config


def create_app(config_dir="/etc/phreakwall"):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "phreakwall-dev-key-change-me")
    app.config["CONFIG_DIR"] = Path(config_dir)

    @app.route("/")
    def index():
        """Dashboard home page."""
        return render_template("index.html", version=__version__)

    @app.route("/config")
    def config():
        """Configuration management page."""
        config_dir = app.config["CONFIG_DIR"]
        files = []

        if config_dir.exists():
            for file in config_dir.iterdir():
                if file.is_file():
                    files.append(
                        {
                            "name": file.name,
                            "path": str(file),
                            "size": file.stat().st_size,
                        }
                    )

        return render_template("config.html", files=files, config_dir=config_dir)

    @app.route("/config/edit/<filename>")
    def edit_config(filename):
        """Edit a configuration file."""
        config_file = app.config["CONFIG_DIR"] / filename

        if not config_file.exists():
            flash(f"File not found: {filename}", "error")
            return redirect(url_for("config"))

        content = config_file.read_text()
        return render_template("edit.html", filename=filename, content=content)

    @app.route("/config/save/<filename>", methods=["POST"])
    def save_config(filename):
        """Save configuration file."""
        config_file = app.config["CONFIG_DIR"] / filename
        content = request.form.get("content", "")

        try:
            config_file.write_text(content)
            flash(f"Saved {filename} successfully", "success")
        except Exception as e:
            flash(f"Error saving {filename}: {e}", "error")

        return redirect(url_for("config"))

    @app.route("/check")
    def check():
        """Validate configuration."""
        options = CompilerOptions(directory=app.config["CONFIG_DIR"])
        compiler = Compiler(options)

        try:
            compiler.initialize_components()
            compiler.validate_configuration()
            result = {"status": "success", "message": "Configuration is valid"}
        except Exception as e:
            result = {"status": "error", "message": str(e)}

        return jsonify(result)

    @app.route("/compile", methods=["POST"])
    def compile_config():
        """Compile firewall configuration."""
        output = Path("/var/lib/phreakwall/firewall.sh")
        options = CompilerOptions(script=output, directory=app.config["CONFIG_DIR"])
        compiler = Compiler(options)

        try:
            result = compiler.compile()
            if result == 0:
                return jsonify(
                    {
                        "status": "success",
                        "message": f"Compiled successfully to {output}",
                    }
                )
            else:
                return jsonify({"status": "error", "message": "Compilation failed"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    @app.route("/status")
    def status():
        """Show firewall status."""
        return render_template("status.html", version=__version__)

    @app.route("/api/status")
    def api_status():
        """API endpoint for status."""
        return jsonify(
            {
                "version": __version__,
                "config_dir": str(app.config["CONFIG_DIR"]),
                "firewall_state": "unknown",
            }
        )

    @app.route("/virtualips")
    def virtualips():
        """Virtual IPs management."""
        return render_template("virtualips.html", version=__version__)

    @app.route("/nat")
    def nat():
        """1:1 NAT configuration (bidirectional)."""
        return render_template("nat.html", version=__version__)

    @app.route("/firewall")
    def firewall():
        """Firewall rules configuration."""
        config_dir = app.config["CONFIG_DIR"]
        rules_file = config_dir / "rules"
        policy_file = config_dir / "policy"

        rules_content = rules_file.read_text() if rules_file.exists() else ""
        policy_content = policy_file.read_text() if policy_file.exists() else ""

        return render_template(
            "firewall.html",
            version=__version__,
            rules=rules_content,
            policy=policy_content,
        )

    @app.route("/portforward")
    def portforward():
        """Port forwarding configuration."""
        return render_template("portforward.html", version=__version__)

    @app.route("/metrics")
    def metrics():
        """System and firewall metrics."""
        return render_template("metrics.html", version=__version__)

    @app.route("/api/virtualips", methods=["GET", "POST"])
    def api_virtualips():
        """API for virtual IPs."""
        if request.method == "POST":
            data = request.json
            return jsonify({"status": "success", "message": "Virtual IP added"})
        return jsonify({"virtualips": []})

    @app.route("/api/nat", methods=["GET", "POST"])
    def api_nat():
        """API for NAT rules."""
        if request.method == "POST":
            data = request.json
            return jsonify({"status": "success", "message": "NAT rule added"})
        return jsonify({"nat_rules": []})

    @app.route("/api/portforward", methods=["GET", "POST"])
    def api_portforward():
        """API for port forwarding."""
        if request.method == "POST":
            data = request.json
            return jsonify({"status": "success", "message": "Port forward added"})
        return jsonify({"forwards": []})

    @app.route("/api/metrics")
    def api_metrics():
        """API for metrics data."""
        import time

        try:
            import psutil

            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            net_io = psutil.net_io_counters()

            return jsonify(
                {
                    "cpu": {"percent": cpu_percent, "count": psutil.cpu_count()},
                    "memory": {
                        "total": memory.total,
                        "used": memory.used,
                        "percent": memory.percent,
                    },
                    "disk": {
                        "total": disk.total,
                        "used": disk.used,
                        "percent": disk.percent,
                    },
                    "network": {
                        "bytes_sent": net_io.bytes_sent,
                        "bytes_recv": net_io.bytes_recv,
                        "packets_sent": net_io.packets_sent,
                        "packets_recv": net_io.packets_recv,
                    },
                    "timestamp": int(time.time()),
                }
            )
        except:
            return jsonify(
                {
                    "cpu": {"percent": 0, "count": 0},
                    "memory": {"total": 0, "used": 0, "percent": 0},
                    "disk": {"total": 0, "used": 0, "percent": 0},
                    "network": {
                        "bytes_sent": 0,
                        "bytes_recv": 0,
                        "packets_sent": 0,
                        "packets_recv": 0,
                    },
                    "timestamp": int(time.time()),
                }
            )

    return app


def main():
    """Run the web application."""
    import argparse

    parser = argparse.ArgumentParser(description="Phreakwall Web Interface")
    parser.add_argument(
        "-d", "--directory", default="/etc/phreakwall", help="Configuration directory"
    )
    parser.add_argument("-p", "--port", type=int, default=5000, help="Port to run on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    app = create_app(args.directory)
    print(f"Starting Phreakwall Web Interface v{__version__}")
    print(f"Open your browser to http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
