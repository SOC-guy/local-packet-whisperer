# Requirements Management for Local Packet Whisperer

This document explains the different requirements files used in the project.

## Production Requirements

### `requirements.txt` (Primary)
**Minimal production dependencies** - Only the essential packages needed to run LPW.

```bash
pip install -r requirements.txt
```

Contains:
- `streamlit` - Web UI framework
- `streamlit-extras` - Additional Streamlit components
- `crewai` - AI agent framework
- `crewai-tools` - Tools for CrewAI
- `scapy` - Pure Python PCAP parsing (no system dependencies)
- `ollama` - LLM client for local models
- `PyYAML` - YAML configuration support

**Size**: 7 packages (minimal, fast installation)
**Use case**: Production deployments, Docker containers, quick setups

---

## Development Requirements

### `requirements-dev.txt` (Optional)
**Development and testing tools** - Add to production requirements for development.

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

Contains:
- `pylance` - Python language server (VS Code)
- `pyright` - Static type checker
- `pytest` - Testing framework
- `python-dotenv` - Environment variable management

**Use case**: Local development, debugging, testing

---

## Installation Guide

### Quick Start (Production)
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run bin/lpw_home.py
```

### Development Setup
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
streamlit run bin/lpw_home.py
```

### Update Dependencies
To update all packages to the latest versions:
```bash
pip install --upgrade -r requirements.txt
```

---

## Package Details

### Direct Dependencies (7 total)

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.40.2 | Web UI framework |
| streamlit-extras | 0.5.0 | Additional UI components |
| crewai | 0.83.0 | AI agent framework |
| crewai-tools | 0.14.0 | AI agent tools |
| scapy | 2.5.0 | Pure Python PCAP parsing |
| ollama | 0.4.2 | LLM client |
| PyYAML | 6.0.2 | Configuration files |

### Transitive Dependencies
When installed, these packages will automatically install their own dependencies (e.g., pandas, numpy, protobuf, etc.). Python's pip will handle this automatically.

---

## Troubleshooting

### Issue: Module not found
**Solution**: Ensure virtual environment is activated and packages are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Version conflicts
**Solution**: Create a fresh virtual environment:
```bash
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: PCAP file not found or cannot be read
**Solution**: Ensure the PCAP file exists and is in the correct format:
```bash
file your_capture.pcap  # Should show "pcap" in output
```

---

## Size Comparison

- **Original requirements.txt**: 300+ lines, 150+ packages
- **New requirements.txt**: 7 lines, 7 packages
- **Reduction**: 95% smaller! 📉

This significantly reduces:
- Installation time
- Disk space usage
- Security attack surface
- Dependency conflicts

---

## Future Maintenance

If you need to add new dependencies:

1. **Production package**: Add to `requirements.txt`
2. **Development tool**: Add to `requirements-dev.txt`
3. **Pin versions**: Always specify exact versions (e.g., `package==1.2.3`)

Example:
```bash
pip install newpackage
pip freeze | grep newpackage
# Add to appropriate requirements.txt
```
