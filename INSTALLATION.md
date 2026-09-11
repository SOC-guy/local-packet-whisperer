# Installation Guide for Local Packet Whisperer (LPW)

## Quick Start (Linux/Ubuntu)

### Using the Automated Setup Script

Run the provided setup script to automatically install all dependencies:

```bash
chmod +x setup.sh
sudo ./setup.sh
```

This script will:
- ✅ Add Python 3.11 PPA and install Python 3.11 with venv and dev tools
- ✅ Install compression tools (zstd)
- ✅ Create Streamlit configuration directory (`~/.streamlit`)
- ✅ Create Streamlit config file with optimized settings (maxUploadSize = 1000 MB)
- ✅ Create PCAP temporary directory (`~/pcap-tmp`)

### After Running the Setup Script

1. **Create a virtual environment** (recommended):
   ```bash
   python3.11 -m venv lpw-env
   source lpw-env/bin/activate
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run LPW**:
   ```bash
   streamlit run bin/lpw_home.py
   ```

---

## Manual Setup (Step-by-Step)

If you prefer to install manually:

```bash
# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Add Python 3.11 repository
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# 3. Install Python 3.11 and dependencies
sudo apt install python3.11 python3.11-venv python3.11-dev

# 4. Install compression tools
sudo apt install zstd

# 5. Create Streamlit configuration
mkdir -p ~/.streamlit
cat > ~/.streamlit/config.toml << 'EOF'
[server]
maxUploadSize = 1000
EOF

# 6. Create PCAP temporary directory
mkdir -p ~/pcap-tmp

# 7. Create virtual environment
python3.11 -m venv lpw-env
source lpw-env/bin/activate

# 8. Install Python packages
pip install -r requirements.txt

# 9. Run LPW
streamlit run bin/lpw_home.py
```

---

## Configuration Details

### Streamlit Settings
- **Location**: `~/.streamlit/config.toml`
- **Max Upload Size**: 1000 MB (default is 200 MB)
- **PCAP Directory**: `~/pcap-tmp`

### System Requirements
- Ubuntu 18.04 LTS or newer
- Python 3.11
- 2GB minimum RAM
- Internet connection (for downloading models)
- **No additional system dependencies** (no TShark/Wireshark needed)

### Troubleshooting

**Issue**: Connection refused to Ollama server
- **Solution**: Ensure Ollama is running: `ollama serve`

**Issue**: Permission denied for `/home/~/pcap-tmp`
- **Solution**: Ensure the directory exists and has proper permissions: `mkdir -p ~/pcap-tmp && chmod 755 ~/pcap-tmp`

**Issue**: Python module not found
- **Solution**: Ensure virtual environment is activated and packages are installed: `pip install -r requirements.txt`

---

## Next Steps

1. Start an Ollama server (if not already running)
2. Configure LLM server settings in LPW Settings ⚙️
3. Upload a PCAP file and start analyzing!

For more information, see the main [README.md](../README.md)
