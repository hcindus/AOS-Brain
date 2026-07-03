#!/usr/bin/env python3
"""
Verify pending items from phone_verification_queue and import to leads
"""

import sqlite3
import csv
import re
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
QUEUE_PATH = "/root/.openclaw/workspace/datadepot/phone_verification_queue.csv"

# California area codes
CA_AREA_CODES = {'209', '213', '279', '310', '323', '408', '415', '424', '442', '510', 
                 '530', '559', '562', '619', '626', '650', '657', '661', '669', '707',
                 '714', '747', '760', '805', '818', '820', '831', '858', '909', '916',
                 '925', '949', '951'}

def validate_phone(phone):
    """Check if phone is valid CA number"""
    if not phone:
        return False, "No phone"
    
    digits = re.sub(r'\D', '', phone)
    if len(digits) != 10:
        return False, "Wrong length"
    
    area_code = digits[:3]
    if area_code not in CA_AREA_CODES:
        return False, f"Non-CA area: {area_code}"
    
    return True, "Valid CA"

def is_placeholder_name(name):
    """Check if name is placeholder/test data"""
    patterns = [
        r'^20\s+',  # Starts with "20 "
        r'\s+\d+$',  # Ends with number
        r'^(Bar|Bistro|Cafe|Coffee|Diner|Restaurant|Taqueria)\s+(House|Co\.?|Grill|Bar)',
        r'\s+(House|Co\.?|Grill|Bar|of)\s+(?:[A-Z][a-z]+\s*)+$',  # "Cafe of Sacramento" pattern
    ]
    
    for pattern in patterns:
        if re.search(pattern, name, re.IGNORECASE):
            return True
    return False

def import_to_leads(record):
    """Import verified record to leads"""
    id_, name, city, state, phone, address, status, real_name, email = record
    
    # Validate
    is_valid, reason = validate_phone(phone)
    is_placeholder = is_placeholder_name(name)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if already exists
    c.execute("SELECT id FROM leads WHERE business_name = ? AND city = ? AND state = ?",
              (name, city, state))
    if c.fetchone():
        conn.close()
        return "skipped", "Already exists"
    
    # Determine action
    if state == 'CA' and is_valid and not is_placeholder:
        # Import as verified lead
        c.execute("""
            INSERT INTO leads (business_name, city, state, phone, address, 
                             source_type, created_at, tags, status, deleted)
            VALUES (?, ?, ?, ?, ?, 'verified_import', datetime('now'), 
                   'verified,phone_check', 'new', 0)
        """, (name, city, state, phone, address))
        action = "imported"
        
    elif state == 'CA' and is_placeholder:
        # Flag as potential placeholder
        c.execute("""
            INSERT INTO leads (business_name, city, state, phone, address,
                             source_type, created_at, tags, status, deleted, notes)
            VALUES (?, ?, ?, ?, ?, 'verified_import', datetime('now'),
                   'placeholder,needs_review', 'new', 0, ?)
        """, (name, city, state, phone, address, f"Placeholder pattern: {reason}"))
        action = "flagged_placeholder"
        
    else:
        # Out of state - low priority
        c.execute("""
            INSERT INTO leads (business_name, city, state, phone, address,
                             source_type, created_at, tags, status, deleted, notes)
            VALUES (?, ?, ?, ?, ?, 'verified_import', datetime('now'),
                   'out_of_state,low_priority', 'new', 0, ?)
        """, (name, city, state, phone, address, f"Non-CA: {reason}"))
        action = "out_of_state"
    
    conn.commit()
    conn.close()
    return action, reason

def main():
    print("=" * 60)
    print("📋 VERIFYING AND IMPORTING PENDING ITEMS")
    print("=" * 60)
    
    # Read queue
    with open(QUEUE_PATH, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        records = list(reader)
    
    print(f"Total pending: {len(records)}")
    print()
    
    # Categorize
    ca_valid = []
    ca_placeholder = []
    other_states = []
    
    for record in records:
        id_, name, city, state, phone, address, status, real_name, email = record
        
        is_valid, reason = validate_phone(phone)
        is_placeholder = is_placeholder_name(name)
        
        if state == 'CA':
            if is_valid and not is_placeholder:
                ca_valid.append(record)
            else:
                ca_placeholder.append((record, reason))
        else:
            other_states.append((record, reason))
    
    print(f"CA - Valid names: {len(ca_valid)}")
    print(f"CA - Placeholder names: {len(ca_placeholder)}")
    print(f"Other states: {len(other_states)}")
    print()
    
    # Import CA valid
    imported = 0
    flagged = 0
    out_of_state = 0
    skipped = 0
    
    print("Importing CA valid records...")
    for record in ca_valid[:10]:  # Limit to first 10 for safety
        action, reason = import_to_leads(record)
        if action == "imported":
            imported += 1
            print(f"  ✅ {record[1][:30]} ({record[2]}, {record[3]})")
        elif action == "skipped":
            skipped += 1
    
    print(f"\nImporting CA placeholder records...")
    for record, reason in ca_placeholder[:10]:
        action, _ = import_to_leads(record)
        if action == "flagged_placeholder":
            flagged += 1
            print(f"  ⚠️  {record[1][:30]} - FLAGGED")
        elif action == "skipped":
            skipped += 1
    
    print(f"\nImporting out-of-state records...")
    for record, reason in other_states[:10]:
        action, _ = import_to_leads(record)
        if action == "out_of_state":
            out_of_state += 1
            print(f"  📍 {record[1][:30]} ({record[3]}) - Low priority")
        elif action == "skipped":
            skipped += 1
    
    print()
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Imported (CA valid): {imported}")
    print(f"Flagged (CA placeholder): {flagged}")
    print(f"Out-of-state: {out_of_state}")
    print(f"Skipped (duplicates): {skipped}")
    print(f"Total processed: {imported + flagged + out_of_state + skipped}")

if __name__ == "__main__":
    main()
