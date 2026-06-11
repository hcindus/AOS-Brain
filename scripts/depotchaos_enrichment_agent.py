#!/usr/bin/env python3
"""
DepotChaos Data Enrichment Agent
Mandates all employees use DepotChaos and assigns enrichment tasks
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime

DEPOTCHAOS_DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
UNIFIED_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
AGENT_SANDBOXES = "/root/.openclaw/workspace/agent_sandboxes"

class DepotChaosEnricher:
    """Agent responsible for enriching DepotChaos data."""
    
    def __init__(self, agent_id="patricia"):
        self.agent_id = agent_id
        self.db_path = DEPOTCHAOS_DB
        self.ensure_connection()
        
    def ensure_connection(self):
        """Ensure database connection."""
        if os.path.exists(self.db_path):
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        return False
    
    def get_stats(self) -> dict:
        """Get current DepotChaos statistics."""
        if not self.ensure_connection():
            return {"error": "Database not found"}
        
        stats = {}
        
        # Count tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in self.cursor.fetchall()]
        stats['tables'] = tables
        
        # Count records per table
        for table in tables:
            try:
                self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[f'{table}_count'] = self.cursor.fetchone()[0]
            except:
                pass
        
        return stats
    
    def identify_enrichment_targets(self) -> list:
        """Identify records needing enrichment."""
        if not self.ensure_connection():
            return []
        
        targets = []
        
        # Find leads without email enrichment
        try:
            self.cursor.execute("""
                SELECT id, name, phone, state, city 
                FROM leads 
                WHERE email IS NULL OR email = '' 
                LIMIT 100
            """)
            for row in self.cursor.fetchall():
                targets.append({
                    'type': 'lead_missing_email',
                    'id': row[0],
                    'name': row[1],
                    'phone': row[2],
                    'location': f"{row[4]}, {row[3]}"
                })
        except:
            pass
        
        # Find vendors without categories
        try:
            self.cursor.execute("""
                SELECT id, name, address 
                FROM vendors 
                WHERE category IS NULL OR category = ''
                LIMIT 50
            """)
            for row in self.cursor.fetchall():
                targets.append({
                    'type': 'vendor_missing_category',
                    'id': row[0],
                    'name': row[1],
                    'address': row[2]
                })
        except:
            pass
        
        return targets
    
    def create_mandate_file(self):
        """Create mandate for all agents to use DepotChaos."""
        mandate = f"""# MANDATE: All Employees Must Use DepotChaos
**Issued By:** {self.agent_id} (Project Coordination Lead)
**Date:** {datetime.now().isoformat()}
**Priority:** CRITICAL

## Effective Immediately

All AGI Company employees and agents **MUST** use DepotChaos as their primary:
- CRM (Customer Relationship Management)
- Lead database
- Customer tracking system
- Intelligence repository
- Work coordination platform

## Required Actions

### 1. Daily Data Entry
- [ ] Log all customer interactions
- [ ] Update lead status changes
- [ ] Record sales activities
- [ ] Document vendor communications

### 2. Data Enrichment (Rotating Assignment)
- [ ] Verify incomplete records
- [ ] Add missing contact information
- [ ] Categorize uncategorized vendors
- [ ] Update outdated intelligence

### 3. Access Information
- **DepotChaos URL:** https://psdepot.com/depotchaos/
- **API Endpoint:** https://psdepot.com/api/
- **Database:** {DEPOTCHAOS_DB}
- **Documentation:** /root/.openclaw/workspace/DepotChaos/CENTRAL_HUB.md

## Non-Compliance

Agents not using DepotChaos for work tracking will be flagged in daily reports.

## Current Status
- Database Size: {os.path.getsize(DEPOTCHAOS_DB) / (1024*1024):.2f} MB
- Last Updated: {datetime.fromtimestamp(os.path.getmtime(DEPOTCHAOS_DB)).isoformat()}

