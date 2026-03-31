#!/bin/bash
# Minecraft Agent Rotation Script

# Stop all current agents
pkill -f 'mineflayer.*agent' 2>/dev/null || true
sleep 2

# Start active batch
# Starting Agent_Steve (Builder)
echo 'Spawning Agent_Steve...'
sleep 1
# Starting Agent_Alex (Explorer)
echo 'Spawning Agent_Alex...'
sleep 1
# Starting Agent_Miner (Miner)
echo 'Spawning Agent_Miner...'
sleep 1
# Starting Agent_Builder (Builder)
echo 'Spawning Agent_Builder...'
sleep 1
# Starting Agent_Explorer (Explorer)
echo 'Spawning Agent_Explorer...'
sleep 1
# Starting Agent_Redstone (Engineer)
echo 'Spawning Agent_Redstone...'
sleep 1
# Starting Agent_Farmer (Farmer)
echo 'Spawning Agent_Farmer...'
sleep 1

# 7 agents now active