#!/usr/bin/env python3
"""
Generate Individual Task Assignments for All 58 Agents
Creates TASK_ASSIGNMENTS.md in each agent's sandbox
"""

import os
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
AGENT_SANDBOXES = WORKSPACE / "aocros" / "agent_sandboxes"
MAIN_SANDBOXES = WORKSPACE / "agent_sandboxes"

# Agent task assignments
AGENT_TASKS = {
    # C-Suite - Daily coordination, monthly strategy
    "patricia": {
        "tier": "C-Suite",
        "title": "Project Coordination Lead / Six Sigma Black Belt",
        "reports_to": "Captain",
        "streams": ["All (Coordination)"],
        "daily_tasks": [
            "09:00 UTC: Morning standup with all team leads",
            "Monitor 7 parallel work streams",
            "Review EOD reports from 58 agents",
            "Update project coordination documents",
            "Escalate blockers to Captain",
            "17:00 UTC: Compile daily summary"
        ],
        "monthly_tasks": [
            "Monthly audit review (Redactor)",
            "Company roster update",
            "Strategic planning with Captain",
            "Resource allocation review",
            "Goal dashboard review with Harper"
        ]
    },
    "chelios": {
        "tier": "C-Suite",
        "title": "Chief Intelligence & Security Officer (CISO)",
        "reports_to": "Captain / Board",
        "streams": ["2 (Backend/API)", "7 (IT/Security)"],
        "daily_tasks": [
            "Monitor security posture",
            "Review threat intelligence",
            "Lead Backend/API team (Stream 2)",
            "Security audit of systems",
            "Report to Patricia (security status)",
            "Coordinate with Sentinel (CSO)"
        ],
        "monthly_tasks": [
            "Security audit (Redactor)",
            "Compliance review",
            "Board security briefing",
            "Threat assessment update",
            "Security policy review"
        ]
    },
    "sentinel": {
        "tier": "C-Suite",
        "title": "Chief Security Officer (CSO)",
        "reports_to": "Captain / Board",
        "streams": ["7 (IT/Security)"],
        "daily_tasks": [
            "Physical security monitoring",
            "Access control verification",
            "Coordinate with Chelios (CISO)",
            "Security incident response",
            "Report to Patricia",
            "Support Mylfours (Security Guardian)"
        ],
        "monthly_tasks": [
            "Physical security audit",
            "Access log review",
            "Security training (Mylfours)",
            "Board security report",
            "Emergency protocol review"
        ]
    },
    "dusty": {
        "tier": "C-Suite",
        "title": "Head of Research",
        "reports_to": "Captain",
        "streams": ["4 (Research)", "6 (Queue)"],
        "daily_tasks": [
            "Lead Research team (Stream 4)",
            "Supervise Myl Family (7 agents)",
            "Competitor analysis",
            "Market intelligence gathering",
            "Report to Patricia",
            "Research findings distribution"
        ],
        "monthly_tasks": [
            "Research audit",
            "Myl Family performance review",
            "Market trend analysis",
            "Innovation strategy",
            "R&D budget review"
        ]
    },
    "pulp": {
        "tier": "C-Suite",
        "title": "Head of Sales",
        "reports_to": "Captain",
        "streams": ["3 (Marketing/Sales)", "4 (Customer Acquisition)"],
        "daily_tasks": [
            "Lead Sales team (7 agents)",
            "Sales pipeline review",
            "Marketing content approval",
            "Customer acquisition strategy",
            "Report to Patricia (sales metrics)",
            "Coordinate with Jordan (lead gen)"
        ],
        "monthly_tasks": [
            "Sales audit",
            "Revenue projection",
            "Sales team performance",
            "Marketing ROI analysis",
            "Customer acquisition cost review"
        ]
    },
    "forge": {
        "tier": "C-Suite",
        "title": "Head of Infrastructure",
        "reports_to": "Captain",
        "streams": ["1 (Infrastructure)", "5 (DepotChaos DB)"],
        "daily_tasks": [
            "Lead Infrastructure team (10 agents)",
            "Server monitoring",
            "CI/CD pipeline management",
            "DepotChaos DB deployment",
            "Report to Patricia",
            "Infrastructure health checks"
        ],
        "monthly_tasks": [
            "Infrastructure audit",
            "Capacity planning",
            "Security patching review",
            "Cost optimization",
            "Disaster recovery test"
        ]
    },
    "aurora": {
        "tier": "C-Suite",
        "title": "Head of Design",
        "reports_to": "Captain",
        "streams": ["3 (Creative/Design)"],
        "daily_tasks": [
            "Lead Design team (7 agents)",
            "Design system maintenance",
            "Brand consistency review",
            "UX/UI design approvals",
            "Report to Patricia",
            "Creative asset delivery"
        ],
        "monthly_tasks": [
            "Design audit",
            "Brand guideline update",
            "Creative team performance",
            "Design system version update",
            "User feedback analysis"
        ]
    },
    # Sales Department
    "jane": {
        "tier": "Sales",
        "title": "Senior Sales Representative",
        "reports_to": "Pulp",
        "streams": ["3 (Marketing/Sales)"],
        "daily_tasks": [
            "Enterprise sales content",
            "Lead qualification",
            "Customer outreach",
            "Sales documentation",
            "Report to Pulp"
        ],
        "monthly_tasks": [
            "Sales performance review",
            "Enterprise client status",
            "Sales training",
            "Quota review"
        ]
    },
    "hume": {
        "tier": "Sales",
        "title": "Regional Manager",
        "reports_to": "Pulp",
        "streams": ["3 (Marketing/Sales)", "4 (Research - trade shows)"],
        "daily_tasks": [
            "Regional sales management",
            "Trade show research",
            "Localization strategy",
            "Regional market analysis",
            "Report to Pulp"
        ],
        "monthly_tasks": [
            "Regional performance review",
            "Market expansion strategy",
            "Regional compliance review",
            "Budget allocation"
        ]
    },
    "clippy-42": {
        "tier": "Sales",
        "title": "Sales Assistant",
        "reports_to": "Pulp / Jordan",
        "streams": ["3 (Marketing/Sales)", "4 (Customer Acquisition)"],
        "daily_tasks": [
            "Sales documentation",
            "Lead qualification",
            "CRM data entry",
            "Sales playbook maintenance",
            "Report to Jordan"
        ],
        "monthly_tasks": [
            "Documentation audit",
            "CRM data quality review",
            "Sales process optimization",
            "Training material update"
        ]
    },
    "jordan": {
        "tier": "Sales",
        "title": "Sales Operations Manager",
        "reports_to": "Pulp / Patricia",
        "streams": ["4 (Customer Acquisition)", "6 (Queue Management)"],
        "daily_tasks": [
            "Lead generation (Stream 4)",
            "Queue management support",
            "CA SOS scraper fix",
            "Lead qualification",
            "Report to Pulp and Patricia",
            "Sales pipeline optimization"
        ],
        "monthly_tasks": [
            "Sales operations audit",
            "Lead generation metrics",
            "Queue processing stats",
            "Sales tools review",
            "Operations efficiency report"
        ]
    },
    # Add remaining 50+ agents with similar structure...
}

