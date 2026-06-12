#!/usr/bin/env python3
"""
Search Priority States for Bars/Restaurants with Keywords
"""

import csv
import os
from datetime import datetime

# High priority states
PRIORITY_STATES = [
    'NY', 'FL', 'IL', 'PA', 'GA', 'NC', 'OH', 'MI', 'AZ', 'MA', 
    'VA', 'NJ', 'CO', 'SC', 'MD', 'KY', 'LA'
]

KEYWORDS = ['nickel', 'nickle', 'pickle', 'peso', 'dollar', 'wooden', 'silver']

# All data directories to search
DATA_PATHS = [
    '/root/.openclaw/workspace/AGI_COMPANY/data/leads_final/',
    '/root/.openclaw/workspace/datadepot/data/',
]

def search_all_databases():
    """Search all available databases for priority states"""
    matches = []
    
    for base_path in DATA_PATHS:
        if not os.path.exists(base_path):
            continue
            
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith('.csv'):
                    # Check if file is for a priority state
                    state_code = None
                    for state in PRIORITY_STATES:
                        if state in file.upper():
                            state_code = state
                            break
                    
                    if not state_code:
                        continue
                    
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                company = str(row.get('Company', '')).lower()
                                
                                for kw in KEYWORDS:
                                    if kw in company:
                                        matches.append({
                                            'name': row.get('Company'),
                                            'type': row.get('Business Type', 'Unknown'),
                                            'address': row.get('Address'),
                                            'city': row.get('City'),
                                            'state': state_code,
                                            'phone': row.get('Phone'),
                                            'keyword': kw,
                                            'source': file
                                        })
                                        break
                    except Exception as e:
                        pass
    
    return matches

if __name__ == '__main__':
    print("Searching PRIORITY STATES (17 high-value states)...")
    print(f"States: {', '.join(PRIORITY_STATES)}")
    print(f"Keywords: {', '.join(KEYWORDS)}")
    print()
    
    matches = search_all_databases()
    
    print(f"Results: {len(matches)} matches found")
    print()
    
    # Group by state
    by_state = {}
    for m in matches:
        state = m['state']
        if state not in by_state:
            by_state[state] = []
        by_state[state].append(m)
    
    print("By State:")
    for state in PRIORITY_STATES:
        count = len(by_state.get(state, []))
        if count > 0:
            print(f"  {state}: {count}")
    
    print()
    print("=== DETAILED RESULTS ===")
    for state in sorted(by_state.keys()):
        print(f"\n{state} ({len(by_state[state])} matches):")
        for m in by_state[state][:10]:
            print(f"  • {m['name']}")
            print(f"    {m['type']} | {m['city']}")
        if len(by_state[state]) > 10:
            print(f"    ... and {len(by_state[state]) - 10} more")
