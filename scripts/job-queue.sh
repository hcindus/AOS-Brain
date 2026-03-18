#!/bin/bash
# Job Queue - Prevent parallel execution of heavy tasks

QUEUE_DIR="/tmp/aos-job-queue"
LOCK_FILE="$QUEUE_DIR/lock"
QUEUE_FILE="$QUEUE_DIR/queue"
RUNNING_FILE="$QUEUE_DIR/running"

mkdir -p "$QUEUE_DIR"

# Function to acquire lock
acquire_lock() {
    local timeout=${1:-5}
    local elapsed=0
    while ! mkdir "$LOCK_FILE" 2>/dev/null; do
        sleep 1
        ((elapsed++))
        if [[ $elapsed -ge $timeout ]]; then
            return 1
        fi
    done
    return 0
}

# Function to release lock
release_lock() {
    rmdir "$LOCK_FILE" 2>/dev/null
}

# Check if job can run
can_run() {
    if [[ -f "$RUNNING_FILE" ]]; then
        local pid=$(cat "$RUNNING_FILE" 2>/dev/null)
        if ps -p "$pid" > /dev/null 2>&1; then
            return 1  # Job still running
        else
            rm -f "$RUNNING_FILE"  # Stale lock
        fi
    fi
    return 0
}

# Queue a job
queue_job() {
    local job_name="$1"
    local job_cmd="$2"
    local priority="${3:-normal}"  # normal, high, low
    
    acquire_lock 10 || return 1
    
    local timestamp=$(date +%s)
    echo "$priority|$timestamp|$job_name|$job_cmd" >> "$QUEUE_FILE"
    
    release_lock
    echo "QUEUED: $job_name"
}

# Run next job in queue
run_next() {
    acquire_lock 10 || return 1
    
    if ! can_run; then
        release_lock
        echo "BUSY: Another job is running"
        return 1
    fi
    
    if [[ ! -s "$QUEUE_FILE" ]]; then
        release_lock
        return 0  # Queue empty
    fi
    
    # Get highest priority job (sort: high > normal > low)
    local job_line=$(sort -t'|' -k1,1r "$QUEUE_FILE" | head -1)
    local job_name=$(echo "$job_line" | cut -d'|' -f3)
    local job_cmd=$(echo "$job_line" | cut -d'|' -f4-)
    
    # Remove from queue
    grep -vF "$job_line" "$QUEUE_FILE" > "$QUEUE_FILE.tmp" && mv "$QUEUE_FILE.tmp" "$QUEUE_FILE"
    
    # Mark as running
    echo "$$" > "$RUNNING_FILE"
    echo "$job_name" >> "$RUNNING_FILE"
    
    release_lock
    
    # Execute job
    echo "RUNNING: $job_name"
    eval "$job_cmd"
    local exit_code=$?
    
    # Clean up
    rm -f "$RUNNING_FILE"
    
    echo "COMPLETED: $job_name (exit=$exit_code)"
    return $exit_code
}

# Kill orphaned processes
cleanup_orphans() {
    # Kill stale Gradle daemons
    ps aux | grep "GradleDaemon" | grep -v grep | awk '{print $2}' | while read pid; do
        local cpu=$(ps -p "$pid" -o %cpu= 2>/dev/null | tr -d ' ')
        if [[ -n "$cpu" && $(echo "$cpu > 50" | bc -l) -eq 1 ]]; then
            echo "Killing orphaned Gradle daemon (PID $pid, CPU $cpu%)"
            kill -9 "$pid" 2>/dev/null
        fi
    done
    
    # Clean stale lock files
    if [[ -f "$RUNNING_FILE" ]]; then
        local pid=$(head -1 "$RUNNING_FILE" 2>/dev/null)
        if ! ps -p "$pid" > /dev/null 2>&1; then
            rm -f "$RUNNING_FILE"
            echo "Cleaned stale running file"
        fi
    fi
}

# Main command handler
case "$1" in
    queue)
        queue_job "$2" "$3" "$4"
        ;;
    run)
        run_next
        ;;
    cleanup)
        cleanup_orphans
        ;;
    status)
        if [[ -f "$RUNNING_FILE" ]]; then
            echo "RUNNING: $(tail -1 "$RUNNING_FILE" 2>/dev/null)"
        else
            echo "IDLE"
        fi
        if [[ -s "$QUEUE_FILE" ]]; then
            echo "QUEUE: $(wc -l < "$QUEUE_FILE") jobs"
            cat "$QUEUE_FILE" | cut -d'|' -f3 | head -5 | nl
        else
            echo "QUEUE: empty"
        fi
        ;;
    *)
        echo "Usage: $0 {queue|run|cleanup|status}"
        echo "  queue <name> <command> [priority] - Add job to queue"
        echo "  run                               - Execute next queued job"
        echo "  cleanup                           - Kill orphaned processes"
        echo "  status                            - Show queue status"
        ;;
esac
