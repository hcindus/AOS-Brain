#!/data/data/com.termux/files/usr/bin/bash
# AOS-Lite with Myl0n Voice Interface Installer
# For Termux/Android

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     AOS-Lite + MYL0N Voice Interface Installer         ║"
echo "║     For Termux/Android                                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# WARNINGS
echo "⚠️  IMPORTANT WARNINGS:"
echo ""
echo "1. This is AOS-LITE (not full AOS)"
echo "   - Limited functionality vs desktop version"
echo "   - SQLite instead of ChromaDB"
echo "   - No GrowingNN (static architecture)"
echo ""
echo "2. Voice Interface Requirements:"
echo "   - Termux API app must be installed"
echo "   - Microphone permission required"
echo "   - Internet connection for TTS/STT"
echo ""
echo "3. Hardware Limitations:"
echo "   - Tiny models only (≤1B parameters)"
echo "   - 500ms tick interval (slower than 200ms)"
echo "   - Battery usage will increase"
echo ""
echo "4. Security:"
echo "   - No automatic vault setup"
echo "   - Manual credential management"
echo "   - Store sensitive data carefully"
echo ""
echo "5. Myl0n Voice Features:"
echo "   - Wake word: 'Hey Myl0n' or 'Hey Miles'"
echo "   - Continuous listening mode"
echo "   - WebSocket connection to brain"
echo "   - Requires Node.js and Python"
echo ""

read -p "Continue with installation? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "📱 Installing AOS-Lite + Myl0n..."

# Update packages
echo "📦 Updating packages..."
pkg update -y
pkg upgrade -y

# Install dependencies
echo "📦 Installing dependencies..."
pkg install -y python python-pip nodejs git curl termux-api

# Install Node.js dependencies
echo "🟢 Installing Node.js packages..."
npm install

# Install Python dependencies
echo "🐍 Installing Python packages..."
pip install --upgrade pip
pip install websockets asyncio

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p ~/.aos-lite/{brain,memory,logs,state}

# Copy files
echo "📋 Copying files..."
cp brain_lite.py ~/.aos-lite/brain/
cp myl0n.js ~/.aos-lite/
cp package.json ~/.aos-lite/

# Create start scripts
echo "🚀 Creating start scripts..."

cat > ~/.aos-lite/start-brain.sh << 'EOF'
#!/bin/bash
echo "Starting AOS-Lite Brain..."
cd ~/.aos-lite
python3 brain/brain_lite.py
EOF

cat > ~/.aos-lite/start-myl0n.sh << 'EOF'
#!/bin/bash
echo "Starting Myl0n Voice Interface..."
echo "Make sure AOS-Lite Brain is running first!"
echo ""
cd ~/.aos-lite
node myl0n.js
EOF

cat > ~/.aos-lite/start-all.sh << 'EOF'
#!/bin/bash
echo "Starting AOS-Lite + Myl0n..."
echo ""

# Start brain in background
echo "🧠 Starting AOS-Lite Brain..."
cd ~/.aos-lite
python3 brain/brain_lite.py &
BRAIN_PID=$!
echo "Brain PID: $BRAIN_PID"

# Wait for brain to start
sleep 2

# Start Myl0n
echo "🎤 Starting Myl0n Voice Interface..."
node myl0n.js

# Cleanup on exit
trap "kill $BRAIN_PID 2>/dev/null; exit" INT TERM
EOF

chmod +x ~/.aos-lite/*.sh

# Create README
cat > ~/.aos-lite/README.txt << 'EOF'
╔══════════════════════════════════════════════════════════╗
║     AOS-Lite + MYL0N Voice Interface                    ║
║     For Termux/Android                                   ║
╚══════════════════════════════════════════════════════════╝

⚠️  WARNINGS:

1. This is AOS-LITE (not full AOS)
2. Requires Termux API app for voice
3. Uses tiny models (≤1B parameters)
4. Battery usage will increase
5. Manual credential management

USAGE:

1. Start Brain only:
   ~/.aos-lite/start-brain.sh

2. Start Myl0n only (Brain must be running):
   ~/.aos-lite/start-myl0n.sh

3. Start both:
   ~/.aos-lite/start-all.sh

VOICE COMMANDS:

- Say "Hey Myl0n" or "Hey Miles" to wake
- Speak naturally after wake word
- Brain will respond via voice

FILES:

~/.aos-lite/
├── brain/
│   └── brain_lite.py      # Brain core
├── myl0n.js               # Voice interface
├── start-brain.sh         # Start brain
├── start-myl0n.sh         # Start voice
├── start-all.sh           # Start both
├── memory/
│   └── brain.db           # SQLite memory
└── logs/
    └── myl0n.log          # Voice logs

TROUBLESHOOTING:

1. "Termux API not available":
   - Install Termux:API app from F-Droid
   - Run: pkg install termux-api

2. "WebSocket connection failed":
   - Make sure brain is running first
   - Check: python3 ~/.aos-lite/brain/brain_lite.py

3. "No speech detected":
   - Check microphone permission
   - Speak clearly and close to device

4. "TTS not working":
   - Check internet connection
   - Try: termux-tts-speak "test"

For full AOS, use VPS installation.
EOF

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║     ✅ Installation Complete!                            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "⚠️  Remember: This is LITE mode with voice!"
echo ""
echo "To start:"
echo "   ~/.aos-lite/start-all.sh"
echo ""
echo "Or separately:"
echo "   ~/.aos-lite/start-brain.sh    # Terminal 1"
echo "   ~/.aos-lite/start-myl0n.sh     # Terminal 2"
echo ""
echo "Wake word: 'Hey Myl0n' or 'Hey Miles'"
echo ""
echo "For help:"
echo "   cat ~/.aos-lite/README.txt"
echo ""
