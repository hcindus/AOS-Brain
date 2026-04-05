#!/bin/bash
# Mortimer Keepalive Script
# Runs every 5 minutes to keep Mortimer model resident in Ollama memory
# Prevents agent timeouts from cold-start loading

curl -s http://localhost:11434/api/generate \
  -d '{"model":"antoniohudnall/Mortimer:latest","prompt":"ping","stream":false}' \
  > /dev/null 2>&1

# Log success (optional, for debugging)
# echo "$(date): Mortimer keepalive ping" >> /var/log/mortimer-keepalive.log