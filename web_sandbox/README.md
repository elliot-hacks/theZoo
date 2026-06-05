
# theZoo Web Sandbox

A FastAPI-based web interface for theZoo malware repository. This web sandbox provides a browser-based interface to browse, search, and interact with the malware database while maintaining all safety features of the original theZoo application.

## ⚠️ SECURITY WARNING ⚠️

**THIS IS A SANDBOX ENVIRONMENT - READ BEFORE PROCEEDING**

This web interface is designed to be run in a **CONTROLLED, ISOLATED ENVIRONMENT**. The theZoo repository contains **LIVE MALWARE** that can:

- Infect your system and spread to other machines
- Steal sensitive information
- Cause permanent damage to your systems
- Spread across networks automatically (worms)

### Safety Guidelines

1. **NEVER** run this on a production server or public network
2. **ALWAYS** run in an isolated virtual machine or container
3. **DISABLE** network access to the VM/container (or use internal-only networking)
4. **NEVER** download or extract malware samples without proper isolation
5. **USE** guest additions or equivalent tools only if absolutely necessary
6. **UNDERSTAND** that you are dealing with dangerous malicious software

### Intended Use

This tool is designed for:
- Malware analysis research
- Educational purposes
- Security professional training
- Understanding malware behavior in controlled environments

**By using this software, you acknowledge that you understand the risks and agree to use it responsibly and legally.**

## Features

- **Web-based Interface**: Access theZoo through any modern web browser
- **Malware Browsing**: Browse the complete malware database with filtering
- **Advanced Search**: Search by name, type, platform, architecture, language, and tags
- **Detailed Information**: View comprehensive metadata for each malware sample
- **Download Management**: Download malware samples (with safety warnings)
- **Database Updates**: Update the malware database from GitHub
- **Documentation Integration**: Built-in access to theZoo documentation
- **Responsive Design**: Works on desktop and mobile browsers

## Installation

1. Clone the theZoo repository (if you haven't already):
   ```bash
   git clone https://github.com/ytisf/theZoo.git
   cd theZoo
   ```

2. Install the web sandbox dependencies:
   ```bash
   cd web_sandbox
   pip install -r requirements.txt
   ```

3. Make sure you have the main theZoo dependencies installed:
   ```bash
   cd ..
   pip install -r requirements.txt
   ```

## Running the Web Sandbox

From the theZoo root directory:

```bash
cd web_sandbox
uvicorn main:app --host=127.0.0.1 --port=8000 --reload
```

**Important Security Notes:**
- The server binds to `127.0.0.1` by default (localhost only) for security
- Do NOT bind to `0.0.0.0` unless you understand the security implications
- Consider using a VPN or isolated network if accessing remotely

Open your browser and navigate to: `http://127.0.0.1:8000`

## Usage

### Main Interface
- **Dashboard**: Overview of the malware database with statistics
- **Browse**: List all malware samples with filtering options
- **Search**: Advanced search with multiple criteria
- **Details**: View detailed information about specific malware
- **Download**: Download malware samples (encrypted and password-protected)

### Safety Features
- All downloads are the original encrypted ZIP files
- Passwords are provided separately for security
- Multiple warning prompts before downloading
- No automatic execution of malware samples

### API Endpoints

The web sandbox also provides a REST API:

- `GET /api/malwares` - List all malware samples
- `GET /api/malwares/{mal_id}` - Get detailed information about a specific malware
- `GET /api/malwares/search?q=query` - Search malware database
- `GET /api/stats` - Get database statistics
- `POST /api/update-db` - Update the malware database

## Documentation

- [theZoo Main Repository](https://github.com/ytisf/theZoo)
- [theZoo Documentation](https://github.com/ytisf/theZoo/blob/master/README.md)
- [Contributing Guidelines](https://github.com/ytisf/theZoo/blob/master/CONTRIBUTING.md)
- [Code of Conduct](https://github.com/ytisf/theZoo/blob/master/CODE-OF-CONDUCT.md)

## Architecture

This web sandbox:
- Uses FastAPI for the backend (modern, fast, async-capable)
- Uses Jinja2 templates for the frontend (server-side rendering)
- Integrates with the existing theZoo database handler
- Maintains compatibility with the original theZoo database structure
- Does NOT modify any existing theZoo code or malware samples

## Contributing

This is a separate web interface for theZoo. If you want to contribute:

1. Make sure to follow the main theZoo [contributing guidelines](https://github.com/ytisf/theZoo/blob/master/CONTRIBUTING.md)
2. Do NOT modify any existing theZoo code or malware samples
3. Test thoroughly in an isolated environment
4. Submit pull requests to the main theZoo repository

## License

This web interface follows the same license as theZoo:

theZoo - the most awesome free malware database on the air
Copyright (C) 2015-2025, Yuval Nativ, Lahad Ludar, 5fingers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

See [LICENSE](../LICENSE.md) for details.

**Note:** This license does not apply to any malicious samples in theZoo's repository.

## Disclaimer

This web interface is provided for educational and research purposes only. The authors are not responsible for any misuse or damage caused by this software. Always use proper safety precautions when dealing with malware.