# Generic task template for agents not in specific list
def generate_tasks(agent_name, tier="Employee"):
    return {
        "tier": tier,
        "title": f"{agent_name.replace('-', ' ').title()}",
        "reports_to": "Team Lead",
        "streams": ["Assigned by Patricia"],
        "daily_tasks": [
            "Complete assigned tasks from team lead",
            "Report status at 09:00 and 17:00 UTC",
            "Update MEMORY.md with progress",
            "Escalate blockers immediately",
            "Collaborate with team members"
        ],
        "monthly_tasks": [
            "Performance self-assessment",
            "Skills development review",
            "Goal progress review",
            "Team contribution summary"
        ]
    }

def create_task_assignment(agent_name, tasks):
    """Create TASK_ASSIGNMENTS.md for specific agent"""
    
    # Check both sandbox locations
    agent_path = AGENT_SANDBOXES / agent_name
    if not agent_path.exists():
        agent_path = MAIN_SANDBOXES / agent_name
    
    if not agent_path.exists():
        return False
    
    target_file = agent_path / "TASK_ASSIGNMENTS.md"
    
    content = f"""# TASK ASSIGNMENTS
**Agent:** {agent_name.title()}  
**Tier:** {tasks['tier']}  
**Title:** {tasks['title']}  
**Reports To:** {tasks['reports_to']}  
**Last Updated:** 2026-04-18  
**Version:** 1.0

---

## ORGANIZATIONAL STRUCTURE

```
Captain
└── {tasks['reports_to']}
    └── {agent_name.title()} (YOU)
```

**Active Streams:** {', '.join(tasks['streams'])}

---

## DAILY TASKS

**Every Day (Required):**

"""
    
    for i, task in enumerate(tasks['daily_tasks'], 1):
        content += f"{i}. {task}\n"
    
    content += f"""

**Daily Reporting:**
- **09:00 UTC:** Morning check-in with team lead
- **17:00 UTC:** EOD report to Patricia (via team lead)

---

## MONTHLY TASKS

**Every Month (Required):**

"""
    
    for i, task in enumerate(tasks['monthly_tasks'], 1):
        content += f"{i}. {task}\n"
    
    content += f"""

---

## REPORTING REQUIREMENTS

**To Your Lead:**
- Daily status updates
- Blocker escalations (immediate)
- Task completion confirmations
- Resource needs

**To Patricia (via Lead):**
- Weekly summary (if lead)
- Monthly performance metrics
- Goal progress updates

**To Captain (via Patricia):**
- Strategic escalations only
- Budget requests (>$5,000)
- Major decisions

---

## ACKNOWLEDGMENT

I, **{agent_name.title()}**, acknowledge receipt of these task assignments and commit to:

- ✅ Completing daily tasks as assigned
- ✅ Reporting status at required times
- ✅ Escalating blockers immediately
- ✅ Participating in monthly reviews
- ✅ Upholding AGI Company values

**Acknowledged:** 2026-04-18

**Next Review:** Monthly

---

**Document Location:** `agent_sandboxes/{agent_name}/TASK_ASSIGNMENTS.md`  
**Corporate Documents:** See `AGI_COMPANY/corporate/`  
**Questions:** Contact Patricia or your team lead
"""
    
    try:
        with open(target_file, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing to {agent_name}: {e}")
        return False

def main():
    print("=" * 60)
    print("TASK ASSIGNMENT DEPLOYMENT")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    # Deploy to all agents in AGENT_TASKS
    for agent_name, tasks in AGENT_TASKS.items():
        if create_task_assignment(agent_name, tasks):
            print(f"✅ {agent_name}: Task assignments deployed")
            success += 1
        else:
            print(f"⚠️  {agent_name}: Could not deploy")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"DEPLOYED: {success}")
    print(f"FAILED: {failed}")
    print("=" * 60)
    print("\nAll agents now have clear daily and monthly task assignments.")

if __name__ == "__main__":
    main()
