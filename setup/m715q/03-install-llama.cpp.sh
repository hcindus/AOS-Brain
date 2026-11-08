#!/usr/bin/env bash
# Install build deps, clone + build llama.cpp (CPU/AVX2 for the Ryzen APU).
# Run ON the M715q after Ubuntu Server is installed and you're logged in.
set -euo pipefail

echo "==> Installing build dependencies ..."
sudo apt-get update
sudo apt-get install -y build-essential cmake git curl ccache

echo "==> Cloning llama.cpp ..."
if [[ ! -d llama.cpp ]]; then
  git clone https://github.com/ggml-org/llama.cpp
fi
cd llama.cpp

echo "==> Building with native CPU optimizations (AVX2 on Zen/Zen+) ..."
cmake -B build -DGGML_NATIVE=ON
cmake --build build -j"$(nproc)"

echo "==> Verifying build ..."
./build/bin/llama-server --version

echo ""
echo "✅ llama.cpp built. Server binary: ./build/bin/llama-server"
echo "   Next: ./04-pull-model.sh   (downloads a starter Q4_K_M 7B model)"
