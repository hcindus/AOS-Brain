#!/bin/bash
# Space Agent Launcher v1.0

SPACE_AGENT_DIR="/var/www/space-agent"
PID_FILE="/tmp/space-agent.pid"
LOG_FILE="/tmp/space-agent.log"
PORT=8081

start() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "Space Agent already running (PID: $(cat $PID_FILE))"
        return
    fi
    
    echo "Starting Space Agent v1.0 on port $PORT..."
    cd "$SPACE_AGENT_DIR/public"
    nohup python3 -m http.server $PORT --bind 0.0.0.0 > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    sleep 1
    
    if kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "✅ Space Agent running at http://localhost:$PORT"
        echo "   Brain API: http://localhost:8080"
    else
        echo "❌ Failed to start"
    fi
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            rm -f "$PID_FILE"
            echo "✅ Space Agent stopped"
        else
            echo "Process not running"
            rm -f "$PID_FILE"
        fi
    else
        echo "Space Agent not running"
    fi
}

status() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "✅ Space Agent running (PID: $(cat $PID_FILE))"
        echo "   URL: http://localhost:$PORT"
        echo "   Log: $LOG_FILE"
    else
        echo "❌ Space Agent not running"
    fi
}

case "${1:-start}" in
    start) start ;;
    stop) stop ;;
    restart) stop; sleep 1; start ;;
    status) status ;;
    *) echo "Usage: $0 {start|stop|restart|status}" ;;
esac
