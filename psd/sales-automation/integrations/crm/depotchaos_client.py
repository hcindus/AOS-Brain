#!/usr/bin/env python3
"""
DepotChaos CRM Integration
Connects sales automation to PSD CRM
"""

import json
import logging
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DepotChaosCRM")


class DepotChaosClient:
    """
    Client for DepotChaos CRM integration
    
    Methods:
    - Create/update leads
    - Create customers
    - Update order status
    - Query contact history
    """
    
    def __init__(self, db_path: str = "/datadepot/data/depotchaos.db"):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Connect to DepotChaos database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            logger.info(f"Connected to DepotChaos: {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            # Fallback to local test DB
            self.conn = sqlite3.connect(":memory:")
            self._init_schema()
    
    def _init_schema(self):
        """Initialize test schema"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY,
                lead_id TEXT UNIQUE,
                company_name TEXT,
                contact_name TEXT,
                email TEXT,
                phone TEXT,
                source TEXT,
                icp_score INTEGER,
                status TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                customer_id TEXT UNIQUE,
                company_name TEXT,
                contact_name TEXT,
                email TEXT,
                phone TEXT,
                deal_value REAL,
                onboarding_status TEXT,
                first_win_recorded BOOLEAN,
                created_at TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY,
                lead_id TEXT,
                activity_type TEXT,
                details TEXT,
                timestamp TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    def create_lead(self, lead: Dict) -> str:
        """
        Create new lead in CRM
        
        Called by Prospector Agent (SOP-043)
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO leads (
                lead_id, company_name, contact_name, email, phone,
                source, icp_score, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead["lead_id"],
            lead.get("company_name", ""),
            lead.get("contact_name", ""),
            lead.get("email", ""),
            lead.get("phone", ""),
            lead.get("source", "unknown"),
            lead.get("icp_score", 0),
            lead.get("status", "new"),
            datetime.now(),
            datetime.now()
        ))
        
        self.conn.commit()
        
        # Log activity
        self._log_activity(lead["lead_id"], "lead_created", 
                          f"Lead created from {lead.get('source', 'unknown')}")
        
        logger.info(f"Created lead: {lead['lead_id']}")
        return lead["lead_id"]
    
    def update_lead_status(self, lead_id: str, status: str, 
                          notes: Optional[str] = None):
        """
        Update lead status
        
        Status flow:
        - new → qualified → proposal_sent → negotiating → closed_won/lost
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            UPDATE leads SET status = ?, updated_at = ?
            WHERE lead_id = ?
        """, (status, datetime.now(), lead_id))
        
        self.conn.commit()
        
        if notes:
            self._log_activity(lead_id, "status_change", notes)
        
        logger.info(f"Updated lead {lead_id} to {status}")
    
    def create_customer(self, customer: Dict) -> str:
        """
        Create customer from closed deal
        
        Called by Closer Agent (SOP-047)
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO customers (
                customer_id, company_name, contact_name, email, phone,
                deal_value, onboarding_status, first_win_recorded, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            customer["customer_id"],
            customer["company_name"],
            customer["contact_name"],
            customer["email"],
            customer["phone"],
            customer["deal_value"],
            customer.get("onboarding_status", "pending"),
            customer.get("first_win_recorded", False),
            datetime.now()
        ))
        
        self.conn.commit()
        
        # Update lead to closed_won
        self.update_lead_status(
            customer.get("lead_id", ""),
            "closed_won",
            f"Converted to customer {customer['customer_id']}"
        )
        
        logger.info(f"Created customer: {customer['customer_id']}")
        return customer["customer_id"]
    
    def get_lead_by_id(self, lead_id: str) -> Optional[Dict]:
        """Get lead by ID"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM leads WHERE lead_id = ?
        """, (lead_id,))
        
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    def get_leads_by_status(self, status: str) -> List[Dict]:
        """Get all leads by status"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM leads WHERE status = ? ORDER BY icp_score DESC
        """, (status,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_hot_leads(self, min_score: int = 7) -> List[Dict]:
        """
        Get hot leads for qualification
        
        Called by Qualifier Agent (SOP-044)
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM leads 
            WHERE icp_score >= ? AND status IN ('new', 'hot')
            ORDER BY icp_score DESC, created_at ASC
            LIMIT 50
        """, (min_score,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_qualified_appointments(self) -> List[Dict]:
        """
        Get qualified appointments for proposal generation
        
        Called by Presenter Agent (SOP-045)
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM leads 
            WHERE status = 'qualified' AND calendar_booked = 1
            ORDER BY updated_at ASC
        """)
        
        return [dict(row) for row in cursor.fetchall()]
    
    def record_win(self, customer_id: str, win_details: Dict):
        """
        Record customer win
        
        Called by Closer Agent when win detected
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            UPDATE customers 
            SET first_win_recorded = TRUE, win_details = ?
            WHERE customer_id = ?
        """, (json.dumps(win_details), customer_id))
        
        self.conn.commit()
        
        logger.info(f"Recorded win for {customer_id}")
    
    def _log_activity(self, lead_id: str, activity_type: str, details: str):
        """Log activity for lead"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO activities (lead_id, activity_type, details, timestamp)
            VALUES (?, ?, ?, ?)
        """, (lead_id, activity_type, details, datetime.now()))
        
        self.conn.commit()
    
    def get_pipeline_metrics(self) -> Dict:
        """
        Get sales pipeline metrics
        """
        cursor = self.conn.cursor()
        
        # Count by status
        cursor.execute("""
            SELECT status, COUNT(*) FROM leads GROUP BY status
        """)
        
        status_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Total leads
        cursor.execute("SELECT COUNT(*) FROM leads")
        total_leads = cursor.fetchone()[0]
        
        # Total customers
        cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = cursor.fetchone()[0]
        
        # Revenue
        cursor.execute("SELECT SUM(deal_value) FROM customers")
        total_revenue = cursor.fetchone()[0] or 0
        
        return {
            "total_leads": total_leads,
            "total_customers": total_customers,
            "total_revenue": total_revenue,
            "by_status": status_counts,
            "conversion_rate": total_customers / total_leads if total_leads > 0 else 0
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    """CLI entry point"""
    client = DepotChaosClient()
    client.connect()
    
    # Test create lead
    test_lead = {
        "lead_id": "LEAD-TEST-001",
        "company_name": "Test Company",
        "contact_name": "John Doe",
        "email": "john@test.com",
        "phone": "555-0100",
        "source": "linkedin",
        "icp_score": 8,
        "status": "hot"
    }
    
    client.create_lead(test_lead)
    
    # Get hot leads
    hot_leads = client.get_hot_leads()
    print(f"Hot leads: {len(hot_leads)}")
    
    # Get metrics
    metrics = client.get_pipeline_metrics()
    print(f"Pipeline: {metrics}")
    
    client.close()


if __name__ == "__main__":
    main()
