#!/usr/bin/env python3
"""
System-wide update: Extract actual business data from JSON and populate intelligence table columns
"""

import sqlite3
import json

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def update_intelligence_records():
    """Update all intelligence records with extracted JSON data"""
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get all intelligence records
    c.execute("SELECT id, business_name, data FROM datadepot_intelligence")
    records = c.fetchall()
    
    updated = 0
    errors = 0
    
    for record_id, business_name, data_json in records:
        if not data_json:
            continue
        
        try:
            data = json.loads(data_json)
            
            # Extract fields from JSON
            updates = []
            params = []
            
            if 'owner_name' in data and data['owner_name']:
                updates.append("owner_name = ?")
                params.append(data['owner_name'])
            
            if 'address' in data and data['address']:
                updates.append("address = ?")
                params.append(data['address'])
            
            if 'city' in data and data['city']:
                updates.append("city = ?")
                params.append(data['city'])
            
            if 'state' in data and data['state']:
                updates.append("state = ?")
                params.append(data['state'])
            
            if 'zip' in data and data['zip']:
                updates.append("zip = ?")
                params.append(data['zip'])
            
            if 'phone' in data and data['phone']:
                updates.append("phone = ?")
                params.append(data['phone'])
            
            if 'status' in data and data['status']:
                updates.append("license_status = ?")
                params.append(data['status'])
            
            if 'issue_date' in data and data['issue_date']:
                updates.append("issue_date = ?")
                params.append(data['issue_date'])
            
            if 'expiration_date' in data and data['expiration_date']:
                updates.append("expiration_date = ?")
                params.append(data['expiration_date'])
            
            # Update the business_name if we have a better one
            if 'dba' in data and data['dba']:
                updates.append("business_name = ?")
                params.append(data['dba'])
            elif 'business_name' in data and data['business_name']:
                updates.append("business_name = ?")
                params.append(data['business_name'])
            
            # Apply updates if any
            if updates:
                set_clause = ', '.join(updates)
                params.append(record_id)
                
                c.execute(f"UPDATE datadepot_intelligence SET {set_clause} WHERE id = ?", params)
                updated += 1
                
                if updated % 5000 == 0:
                    print(f"Updated {updated} records...")
                    conn.commit()
                    
        except json.JSONDecodeError:
            errors += 1
        except Exception as e:
            print(f"Error on record {record_id}: {e}")
            errors += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n=== System-Wide Update Complete ===")
    print(f"Total records processed: {len(records)}")
    print(f"Records updated: {updated}")
    print(f"JSON parse errors: {errors}")

if __name__ == "__main__":
    update_intelligence_records()
