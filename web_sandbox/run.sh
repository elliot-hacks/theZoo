#!/bin/bash

# theZoo Web Sandbox - Run Script
# This script starts the FastAPI web sandbox server

echo "=============================================="
echo "  theZoo Web Sandbox"
echo "  A web-based interface for theZoo repository"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found. Please run this script from the web_sandbox directory."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if requirements are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Error: FastAPI is not installed. Please run: pip install -r requirements.txt"
    exit 1
fi

# Default configuration
HOST=${HOST:-127.0.0.1}
PORT=${PORT:-8000}
RELOAD=${RELOAD:-true}

echo "Starting theZoo Web Sandbox..."
echo ""
echo "⚠️  SECURITY WARNING ⚠️"
echo "This sandbox should ONLY be run in an isolated environment!"
echo "The theZoo repository contains LIVE MALWARE that can:"
echo "  - Infect your system"
echo "  - Spread to other machines"
echo "  - Cause permanent damage"
echo ""
echo "Server Configuration:"
echo "  Host: $HOST"
echo "  Port: $PORT"
echo "  Reload: $RELOAD"
echo ""
echo "Access the web interface at: http://$HOST:$PORT"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=============================================="
echo ""

# Start the server
python3 -m uvicorn main:app --host $HOST --port $PORT $([ "$RELOAD" = "true" ] && echo "--reload")