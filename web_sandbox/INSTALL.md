# theZoo Web Sandbox - Installation & Quick Start Guide

## Quick Installation

### Prerequisites
- Python 3.7 or higher
- Git (to clone the repository)
- theZoo repository already set up with malware database

### Step-by-Step Installation

1. **Navigate to theZoo root directory:**
   ```bash
   cd /path/to/theZoo
   ```

2. **Install theZoo dependencies (if not already done):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install web sandbox dependencies:**
   ```bash
   cd web_sandbox
   pip install -r requirements.txt
   ```

## Running the Web Sandbox

### Method 1: Using the run script (Recommended)

**Linux/macOS:**
```bash
cd web_sandbox
chmod +x run.sh
./run.sh
```

**Windows:**
```cmd
cd web_sandbox
run.bat
```

### Method 2: Direct command

```bash
cd web_sandbox
python -m uvicorn main:app --host=127.0.0.1 --port=8000 --reload
```

### Method 3: Using Python directly

```bash
cd web_sandbox
python main.py
```

## Accessing the Interface

Once the server starts, open your web browser and navigate to:

**http://127.0.0.1:8000**

You should see the theZoo Web Sandbox dashboard with:
- Database statistics
- Quick action buttons
- Recent malware entries
- Safety guidelines

## API Access

The web sandbox provides a REST API. You can access:

- **Interactive API docs:** http://127.0.0.1:8000/docs
- **Alternative API docs:** http://127.0.0.1:8000/redoc
- **API base URL:** http://127.0.0.1:8000/api/

### Example API Calls

```bash
# Get database statistics
curl http://127.0.0.1:8000/api/stats

# List malware samples
curl http://127.0.0.1:8000/api/malwares

# Search for ransomware
curl "http://127.0.0.1:8000/api/malwares/search?q=ransomware"

# Get specific malware details
curl http://127.0.0.1:8000/api/malwares/1
```

## Configuration

### Environment Variables

You can configure the server using environment variables:

```bash
# Set custom host (default: 127.0.0.1)
export HOST=127.0.0.1

# Set custom port (default: 8000)
export PORT=8000

# Enable/disable reload (default: true)
export RELOAD=true
```

### Running on Different Host/Port

```bash
# Run on all interfaces (NOT RECOMMENDED for security)
HOST=0.0.0.0 PORT=8080 ./run.sh

# Or directly with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Troubleshooting

### Issue: "FastAPI is not installed"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Database connection not available"

**Solution:**
- Make sure you're running from the theZoo root directory
- Verify that `conf/maldb.db` exists
- Check that the main theZoo requirements are installed

### Issue: "Port already in use"

**Solution:**
```bash
# Use a different port
PORT=8080 ./run.sh
```

### Issue: "Cannot access from other computers"

**Solution:**
By default, the server only accepts connections from localhost for security. If you need remote access (NOT RECOMMENDED):

```bash
# Run on all interfaces
HOST=0.0.0.0 ./run.sh
```

**⚠️ SECURITY WARNING:** Only do this in isolated, controlled environments!

## Features Overview

### Web Interface
- **Dashboard** - Overview with statistics and recent entries
- **Browse** - Paginated list with filtering options
- **Search** - Advanced search by multiple criteria
- **Details** - Comprehensive malware information
- **Download** - Safe download with multiple warnings
- **Documentation** - Built-in documentation and guides
- **About** - License, credits, and project information

### API Endpoints
- `GET /api/stats` - Database statistics
- `GET /api/malwares` - List malware samples (paginated)
- `GET /api/malwares/{id}` - Get malware details
- `GET /api/malwares/search?q=query` - Search malware
- `POST /api/update-db` - Update database

## Security Reminders

### ⚠️ CRITICAL SAFETY RULES

1. **NEVER** run this on a production server
2. **ALWAYS** run in an isolated virtual machine
3. **DISABLE** network access to the VM
4. **NEVER** expose to public networks
5. **USE** only for educational purposes

### Recommended Setup

1. Create an isolated VM with no internet access
2. Install theZoo and web sandbox in the VM
3. Run the web sandbox on localhost only
4. Access from the host machine via browser
5. Never download or extract malware samples on the host

## Uninstallation

To remove the web sandbox:

```bash
# Remove the web_sandbox directory
rm -rf web_sandbox

# Or if you want to keep the code but remove dependencies:
pip uninstall fastapi uvicorn jinja2 python-multipart aiofiles
```

## Getting Help

- **Documentation:** http://127.0.0.1:8000/documentation
- **GitHub Issues:** https://github.com/ytisf/theZoo/issues
- **Main Repository:** https://github.com/ytisf/theZoo

## Contributing

If you want to contribute to the web sandbox:

1. Follow the main theZoo contributing guidelines
2. Do NOT modify existing theZoo code or malware samples
3. Test thoroughly in isolated environments
4. Submit pull requests to the main theZoo repository

## License

This web interface follows the same GPL v3.0 license as theZoo.

See [LICENSE.md](../LICENSE.md) for details.

---

**Remember:** This is a tool for education and research only. Always use proper safety precautions when dealing with malware.