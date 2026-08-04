#!/bin/bash
# Ollama Keepalive - Keep Mortimer model resident
# Updated: 2026-08-04 (fixed timeout + keep_alive param)

MORTIMER_MODEL="antoniohudnall/Mort_II:latest"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Keeping Mortimer model resident..."

# Use keep_alive param + 120s timeout for cold-load scenarios
HTTP_CODE=$(curl -s --max-time 120 -w "%{http_code}" -o /dev/null \
  http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"${MORTIMER_MODEL}\",
    \"prompt\": \".\",
    \"stream\": false,
    \"keep_alive\": \"30m\",
    \"options\": {
      \"num_predict\": 1
    }
  }")

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Mortimer keepalive successful"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "⚠️  Ollama not responding (timeout)"
else
    echo "⚠️  Keepalive returned HTTP $HTTP_CODE"
fi
