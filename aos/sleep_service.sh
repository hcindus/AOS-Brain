#!/bin/bash
# AOS Sleep Scheduler Service Script
# Manages sleep cycles for memory consolidation

case "$1" in
  start)
    echo "Starting AOS Sleep Scheduler..."
    nohup python3 /root/.openclaw/workspace/aos/sleep_scheduler.py > /var/log/aos/sleep_scheduler.log 2>&1 &
    echo $! > /var/run/aos_sleep.pid
    echo "Sleep scheduler started."
    ;;
  stop)
    if [ -f /var/run/aos_sleep.pid ]; then
      echo "Stopping AOS Sleep Scheduler..."
      kill $(cat /var/run/aos_sleep.pid) 2>/dev/null
      rm /var/run/aos_sleep.pid
      echo "Sleep scheduler stopped."
    else
      echo "Sleep scheduler not running."
    fi
    ;;
  status)
    if [ -f /var/run/aos_sleep.pid ] && kill -0 $(cat /var/run/aos_sleep.pid) 2>/dev/null; then
      echo "AOS Sleep Scheduler is running (PID: $(cat /var/run/aos_sleep.pid))"
    else
      echo "AOS Sleep Scheduler is not running"
    fi
    ;;
  *)
    echo "Usage: $0 {start|stop|status}"
    exit 1
    ;;
esac
