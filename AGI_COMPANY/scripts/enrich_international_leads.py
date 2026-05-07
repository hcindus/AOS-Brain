#!/usr/bin/env python3
"""
Enrich and merge international leads (Canada & Mexico)
- Combine all INTL CSV files
- Add enrichment scores
- Generate summary report
- Upload to DepotChaos
"""

import csv
import json
import glob
import os
from datetime import datetime

DATA_DIR = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated"
OUTPUT_FILE = f"{DATA_DIR}/INTL_MASTER_MERGED_2026-05-07.csv"
REPORT_FILE = f"{DATA_DIR}/INTL_REPORT_2026-05-07.json"

REGION_MAP = {
    "INTL_canada_ontario.csv": {"region": "Canada", "sub_region": "Ontario", "cities": "Toronto"},
    "INTL_canada_quebec.csv": {"region": "Canada", "sub_region": "Quebec", "cities": "Montreal"},
    "INTL_canada_bc.csv": {"region": "Canada", "sub_region": "British Columbia", "cities": "Vancouver"},
    "INTL_canada_alberta.csv": {"region": "Canada", "sub_region": "Alberta", "cities": "Calgary, Edmonton"},
    "INTL_canada_manitoba.csv": {"region": "Canada", "sub_region": "Manitoba", "cities": "Winnipeg"},
    "INTL_canada_saskatchewan.csv": {"region": "Canada", "sub_region": "Saskatchewan", "cities": "Regina, Saskatoon"},
    "INTL_canada_novascotia.csv": {"region": "Canada", "sub_region": "Nova Scotia", "cities": "Halifax"},
    "INTL_canada_newbrunswick.csv": {"region": "Canada", "sub_region": "New Brunswick", "cities": "Fredericton, Moncton, Saint John"},
    "INTL_mexico_cdmx.csv": {"region": "Mexico", "sub_region": "Ciudad de México", "cities": "Mexico City"},
    "INTL_mexico_jalisco.csv": {"region": "Mexico", "sub_region": "Jalisco", "cities": "Guadalajara"},
    "INTL_mexico_nuevoleon.csv": {"region": "Mexico", "sub_region": "Nuevo León", "cities": "Monterrey"},
    "INTL_mexico_bajacalifornia.csv": {"region": "Mexico", "sub_region": "Baja California", "cities": "Tijuana, Mexicali"},
    "INTL_mexico_chihuahua.csv": {"region": "Mexico", "sub_region": "Chihuahua", "cities": "Chihuahua City, Ciudad Juárez"},
    "INTL_mexico_puebla.csv": {"region": "Mexico", "sub_region": "Puebla", "cities": "Puebla"},
    "INTL_mexico_queretaro.csv": {"region": "Mexico", "sub_region": "Querétaro", "cities": "Querétaro"},
    "INTL_mexico_veracruz.csv": {"region": "Mexico", "sub_region": "Veracruz", "cities": "Veracruz, Xalapa"},
}

def calculate_lead_score(lead):
    """Calculate enrichment score 0-100"""
    score = 50  # Base score
    
    # Boost for complete data
    if lead.get('phone') and len(lead.get('phone', '')) > 8:
        score += 15
    if lead.get('address') and len(lead.get('address', '')) > 5:
        score += 10
    if lead.get('category'):
        score += 10
    
    # Industry weighting (POS-relevant industries)
    pos_industries = ['Retail', 'Restaurants', 'Food Services', 'Comercio', 'Restaurantes', 
                      'Food', 'Alimentos', 'Tourism', 'Turismo', 'Hospitality']
    category = lead.get('category', '')
    if any(ind.lower() in category.lower() for ind in pos_industries):
        score += 15
    
    return min(score, 100)

def normalize_lead(row, region_info):
    """Normalize lead data to common schema"""
    normalized = {
        'business_name': row.get('business_name', ''),
        'category': row.get('category', ''),
        'address': row.get('address', ''),
        'city': row.get('city', ''),
        'province_state': row.get('province', row.get('state', '')),
        'postal_code': row.get('postal_code', ''),
        'phone': row.get('phone', ''),
        'country': row.get('country', ''),
        'source': row.get('source', ''),
        'date_scraped': row.get('date_scraped', ''),
        'region': region_info['region'],
        'sub_region': region_info['sub_region'],
        'cities': region_info['cities'],
        'naics_code': row.get('naics_code', ''),
        'tax_id': row.get('rfc', ''),  # Mexico uses RFC
        'employee_count': row.get('employee_count', ''),
        'status': row.get('status', ''),
    }
    return normalized

def merge_and_enrich():
    """Merge all INTL CSVs and enrich data"""
    all_leads = []
    region_stats = {}
    
    csv_files = glob.glob(f"{DATA_DIR}/INTL_*.csv")
    
    for filepath in csv_files:
        filename = os.path.basename(filepath)
        if 'MASTER' in filename or 'REPORT' in filename:
            continue
            
        region_info = REGION_MAP.get(filename, {"region": "Unknown", "sub_region": "Unknown", "cities": ""})
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalize the lead
                normalized = normalize_lead(row, region_info)
                
                # Calculate lead score
                normalized['lead_score'] = calculate_lead_score(normalized)
                normalized['enriched_date'] = datetime.now().isoformat()
                
                all_leads.append(normalized)
        
        # Count will be calculated after processing
        key = f"{region_info['region']} - {region_info['sub_region']}"
        region_stats[key] = {
            "file": filename,
            "count": 0,  # Will update after processing
            "cities": region_info['cities']
        }
    
    # Write merged file
    if all_leads:
        fieldnames = list(all_leads[0].keys())
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_leads)
    
    # Calculate totals per region
    canada_count = len([l for l in all_leads if l['region'] == 'Canada'])
    mexico_count = len([l for l in all_leads if l['region'] == 'Mexico'])
    
    # Update region stats counts
    for key in region_stats:
        region, sub = key.split(" - ", 1)
        region_stats[key]['count'] = len([l for l in all_leads if l['sub_region'] == sub])
    
    report = {
        "scrape_date": datetime.now().isoformat(),
        "total_leads": len(all_leads),
        "regions": {
            "Canada": {
                "total": canada_count,
                "provinces": {}
            },
            "Mexico": {
                "total": mexico_count,
                "states": {}
            }
        },
        "files_processed": len([f for f in csv_files if 'MASTER' not in f and 'REPORT' not in f]),
        "merged_file": OUTPUT_FILE
    }
    
    # Add per-province/state counts
    for key, info in region_stats.items():
        region, sub = key.split(" - ", 1)
        if region == "Canada":
            report["regions"]["Canada"]["provinces"][sub] = info
        else:
            report["regions"]["Mexico"]["states"][sub] = info
    
    with open(REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=2)
    
    return len(all_leads), canada_count, mexico_count, report

if __name__ == "__main__":
    print(f"[{datetime.now()}] Starting international lead enrichment...")
    total, canada, mexico, report = merge_and_enrich()
    print(f"[{datetime.now()}] ✓ Enrichment complete!")
    print(f"   Total leads: {total}")
    print(f"   Canada: {canada}")
    print(f"   Mexico: {mexico}")
    print(f"   Merged file: {OUTPUT_FILE}")
    print(f"   Report file: {REPORT_FILE}")
