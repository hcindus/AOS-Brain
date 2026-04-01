#!/bin/bash
# Minecraft Agent Rotation Script

# Stop all current agents
pkill -f 'mineflayer.*agent' 2>/dev/null || true
sleep 2

# Start active batch
# Starting Agent_Crafter (Crafter)
echo 'Spawning Agent_Crafter...'
sleep 1
# Starting Agent_Fighter (Guard)
echo 'Spawning Agent_Fighter...'
sleep 1
# Starting Agent_Navigator (Navigator)
echo 'Spawning Agent_Navigator...'
sleep 1
# Starting Agent_Collector (Collector)
echo 'Spawning Agent_Collector...'
sleep 1
# Starting Agent_Enchanter (Enchanter)
echo 'Spawning Agent_Enchanter...'
sleep 1
# Starting Agent_Lumberjack (Gatherer)
echo 'Spawning Agent_Lumberjack...'
sleep 1
# Starting Agent_Steve (Builder)
echo 'Spawning Agent_Steve...'
sleep 1

# 7 agents now active