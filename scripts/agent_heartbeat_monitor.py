#!/usr/bin/env python3
"""
Agent Heartbeat Activator v1.0
Monitors for pending tasks and activates agents on heartbeat
"""

import os
import json
import glob
from datetime import datetime

def check_pending_tasks():
    """Check all agent sandboxes for pending tasks"""
    workspace = "/root/.openclaw/workspace"
    agents = ["aurora", "chelios", "forge", "patricia"]
    
    status = {}
    for agent in agents:
        tasks_dir = f"{workspace}/agent_sandboxes/{agent}/tasks"
        tasks = glob.glob(f"{tasks_dir}/*.md") if os.path.exists(tasks_dir) else []
        status[agent] = len(tasks)
    
    return status

def check_patricia_queue():
    """Check Patricia's production queue"""
    workspace = "/root/.openclaw/workspace"
    queue_files = glob.glob(f"{workspace}/agent_sandboxes/patricia/data/patricia_queue_*.json")
    
    if not queue_files:
        return 0
    
    latest = max(queue_files, key=os.path.getmtime)
    try:
        with open(latest) as f:
            data = json.load(f)
            return data.get("total_items", 0)
    except:
        return 0

def generate_heartbeat_response():
    """Generate heartbeat response with agent activation status"""
    task_status = check_pending_tasks()
    queue_count = check_patricia_queue()
    
    total_tasks = sum(task_status.values())
    
    response = {
        "timestamp": datetime.utcnow().isoformat(),
        "pending_tasks": task_status,
        "production_queue": queue_count,
        "total_pending": total_tasks + queue_count,
        "agents_needing_activation": [agent for agent, count in task_status.items() if count > 0]
    }
    
    return response

if __name__ == "__main__":
    status = generate_heartbeat_response()
    print(json.dumps(status, indent=2))
    
    # Exit with code based on pending work
    if status["total_pending"] > 0:
        print(f"\n⚠️  {status['total_pending']} items pending - agents need activation")
        exit(1)  # Signal that work is pending
    else:
        print("\n✅ No pending tasks")
        exit(0)
