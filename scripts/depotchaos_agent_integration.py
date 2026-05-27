#!/usr/bin/env python3
"""
Agent DepotChaos Integration Module
Ensures all agents use DepotChaos for their daily work
"""

import json
import os
from datetime import datetime
from pathlib import Path

AGENT_SANDBOXES = Path("/root/.openclaw/workspace/agent_sandboxes")
DEPOTCHAOS_TASKS = [
    {
        "title": "Daily DepotChaos Check-in",
        "description": "Log into DepotChaos and check dashboard for updates",
        "frequency": "daily",
        "time": "09:00",
        "priority": "HIGH"
    },
    {
        "title": "Update Customer Interactions",
        "description": "Log all customer calls, emails, and meetings in DepotChaos",
        "frequency": "daily",
        "time": "ongoing",
        "priority": "CRITICAL"
    },
    {
        "title": "Enrich Vendor Data",
        "description": "Research and update missing vendor information (phone, email, website)",
        "frequency": "weekly",
        "time": "as assigned",
        "priority": "NORMAL"
    },
    {
        "title": "Lead Status Updates",
        "description": "Update lead statuses and add notes in DepotChaos CRM",
        "frequency": "daily",
        "time": "16:00",
        "priority": "HIGH"
    },
    {
        "title": "Submit Daily Report",
        "description": "Record daily activities and outcomes in DepotChaos",
        "frequency": "daily",
        "time": "17:00",
        "priority": "CRITICAL"
    }
]

AGENT_SPECIFIC_TASKS = {
    "patricia": [
        {"title": "Review DepotChaos Metrics", "description": "Monitor data quality and agent usage", "frequency": "daily"}
    ],
    "jordan": [
        {"title": "Sales Pipeline Update", "description": "Update sales pipeline in DepotChaos", "frequency": "daily"}
    ],
    "pulp": [
        {"title": "Lead Assignment", "description": "Assign new leads to sales reps via DepotChaos", "frequency": "daily"}
    ],
    "dusty": [
        {"title": "Intelligence Review", "description": "Review and categorize intelligence data", "frequency": "daily"}
    ],
    "sentinel": [
        {"title": "Security Audit", "description": "Review access logs and security events", "frequency": "daily"}
    ]
}


def create_depotchaos_task_file(agent_id: str):
    """Create DepotChaos task file for an agent."""
    
    task_content = f"""# DepotChaos Work Tasks
**Agent:** {agent_id}
**Created:** {datetime.now().isoformat()}
**Mandate:** ALL work must be tracked in DepotChaos

## DepotChaos Access
- **URL:** https://psdepot.com/depotchaos/
- **API:** https://psdepot.com/api/
- **Documentation:** /root/.openclaw/workspace/DepotChaos/CENTRAL_HUB.md

## Daily Requirements

### Must Complete Every Day:

"""
    
    # Add standard tasks
    for task in DEPOTCHAOS_TASKS:
        task_content += f"""
#### {task['title']} [{task['priority']}]
- **Frequency:** {task['frequency']}
- **Time:** {task['time']}
- **Description:** {task['description']}
- [ ] Completed

"""
    
    # Add agent-specific tasks
    if agent_id in AGENT_SPECIFIC_TASKS:
        task_content += "## Department-Specific Tasks\n\n"
        for task in AGENT_SPECIFIC_TASKS[agent_id]:
            task_content += f"""
#### {task['title']}
- **Frequency:** {task['frequency']}
- **Description:** {task['description']}
- [ ] Completed

"""
    
    task_content += f"""
## Data Enrichment Assignment

You may be assigned specific records to enrich. Check:
- `/root/.openclaw/workspace/DepotChaos/enrichment_queue/`
- DepotChaos dashboard for flagged records

## Tools Available

- **Yelp Enrichment:** `python3 /root/.openclaw/workspace/DepotChaos/yelp_enrichment.py`
- **Web Scrapers:** Agent skills
- **Database Direct:** `{agent_id}@psdepot.com` access

## Reporting

Submit daily progress via:
1. DepotChaos activity log
2. Update this task file
3. Report blockers to Patricia

## Compliance

⚠️ **WARNING:** Agents not using DepotChaos for work tracking will be flagged.
All customer interactions, lead updates, and sales activities MUST be logged.

---
**Last Updated:** {datetime.now().isoformat()}
**Next Review:** Daily
"""
    
    return task_content


def distribute_to_all_agents():
    """Distribute DepotChaos tasks to all agents."""
    
    print("📦 Distributing DepotChaos tasks to all agents...")
    
    distributed = 0
    for agent_dir in AGENT_SANDBOXES.iterdir():
        if agent_dir.is_dir():
            agent_id = agent_dir.name
            
            # Create tasks directory if needed
            tasks_dir = agent_dir / "tasks"
            tasks_dir.mkdir(exist_ok=True)
            
            # Write task file
            task_file = tasks_dir / "DEPOTCHAOS_MANDATORY.md"
            task_content = create_depotchaos_task_file(agent_id)
            
            with open(task_file, 'w') as f:
                f.write(task_content)
            
            distributed += 1
            print(f"  ✅ {agent_id}")
    
    return distributed


def create_workflow_integration():
    """Create workflow that integrates DepotChaos into agent operations."""
    
    workflow = {
        "system": "DepotChaos",
        "version": "1.0",
        "integration_points": {
            "perception": "Check DepotChaos for assigned leads/tasks",
            "cognition": "Query DepotChaos for customer history before decisions",
            "action": "Log all actions in DepotChaos activity log",
            "memory": "Store outcomes in DepotChaos database",
            "reward": "Track performance metrics from DepotChaos reports"
        },
        "daily_routine": {
            "09:00": "Login to DepotChaos, check assignments",
            "09:30": "Review customer history before outreach",
            "10:00-16:00": "Work with DepotChaos logging active",
            "16:30": "Update lead statuses",
            "17:00": "Submit daily report, log activities"
        },
        "mandatory_logging": [
            "Customer calls",
            "Email sent/received",
            "Lead status changes",
            "Sales closed",
            "Vendor interactions",
            "Intelligence gathered"
        ]
    }
    
    workflow_file = Path("/root/.openclaw/workspace/DEPOTCHAOS_WORKFLOW.json")
    with open(workflow_file, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    return workflow_file


def main():
    print("🏭 DEPOTCHAOS AGENT INTEGRATION")
    print("=" * 60)
    print()
    
    # Distribute tasks
    count = distribute_to_all_agents()
    print(f"\n✅ Distributed DepotChaos tasks to {count} agents")
    
    # Create workflow
    workflow_file = create_workflow_integration()
    print(f"✅ Created workflow integration: {workflow_file}")
    
    print()
    print("📋 Summary:")
    print("  - All agents have DepotChaos mandate in tasks/")
    print("  - Daily workflow requires DepotChaos usage")
    print("  - Data enrichment tasks assigned")
    print("  - Performance tracked via DepotChaos")
    
    print()
    print("🔔 Reminder for agents:")
    print("  1. Check tasks/DEPOTCHAOS_MANDATORY.md daily")
    print("  2. Log ALL work in DepotChaos")
    print("  3. Use https://psdepot.com/depotchaos/")
    print("  4. Report blockers to Patricia")


if __name__ == "__main__":
    main()
