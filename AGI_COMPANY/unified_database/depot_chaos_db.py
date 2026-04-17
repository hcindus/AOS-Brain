#!/usr/bin/env python3
"""
DepotChaos Unified Database
Central database for AGI Company agents, departments, and operations
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

class DepotChaosDB:
    """Unified database for AGI Company operations"""
    
    DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
    
    def __init__(self):
        self.db_path = Path(self.DB_PATH)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()
        print("🏛️ DepotChaos Unified Database initialized")
    
    def init_schema(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        # Departments table
        c.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                head_agent TEXT,
                parent_dept TEXT,
                status TEXT DEFAULT 'active',
                priority INTEGER DEFAULT 5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Agents table
        c.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                department_id TEXT,
                role TEXT,
                level TEXT DEFAULT 'employee',
                status TEXT DEFAULT 'active',
                schedule TEXT,
                last_checkin TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id)
            )
        ''')
        
        # Tasks table
        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                agent_id TEXT,
                department_id TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'normal',
                due_date TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (agent_id) REFERENCES agents(id),
                FOREIGN KEY (department_id) REFERENCES departments(id)
            )
        ''')
        
        # Leads/Opportunities table (from scraper)
        c.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id TEXT PRIMARY KEY,
                company_name TEXT,
                county TEXT,
                entity_number TEXT,
                sos_url TEXT,
                status TEXT DEFAULT 'new',
                assigned_agent TEXT,
                assigned_dept TEXT,
                enrichment_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assigned_agent) REFERENCES agents(id),
                FOREIGN KEY (assigned_dept) REFERENCES departments(id)
            )
        ''')
        
        # Schedule table
        c.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT,
                task_type TEXT,
                cron_expression TEXT,
                last_run TIMESTAMP,
                next_run TIMESTAMP,
                enabled BOOLEAN DEFAULT 1,
                FOREIGN KEY (agent_id) REFERENCES agents(id)
            )
        ''')
        
        # Check-ins table
        c.execute('''
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT,
                department_id TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                blockers TEXT,
                needs TEXT,
                FOREIGN KEY (agent_id) REFERENCES agents(id),
                FOREIGN KEY (department_id) REFERENCES departments(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def seed_departments(self):
        """Seed initial departments"""
        departments = [
            # APEX (Executive Team)
            ("apex", "APEX - Executive Office", "qora", None, "active", 1),
            ("security", "Security Department", "sentinel", None, "active", 1),
            ("engineering", "Engineering", "spindle", None, "active", 2),
            ("operations", "Operations", "ralph", None, "active", 2),
            ("finance", "Finance", "ledger-9", None, "active", 2),
            ("marketing", "Marketing", "velum", None, "active", 3),
            ("sales", "Sales", "pulp", None, "active", 3),
            ("hr", "Human Resources", "feelix", None, "active", 3),
            ("supply_chain", "Supply Chain", "fiber", None, "active", 4),
            ("legal", "Legal", "redactor", None, "active", 4),
            ("innovation", "Innovation Lab", "mill", None, "active", 4),
            ("warehouse", "Warehouse Operations", "boxtron", None, "active", 5),
            ("dark_factory", "Dark Factory", "forge", None, "active", 5),
        ]
        
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.executemany('''
            INSERT OR IGNORE INTO departments (id, name, head_agent, parent_dept, status, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', departments)
        conn.commit()
        conn.close()
        print(f"✅ Seeded {len(departments)} departments")
    
    def seed_agents(self):
        """Seed initial agents"""
        agents = [
            # APEX Team (Priority 1)
            ("qora", "QORA", "apex", "CEO", "executive"),
            ("ralph", "RALPH", "operations", "Chief of Staff", "executive"),
            ("spindle", "SPINDLE", "engineering", "CTO", "executive"),
            ("sentinel", "SENTINEL", "security", "CSO", "executive"),
            ("ledger-9", "LEDGER-9", "finance", "CFO", "executive"),
            ("velum", "VELUM", "marketing", "Chief Brand Officer", "executive"),
            ("feelix", "FEELIX", "hr", "HR Director", "executive"),
            
            # Department Heads (Priority 2)
            ("alpha-9", "ALPHA-9", "engineering", "CIO", "director"),
            ("mill", "MILL", "innovation", "Chief Innovation Officer", "director"),
            ("fiber", "FIBER", "supply_chain", "Head of Supply Chain", "director"),
            ("redactor", "REDACTOR", "legal", "General Counsel", "director"),
            ("boxtron", "BOXTRON", "warehouse", "Warehouse Supervisor", "director"),
            ("hume", "HUME", "warehouse", "Regional Manager", "manager"),
            ("pulp", "PULP", "sales", "Head of Sales", "director"),
            
            # Key Employees (Priority 3)
            ("scribble", "SCRIBBLE", "marketing", "Content Strategist", "employee"),
            ("clippy-42", "CLIPPY-42", "warehouse", "Assistant to Regional Manager", "employee"),
            ("jane", "JANE", "sales", "Senior Sales Rep", "employee"),
            ("pipeline", "PIPELINE", "engineering", "Integrations", "employee"),
            ("stacktrace", "STACKTRACE", "engineering", "Debugging", "employee"),
            ("bugcatcher", "BUGCATCHER", "engineering", "QA", "employee"),
            ("taptap", "TAPTAP", "engineering", "UX", "employee"),
            
            # Specialized Agents
            ("miles", "MILES", "apex", "Autonomous Operations Engine", "special"),
            ("jordan", "JORDAN", "engineering", "Systems Engineer", "special"),
            ("patricia", "PATRICIA", "dark_factory", "Quality Control", "special"),
            ("forge", "FORGE", "dark_factory", "Factory Manager", "special"),
        ]
        
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.executemany('''
            INSERT OR IGNORE INTO agents (id, name, department_id, role, level)
            VALUES (?, ?, ?, ?, ?)
        ''', agents)
        conn.commit()
        conn.close()
        print(f"✅ Seeded {len(agents)} agents")
    
    def import_leads(self):
        """Import leads from scraper data"""
        leads_file = Path("/root/.openclaw/workspace/data/scraper/enriched_leads_20260417_0344.json")
        if not leads_file.exists():
            print("⚠️ No leads file found")
            return
        
        with open(leads_file) as f:
            data = json.load(f)
        
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        for i, lead in enumerate(data.get('results', [])):
            lead_id = f"LEAD-{datetime.now().strftime('%Y%m%d')}-{i:04d}"
            c.execute('''
                INSERT OR IGNORE INTO leads 
                (id, company_name, county, entity_number, sos_url, status, enrichment_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                lead_id,
                lead.get('name'),
                lead.get('county'),
                lead.get('entity_number'),
                lead.get('sos_url'),
                lead.get('status', 'new'),
                json.dumps(lead)
            ))
        
        conn.commit()
        conn.close()
        print(f"✅ Imported {len(data.get('results', []))} leads")


def main():
    db = DepotChaosDB()
    db.seed_departments()
    db.seed_agents()
    db.import_leads()
    print("\n🏛️ DepotChaos Unified Database ready!")


if __name__ == "__main__":
    main()
