#!/bin/bash
# Ollama Keepalive - Keep Mortimer model resident
# Updated: 2026-04-02

MORTIMER_MODEL="antoniohudnall/Mortimer:latest"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Keeping Mortimer model resident..."

# Send a lightweight keepalive request
curl -s http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"${MORTIMER_MODEL}\",
    \"prompt\": \".\",
    \"stream\": false,
    \"options\": {
      \"num_predict\": 1
    }
  }" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Mortimer keepalive successful"
else
    echo "⚠️  Keepalive check needed"
fi
