#!/usr/bin/env bash
set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

echo -e "${BLUE}🤖 AOS – Autonomous Operating System (VPS Install)${NC}"
echo ""

sudo apt update -y
sudo apt install -y python3 python3-pip git curl nodejs redis-server tmux wget

mkdir -p ~/.aos/models ~/.aos/brain/state ~/.aos/memory/vector ~/.aos/logs

echo -e "${BLUE}🧠 Choose model mode:${NC}"
echo "1) Download GGUF models automatically"
echo "2) Use models already in ~/.aos/models"
echo "3) Use Ollama to manage models"
read -p "Enter choice (1/2/3): " MODE

cd ~/.aos/models

if [ "$MODE" = "1" ]; then
 echo -e "${BLUE}⬇️ Downloading GGUF models...${NC}"
 curl -LO https://huggingface.co/your-org/qwen2.5-3b-q4.gguf
 curl -LO https://huggingface.co/your-org/phi3-mini-3.8b-q4.gguf
 curl -LO https://huggingface.co/your-org/phi3-mini-1.8b-q4.gguf
 curl -LO https://huggingface.co/your-org/bge-small-q4.gguf
 curl -LO https://huggingface.co/your-org/tiny-llm-350m-q4.gguf
elif [ "$MODE" = "3" ]; then
 echo -e "${BLUE}📦 Installing Ollama...${NC}"
 curl -fsSL https://ollama.com/install.sh | sh
 ollama pull qwen2.5:3b
 ollama pull phi3:3.8b
 ollama pull phi3:1.8b
 ollama pull bge-small
 ollama pull tiny-llm
fi

echo -e "${BLUE}🔧 Installing OpenClaw...${NC}"
npm install -g openclaw@2026.2.19 || echo -e "${YELLOW}⚠️ OpenClaw install may be partial.${NC}"

echo -e "${BLUE}💾 Creating 30GB swapfile...${NC}"
sudo fallocate -l 30G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile || true
sudo swapon /swapfile || true

cp -r config docs brain visualizer test ~/.aos/

echo -e "${GREEN}🎉 AOS VPS installation complete.${NC}"
echo -e "Run brain: ${YELLOW}python3 ~/.aos/brain/brain.py${NC}"
echo -e "Run viz: ${YELLOW}python3 ~/.aos/visualizer/brain_visualizer.py${NC}"
echo -e "Run gateway: ${YELLOW}openclaw gateway --verbose${NC}"
