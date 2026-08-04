#!/bin/bash
# Ollama Keepalive - Keep Mortimer model resident
# Updated: 2026-08-04 - Uses ollama ps to check, only loads if missing
# OLLAMA_KEEP_ALIVE=168h keeps models loaded 1 week

MORTIMER_MODEL="antoniohudnall/Mort_II:latest"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking Mortimer model..."

# Check if model is already loaded (fast, no generation needed)
if ollama ps 2>/dev/null | grep -q "$MORTIMER_MODEL"; then
    echo "✅ Mortimer already loaded"
    exit 0
fi

# Model not loaded - do a one-shot load with long timeout
echo "   Model not loaded, loading now..."
HTTP_CODE=$(curl -s --max-time 300 -w "%{http_code}" -o /dev/null \
  http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"${MORTIMER_MODEL}\",
    \"prompt\": \".\",
    \"stream\": false,
    \"keep_alive\": \"168h\",
    \"options\": {
      \"num_predict\": 1
    }
  }")

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Mortimer loaded successfully"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "⚠️  Ollama not responding (timeout after 5min)"
else
    echo "⚠️  Load returned HTTP $HTTP_CODE"
fi
