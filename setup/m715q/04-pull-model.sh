#!/usr/bin/env bash
# Pull a starter GGUF model and launch llama-server with an OpenAI-compatible API.
# Run ON the M715q (inside the llama.cpp dir, or anywhere — adjust paths).
set -euo pipefail

# Pick your model. Default: Qwen2.5 7B Instruct Q4_K_M (~4.7 GB, fits easily in 32GB).
MODEL_URL="${MODEL_URL:-https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF/resolve/main/Qwen2.5-7B-Instruct-Q4_K_M.gguf}"
MODEL_FILE="$(basename "$MODEL_URL")"

if [[ ! -f "$MODEL_FILE" ]]; then
  echo "==> Downloading model ..."
  curl -fL -o "$MODEL_FILE" "$MODEL_URL"
fi

echo "==> Launching llama-server on :8080 (OpenAI-compatible) ..."
# --host 0.0.0.0 so the other box / LAN can reach it. Drop if you only want localhost.
exec ./build/bin/llama-server \
  -m "$MODEL_FILE" \
  --host 0.0.0.0 \
  --port 8080

# Test it from another machine:
#   curl http://<box-ip>:8080/v1/chat/completions \
#     -H 'Content-Type: application/json' \
#     -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"hi"}]}'
