#!/usr/bin/env python3
"""
Brain Health Monitor v1.1
Automated health monitoring for Brain v4.5
Checks socket every 60 seconds, alerts if down for 5+ minutes
"""

import socket
import json
import logging
from datetime import datetime
from pathlib import Path

# Config
BRAIN_SOCKET = "/tmp/aos_brain.sock"
CHECK_INTERVAL = 60  # seconds
ALERT_THRESHOLD = 300  # 5 minutes
LOG_FILE = "/var/log/aos/brain_health.log"
STATUS_FILE = "/tmp/brain_health.status"

# Setup logging
Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BrainHealthMonitor:
    def __init__(self):
        self.consecutive_failures = 0
        self.last_success = datetime.now()
        self.is_healthy = True
        
    def check_socket(self) -> bool:
        """Check if Brain socket is responding"""
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(BRAIN_SOCKET)
            sock.send(json.dumps({"cmd": "ping"}).encode())
            response = sock.recv(1024).decode()
            sock.close()
            
            data = json.loads(response)
            if data.get("pong") == True or data.get("status") == "ok":
                return True
            return False
        except Exception as e:
            logger.debug(f"Socket check failed: {e}")
            return False
    
    def send_alert(self, message: str):
        """Send alert"""
        logger.error(f"🚨 ALERT: {message}")
        with open(STATUS_FILE, 'w') as f:
            f.write(f"DOWN|{datetime.now().isoformat()}|{message}")
    
    def send_recovery_notice(self):
        """Send recovery notification"""
        downtime = (datetime.now() - self.last_success).total_seconds()
        logger.info(f"✅ Brain recovered after {downtime:.0f}s downtime")
        with open(STATUS_FILE, 'w') as f:
            f.write(f"UP|{datetime.now().isoformat()}|Recovered")
    
    def run(self):
        """Main monitoring loop"""
        logger.info("="*60)
        logger.info("🧠 BRAIN HEALTH MONITOR v1.1 STARTED")
        logger.info("="*60)
        logger.info(f"Target: {BRAIN_SOCKET}")
        logger.info(f"Check interval: {CHECK_INTERVAL}s")
        logger.info(f"Alert threshold: {ALERT_THRESHOLD}s")
        
        import time
        while True:
            is_alive = self.check_socket()
            
            if is_alive:
                if not self.is_healthy:
                    self.send_recovery_notice()
                    self.is_healthy = True
                    self.consecutive_failures = 0
                
                self.last_success = datetime.now()
                logger.debug("✅ Brain socket healthy")
            else:
                self.consecutive_failures += 1
                failure_time = self.consecutive_failures * CHECK_INTERVAL
                
                if self.is_healthy:
                    logger.warning(f"⚠️ Brain socket unresponsive ({failure_time}s)")
                
                if failure_time >= ALERT_THRESHOLD and self.is_healthy:
                    self.is_healthy = False
                    self.send_alert(
                        f"Brain v4.5 DOWN for {ALERT_THRESHOLD}s+ "
                        f"(Socket {BRAIN_SOCKET})"
                    )
            
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor = BrainHealthMonitor()
    try:
        monitor.run()
    except KeyboardInterrupt:
        logger.info("👋 Brain Health Monitor stopped")
