#!/bin/bash
#
# Phreakwall Easy Install Script
#
# One-command installation for Phreakwall firewall manager
#
# Usage: curl -sSL https://phreakwall.org/install.sh | sudo bash
#    or: sudo bash easy-install.sh
#
# Copyright (c) 2025 Phreakwall Contributors

set -e

VERSION="6.0.2"
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
NC="\033[0m"

echo -e "${BOLD}${BLUE}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║         🔥 PHREAKWALL EASY INSTALLER 🔥              ║"
echo "║                                                       ║"
echo "║         Modern Python Firewall Manager               ║"
echo "║                Version $VERSION                      ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}ERROR: This script must be run as root${NC}"
    echo "Please run: sudo bash $0"
    exit 1
fi

# Detect OS
echo -e "${BLUE}→ Detecting operating system...${NC}"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VER=$VERSION_ID
    echo -e "${GREEN}✓ Detected: $PRETTY_NAME${NC}"
else
    echo -e "${RED}✗ Cannot detect OS${NC}"
    exit 1
fi

# Check Python version
echo -e "${BLUE}→ Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
        echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
    else
        echo -e "${YELLOW}⚠ Python 3.10+ required, found $PYTHON_VERSION${NC}"
        echo -e "${BLUE}→ Installing Python 3.10+...${NC}"

        case $OS in
            ubuntu|debian)
                apt-get update
                apt-get install -y python3.10 python3.10-venv python3-pip
                ;;
            centos|rhel|fedora)
                dnf install -y python3.10 python3-pip
                ;;
            *)
                echo -e "${RED}✗ Unsupported OS for auto-install${NC}"
                echo "Please install Python 3.10+ manually"
                exit 1
                ;;
        esac
    fi
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo -e "${BLUE}→ Installing Python 3...${NC}"

    case $OS in
        ubuntu|debian)
            apt-get update
            apt-get install -y python3 python3-venv python3-pip
            ;;
        centos|rhel|fedora)
            dnf install -y python3 python3-pip
            ;;
        *)
            echo -e "${RED}✗ Unsupported OS${NC}"
            exit 1
            ;;
    esac
fi

# Install system dependencies
echo -e "${BLUE}→ Installing system dependencies...${NC}"
case $OS in
    ubuntu|debian)
        apt-get update
        apt-get install -y iptables netfilter-persistent git
        ;;
    centos|rhel|fedora)
        dnf install -y iptables iptables-services git
        ;;
    *)
        echo -e "${YELLOW}⚠ Unknown OS, skipping system dependencies${NC}"
        ;;
esac
echo -e "${GREEN}✓ System dependencies installed${NC}"

# Install Phreakwall
echo -e "${BLUE}→ Installing Phreakwall...${NC}"

if [ -f "setup.py" ]; then
    # Installing from local directory
    echo "Installing from current directory..."
    python3 -m pip install --upgrade pip
    python3 -m pip install -e .
else
    # Install from PyPI (when available)
    echo "Installing from PyPI..."
    python3 -m pip install --upgrade pip
    python3 -m pip install phreakwall
fi

echo -e "${GREEN}✓ Phreakwall installed${NC}"

# Create configuration directory
echo -e "${BLUE}→ Setting up configuration...${NC}"
mkdir -p /etc/phreakwall
mkdir -p /var/lib/phreakwall
mkdir -p /var/log/phreakwall

# Initialize configuration if not exists
if [ ! -f "/etc/phreakwall/phreakwall.conf" ]; then
    echo "Creating default configuration..."
    phreakwall init -d /etc/phreakwall
    echo -e "${GREEN}✓ Default configuration created${NC}"
else
    echo -e "${YELLOW}⚠ Configuration already exists, skipping${NC}"
fi

# Install systemd service
echo -e "${BLUE}→ Installing systemd service...${NC}"
cat > /etc/systemd/system/phreakwall.service << 'EOF'
[Unit]
Description=Phreakwall Firewall
Documentation=https://docs.phreakwall.org
After=network-pre.target
Before=network.target
Wants=network-pre.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/local/bin/phreakwall start
ExecStop=/usr/local/bin/phreakwall stop
ExecReload=/usr/local/bin/phreakwall reload
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
echo -e "${GREEN}✓ Systemd service installed${NC}"

# Install web interface (optional)
echo ""
read -p "Install web interface? (y/N): " INSTALL_WEB
if [[ $INSTALL_WEB =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}→ Installing web interface dependencies...${NC}"
    python3 -m pip install flask

    cat > /etc/systemd/system/phreakwall-web.service << 'EOF'
[Unit]
Description=Phreakwall Web Interface
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/python3 -m phreakwall.web.app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable phreakwall-web
    systemctl start phreakwall-web

    echo -e "${GREEN}✓ Web interface installed and started${NC}"
    echo -e "${GREEN}  Access at: http://localhost:5000${NC}"
fi

# Completion
echo ""
echo -e "${BOLD}${GREEN}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║         ✓ INSTALLATION COMPLETE ✓                    ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BOLD}Next Steps:${NC}"
echo ""
echo -e "  1. ${BLUE}Edit configuration:${NC}"
echo "     nano /etc/phreakwall/zones"
echo "     nano /etc/phreakwall/rules"
echo "     nano /etc/phreakwall/policy"
echo ""
echo -e "  2. ${BLUE}Validate configuration:${NC}"
echo "     phreakwall check"
echo ""
echo -e "  3. ${BLUE}Enable and start firewall:${NC}"
echo "     systemctl enable phreakwall"
echo "     systemctl start phreakwall"
echo ""
echo -e "  4. ${BLUE}Check status:${NC}"
echo "     phreakwall status"
echo "     systemctl status phreakwall"
echo ""
echo -e "${BOLD}Documentation:${NC}"
echo "  • User Guide:     https://docs.phreakwall.org"
echo "  • GitHub:         https://github.com/phreakwall/phreakwall"
echo "  • Configuration:  /etc/phreakwall/"
echo ""
echo -e "${GREEN}Thank you for installing Phreakwall! 🔥${NC}"
