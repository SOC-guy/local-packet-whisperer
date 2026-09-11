#!/bin/bash

# Local Packet Whisperer (LPW) Installation Script
# This script installs and configures LPW on your system

set -e  # Exit on any error

echo "================================"
echo "Local Packet Whisperer Setup"
echo "================================"
echo ""

# Check if running as root for system package installation
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  This script needs sudo privileges for system package installation."
    echo "Re-running with sudo..."
    sudo "$0"
    exit $?
fi

echo "📦 Updating package manager..."
apt update
apt upgrade -y

echo ""
echo "🐍 Installing Python 3.11..."
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install python3.11 python3.11-venv python3.11-dev -y

echo ""
echo "📦 Installing compression tools..."
apt install zstd -y

echo ""
echo "🔧 Creating Streamlit configuration directory..."
STREAMLIT_DIR="$HOME/.streamlit"
mkdir -p "$STREAMLIT_DIR"

echo "📝 Creating Streamlit config.toml..."
cat > "$STREAMLIT_DIR/config.toml" << 'EOF'
[server]
maxUploadSize = 1000
EOF

echo ""
echo "📁 Creating PCAP temporary directory..."
mkdir -p "$HOME/pcap-tmp"

echo ""
echo "✅ Installation complete!"
echo ""
echo "================================"
echo "Next steps:"
echo "================================"
echo ""
echo "1. Create a Python 3.11 virtual environment:"
echo "   python3.11 -m venv lpw-env"
echo ""
echo "2. Activate the virtual environment:"
echo "   source lpw-env/bin/activate"
echo ""
echo "3. Install LPW dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "4. Run LPW:"
echo "   streamlit run bin/lpw_home.py"
echo ""
echo "================================"
echo "Configuration details:"
echo "================================"
echo "Streamlit config: $STREAMLIT_DIR/config.toml"
echo "PCAP directory: $HOME/pcap-tmp"
echo "Max upload size: 1000 MB"
echo ""
