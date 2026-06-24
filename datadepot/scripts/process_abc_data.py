#!/usr/bin/env python3
"""
MYL DataDepot - CA ABC License Data Processor
Patricia Agent - Daily Collection Job
"""

import csv
import os
import sys
from datetime import datetime, timedelta
import json

# Configuration
DATA_DIR = "/root/.openclaw/workspace/datadepot/data"
LOG_DIR = "/root/.openclaw/workspace/datadepot/logs"
ENRICHMENT_DIR = "/root/.openclaw/workspace/datadepot/enrichment"

# Restaurant/bar license types we care about
RESTAURANT_TYPES = {'20', '41', '42', '47', '48', '49', '40', '21', '01'}

def parse_update_date(line):
    """Extract date from the header line"""
    # Format: "Updated Wednesday 24th of June 2026 03:50:22 AM"
    try:
        parts = line.strip().replace('"', '').split()
        # Find date parts
        day = ''
        month = ''
        year = ''
        for i, part in enumerate(parts):
            if 'th' in part or 'st' in part or 'nd' in part or 'rd' in part:
                day = part.replace('th', '').replace('st', '').replace('nd', '').replace('rd', '')
            if part in ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']:
                month = part
            if len(part) == 4 and part.isdigit():
                year = part
        if day and month and year:
            date_str = f"{day} {month} {year}"
            return datetime.strptime(date_str, "%d %B %Y")
    except:
        pass
    return datetime.now()

def is_restaurant_license(license_type):
    """Check if license type is restaurant/bar related"""
    return str(license_type).strip() in RESTAURANT_TYPES

def enrich_record(record):
    """Simulate enrichment with Google Business data"""
    # In production, this would call Google Places API
    record['enriched'] = True
    record['enrichment_date'] = datetime.now().isoformat()
    
    # Simulate POS detection likelihood based on business type
    dba = record.get('DBA Name', '').upper()
    name = record.get('Primary Name', '').upper()
    
    # Simple heuristics for POS likelihood
    pos_indicators = ['RESTAURANT', 'CAFE', 'PIZZA', 'BAR', 'GRILL', 'KITCHEN', 
                      'BISTRO', 'EATERY', 'TAVERN', 'PUB', 'BREWERY']
    
    record['pos_likelihood'] = 'high' if any(ind in dba or ind in name for ind in pos_indicators) else 'medium'
    record['replacement_score'] = calculate_replacement_score(record)
    
    return record

def calculate_replacement_score(record):
    """Calculate replacement likelihood score (0-100)"""
    score = 50  # Base score
    
    # Active licenses are more valuable
    if record.get('Type Status', '').upper() == 'ACTIVE':
        score += 20
    
    # Restaurant types score higher
    if record.get('License Type', '') in ['41', '47', '48']:
        score += 15
    
    # Newer applications are hotter leads
    if record.get('Type Status', '').upper() == 'PEND':
        score += 10
        
    return min(100, max(0, score))

