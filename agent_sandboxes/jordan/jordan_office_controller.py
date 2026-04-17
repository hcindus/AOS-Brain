#!/usr/bin/env python3
"""
Jordan Office Controller
Manages AGI Company office operations and integrations
"""

import subprocess
import json
import sqlite3
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class JordanOfficeController:
    """Jordan's interface to manage the AGI Company office"""
    
    VERSION = "1.0.0"
    WORKSPACE = "/root/.openclaw/workspace"
    
    def __init__(self):
        print(f"🔧 Jordan Office Controller v{self.VERSION} initialized")
        self.systems = self._discover_systems()
    
    def _discover_systems(self) -> Dict:
        """Discover all AGI Company systems"""
        systems = {
            "brain": {"name": "Complete Brain v4", "status": "checking..."},
            "mission_control": {"name": "Mission Control", "status": "checking..."},
            "dark_factory": {"name": "Dark Factory Pipeline", "status": "checking..."},
            "patricia": {"name": "Patricia/THIS", "status": "checking..."},
            "roblox": {"name": "Roblox Bridge", "status": "checking..."},
            "minecraft": {"name": "Minecraft Server", "status": "checking..."},
            "git": {"name": "Git Repository", "status": "checking..."},
        }
        return systems
    
    def check_system_status(self, system_name: str) -> Dict:
        """Check status of a specific system"""
        status = {"name": system_name, "running": False, "details": {}}
        
        try:
            if system_name == "brain":
                result = subprocess.run(
                    ["systemctl", "is-active", "aos-brain-v4"],
                    capture_output=True, text=True, timeout=5
                )
                status["running"] = result.stdout.strip() == "active"
                status["details"]["service"] = "aos-brain-v4"
            
            elif system_name == "mission_control":
                result = subprocess.run(
                    ["systemctl", "is-active", "aos-mission-control"],
                    capture_output=True, text=True, timeout=5
                )
                status["running"] = result.stdout.strip() == "active"
                status["details"]["service"] = "aos-mission-control"
                status["details"]["port"] = 8080
            
            elif system_name == "dark_factory":
                result = subprocess.run(
                    ["systemctl", "is-active", "dark-factory-pipeline"],
                    capture_output=True, text=True, timeout=5
                )
                status["running"] = result.stdout.strip() == "active"
                status["details"]["service"] = "dark-factory-pipeline"
            
            elif system_name == "patricia":
                # Check if Patricia has recent reports
                report_dir = Path(f"{self.WORKSPACE}/agent_sandboxes/patricia/reports")
                if report_dir.exists():
                    reports = list(report_dir.glob("*.json"))
                    status["running"] = len(reports) > 0
                    status["details"]["report_count"] = len(reports)
                else:
                    status["running"] = False
            
            elif system_name == "minecraft":
                result = subprocess.run(
                    ["pgrep", "-f", "minecraft_server"],
                    capture_output=True, timeout=2
                )
                status["running"] = result.returncode == 0
            
            elif system_name == "git":
                result = subprocess.run(
                    ["git", "status", "--short"],
                    cwd=self.WORKSPACE,
                    capture_output=True, text=True, timeout=5
                )
                status["running"] = True
                status["details"]["uncommitted_changes"] = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                
        except Exception as e:
            status["error"] = str(e)
        
        return status
    
    def get_full_status(self) -> Dict:
        """Get status of all systems"""
        print("🔍 Scanning AGI Company systems...")
        
        full_status = {
            "timestamp": datetime.now().isoformat(),
            "systems": {}
        }
        
        for system_id in self.systems:
            status = self.check_system_status(system_id)
            full_status["systems"][system_id] = status
            self.systems[system_id]["status"] = "running" if status["running"] else "stopped"
        
        # Overall health
        running = sum(1 for s in full_status["systems"].values() if s["running"])
        total = len(full_status["systems"])
        full_status["health_percentage"] = round((running / total) * 100, 1)
        full_status["overall_status"] = "healthy" if running == total else "degraded"
        
        return full_status
    
    def run_office_diagnostics(self) -> Dict:
        """Run comprehensive office diagnostics"""
        print("🔧 Running office diagnostics...")
        
        diagnostics = {
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # Check 1: Brain socket
        try:
            result = subprocess.run(
                ['bash', '-c', 'echo \'{"cmd":"status"}\' | nc -U /tmp/aos_brain.sock 2>/dev/null | head -1'],
                capture_output=True, text=True, timeout=5
            )
            diagnostics["checks"]["brain_socket"] = {
                "status": "pass" if result.stdout else "fail",
                "response": result.stdout[:100] if result.stdout else "No response"
            }
        except Exception as e:
            diagnostics["checks"]["brain_socket"] = {"status": "error", "error": str(e)}
        
        # Check 2: Mission Control HTTP
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:8080/api/status"],
                capture_output=True, text=True, timeout=5
            )
            diagnostics["checks"]["mission_control_http"] = {
                "status": "pass" if result.stdout else "fail",
                "response": result.stdout[:200] if result.stdout else "No response"
            }
        except Exception as e:
            diagnostics["checks"]["mission_control_http"] = {"status": "error", "error": str(e)}
        
        # Check 3: Dark Factory queue
        try:
            conn = sqlite3.connect(f"{self.WORKSPACE}/data/factory/dark_factory.db")
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM production_orders WHERE status != 'completed'")
            pending = c.fetchone()[0]
            conn.close()
            diagnostics["checks"]["dark_factory_queue"] = {
                "status": "pass",
                "pending_orders": pending
            }
        except Exception as e:
            diagnostics["checks"]["dark_factory_queue"] = {"status": "error", "error": str(e)}
        
        # Check 4: Git status
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.WORKSPACE,
                capture_output=True, text=True, timeout=5
            )
            changes = result.stdout.strip().split('\n') if result.stdout.strip() else []
            diagnostics["checks"]["git_status"] = {
                "status": "pass",
                "uncommitted": len(changes),
                "needs_sync": len(changes) > 0
            }
        except Exception as e:
            diagnostics["checks"]["git_status"] = {"status": "error", "error": str(e)}
        
        # Summary
        passed = sum(1 for c in diagnostics["checks"].values() if c.get("status") == "pass")
        total = len(diagnostics["checks"])
        diagnostics["summary"] = {
            "passed": passed,
            "total": total,
            "success_rate": f"{passed}/{total}"
        }
        
        return diagnostics
    
    def sync_to_github(self) -> bool:
        """Sync all changes to GitHub"""
        print("☁️ Syncing to GitHub...")
        
        try:
            # Add all changes
            subprocess.run(
                ["git", "add", "-A"],
                cwd=self.WORKSPACE,
                check=True, timeout=10
            )
            
            # Commit
            timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M")
            result = subprocess.run(
                ["git", "commit", "-m", f"Jordan office sync {timestamp}"],
                cwd=self.WORKSPACE,
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0 or "nothing to commit" in result.stdout:
                # Push
                subprocess.run(
                    ["git", "push", "origin", "master"],
                    cwd=self.WORKSPACE,
                    check=True, timeout=30
                )
                print("✅ GitHub sync complete")
                return True
            else:
                print("ℹ️ No changes to sync")
                return True
                
        except Exception as e:
            print(f"❌ GitHub sync failed: {e}")
            return False
    
    def generate_office_report(self) -> str:
        """Generate office status report"""
        status = self.get_full_status()
        diagnostics = self.run_office_diagnostics()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║        🔧 JORDAN'S AGI COMPANY OFFICE REPORT                 ║
╠══════════════════════════════════════════════════════════════╣
║ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
║ Overall Health: {status['health_percentage']}% ({status['overall_status'].upper()})
╠══════════════════════════════════════════════════════════════╣
║ SYSTEM STATUS
║ ─────────────────────────────────────────────────────────────"""
        
        for system_id, system_status in status["systems"].items():
            emoji = "✅" if system_status["running"] else "❌"
            name = self.systems[system_id]["name"]
            report += f"\n║  {emoji} {name:<25} | {('RUNNING' if system_status['running'] else 'STOPPED'):<10}"
        
        report += """
╠══════════════════════════════════════════════════════════════╣
║ DIAGNOSTICS
║ ─────────────────────────────────────────────────────────────"""
        
        for check_name, check_result in diagnostics["checks"].items():
            emoji = "✅" if check_result.get("status") == "pass" else "❌"
            report += f"\n║  {emoji} {check_name:<25} | {check_result.get('status', 'unknown'):<10}"
        
        report += f"""
╠══════════════════════════════════════════════════════════════╣
║ SUMMARY: {diagnostics['summary']['success_rate']} checks passed
╚══════════════════════════════════════════════════════════════╝"""
        
        return report
    
    def run_office_tick(self):
        """Run one office management tick"""
        print("🔧 Jordan running office tick...")
        
        # Check all systems
        status = self.get_full_status()
        
        # Run diagnostics
        diagnostics = self.run_office_diagnostics()
        
        # Sync to GitHub if there are changes
        if diagnostics["checks"].get("git_status", {}).get("needs_sync", False):
            self.sync_to_github()
        
        # Report issues if any systems down
        if status["overall_status"] == "degraded":
            down_systems = [name for name, s in status["systems"].items() if not s["running"]]
            print(f"⚠️  Systems requiring attention: {', '.join(down_systems)}")
        
        print("✅ Office tick complete\n")
        return status


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Jordan Office Controller')
    parser.add_argument('command', choices=['status', 'diagnostics', 'report', 'sync', 'tick'])
    args = parser.parse_args()
    
    controller = JordanOfficeController()
    
    if args.command == 'status':
        status = controller.get_full_status()
        print(json.dumps(status, indent=2))
    
    elif args.command == 'diagnostics':
        diagnostics = controller.run_office_diagnostics()
        print(json.dumps(diagnostics, indent=2))
    
    elif args.command == 'report':
        print(controller.generate_office_report())
    
    elif args.command == 'sync':
        controller.sync_to_github()
    
    elif args.command == 'tick':
        controller.run_office_tick()


if __name__ == "__main__":
    main()
