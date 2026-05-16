#!/bin/bash
# Client Outreach App Startup Script
# Port: 8083

cd /root/.openclaw/workspace/client-outreach

# Initialize database if needed
if [ ! -f "database/outreach.db" ]; then
    echo "Initializing database..."
    sqlite3 database/outreach.db < database/schema.sql
    echo "Database created with demo data"
fi

# Start the FastAPI app
echo "Starting Client Outreach app on port 8083..."
python3 app/main.py
