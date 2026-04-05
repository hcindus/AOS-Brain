#!/usr/bin/env python3
"""Watchdog - Keeps brain/heart/stomach/agents alive"""

import os
import sys
import time
import subprocess
import psutil

PROCESSES = {
    "brain": {"cmd": "python3 /root/.openclaw/workspace/AOS/brain/brain.py", "min": 1},
    "heart": {"cmd": "python3 /root/.openclaw/workspace/aos_brain_py/heart/ternary_heart.py", "min": 1},
    "stomach": {"cmd": "python3 /tmp/run_stomach.py", "min": 1},
    "minecraft": {"cmd": "systemctl start minecraft", "check": "java.*minecraft", "min": 1},
    "multi_agent": {"cmd": "python3 /root/.openclaw/workspace/AGI_COMPANY/shared/brain/minecraft_bridge/multi_agent.py", "min": 0}
}

def check_process(name, config):
    count = 0
    for proc in psutil.process_iter(['cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            if name in cmdline or (config.get('check') and config['check'] in cmdline):
                count += 1
        except: pass
    return count >= config['min']

def restart(name, config):
    print(f"[WATCHDOG] Restarting {name}...")
    os.system(config['cmd'] + " &")

def main():
    print("[WATCHDOG] Starting monitoring...")
    while True:
        for name, config in PROCESSES.items():
            if not check_process(name, config):
                restart(name, config)
        time.sleep(10)

if __name__ == "__main__":
    main()
