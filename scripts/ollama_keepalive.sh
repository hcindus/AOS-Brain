#!/bin/bash
# VERSION: 1.0.0
# UPDATED: 2026-04-02 04:08 UTC
# CHANGELOG: Initial model residency script
#
# Ollama Model Keepalive
# Prevents model eviction from memory with lightweight pings

for model in "antoniohudnall/Mortimer:latest"; do
    # Quick ping with timeout - non-blocking
    curl -s --max-time 3 http://localhost:11434/api/generate \
      -d "{\"model\":\"$model\",\"prompt\":\":\",\"stream\":false,\"options\":{\"num_predict\":1}}" \
      > /dev/null 2>&1 &
done
wait
