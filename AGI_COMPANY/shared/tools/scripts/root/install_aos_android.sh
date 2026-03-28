#!/data/data/com.termux/files/usr/bin/bash
set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

echo -e "${BLUE}🤖 AOS – Android / Termux Setup${NC}"
echo ""

SDK=$(getprop ro.build.version.sdk 2>/dev/null || echo "0")
LIMITED_MODE=false

if [ "$SDK" -lt 26 ]; then
 echo -e "${YELLOW}⚠️ Android API $SDK detected (AOS + OpenClaw prefer 26+).${NC}"
 echo "Options:"
 echo " 1. Use UserLAnd / proot-distro (recommended)"
 echo " 2. Continue with limited AOS-Lite"
 read -p "Continue? (y/N): " choice
 if [[ ! "$choice" =~ ^[Yy]$ ]]; then
 echo -e "${BLUE}💡 Try UserLAnd for full AOS.${NC}"
 exit 0
 fi
 LIMITED_MODE=true
fi

echo -e "${BLUE}📦 Updating packages...${NC}"
yes | pkg update || echo -e "${YELLOW}⚠️ Update had issues, continuing...${NC}"
yes | pkg upgrade || true

if [ "$LIMITED_MODE" = true ]; then
 pkg install -y git nodejs-lts openssh python
else
 pkg install -y git nodejs openssh tmux wget curl python
fi

echo -e "${BLUE}🔐 Starting SSH...${NC}"
sshd 2>/dev/null || echo -e "${YELLOW}⚠️ SSH may already be running${NC}"

echo -e "${BLUE}🌐 Network info:${NC}"
ifconfig 2>/dev/null | grep "inet " | head -1 || ip addr show | grep "inet " | head -1

mkdir -p ~/.aos/models ~/.aos/brain/state ~/.aos/logs

echo -e "${BLUE}🧠 Choose AOS-Lite model mode:${NC}"
echo "1) Tiny local model (<=1B)"
echo "2) Ollama (experimental)"
echo "3) Cloud inference (Gemini/OpenRouter via OpenClaw)"
read -p "Enter choice (1/2/3): " MODE

cd ~/.aos/models

if [ "$MODE" = "1" ]; then
 curl -LO https://huggingface.co/your-org/tiny-llm-350m-q4.gguf
elif [ "$MODE" = "2" ]; then
 curl -fsSL https://ollama.com/install.sh | sh || echo -e "${RED}❌ Ollama install failed.${NC}"
 ollama pull tiny-llm || true
fi

echo -e "${BLUE}🤖 Installing OpenClaw...${NC}"
npm i -g openclaw || echo -e "${YELLOW}⚠️ OpenClaw may not fully work on Android.${NC}"

cp -r config docs brain visualizer test ~/.aos/

echo -e "${GREEN}🎉 AOS-Lite installed.${NC}"
echo -e "Run brain: ${YELLOW}python3 ~/.aos/brain/brain.py${NC}"
echo -e "Run gateway: ${YELLOW}openclaw gateway --verbose${NC}"