def process_daily_export():
    """Main processing function"""
    input_file = os.path.join(DATA_DIR, "ABC-DailyDataExport.csv")
    output_file = os.path.join(DATA_DIR, "ca_abc_licenses_raw.csv")
    
    # Today's date
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    stats = {
        'total_records': 0,
        'restaurant_records': 0,
        'new_records': 0,
        'enriched': 0,
        'high_value_leads': 0
    }
    
    new_restaurant_records = []
    
    print(f"[{datetime.now().isoformat()}] Starting CA ABC Daily Data Processing")
    print(f"[{datetime.now().isoformat()}] Processing file: {input_file}")
    
    # Read and process the export file
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        # First line is update date
        first_line = f.readline()
        file_date = parse_update_date(first_line)
        print(f"[{datetime.now().isoformat()}] Data export date: {file_date}")
        
        # Read CSV data
        reader = csv.DictReader(f)
        
        for row in reader:
            stats['total_records'] += 1
            
            license_type = row.get('License Type', '').strip()
            
            # Filter for restaurant types
            if is_restaurant_license(license_type):
                stats['restaurant_records'] += 1
                
                # Check if this appears to be new (PEND status or recent)
                status = row.get('Type Status', '').strip().upper()
                if status in ['PEND', 'ACTIVE']:
                    stats['new_records'] += 1
                    
                    # Enrich the record
                    enriched = enrich_record(row)
                    new_restaurant_records.append(enriched)
                    stats['enriched'] += 1
                    
                    # Check for high-value leads
                    if enriched.get('replacement_score', 0) >= 70:
                        stats['high_value_leads'] += 1
    
    # Append new records to the raw CSV
    file_exists = os.path.exists(output_file)
    with open(output_file, 'a', newline='', encoding='utf-8') as f:
        if new_restaurant_records:
            writer = csv.DictWriter(f, fieldnames=new_restaurant_records[0].keys())
            if not file_exists:
                writer.writeheader()
            writer.writerows(new_restaurant_records)
    
    print(f"[{datetime.now().isoformat()}] Processing complete")
    print(f"[{datetime.now().isoformat()}] Stats: {json.dumps(stats, indent=2)}")
    
    return stats, new_restaurant_records

def generate_report(stats, records, output_dir):
    """Generate daily summary report"""
    today_str = datetime.now().strftime("%Y%m%d")
    report_file = os.path.join(output_dir, f"daily_collection_{today_str}.log")
    
    high_value_count = len([r for r in records if r.get('replacement_score', 0) >= 70])
    
    report = f"""
================================================================================
MYL DataDepot - Daily Collection Report
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}
Agent: Patricia (MYL Data Agent)
================================================================================

DATA COLLECTION SUMMARY
-----------------------
Total Records Scanned:      {stats['total_records']:,}
Restaurant/Bar Licenses:    {stats['restaurant_records']:,}
New/Updated Records:        {stats['new_records']:,}
Records Enriched:           {stats['enriched']:,}
High-Value Leads:           {high_value_count}

DATA SOURCE
-----------
Source: CA ABC Daily Export
URL: https://www.abc.ca.gov/wp-content/uploads/DailyExport-CSV.zip
Export Date: {datetime.now().strftime("%Y-%m-%d")}

ENRICHMENT STATUS
-----------------
Google Business Lookup:      Simulated (API integration pending)
POS Detection Model:         Heuristic-based scoring active
Replacement Scores:          Calculated for all new records

DATA QUALITY METRICS
--------------------
Records with Complete Address: {len([r for r in records if r.get('Prem Zip', '').strip()])}
Records with DBA Name:         {len([r for r in records if r.get('DBA Name', '').strip()])}
Active Status Records:         {len([r for r in records if r.get('Type Status', '').upper() == 'ACTIVE'])}
Pending Status Records:        {len([r for r in records if r.get('Type Status', '').upper() == 'PEND'])}

OUTPUT FILES
------------
Raw Data: /datadepot/data/ca_abc_licenses_raw.csv
This Log: /datadepot/logs/daily_collection_{today_str}.log

NOTIFICATIONS
-------------
Pulp Notification: {'REQUIRED' if high_value_count > 0 else 'Not required'}
High-value leads detected: {high_value_count}

NEXT STEPS
----------
1. Review high-value leads for outreach
2. Sync enrichment data to CRM
3. Update POS detection model with new training data

================================================================================
End of Report
================================================================================
"""
    
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"[{datetime.now().isoformat()}] Report written to: {report_file}")
    return report

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(ENRICHMENT_DIR, exist_ok=True)
    
    # Process data
    stats, records = process_daily_export()
    
    # Generate report
    report = generate_report(stats, records, LOG_DIR)
    
    # Print summary
    print("\n" + "="*80)
    print("DAILY COLLECTION COMPLETE")
    print("="*80)
    print(f"New restaurant licenses found: {stats['new_records']}")
    print(f"High-value leads: {stats['high_value_leads']}")
    print(f"Total processed: {stats['total_records']}")
    print("="*80)
