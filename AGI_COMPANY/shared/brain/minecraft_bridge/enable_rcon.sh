#!/bin/bash
# Enable RCON for Minecraft server

echo "Enabling Minecraft RCON..."

# Stop server
systemctl stop minecraft

# Edit server.properties
MC_DIR="/opt/minecraft-server"
PROP_FILE="$MC_DIR/server.properties"

# Backup
cp $PROP_FILE $PROP_FILE.bak

# Enable RCON with password
sed -i 's/enable-rcon=false/enable-rcon=true/' $PROP_FILE
sed -i 's/rcon.password=.*/rcon.password=aosbrain123/' $PROP_FILE

echo "RCON enabled. Password: aosbrain123"
echo "Port: 25575"

# Start server
systemctl start minecraft

echo "Minecraft server restarting..."
sleep 5
systemctl status minecraft --no-pager -l | head -5
