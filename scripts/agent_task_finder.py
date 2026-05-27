#!/usr/bin/env python3
"""
Agent Task Finder - Auto-Assign Work to Idle Agents
Creates default tasks for agents without explicit assignments
"""

import os
import json
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace"
LOG_FILE = "/var/log/aos/task_finder.log"

def log(message):
    timestamp = datetime.utcnow().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def create_task(agent, location, role, content):
    """Create a task file for an agent"""
    tasks_dir = os.path.join(location, "tasks")
    os.makedirs(tasks_dir, exist_ok=True)
    
    # Check if tasks already exist
    existing = [f for f in os.listdir(tasks_dir) if f.endswith('.md')]
    if existing:
        return False
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
    task_file = os.path.join(tasks_dir, f"AUTO_TASK_{role.upper()}_{timestamp}.md")
    
    with open(task_file, "w") as f:
        f.write(content)
    
    log(f"Created {role} task for {agent}")
    return True

def get_sales_task(agent):
    return f"""# AUTO-GENERATED TASK - Sales Activity
**Agent:** {agent}
**Role:** Sales
**Generated:** {datetime.utcnow().isoformat()}
**Priority:** NORMAL

## Find Work - Sales Department

### Immediate Actions:
1. Review lead database for high-priority prospects
2. Check email queue for follow-ups (1,700+ pending)
3. Analyze sales metrics and identify opportunities
4. Research competitor activity

### Daily Activities:
- [ ] Contact 10 prospects from lead list
- [ ] Send follow-up emails to warm leads
- [ ] Update CRM with activity
- [ ] Report findings to Pulp

### Data Sources:
- Leads: /root/.openclaw/workspace/data/scraper/
- CRM: DepotChaos database
- Reports: /root/.openclaw/workspace/daily_reports/

**Status:** Auto-assigned | Due: End of day
"""

def get_security_task(agent):
    return f"""# AUTO-GENERATED TASK - Security Audit
**Agent:** {agent}
**Role:** Security
**Generated:** {datetime.utcnow().isoformat()}
**Priority:** HIGH

## Find Work - Security Department

### Immediate Actions:
1. Run security audit on all systems
2. Check for unauthorized access attempts
3. Review log files for anomalies
4. Verify all agents have proper credentials

### Daily Activities:
- [ ] Review system logs for security events
- [ ] Check agent authentication status
- [ ] Run vulnerability scan
- [ ] Update security documentation

### Data Sources:
- Logs: /var/log/
- Agent Status: /root/.openclaw/workspace/data/scraper/agent_status.json
- Security Reports: /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/security_audit_firm/

**Status:** Auto-assigned | Due: End of day
"""

def get_general_task(agent):
    return f"""# AUTO-GENERATED TASK - General Assignment
**Agent:** {agent}
**Role:** Team Member
**Generated:** {datetime.utcnow().isoformat()}
**Priority:** NORMAL

## Find Work - General Assignment

### Company-Wide Opportunities:
- Archive old daily reports (7+ days old)
- Process stale email follow-ups (1,700+ pending)
- Commit uncommitted changes to git
- Update documentation
- Assist other departments

### Daily Activities:
- [ ] Review workspace for improvements
- [ ] Check for incomplete work from teammates
- [ ] Offer assistance to overloaded agents
- [ ] Document findings

**Status:** Auto-assigned | Due: End of day
"""

def main():
    log("Task Finder scanning for idle agents...")
    
    # Core sandboxes and their roles
    agents = {
        "aurora": ("agent_sandboxes/aurora", "general"),
        "chelios": ("agent_sandboxes/chelios", "security"),
        "forge": ("agent_sandboxes/forge", "general"),
        "patricia": ("agent_sandboxes/patricia", "general"),
        "jordan": ("agent_sandboxes/jordan", "sales"),
    }
    
    idle_count = 0
    
    for agent, (path, role) in agents.items():
        location = os.path.join(WORKSPACE, path)
        if not os.path.exists(location):
            continue
        
        # Check existing tasks
        tasks_dir = os.path.join(location, "tasks")
        existing_tasks = []
        if os.path.exists(tasks_dir):
            existing_tasks = [f for f in os.listdir(tasks_dir) if f.endswith('.md')]
        
        if not existing_tasks:
            # Create appropriate task
            if role == "sales":
                content = get_sales_task(agent)
            elif role == "security":
                content = get_security_task(agent)
            else:
                content = get_general_task(agent)
            
            if create_task(agent, location, role, content):
                idle_count += 1
    
    # Check company-wide work
    log("Checking company-wide opportunities...")
    
    # Old reports
    daily_reports = os.path.join(WORKSPACE, "daily_reports")
    if os.path.exists(daily_reports):
        old_count = len([f for f in os.listdir(daily_reports) if f.endswith('.md')])
        if old_count > 5:
            log(f"{old_count} daily reports exist - archiving needed")
    
    # Git status
    git_dir = os.path.join(WORKSPACE, ".git")
    if os.path.exists(git_dir):
        import subprocess
        try:
            result = subprocess.run(
                ["git", "-C", WORKSPACE, "status", "--porcelain"],
                capture_output=True, text=True
            )
            uncommitted = len([l for l in result.stdout.split('\n') if l.strip()])
            if uncommitted > 0:
                log(f"{uncommitted} uncommitted changes - agents should commit")
        except:
            pass
    
    log(f"Task Finder complete - Created tasks for {idle_count} idle agents")
    log("---")

if __name__ == "__main__":
    main()
