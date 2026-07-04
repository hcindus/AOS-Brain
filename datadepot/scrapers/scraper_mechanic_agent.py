#!/usr/bin/env python3
"""
SCRAPER MECHANIC AGENT
Monitors scrapers, diagnoses failures, repairs, and restarts
The pit crew for data collection
"""

import sqlite3
import subprocess
import json
import time
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import logging
import threading
import signal

# Configuration
CONFIG_FILE = Path("/root/.openclaw/workspace/datadepot/scrapers/scraper_config.json")
LOG_FILE = Path("/var/log/aos/scraper_mechanic.log")
PID_FILE = Path("/var/run/scraper_mechanic.pid")
DB_PATH = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"

# Ensure log directory exists
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [MECHANIC] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScraperMechanic:
    def __init__(self):
        self.running = True
        self.scrapers = {}
        self.load_config()
        self.setup_signal_handlers()
        
    def setup_signal_handlers(self):
        """Handle shutdown gracefully"""
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)
        
    def shutdown(self, signum, frame):
        """Graceful shutdown"""
        logger.info("=" * 60)
        logger.info("SHUTDOWN SIGNAL RECEIVED - Stopping mechanic...")
        logger.info("=" * 60)
        self.running = False
        
    def load_config(self):
        """Load scraper configuration"""
        default_config = {
            "check_interval": 60,
            "max_failures": 3,
            "restart_delay": 30,
            "scrapers": {
                "ak_priority": {
                    "script": "/root/.openclaw/workspace/datadepot/scrapers/alaska_business_scraper.py",
                    "enabled": True,
                    "schedule": "0 */6 * * *",
                    "last_run": None,
                    "status": "idle",
                    "failures": 0
                },
                "multi_state": {
                    "script": "/root/.openclaw/workspace/datadepot/scrapers/multi_state_business_scraper.py",
                    "enabled": True,
                    "schedule": "0 */12 * * *",
                    "last_run": None,
                    "status": "idle",
                    "failures": 0
                }
            },
            "remaining_states": {
                "AL": {"cities": ["Birmingham", "Montgomery", "Mobile", "Huntsville"], "enabled": True},
                "NM": {"cities": ["Albuquerque", "Santa Fe", "Las Cruces", "Rio Rancho"], "enabled": True},
                "MS": {"cities": ["Jackson", "Gulfport", "Southaven", "Hattiesburg"], "enabled": True},
                "KY": {"cities": ["Louisville", "Lexington", "Bowling Green", "Owensboro"], "enabled": True},
                "AR": {"cities": ["Little Rock", "Fort Smith", "Fayetteville", "Springdale"], "enabled": True},
                "IA": {"cities": ["Des Moines", "Cedar Rapids", "Davenport", "Sioux City"], "enabled": True},
                "KS": {"cities": ["Wichita", "Overland Park", "Kansas City", "Topeka"], "enabled": True},
                "ID": {"cities": ["Boise", "Meridian", "Nampa", "Idaho Falls"], "enabled": True},
                "MN": {"cities": ["Minneapolis", "St. Paul", "Rochester", "Duluth"], "enabled": True},
                "UT": {"cities": ["Salt Lake City", "West Valley City", "Provo", "West Jordan"], "enabled": True},
                "OK": {"cities": ["Oklahoma City", "Tulsa", "Norman", "Broken Arrow"], "enabled": True},
                "MO": {"cities": ["Kansas City", "St. Louis", "Springfield", "Columbia"], "enabled": True},
                "WI": {"cities": ["Milwaukee", "Madison", "Green Bay", "Kenosha"], "enabled": True},
                "IN": {"cities": ["Indianapolis", "Fort Wayne", "Evansville", "South Bend"], "enabled": True},
                "MI": {"cities": ["Detroit", "Grand Rapids", "Warren", "Sterling Heights"], "enabled": True},
                "OH": {"cities": ["Columbus", "Cleveland", "Cincinnati", "Toledo"], "enabled": True},
                "GA": {"cities": ["Atlanta", "Augusta", "Columbus", "Macon"], "enabled": True},
                "SC": {"cities": ["Charleston", "Columbia", "North Charleston", "Mount Pleasant"], "enabled": True},
                "NC": {"cities": ["Charlotte", "Raleigh", "Greensboro", "Durham"], "enabled": True},
                "VA": {"cities": ["Virginia Beach", "Norfolk", "Chesapeake", "Richmond"], "enabled": True},
                "MD": {"cities": ["Baltimore", "Frederick", "Rockville", "Gaithersburg"], "enabled": True},
                "CT": {"cities": ["Bridgeport", "New Haven", "Stamford", "Hartford"], "enabled": True},
                "MA": {"cities": ["Boston", "Worcester", "Springfield", "Cambridge"], "enabled": True},
                "NJ": {"cities": ["Newark", "Jersey City", "Paterson", "Elizabeth"], "enabled": True},
                "PA": {"cities": ["Philadelphia", "Pittsburgh", "Allentown", "Erie"], "enabled": True},
                "NY": {"cities": ["New York City", "Buffalo", "Rochester", "Yonkers"], "enabled": True},
                "VT": {"cities": ["Burlington", "South Burlington", "Rutland", "Barre"], "enabled": True},
                "NH": {"cities": ["Manchester", "Nashua", "Concord", "Derry"], "enabled": True},
                "ME": {"cities": ["Portland", "Lewiston", "Bangor", "South Portland"], "enabled": True},
                "RI": {"cities": ["Providence", "Warwick", "Cranston", "Pawtucket"], "enabled": True},
                "DE": {"cities": ["Wilmington", "Dover", "Newark", "Middletown"], "enabled": True},
                "WV": {"cities": ["Charleston", "Huntington", "Morgantown", "Parkersburg"], "enabled": True},
                "DC": {"cities": ["Washington"], "enabled": True}
            }
        }
        
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        """Save configuration"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def check_database_health(self):
        """Diagnose database connection issues"""
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM vendors")
            count = c.fetchone()[0]
            conn.close()
            return True, f"Database healthy: {count} vendors"
        except Exception as e:
            return False, f"Database error: {str(e)}"
            
    def check_disk_space(self):
        """Check available disk space"""
        try:
            stat = os.statvfs('/root/.openclaw/workspace')
            free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
            if free_gb < 1.0:
                return False, f"Low disk space: {free_gb:.2f}GB free"
            return True, f"Disk space OK: {free_gb:.2f}GB free"
        except Exception as e:
            return False, f"Disk check error: {str(e)}"
            
    def diagnose_scraper(self, scraper_name):
        """Run diagnostics on a scraper"""
        issues = []
        fixes = []
        
        # Check database
        db_ok, db_msg = self.check_database_health()
        if not db_ok:
            issues.append(db_msg)
            fixes.append("RESTART_DATABASE")
            
        # Check disk space
        disk_ok, disk_msg = self.check_disk_space()
        if not disk_ok:
            issues.append(disk_msg)
            fixes.append("CLEAR_LOGS")
            
        # Check if script exists
        scraper_config = self.config["scrapers"].get(scraper_name, {})
        script_path = scraper_config.get("script", "")
        if not Path(script_path).exists():
            issues.append(f"Script not found: {script_path}")
            fixes.append("REINSTALL_SCRAPER")
            
        return issues, fixes
        
    def apply_fix(self, scraper_name, fix_type):
        """Apply a fix"""
        logger.info(f"Applying fix '{fix_type}' to {scraper_name}")
        
        if fix_type == "RESTART_DATABASE":
            try:
                subprocess.run(["systemctl", "restart", "depotchaos"], check=True)
                logger.info("Database service restarted")
                return True
            except Exception as e:
                logger.error(f"Failed to restart database: {e}")
                return False
                
        elif fix_type == "CLEAR_LOGS":
            try:
                log_dir = Path("/var/log/aos")
                for log_file in log_dir.glob("*.log"):
                    if log_file.stat().st_size > 100*1024*1024:  # >100MB
                        log_file.write_text("")  # Truncate
                        logger.info(f"Cleared log: {log_file}")
                return True
            except Exception as e:
                logger.error(f"Failed to clear logs: {e}")
                return False
                
        elif fix_type == "REINSTALL_SCRAPER":
            # Recreate the scraper script from template
            logger.info("Reinstalling scraper...")
            return self.reinstall_scraper(scraper_name)
            
        return False
        
    def reinstall_scraper(self, scraper_name):
        """Reinstall a scraper from backup/template"""
        # This would restore from git or template
        logger.info(f"Reinstalling {scraper_name}...")
        return True
        
    def run_scraper(self, scraper_name):
        """Run a scraper and monitor it"""
        if scraper_name not in self.config["scrapers"]:
            logger.error(f"Unknown scraper: {scraper_name}")
            return False
            
        scraper_config = self.config["scrapers"][scraper_name]
        script_path = scraper_config["script"]
        
        if not Path(script_path).exists():
            logger.error(f"Script not found: {script_path}")
            return False
            
        # Update status
        scraper_config["status"] = "running"
        scraper_config["last_run"] = datetime.now().isoformat()
        self.save_config()
        
        logger.info(f"Starting {scraper_name}...")
        
        try:
            # Run scraper with timeout
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
                cwd=str(Path(script_path).parent)
            )
            
            if result.returncode == 0:
                logger.info(f"{scraper_name} completed successfully")
                scraper_config["status"] = "idle"
                scraper_config["failures"] = 0
                self.save_config()
                return True
            else:
                logger.error(f"{scraper_name} failed with code {result.returncode}")
                logger.error(f"STDERR: {result.stderr[:500]}")
                scraper_config["status"] = "failed"
                scraper_config["failures"] += 1
                self.save_config()
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"{scraper_name} timed out after 1 hour")
            scraper_config["status"] = "timeout"
            scraper_config["failures"] += 1
            self.save_config()
            return False
            
        except Exception as e:
            logger.error(f"{scraper_name} exception: {e}")
            scraper_config["status"] = "error"
            scraper_config["failures"] += 1
            self.save_config()
            return False
            
    def repair_and_restart(self, scraper_name):
        """Diagnose, repair, and restart a scraper"""
        logger.info(f"=" * 60)
        logger.info(f"REPAIR MODE: {scraper_name}")
        logger.info(f"=" * 60)
        
        # Diagnose
        issues, fixes = self.diagnose_scraper(scraper_name)
        
        if not issues:
            logger.info(f"No issues found for {scraper_name}, attempting restart...")
            return self.run_scraper(scraper_name)
            
        # Log issues
        logger.warning(f"Found {len(issues)} issues:")
        for issue in issues:
            logger.warning(f"  - {issue}")
            
        # Apply fixes
        logger.info(f"Applying {len(fixes)} fixes...")
        for fix in fixes:
            if not self.apply_fix(scraper_name, fix):
                logger.error(f"Fix failed: {fix}")
                return False
                
        # Retry
        logger.info(f"Fixes applied, retrying {scraper_name}...")
        return self.run_scraper(scraper_name)
        
    def check_all_scrapers(self):
        """Check all scrapers and repair if needed"""
        for scraper_name, config in self.config["scrapers"].items():
            if not config.get("enabled", True):
                continue
                
            failures = config.get("failures", 0)
            status = config.get("status", "idle")
            
            # Check if scraper needs attention
            if failures >= self.config["max_failures"]:
                logger.warning(f"{scraper_name} has {failures} failures, entering repair mode")
                self.repair_and_restart(scraper_name)
            elif status in ["failed", "timeout", "error"]:
                logger.info(f"{scraper_name} status is '{status}', attempting repair")
                self.repair_and_restart(scraper_name)
            elif status == "idle":
                # Check if scheduled to run
                self.check_schedule(scraper_name)
                
    def check_schedule(self, scraper_name):
        """Check if scraper should run based on schedule"""
        config = self.config["scrapers"][scraper_name]
        last_run_str = config.get("last_run")
        
        if not last_run_str:
            # Never run, start it
            logger.info(f"{scraper_name} has never run, starting...")
            return self.run_scraper(scraper_name)
            
        last_run = datetime.fromisoformat(last_run_str)
        elapsed = (datetime.now() - last_run).total_seconds()
        
        # Simple interval check (every 6 hours for AK, 12 for multi-state)
        interval_hours = 6 if "ak" in scraper_name.lower() else 12
        interval_seconds = interval_hours * 3600
        
        if elapsed >= interval_seconds:
            logger.info(f"{scraper_name} scheduled to run (last run: {elapsed/3600:.1f}h ago)")
            return self.run_scraper(scraper_name)
            
        return True
        
    def run(self):
        """Main loop"""
        logger.info("=" * 60)
        logger.info("SCRAPER MECHANIC AGENT STARTED")
        logger.info("=" * 60)
        logger.info(f"Config: {CONFIG_FILE}")
        logger.info(f"Log: {LOG_FILE}")
        logger.info(f"Check interval: {self.config['check_interval']}s")
        logger.info("=" * 60)
        
        # Write PID file
        PID_FILE.write_text(str(os.getpid()))
        
        while self.running:
            try:
                self.check_all_scrapers()
                
                # Sleep with interrupt checking
                for _ in range(self.config["check_interval"]):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                logger.exception(f"Main loop error: {e}")
                time.sleep(10)
                
        # Cleanup
        if PID_FILE.exists():
            PID_FILE.unlink()
        logger.info("Mechanic agent stopped")

if __name__ == "__main__":
    mechanic = ScraperMechanic()
    mechanic.run()
