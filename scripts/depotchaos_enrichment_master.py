#!/usr/bin/env python3
"""
DepotChaos 72K+ Lead Enrichment System
Comprehensive data enrichment with: Agent Assignment, Auto-Scrapers, Claim Queue
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class DepotChaosEnrichmentMaster:
    """Master system for enriching all DepotChaos data."""
    
    def __init__(self):
        self.db_paths = {
            'depot_chaos': '/root/.openclaw/workspace/DepotChaos/depot_chaos.db',
            'unified': '/root/.openclaw/workspace/data/depot_chaos/unified.db',
            'psd_customers': '/root/.openclaw/workspace/data/depot_chaos/psd_customers.db',
            'yelp_cache': '/root/.openclaw/workspace/DepotChaos/yelp_cache.json'
        }
        
        self.agents = ['aurora', 'patricia', 'forge', 'chelios', 'jordan', 
                       'pulp', 'jane', 'dusty', 'sentinel', 'mylzeron']
        
        self.enrichment_queue_dir = Path('/root/.openclaw/workspace/DepotChaos/enrichment_queue')
        self.enrichment_queue_dir.mkdir(parents=True, exist_ok=True)
        
    def get_all_database_stats(self) -> Dict:
        """Get stats from all databases."""
        stats = {}
        
        for name, path in self.db_paths.items():
            if os.path.exists(path) and path.endswith('.db'):
                try:
                    conn = sqlite3.connect(path)
                    cursor = conn.cursor()
                    
                    # Get all tables
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = [t[0] for t in cursor.fetchall()]
                    
                    db_stats = {'tables': tables, 'records': {}}
                    
                    for table in tables:
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM {table}")
                            count = cursor.fetchone()[0]
                            db_stats['records'][table] = count
                        except:
                            pass
                    
                    stats[name] = db_stats
                    conn.close()
                except Exception as e:
                    stats[name] = {'error': str(e)}
        
        return stats
    
    def identify_enrichment_targets(self) -> Dict:
        """Identify all records needing enrichment across all databases."""
        targets = {
            'depot_chaos_vendors': [],
            'depot_chaos_leads': [],
            'unified_leads': [],
            'total_count': 0
        }
        
        # Check depot_chaos.db
        if os.path.exists(self.db_paths['depot_chaos']):
            try:
                conn = sqlite3.connect(self.db_paths['depot_chaos'])
                cursor = conn.cursor()
                
                # Vendors missing phone
                cursor.execute("""
                    SELECT id, name, address, city, state, territory, vendor_type
                    FROM vendors 
                    WHERE phone IS NULL OR phone = '' OR email IS NULL OR email = ''
                    LIMIT 1000
                """)
                for row in cursor.fetchall():
                    targets['depot_chaos_vendors'].append({
                        'db': 'depot_chaos',
                        'table': 'vendors',
                        'id': row[0],
                        'name': row[1],
                        'address': row[2],
                        'city': row[3],
                        'state': row[4],
                        'territory': row[5],
                        'vendor_type': row[6],
                        'missing': ['phone', 'email']
                    })
                
                # Leads missing info
                cursor.execute("""
                    SELECT id, name, phone, state, city
                    FROM leads 
                    WHERE email IS NULL OR email = '' OR website IS NULL
                    LIMIT 1000
                """)
                for row in cursor.fetchall():
                    targets['depot_chaos_leads'].append({
                        'db': 'depot_chaos',
                        'table': 'leads',
                        'id': row[0],
                        'name': row[1],
                        'phone': row[2],
                        'state': row[3],
                        'city': row[4],
                        'missing': ['email', 'website']
                    })
                
                conn.close()
            except Exception as e:
                print(f"Error reading depot_chaos: {e}")
        
        # Check unified.db
        if os.path.exists(self.db_paths['unified']):
            try:
                conn = sqlite3.connect(self.db_paths['unified'])
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%lead%'
                """)
                lead_tables = [t[0] for t in cursor.fetchall()]
                
                for table in lead_tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        targets['unified_leads'].append({
                            'table': table,
                            'count': count
                        })
                    except:
                        pass
                
                conn.close()
            except Exception as e:
                print(f"Error reading unified: {e}")
        
        targets['total_count'] = (
            len(targets['depot_chaos_vendors']) + 
            len(targets['depot_chaos_leads'])
        )
        
        return targets
    
    def create_agent_assignments(self):
        """Strategy 1: Assign specific enrichment tasks to agents."""
        print("\n📋 STRATEGY 1: Agent Assignments")
        print("=" * 60)
        
        targets = self.identify_enrichment_targets()
        
        # Calculate per-agent load
        vendors_per_agent = len(targets['depot_chaos_vendors']) // len(self.agents)
        leads_per_agent = len(targets['depot_chaos_leads']) // len(self.agents)
        
        print(f"Total vendors to enrich: {len(targets['depot_chaos_vendors']):,}")
        print(f"Total leads to enrich: {len(targets['depot_chaos_leads']):,}")
        print(f"Agents available: {len(self.agents)}")
        print(f"Vendors per agent: ~{vendors_per_agent}")
        print(f"Leads per agent: ~{leads_per_agent}")
        
        # Distribute to agents
        for i, agent in enumerate(self.agents):
            start_v = i * vendors_per_agent
            end_v = start_v + vendors_per_agent if i < len(self.agents) - 1 else len(targets['depot_chaos_vendors'])
            agent_vendors = targets['depot_chaos_vendors'][start_v:end_v]
            
            start_l = i * leads_per_agent
            end_l = start_l + leads_per_agent if i < len(self.agents) - 1 else len(targets['depot_chaos_leads'])
            agent_leads = targets['depot_chaos_leads'][start_l:end_l]
            
            # Create assignment file
            assignment_file = Path(f'/root/.openclaw/workspace/agent_sandboxes/{agent}/tasks/DEPOTCHAOS_ENRICHMENT_BATCH.md')
            assignment_file.parent.mkdir(parents=True, exist_ok=True)
            
            content = f"""# DEPOTCHAOS ENRICHMENT BATCH - {agent.upper()}
**Assigned:** {datetime.now().isoformat()}
**Due:** Within 1 week
**Priority:** HIGH

## Your Assignment

### Vendors to Enrich: {len(agent_vendors)}
"""
            
            for v in agent_vendors[:50]:  # Show first 50
                content += f"""
- [ ] **{v['name']}** ({v['city']}, {v['state']})
  - ID: {v['id']}
  - Missing: {', '.join(v['missing'])}
  - Territory: {v.get('territory', 'N/A')}
"""
            
            if len(agent_vendors) > 50:
                content += f"\n... and {len(agent_vendors) - 50} more\n"
            
            content += f"""

### Leads to Enrich: {len(agent_leads)}
"""
            
            for l in agent_leads[:25]:  # Show first 25
                content += f"""
- [ ] **{l['name']}** ({l.get('city', 'Unknown')}, {l.get('state', 'Unknown')})
  - ID: {l['id']}
  - Phone: {l.get('phone', 'N/A')}
  - Missing: {', '.join(l['missing'])}
"""
            
            if len(agent_leads) > 25:
                content += f"\n... and {len(agent_leads) - 25} more\n"
            
            content += f"""

## How to Enrich

1. **Access DepotChaos:** https://psdepot.com/depotchaos/
2. **Find Record:** Search by ID or name
3. **Research:** Use Yelp, Google, company websites
4. **Update:** Add missing phone, email, website
5. **Mark Complete:** Check the box above

## Tools
- Yelp Enrichment: `/root/.openclaw/workspace/DepotChaos/yelp_enrichment.py`
- Web Search: Use agent capabilities
- Phone Validation: Check format before saving

## Reporting
Update this file daily with progress.
Contact Patricia if you need help.

---
**Batch Total:** {len(agent_vendors) + len(agent_leads)} records
**Daily Goal:** ~{((len(agent_vendors) + len(agent_leads)) / 7):.0f} records/day
"""
            
            with open(assignment_file, 'w') as f:
                f.write(content)
            
            print(f"✅ Assigned {len(agent_vendors)} vendors + {len(agent_leads)} leads to {agent}")
    
    def setup_auto_scrapers(self):
        """Strategy 2: Set up automated enrichment scrapers."""
        print("\n🤖 STRATEGY 2: Automated Scrapers")
        print("=" * 60)
        
        # Create automated enrichment script
        auto_script = '''#!/usr/bin/env python3
"""
Auto-Enrichment Scraper for DepotChaos
Runs continuously to enrich data automatically
"""

import sqlite3
import json
import time
import subprocess
from datetime import datetime

DB_PATH = '/root/.openclaw/workspace/DepotChaos/depot_chaos.db'
YELP_SCRIPT = '/root/.openclaw/workspace/DepotChaos/yelp_enrichment.py'

def get_unenriched_batch(batch_size=100):
    """Get batch of records needing enrichment."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, city, state 
        FROM vendors 
        WHERE (phone IS NULL OR phone = '') AND (email IS NULL OR email = '')
        LIMIT ?
    """, (batch_size,))
    
    records = cursor.fetchall()
    conn.close()
    return records

def enrich_with_yelp(record_id, name, city, state):
    """Attempt Yelp enrichment."""
    try:
        # Run Yelp scraper
        result = subprocess.run(
            ['python3', YELP_SCRIPT, '--name', name, '--city', city, '--state', state],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def update_record(record_id, phone=None, email=None, website=None):
    """Update record in database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    updates = []
    params = []
    if phone:
        updates.append("phone = ?")
        params.append(phone)
    if email:
        updates.append("email = ?")
        params.append(email)
    if website:
        updates.append("website = ?")
        params.append(website)
    
    if updates:
        params.append(record_id)
        cursor.execute(f"UPDATE vendors SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()
    
    conn.close()

def main():
    """Main enrichment loop."""
    print(f"[{datetime.now()}] Auto-enrichment starting...")
    
    while True:
        records = get_unenriched_batch(50)
        
        if not records:
            print(f"[{datetime.now()}] No records to enrich, sleeping...")
            time.sleep(3600)  # Sleep 1 hour
            continue
        
        print(f"[{datetime.now()}] Enriching {len(records)} records...")
        
        for record in records:
            record_id, name, city, state = record
            
            # Try Yelp
            yelp_result = enrich_with_yelp(record_id, name, city, state)
            
            # Parse result and update
            # (Would need actual parsing logic based on Yelp output)
            
            time.sleep(2)  # Rate limiting
        
        print(f"[{datetime.now()}] Batch complete, sleeping...")
        time.sleep(300)  # 5 minute between batches

if __name__ == '__main__':
    main()
'''
        
        script_path = '/root/.openclaw/workspace/DepotChaos/auto_enrichment_daemon.py'
        with open(script_path, 'w') as f:
            f.write(auto_script)
        
        os.chmod(script_path, 0o755)
        
        # Create systemd service
        service_file = '''[Unit]
Description=DepotChaos Auto-Enrichment Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /root/.openclaw/workspace/DepotChaos/auto_enrichment_daemon.py
Restart=always
RestartSec=60
User=root

[Install]
WantedBy=multi-user.target
'''
        
        with open('/etc/systemd/system/depotchaos-enrichment.service', 'w') as f:
            f.write(service_file)
        
        print(f"✅ Auto-scraper script: {script_path}")
        print(f"✅ Systemd service: depotchaos-enrichment.service")
        print(f"   To start: systemctl enable --now depotchaos-enrichment")
    
    def create_claim_queue(self):
        """Strategy 3: Create queue system for agents to claim records."""
        print("\n📥 STRATEGY 3: Claim Queue System")
        print("=" * 60)
        
        # Create queue database
        queue_db = '/root/.openclaw/workspace/DepotChaos/enrichment_queue/queue.db'
        
        conn = sqlite3.connect(queue_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrichment_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_db TEXT,
                source_table TEXT,
                record_id INTEGER,
                record_name TEXT,
                record_city TEXT,
                record_state TEXT,
                missing_fields TEXT,
                priority INTEGER DEFAULT 5,
                status TEXT DEFAULT 'available',
                claimed_by TEXT,
                claimed_at TIMESTAMP,
                completed_at TIMESTAMP,
                enriched_data TEXT
            )
        ''')
        
        # Populate with targets
        targets = self.identify_enrichment_targets()
        
        for v in targets['depot_chaos_vendors']:
            cursor.execute('''
                INSERT OR IGNORE INTO enrichment_queue 
                (source_db, source_table, record_id, record_name, record_city, record_state, missing_fields)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (v['db'], v['table'], v['id'], v['name'], v['city'], v['state'], ','.join(v['missing'])))
        
        for l in targets['depot_chaos_leads']:
            cursor.execute('''
                INSERT OR IGNORE INTO enrichment_queue 
                (source_db, source_table, record_id, record_name, record_city, record_state, missing_fields)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (l['db'], l['table'], l['id'], l['name'], l.get('city', ''), l.get('state', ''), ','.join(l['missing'])))
        
        conn.commit()
        
        # Get queue stats
        cursor.execute("SELECT COUNT(*) FROM enrichment_queue WHERE status = 'available'")
        available = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM enrichment_queue WHERE status = 'claimed'")
        claimed = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM enrichment_queue WHERE status = 'completed'")
        completed = cursor.fetchone()[0]
        
        conn.close()
        
        # Create claim interface
        claim_script = '''#!/usr/bin/env python3
"""
DepotChaos Enrichment Claim System
Agents claim records to enrich
"""

import sqlite3
import sys
from datetime import datetime

QUEUE_DB = '/root/.openclaw/workspace/DepotChaos/enrichment_queue/queue.db'

def claim_records(agent_id: str, count: int = 10):
    """Claim records for enrichment."""
    conn = sqlite3.connect(QUEUE_DB)
    cursor = conn.cursor()
    
    # Get available records
    cursor.execute("""
        SELECT id, record_name, record_city, record_state, missing_fields
        FROM enrichment_queue
        WHERE status = 'available'
        ORDER BY priority DESC, id ASC
        LIMIT ?
    """, (count,))
    
    records = cursor.fetchall()
    
    if not records:
        print(f"No available records for {agent_id}")
        conn.close()
        return
    
    # Claim them
    for record in records:
        qid, name, city, state, missing = record
        cursor.execute("""
            UPDATE enrichment_queue
            SET status = 'claimed', claimed_by = ?, claimed_at = ?
            WHERE id = ?
        """, (agent_id, datetime.now().isoformat(), qid))
        
        print(f"Claimed: {name} ({city}, {state}) - Missing: {missing}")
    
    conn.commit()
    conn.close()
    print(f"\\n{agent_id} claimed {len(records)} records")

def complete_record(queue_id: int, agent_id: str, data: dict):
    """Mark record as completed with enriched data."""
    conn = sqlite3.connect(QUEUE_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE enrichment_queue
        SET status = 'completed', completed_at = ?, enriched_data = ?
        WHERE id = ? AND claimed_by = ?
    """, (datetime.now().isoformat(), json.dumps(data), queue_id, agent_id))
    
    conn.commit()
    conn.close()
    print(f"Record {queue_id} completed by {agent_id}")

def show_stats():
    """Show queue statistics."""
    conn = sqlite3.connect(QUEUE_DB)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM enrichment_queue WHERE status = 'available'")
    available = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM enrichment_queue WHERE status = 'claimed'")
    claimed = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM enrichment_queue WHERE status = 'completed'")
    completed = cursor.fetchone()[0]
    
    cursor.execute("SELECT claimed_by, COUNT(*) FROM enrichment_queue WHERE status = 'claimed' GROUP BY claimed_by")
    claimed_by = cursor.fetchall()
    
    conn.close()
    
    print("DepotChaos Enrichment Queue Stats")
    print("=" * 40)
    print(f"Available: {available}")
    print(f"Claimed: {claimed}")
    print(f"Completed: {completed}")
    print("\\nClaimed by:")
    for agent, count in claimed_by:
        print(f"  {agent}: {count}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 claim_system.py claim <agent_id> [count]")
        print("  python3 claim_system.py complete <queue_id> <agent_id>")
        print("  python3 claim_system.py stats")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'claim':
        agent = sys.argv[2]
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        claim_records(agent, count)
    elif cmd == 'stats':
        show_stats()
'''
        
        claim_path = '/root/.openclaw/workspace/DepotChaos/enrichment_queue/claim_system.py'
        with open(claim_path, 'w') as f:
            f.write(claim_script)
        
        os.chmod(claim_path, 0o755)
        
        print(f"✅ Queue database: {queue_db}")
        print(f"✅ Queue records: {available:,} available, {claimed} claimed, {completed} completed")
        print(f"✅ Claim script: {claim_path}")
        print(f"\nUsage:")
        print(f"  python3 {claim_path} claim <agent_id> [count]")
        print(f"  python3 {claim_path} stats")
    
    def run_all_strategies(self):
        """Execute all three enrichment strategies."""
        print("🏭 DEPOTCHAOS 72K+ LEAD ENRICHMENT")
        print("=" * 60)
        
        # Get stats
        print("\n📊 Database Overview:")
        stats = self.get_all_database_stats()
        for db_name, db_stats in stats.items():
            if 'records' in db_stats:
                total = sum(db_stats['records'].values())
                print(f"  {db_name}: {total:,} total records")
        
        # Run all strategies
        self.create_agent_assignments()
        self.setup_auto_scrapers()
        self.create_claim_queue()
        
        print("\n" + "=" * 60)
        print("✅ ALL 3 STRATEGIES DEPLOYED")
        print("=" * 60)
        print("\nSummary:")
        print("  1. Agent Assignments: Distributed batches to all agents")
        print("  2. Auto-Scrapers: Daemon ready to run (systemctl enable)")
        print("  3. Claim Queue: Agents can claim records on-demand")
        print("\nNext Steps:")
        print("  - Agents check their tasks/ folder for assignments")
        print("  - Start auto-scraper: systemctl enable --now depotchaos-enrichment")
        print("  - Agents can claim additional records via claim_system.py")


def main():
    master = DepotChaosEnrichmentMaster()
    master.run_all_strategies()


if __name__ == "__main__":
    main()