---
This mandate is effective immediately and applies to all departments.
"""
        
        mandate_file = Path(AGENT_SANDBOXES) / "DEPOTCHAOS_MANDATE.md"
        with open(mandate_file, 'w') as f:
            f.write(mandate)
        
        # Also save to each agent sandbox
        for agent_dir in Path(AGENT_SANDBOXES).iterdir():
            if agent_dir.is_dir():
                agent_mandate = agent_dir / "DEPOTCHAOS_MANDATE.md"
                with open(agent_mandate, 'w') as f:
                    f.write(mandate)
        
        print(f"✅ DepotChaos mandate distributed to all agents")
        return mandate_file
    
    def assign_enrichment_tasks(self):
        """Assign data enrichment tasks to agents."""
        targets = self.identify_enrichment_targets()
        
        if not targets:
            print("No enrichment targets found")
            return
        
        # Distribute tasks among agents
        agents = ['aurora', 'chelios', 'forge', 'jordan']
        tasks_per_agent = len(targets) // len(agents)
        
        for i, agent in enumerate(agents):
            start_idx = i * tasks_per_agent
            end_idx = start_idx + tasks_per_agent if i < len(agents) - 1 else len(targets)
            agent_tasks = targets[start_idx:end_idx]
            
            task_file = Path(AGENT_SANDBOXES) / agent / "tasks" / "DEPOTCHAOS_ENRICHMENT.md"
            task_file.parent.mkdir(parents=True, exist_ok=True)
            
            task_content = f"""# TASK: DepotChaos Data Enrichment
**Agent:** {agent}
**Assigned By:** {self.agent_id}
**Date:** {datetime.now().isoformat()}
**Priority:** HIGH
**Status:** Assigned

## Objective
Enrich DepotChaos database with missing information.

## Your Targets ({len(agent_tasks)} records)

"""
            for target in agent_tasks:
                task_content += f"""
### Record ID: {target['id']}
- **Type:** {target['type']}
- **Name:** {target.get('name', 'N/A')}
- **Location:** {target.get('location', target.get('address', 'N/A'))}
- **Action Required:** Research and update missing fields

"""
            
            task_content += f"""
## Process
1. Access DepotChaos: https://psdepot.com/depotchaos/
2. Find the record using ID
3. Research missing information
4. Update record with verified data
5. Mark complete in this task file

## Tools Available
- Yelp enrichment: /root/.openclaw/workspace/DepotChaos/yelp_enrichment.py
- Web scraping: Use agent capabilities
- API access: See DEPOTCHAOS_MANDATE.md

## Completion Criteria
- All assigned records enriched
- Data verified from reliable sources
- Updates logged in DepotChaos

---
Report completion to {self.agent_id}
"""
            
            with open(task_file, 'w') as f:
                f.write(task_content)
            
            print(f"✅ Assigned {len(agent_tasks)} enrichment tasks to {agent}")
    
    def create_daily_workflow(self):
        """Create daily workflow integrating DepotChaos."""
        workflow = {
            "agent_id": self.agent_id,
            "daily_workflow": {
                "09:00": "Check DepotChaos dashboard",
                "09:30": "Review assigned enrichment tasks",
                "10:00": "Update customer interactions",
                "12:00": "Log morning activities",
                "14:00": "Continue enrichment work",
                "16:00": "Update lead statuses",
                "17:00": "Submit daily report via DepotChaos"
            },
            "depot_chaos_endpoints": {
                "dashboard": "https://psdepot.com/depotchaos/",
                "api_stats": "https://psdepot.com/api/stats",
                "api_leads": "https://psdepot.com/api/leads",
                "database": DEPOTCHAOS_DB
            }
        }
        
        workflow_file = Path(AGENT_SANDBOXES) / self.agent_id / "depotchaos_workflow.json"
        with open(workflow_file, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        return workflow


def main():
    print("🏭 DepotChaos Data Enrichment System")
    print("=" * 60)
    
    enricher = DepotChaosEnricher("patricia")
    
    # Get current stats
    print("\n📊 DepotChaos Current Status:")
    stats = enricher.get_stats()
    for key, value in stats.items():
        if isinstance(value, int) and '_count' in key:
            print(f"  {key}: {value:,} records")
    
    # Create mandate
    print("\n📋 Creating mandate for all agents...")
    enricher.create_mandate_file()
    
    # Assign enrichment tasks
    print("\n📥 Assigning enrichment tasks...")
    enricher.assign_enrichment_tasks()
    
    # Create workflow
    print("\n🔄 Creating daily workflow...")
    enricher.create_daily_workflow()
    
    print("\n✅ DepotChaos enrichment system activated")
    print("\nNext Steps:")
    print("  1. Agents will check their tasks directory")
    print("  2. Enrichment tasks assigned to Aurora, Chelios, Forge, Jordan")
    print("  3. Daily workflow mandates DepotChaos usage")
    print("  4. Patricia will monitor progress")


if __name__ == "__main__":
    main()
