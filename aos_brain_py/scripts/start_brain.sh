#!/bin/bash
# Start the ternary brain server

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$PROJECT_DIR/.venv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧠 Starting Ternary Brain Server${NC}"
echo "====================================="

# Check Python
echo -n "Checking Python... "
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}FAIL${NC}"
    echo "Python3 is required but not installed."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}OK${NC} (Python $PYTHON_VERSION)"

# Create virtual environment if needed
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install dependencies
echo -n "Installing dependencies... "
if ! pip install -q -r "$PROJECT_DIR/requirements.txt" 2>/dev/null; then
    echo -e "${YELLOW}WARN${NC} (some packages may have failed)"
else
    echo -e "${GREEN}OK${NC}"
fi

# Create required directories
echo -n "Creating directories... "
mkdir -p "$HOME/.aos/brain/state"
mkdir -p "$HOME/.aos/logs"
echo -e "${GREEN}OK${NC}"

# Check if brain is already running
echo -n "Checking for existing brain process... "
if pgrep -f "brain_server.py" > /dev/null; then
    echo -e "${YELLOW}ALREADY RUNNING${NC}"
    echo "Use 'pkill -f brain_server.py' to stop, then restart."
    exit 1
fi
echo -e "${GREEN}OK${NC}"

# Start the brain server
echo ""
echo -e "${GREEN}🚀 Starting brain server...${NC}"
echo "HTTP API: http://localhost:5000"
echo "Socket: /tmp/aos_brain.sock"
echo "Health: http://localhost:5000/health"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run in foreground (for systemd, use --daemon)
cd "$PROJECT_DIR"
exec python3 -m brain.brain_server "$@"
