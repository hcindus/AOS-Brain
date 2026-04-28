#!/usr/bin/env python3
"""
Performance Supply Depot - AI Sales Agent System
Main orchestrator for the 4-agent sales team

Agents:
- Miles: Primary sales (outbound/inbound)
- Clippy-42: Assistant (research, scheduling)
- Pulp: Closer (high-value deals)
- Jane: Nurturer (retention, follow-up)
"""

import json
import sqlite3
import random
from datetime import datetime
from pathlib import Path

class DepotSalesSystem:
    def __init__(self, db_path="/root/.openclaw/workspace/AGI_COMPANY/agents/sales/sales_crm.db"):
        self.db_path = db_path
        self.init_database()
        
        # Load knowledge base
        self.knowledge = self.load_knowledge()
        
    def init_database(self):
        """Initialize CRM database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Leads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY,
                business_name TEXT,
                contact_name TEXT,
                phone TEXT,
                email TEXT,
                business_type TEXT,
                state TEXT,
                status TEXT DEFAULT 'new',
                assigned_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_contact TIMESTAMP,
                next_contact TIMESTAMP,
                notes TEXT
            )
        ''')
        
        # Calls table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY,
                lead_id INTEGER,
                agent_name TEXT,
                direction TEXT,  -- inbound/outbound
                outcome TEXT,    -- connected, voicemail, no_answer, etc.
                duration INTEGER, -- seconds
                notes TEXT,
                transcript TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        ''')
        
        # Opportunities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS opportunities (
                id INTEGER PRIMARY KEY,
                lead_id INTEGER,
                agent_name TEXT,
                value REAL,
                stage TEXT,  -- prospecting, discovery, proposal, negotiation, closed_won, closed_lost
                products TEXT,
                close_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ CRM initialized: {self.db_path}")
    
    def load_knowledge(self):
        """Load product knowledge and pricing"""
        return {
            "products": {
                "thermal_paper": {
                    "name": "Thermal Receipt Paper",
                    "sizes": ["3 1/8\" x 230'", "2 1/4\" x 85'"],
                    "price_per_case": 69.00,  # Updated based on competitive analysis
                    "price_per_roll": 1.38,     # $69/50 rolls
                    "case_qty": 50,
                    "description": "High-quality thermal paper for POS printers"
                },
                "ink_ribbons": {
                    "name": "Impact Printer Ribbons",
                    "models": ["ERC 30/34/38", "Star SP700"],
                    "price_per_dozen": {"ERC": 42.00, "Star": 52.00},
                    "price_each": {"ERC": 3.50, "Star": 4.33},
                    "description": "Black/red ribbons for impact printers"
                },
                "pos_systems": {
                    "sam4s_er260": {"name": "SAM4S ER-260", "price": 495.00},
                    "sam4s_er940": {"name": "SAM4S ER-940", "price": 895.00},
                    "sam4s_sap630": {"name": "SAM4S SAP-630", "price": 1395.00},
                },
                "scales": {
                    "cas_lp1000": {"name": "CAS LP-1000 Label Scale", "price": 1495.00},
                    "integrated": {"name": "Integrated POS Scale", "price": 795.00},
                }
            },
            "services": {
                "cabling": {"rate": 180.00, "unit": "hour", "name": "Custom Cabling"},
                "printer_repair": {"rate": 195.00, "unit": "hour", "name": "Printer Repair"},
                "pos_installation": {"rate": 180.00, "unit": "hour", "name": "POS Installation"},
                "scale_setup": {"rate": 195.00, "unit": "hour", "name": "Label & Scale Setup"},
            },
            "company": {
                "name": "Performance Supply Depot",
                "phone": "888-881-6834",
                "alt_phone": "415-571-9724",
                "email": "info@psdepot.com",
                "website": "https://psdepot.com",
                "years_in_business": 19,  # Since 2005
                "location": "Las Vegas, NV",
                "customers_served": "10,000+",
                "same_day_delivery": True,
                "service_area": "Las Vegas metro area"
            },
            "objection_handling": {
                "too_expensive": [
                    "I understand budget is important. Many of our customers found that when they factor in downtime costs from printer failures, our total cost is actually lower.",
                    "Let's look at what you're spending now, including emergency repairs and last-minute shipping. We might save you money.",
                    "We offer financing options and can work within your budget. What if we started with just the essentials?"
                ],
                "happy_with_current_supplier": [
                    "That's great that you have a good relationship. What happens when you have an emergency Friday night—do they answer the phone?",
                    "Feel, Felt, Found: I understand you feel comfortable with your current supplier. Many of our customers felt the same way until they experienced same-day delivery and on-site support.",
                    "Would you be open to a backup option? Many restaurants keep us as a Plan B for emergencies."
                ],
                "just_buy_on_amazon": [
                    "Amazon's great for many things. But when your printer's down and you need it fixed today, who's coming to help? We're local.",
                    "Absolutely, you can buy paper cheaper. But we offer something Amazon can't: same-day delivery in Vegas and on-site repair when things break.",
                    "Fair point. What's your plan when a printer fails Friday at 6 PM and you have a full house?"
                ],
                "need_to_think_about_it": [
                    "Of course, this is an important decision. What specific concerns do you need to think through?",
                    "I understand. When would be a good time for me to follow up—tomorrow or later this week?",
                    "What information would help you make this decision? I can send over a comparison sheet."
                ],
                "call_back_later": [
                    "I know you're busy. What time works better for you—morning or afternoon?",
                    "No problem. When would be the best time to reach you? I want to respect your schedule.",
                    "I hear that a lot. How about I send you some information via email, and we touch base Thursday?"
                ]
            }
        }
    
    def get_agent_script(self, agent_name, call_type="outbound"):
        """Get appropriate script for agent"""
        scripts = {
            "miles": {
                "greeting": "Hey, this is Miles from Performance Supply Depot. I hope I'm not catching you at a bad time.",
                "qualifying_questions": [
                    "Are you the person who handles the supplies for {business_name}?",
                    "What POS system are you currently running?",
                    "Who's your current supplier for receipt paper and printer supplies?",
                    "How's that working out for you?",
                    "Are you dealing with any printer issues or supply shortages?"
                ],
                "value_prop": "We specialize in POS supplies and printer repair for busy restaurants here in Vegas. Same-day delivery and on-site service when you need it.",
                "close": "Would it make sense for us to send over a quick quote? Just let me know what supplies you use most.",
                "voicemail": "Hi, this is Miles from Performance Supply Depot. I'm calling about your POS supplies. We're a local Vegas company specializing in same-day delivery and on-site printer repair. Give me a call back at 888-881-6834. Thanks!"
            },
            "pulp": {
                "greeting": "Hi {contact_name}, this is Pulp from Performance Supply Depot. Miles mentioned you're looking at some options for your POS setup.",
                "discovery": [
                    "Walk me through your current setup—how many terminals do you have?",
                    "What's your biggest pain point right now?",
                    "If we could solve one problem for you, what would it be?",
                    "What's your timeline for making a change?"
                ],
                "close": "Based on what you've told me, here's what I recommend... [present solution]. The investment is ${price}. When can we get this scheduled?"
            },
            "jane": {
                "greeting": "Hi {contact_name}, it's Jane from Performance Supply Depot. I'm just checking in to see how everything's working out.",
                "check_in": [
                    "How's the new setup working for you?",
                    "Any questions or issues I can help with?",
                    "Are you running low on any supplies?",
                    "Can I schedule your next delivery?"
                ],
                "upsell": "I noticed you're using {product}. Many restaurants like yours also benefit from {upsell_product}. Want me to include that in your next order?"
            }
        }
        
        return scripts.get(agent_name, scripts["miles"])
    
    def generate_call_summary(self, lead_id, agent_name, outcome, notes):
        """Generate and save call summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO calls (lead_id, agent_name, outcome, notes, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (lead_id, agent_name, outcome, notes, datetime.now()))
        
        # Update lead status
        cursor.execute('''
            UPDATE leads 
            SET last_contact = ?, status = ?
            WHERE id = ?
        ''', (datetime.now(), outcome, lead_id))
        
        conn.commit()
        conn.close()
        
        return {
            "lead_id": lead_id,
            "agent": agent_name,
            "outcome": outcome,
            "timestamp": datetime.now().isoformat(),
            "next_steps": self.suggest_next_steps(outcome)
        }
    
    def suggest_next_steps(self, outcome):
        """Suggest next steps based on call outcome"""
        steps = {
            "connected_interested": "Schedule discovery call with Pulp",
            "connected_not_interested": "Add to nurture sequence, follow up in 90 days",
            "voicemail": "Send email follow-up, try again in 3 days",
            "no_answer": "Try different time, max 3 attempts",
            "wrong_person": "Get decision maker name, retry",
            "appointment_set": "Send calendar invite, prepare Pulp",
            "closed_won": "Hand off to Jane for onboarding",
            "closed_lost": "Analyze why, update objection handling"
        }
        return steps.get(outcome, "Review and follow standard process")
    
    def get_daily_tasks(self, agent_name):
        """Get daily task list for an agent"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get leads assigned to this agent
        cursor.execute('''
            SELECT * FROM leads 
            WHERE assigned_agent = ? 
            AND (next_contact IS NULL OR next_contact <= ?)
            AND status NOT IN ('closed_won', 'closed_lost', 'do_not_contact')
            ORDER BY last_contact ASC
            LIMIT 20
        ''', (agent_name, datetime.now()))
        
        leads = cursor.fetchall()
        conn.close()
        
        return {
            "agent": agent_name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "leads_to_contact": len(leads),
            "leads": leads
        }

def main():
    print("=" * 60)
    print("Performance Supply Depot - AI Sales Agent System")
    print("=" * 60)
    print()
    
    # Initialize system
    system = DepotSalesSystem()
    
    print("Available commands:")
    print("  get_script <miles|pulp|jane> - Get agent script")
    print("  get_tasks <agent_name> - Get daily task list")
    print("  load_campaigns - Import leads from campaign files")
    print("  stats - Show system statistics")
    print()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "get_script" and len(sys.argv) > 2:
            agent = sys.argv[2]
            script = system.get_agent_script(agent)
            print(f"\n🎭 {agent.upper()} Script:")
            print(json.dumps(script, indent=2))
            
        elif command == "stats":
            print("\n📊 System Statistics:")
            print(f"Products in knowledge base: {len(system.knowledge['products'])}")
            print(f"Services: {len(system.knowledge['services'])}")
            print(f"Objection handlers: {len(system.knowledge['objection_handling'])}")
            
        else:
            print(f"Unknown command: {command}")

if __name__ == "__main__":
    import sys
    main()
