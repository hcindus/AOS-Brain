#!/usr/bin/env python3
"""
Temporal Workflow for DepotChaos - MS-Connect Follow-up Automation
Performance Supply Depot / AM HUD Supply
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict, Any
import json
import os

# Temporal imports (will work when temporal-sdk is installed)
try:
    from temporalio import workflow, activity
    from temporalio.client import Client
    from temporalio.worker import Worker
    TEMPORAL_AVAILABLE = True
except ImportError:
    TEMPORAL_AVAILABLE = False
    print("Note: temporalio not installed. Workflow definitions created for later deployment.")


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


@dataclass
class FollowUpTask:
    """Represents a follow-up task from the MS-Connect report"""
    id: str
    title: str
    description: str
    priority: Priority
    owner: str
    due_date: datetime
    status: Status
    vendor: str
    category: str  # "dealer_outreach", "demo_scheduling", "evaluation", "training"
    reminders: List[datetime]
    notes: str = ""


# Task definitions from the report
MS_CONNECT_TASKS = [
    {
        "id": "PECAN-001",
        "title": "Contact Pecan POS - West Coast Dealer Interest",
        "description": "Express interest in Pecan POS West Coast dealer program. Emphasize local presence and restaurant expertise.",
        "priority": Priority.HIGH,
        "owner": "Antonio",
        "due_days": 2,
        "vendor": "Pecan POS",
        "category": "dealer_outreach",
        "reminder_days": [1, 2]
    },
    {
        "id": "DINER-001",
        "title": "Diner Daddy Lead Program Signup",
        "description": "Enroll in Diner Daddy lead program. They do demos for you - low barrier to entry.",
        "priority": Priority.HIGH,
        "owner": "Antonio",
        "due_days": 2,
        "vendor": "Diner Daddy",
        "category": "dealer_outreach",
        "reminder_days": [1, 2]
    },
    {
        "id": "PECAN-002",
        "title": "Request Pecan POS Demo",
        "description": "Schedule comprehensive demo focusing on restaurant workflow, AI Bunny features, and hybrid data options.",
        "priority": Priority.HIGH,
        "owner": "Antonio",
        "due_days": 5,
        "vendor": "Pecan POS",
        "category": "demo_scheduling",
        "reminder_days": [3, 5]
    },
    {
        "id": "COMP-001",
        "title": "Toast Competitive Gap Analysis",
        "description": "Document current competitive positioning gaps vs Toast. Focus on pricing, features, and service.",
        "priority": Priority.HIGH,
        "owner": "Team",
        "due_days": 9,
        "vendor": "Internal",
        "category": "evaluation",
        "reminder_days": [7, 9]
    },
    {
        "id": "ARTISAN-001",
        "title": "Artisan POS Territory Verification",
        "description": "Check available territories for Artisan POS resale. Verify West Coast availability.",
        "priority": Priority.MEDIUM,
        "owner": "Antonio",
        "due_days": 10,
        "vendor": "Artisan POS",
        "category": "dealer_outreach",
        "reminder_days": [8, 10]
    },
    {
        "id": "PIONEER-001",
        "title": "Pioneer Solutions AI Partnership",
        "description": "Contact Pioneer Solutions about 'Get Book' AI solutions partnership opportunity.",
        "priority": Priority.MEDIUM,
        "owner": "Antonio",
        "due_days": 10,
        "vendor": "Pioneer Solutions",
        "category": "dealer_outreach",
        "reminder_days": [8, 10]
    },
    {
        "id": "ORDER-001",
        "title": "Order Counter Follow-up",
        "description": "Follow up on pricing pressure insights from Order Counter open forum.",
        "priority": Priority.MEDIUM,
        "owner": "Antonio",
        "due_days": 15,
        "vendor": "Order Counter",
        "category": "dealer_outreach",
        "reminder_days": [13, 15]
    },
    {
        "id": "PRICE-001",
        "title": "Competitive Pricing Matrix",
        "description": "Create pricing comparison matrix: Pecan vs Diner Daddy vs Toast vs Square.",
        "priority": Priority.MEDIUM,
        "owner": "Team",
        "due_days": 16,
        "vendor": "Internal",
        "category": "evaluation",
        "reminder_days": [14, 16]
    },
    {
        "id": "LOCAL-001",
        "title": "Spanish/French Localization Assessment",
        "description": "Evaluate localization requirements for diverse West Coast markets.",
        "priority": Priority.MEDIUM,
        "owner": "Team",
        "due_days": 20,
        "vendor": "Internal",
        "category": "evaluation",
        "reminder_days": [18, 20]
    },
    {
        "id": "HERO-001",
        "title": "Hero Consulting Partnership",
        "description": "Explore Hero Consulting partnership for workflow optimization services.",
        "priority": Priority.LOW,
        "owner": "Antonio",
        "due_days": 41,
        "vendor": "Hero Consulting",
        "category": "dealer_outreach",
        "reminder_days": [38, 41]
    },
    {
        "id": "HARDWARE-001",
        "title": "MS Cash Drawer Bundling Options",
        "description": "Evaluate hardware bundling options with MS Cash Drawer.",
        "priority": Priority.LOW,
        "owner": "Team",
        "due_days": 55,
        "vendor": "MS Cash Drawer",
        "category": "evaluation",
        "reminder_days": [52, 55]
    },
    {
        "id": "TECH-001",
        "title": "SQL Database Team Training",
        "description": "Schedule SQL database training for technical team. Support Artisan/Pecan technical requirements.",
        "priority": Priority.LOW,
        "owner": "Team",
        "due_days": 71,
        "vendor": "Internal",
        "category": "training",
        "reminder_days": [68, 71]
    },
    {
        "id": "SCAN-001",
        "title": "Scan Data Workflow Development",
        "description": "Develop scan data workflows for tobacco store and small grocery verticals.",
        "priority": Priority.LOW,
        "owner": "Team",
        "due_days": 86,
        "vendor": "Internal",
        "category": "evaluation",
        "reminder_days": [83, 86]
    }
]


class TaskManager:
    """Local task manager for when Temporal is not available"""
    
    def __init__(self, storage_path: str = "/root/.openclaw/workspace/depotchaos/tasks.json"):
        self.storage_path = storage_path
        self.tasks: Dict[str, FollowUpTask] = {}
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from persistent storage"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                for task_data in data.get('tasks', []):
                    task = FollowUpTask(
                        id=task_data['id'],
                        title=task_data['title'],
                        description=task_data['description'],
                        priority=Priority(task_data['priority']),
                        owner=task_data['owner'],
                        due_date=datetime.fromisoformat(task_data['due_date']),
                        status=Status(task_data['status']),
                        vendor=task_data['vendor'],
                        category=task_data['category'],
                        reminders=[datetime.fromisoformat(r) for r in task_data['reminders']],
                        notes=task_data.get('notes', '')
                    )
                    self.tasks[task.id] = task
    
    def _save_tasks(self):
        """Save tasks to persistent storage"""
        data = {
            'tasks': [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'priority': task.priority.value,
                    'owner': task.owner,
                    'due_date': task.due_date.isoformat(),
                    'status': task.status.value,
                    'vendor': task.vendor,
                    'category': task.category,
                    'reminders': [r.isoformat() for r in task.reminders],
                    'notes': task.notes
                }
                for task in self.tasks.values()
            ]
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def initialize_tasks(self):
        """Initialize tasks from MS_CONNECT_TASKS"""
        now = datetime.now()
        
        for task_def in MS_CONNECT_TASKS:
            due_date = now + timedelta(days=task_def['due_days'])
            reminders = [now + timedelta(days=rd) for rd in task_def['reminder_days']]
            
            task = FollowUpTask(
                id=task_def['id'],
                title=task_def['title'],
                description=task_def['description'],
                priority=task_def['priority'],
                owner=task_def['owner'],
                due_date=due_date,
                status=Status.PENDING,
                vendor=task_def['vendor'],
                category=task_def['category'],
                reminders=reminders
            )
            
            self.tasks[task.id] = task
        
        self._save_tasks()
        print(f"Initialized {len(self.tasks)} follow-up tasks")
    
    def get_tasks_by_priority(self, priority: Priority) -> List[FollowUpTask]:
        """Get tasks filtered by priority"""
        return [t for t in self.tasks.values() if t.priority == priority]
    
    def get_tasks_by_owner(self, owner: str) -> List[FollowUpTask]:
        """Get tasks filtered by owner"""
        return [t for t in self.tasks.values() if t.owner.lower() == owner.lower()]
    
    def get_tasks_by_vendor(self, vendor: str) -> List[FollowUpTask]:
        """Get tasks filtered by vendor"""
        return [t for t in self.tasks.values() if t.vendor.lower() == vendor.lower()]
    
    def get_overdue_tasks(self) -> List[FollowUpTask]:
        """Get overdue tasks"""
        now = datetime.now()
        return [t for t in self.tasks.values() if t.due_date < now and t.status != Status.COMPLETED]
    
    def get_upcoming_reminders(self, hours: int = 24) -> List[FollowUpTask]:
        """Get tasks with reminders in the next N hours"""
        now = datetime.now()
        upcoming = now + timedelta(hours=hours)
        
        result = []
        for task in self.tasks.values():
            for reminder in task.reminders:
                if now <= reminder <= upcoming and task.status != Status.COMPLETED:
                    result.append(task)
                    break
        return result
    
    def update_task_status(self, task_id: str, status: Status, notes: str = ""):
        """Update task status"""
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            if notes:
                self.tasks[task_id].notes = notes
            self._save_tasks()
            return True
        return False
    
    def print_summary(self):
        """Print task summary"""
        print("\n" + "="*60)
        print("DEPOTCHAOS - MS-CONNECT FOLLOW-UP TASKS")
        print("="*60)
        
        # By priority
        print("\n📊 BY PRIORITY:")
        for priority in [Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            tasks = self.get_tasks_by_priority(priority)
            pending = [t for t in tasks if t.status == Status.PENDING]
            icon = "🔴" if priority == Priority.HIGH else "🟡" if priority == Priority.MEDIUM else "🟢"
            print(f"  {icon} {priority.value.upper()}: {len(pending)}/{len(tasks)} pending")
        
        # Overdue
        overdue = self.get_overdue_tasks()
        if overdue:
            print(f"\n⏰ OVERDUE TASKS: {len(overdue)}")
            for task in overdue[:5]:
                days_overdue = (datetime.now() - task.due_date).days
                print(f"  - {task.id}: {task.title} ({days_overdue} days overdue)")
        
        # Upcoming reminders
        upcoming = self.get_upcoming_reminders(48)
        if upcoming:
            print(f"\n🔔 UPCOMING REMINDERS (48h): {len(upcoming)}")
            for task in upcoming[:5]:
                print(f"  - {task.id}: {task.title}")
        
        # High priority next
        high_priority = self.get_tasks_by_priority(Priority.HIGH)
        pending_high = [t for t in high_priority if t.status == Status.PENDING]
        if pending_high:
            print("\n🔥 HIGH PRIORITY - NEXT ACTIONS:")
            for task in sorted(pending_high, key=lambda x: x.due_date)[:3]:
                days_left = (task.due_date - datetime.now()).days
                print(f"  - {task.title}")
                print(f"    Due: {task.due_date.strftime('%Y-%m-%d')} ({days_left} days)")
                print(f"    Owner: {task.owner}")
        
        print("\n" + "="*60)


def generate_cron_script():
    """Generate a cron script for task reminders"""
    script = '''#!/bin/bash
# DepotChaos MS-Connect Follow-up Reminder System
# Add to crontab: */15 * * * * /root/.openclaw/workspace/depotchaos/remind.sh

PYTHON_PATH="/usr/bin/python3"
WORKFLOW_PATH="/root/.openclaw/workspace/depotchaos/temporal_workflow.py"
LOG_FILE="/var/log/depotchaos/reminders.log"

# Ensure log directory exists
mkdir -p /var/log/depotchaos

# Run reminder check
$PYTHON_PATH $WORKFLOW_PATH --check-reminders >> $LOG_FILE 2>&1

# Check for overdue tasks daily at 8am
# 0 8 * * * /root/.openclaw/workspace/depotchaos/remind.sh --overdue
'''
    
    script_path = "/root/.openclaw/workspace/depotchaos/remind.sh"
    with open(script_path, 'w') as f:
        f.write(script)
    os.chmod(script_path, 0o755)
    print(f"Generated cron script: {script_path}")
    
    # Generate systemd service for continuous monitoring
    service = '''[Unit]
Description=DepotChaos MS-Connect Follow-up Task Monitor
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/depotchaos
ExecStart=/usr/bin/python3 /root/.openclaw/workspace/depotchaos/temporal_workflow.py --daemon
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
'''
    
    service_path = "/root/.openclaw/workspace/depotchaos/depotchaos-tasks.service"
    with open(service_path, 'w') as f:
        f.write(service)
    print(f"Generated systemd service: {service_path}")
    print(f"\nTo install:")
    print(f"  sudo cp {service_path} /etc/systemd/system/")
    print(f"  sudo systemctl daemon-reload")
    print(f"  sudo systemctl enable depotchaos-tasks")
    print(f"  sudo systemctl start depotchaos-tasks")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DepotChaos MS-Connect Follow-up Workflow')
    parser.add_argument('--init', action='store_true', help='Initialize tasks from report')
    parser.add_argument('--summary', action='store_true', help='Show task summary')
    parser.add_argument('--check-reminders', action='store_true', help='Check for upcoming reminders')
    parser.add_argument('--overdue', action='store_true', help='Show overdue tasks')
    parser.add_argument('--by-priority', type=str, help='Show tasks by priority (high/medium/low)')
    parser.add_argument('--by-owner', type=str, help='Show tasks by owner')
    parser.add_argument('--by-vendor', type=str, help='Show tasks by vendor')
    parser.add_argument('--update-status', nargs=2, metavar=('TASK_ID', 'STATUS'), help='Update task status')
    parser.add_argument('--generate-scripts', action='store_true', help='Generate cron and systemd scripts')
    parser.add_argument('--daemon', action='store_true', help='Run in daemon mode (check reminders periodically)')
    
    args = parser.parse_args()
    
    manager = TaskManager()
    
    if args.init:
        manager.initialize_tasks()
    
    if args.summary:
        manager.print_summary()
    
    if args.check_reminders:
        upcoming = manager.get_upcoming_reminders(48)
        if upcoming:
            print(f"🔔 Tasks with reminders in next 48 hours:")
            for task in upcoming:
                print(f"  - {task.id}: {task.title}")
        else:
            print("No upcoming reminders")
    
    if args.overdue:
        overdue = manager.get_overdue_tasks()
        if overdue:
            print(f"⏰ Overdue tasks:")
            for task in overdue:
                print(f"  - {task.id}: {task.title}")
        else:
            print("No overdue tasks")
    
    if args.by_priority:
        try:
            priority = Priority(args.by_priority.lower())
            tasks = manager.get_tasks_by_priority(priority)
            print(f"\n{args.by_priority.upper()} priority tasks:")
            for task in tasks:
                print(f"  [{task.status.value}] {task.id}: {task.title}")
        except ValueError:
            print(f"Invalid priority: {args.by_priority}")
    
    if args.by_owner:
        tasks = manager.get_tasks_by_owner(args.by_owner)
        print(f"\nTasks for {args.by_owner}:")
        for task in tasks:
            print(f"  [{task.status.value}] {task.id}: {task.title}")
    
    if args.by_vendor:
        tasks = manager.get_tasks_by_vendor(args.by_vendor)
        print(f"\nTasks for {args.by_vendor}:")
        for task in tasks:
            print(f"  [{task.status.value}] {task.id}: {task.title}")
    
    if args.update_status:
        task_id, status_str = args.update_status
        try:
            status = Status(status_str.lower())
            if manager.update_task_status(task_id, status):
                print(f"Updated {task_id} to {status.value}")
            else:
                print(f"Task {task_id} not found")
        except ValueError:
            print(f"Invalid status: {status_str}")
    
    if args.generate_scripts:
        generate_cron_script()
    
    if args.daemon:
        print("Running in daemon mode (checking every hour)...")
        while True:
            upcoming = manager.get_upcoming_reminders(2)  # Check next 2 hours
            if upcoming:
                print(f"[{datetime.now()}] {len(upcoming)} tasks with upcoming reminders")
                for task in upcoming:
                    print(f"  - {task.title}")
            time.sleep(3600)  # Sleep for 1 hour


if __name__ == "__main__":
    import time
    main()
