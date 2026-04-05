#!/usr/bin/env python3
"""
AI Enrichment Pipeline for Leads
- Validate emails
- Score leads (Priority A/B/C)
- Deduplicate
- Merge with existing data
"""

import csv
import re
import hashlib
from pathlib import Path
from collections import defaultdict

INPUT_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/data/leads_county_level")
OUTPUT_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/data/leads_enriched")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EXISTING_LEADS = Path("/root/.openclaw/workspace/AGI_COMPANY/data/leads_consolidated/COMPLETED_ALL_STATES.csv")

def validate_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def score_lead(lead):
    """Score lead based on population"""
    try:
        # Extract population from Notes field
        pop_str = lead.get('Notes', '').split('Pop: ')[1].split(',')[0]
        population = int(pop_str.replace(',', ''))
        
        if population > 2000000:
            return 'A'  # Major metro
        elif population > 1000000:
            return 'B'  # Large metro
        else:
            return 'C'  # Medium metro
    except:
        return 'C'  # Default

def get_lead_hash(lead):
    """Generate hash for deduplication"""
    key = f"{lead['Email']}|{lead['Phone']}"
    return hashlib.md5(key.encode()).hexdigest()

def load_county_leads():
    """Load all county-level leads"""
    leads = []
    master_file = INPUT_DIR / "COUNTY_MASTER_ALL.csv"
    
    if master_file.exists():
        with open(master_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append(row)
    
    return leads

def load_existing_leads():
    """Load existing state-level leads"""
    leads = []
    
    if EXISTING_LEADS.exists():
        with open(EXISTING_LEADS, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Add source tag
                row['Tags'] = row.get('Tags', '') + ', State_Level'
                row['County'] = 'N/A'
                leads.append(row)
    
    return leads

def enrich_leads(leads):
    """Enrich leads with validation and scoring"""
    enriched = []
    validation_stats = {'valid': 0, 'invalid': 0}
    score_stats = {'A': 0, 'B': 0, 'C': 0}
    
    for lead in leads:
        # Validate email
        email_valid = validate_email(lead.get('Email', ''))
        if email_valid:
            validation_stats['valid'] += 1
        else:
            validation_stats['invalid'] += 1
            lead['Tags'] = lead.get('Tags', '') + ', Invalid_Email'
        
        # Score lead
        priority = score_lead(lead)
        lead['Priority'] = priority
        score_stats[priority] += 1
        
        # Add validation flag
        lead['Email_Valid'] = 'Yes' if email_valid else 'No'
        
        enriched.append(lead)
    
    return enriched, validation_stats, score_stats

def deduplicate_leads(leads):
    """Remove duplicates based on email+phone hash"""
    seen = set()
    unique = []
    duplicates = 0
    
    for lead in leads:
        lead_hash = get_lead_hash(lead)
        if lead_hash not in seen:
            seen.add(lead_hash)
            unique.append(lead)
        else:
            duplicates += 1
    
    return unique, duplicates

def save_enriched_leads(leads, validation_stats, score_stats):
    """Save enriched leads"""
    # Master enriched file
    master_file = OUTPUT_DIR / "ENRICHED_MASTER.csv"
    with open(master_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['First Name', 'Last Name', 'Email', 'Phone', 'Company', 
                     'City', 'County', 'State', 'Country', 'Priority', 'Email_Valid', 
                     'Tags', 'Notes', 'Source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for lead in leads:
            # Only write selected fields
            row = {k: lead.get(k, '') for k in fieldnames}
            writer.writerow(row)
    
    # Priority files
    for priority in ['A', 'B', 'C']:
        priority_leads = [l for l in leads if l.get('Priority') == priority]
        if priority_leads:
            file_path = OUTPUT_DIR / f"PRIORITY_{priority}_LEADS.csv"
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = list(priority_leads[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(priority_leads)
    
    # Validation report
    report_file = OUTPUT_DIR / "ENRICHMENT_REPORT.txt"
    with open(report_file, 'w') as f:
        f.write("AI ENRICHMENT REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total Leads Processed: {len(leads)}\n\n")
        f.write("Email Validation:\n")
        f.write(f"  Valid: {validation_stats['valid']}\n")
        f.write(f"  Invalid: {validation_stats['invalid']}\n")
        f.write(f"  Valid Rate: {validation_stats['valid']/len(leads)*100:.1f}%\n\n")
        f.write("Lead Scoring:\n")
        f.write(f"  Priority A (Major Metro): {score_stats['A']}\n")
        f.write(f"  Priority B (Large Metro): {score_stats['B']}\n")
        f.write(f"  Priority C (Medium Metro): {score_stats['C']}\n")

def main():
    print("=" * 60)
    print("AI ENRICHMENT PIPELINE")
    print("=" * 60)
    print()
    
    # Load data
    print("Loading leads...")
    county_leads = load_county_leads()
    print(f"  County-level leads: {len(county_leads)}")
    
    existing_leads = load_existing_leads()
    print(f"  Existing state-level leads: {len(existing_leads)}")
    
    # Merge
    print("\nMerging datasets...")
    all_leads = county_leads + existing_leads
    print(f"  Total before enrichment: {len(all_leads)}")
    
    # Enrich
    print("\nEnriching leads (AI processing)...")
    enriched_leads, validation_stats, score_stats = enrich_leads(all_leads)
    print(f"  Valid emails: {validation_stats['valid']}")
    print(f"  Invalid emails: {validation_stats['invalid']}")
    print(f"  Priority A: {score_stats['A']}")
    print(f"  Priority B: {score_stats['B']}")
    print(f"  Priority C: {score_stats['C']}")
    
    # Deduplicate
    print("\nDeduplicating...")
    unique_leads, duplicates = deduplicate_leads(enriched_leads)
    print(f"  Removed {duplicates} duplicates")
    print(f"  Unique leads: {len(unique_leads)}")
    
    # Save
    print("\nSaving enriched leads...")
    save_enriched_leads(unique_leads, validation_stats, score_stats)
    print(f"  ✓ Saved to: {OUTPUT_DIR}")
    
    # Summary
    print("\n" + "=" * 60)
    print("ENRICHMENT COMPLETE")
    print("=" * 60)
    print(f"Final lead count: {len(unique_leads)}")
    print(f"Quality: {(validation_stats['valid']/len(all_leads)*100):.1f}% valid emails")
    print("\nOutput files:")
    print("  - ENRICHED_MASTER.csv (all leads)")
    print("  - PRIORITY_A_LEADS.csv (major metros)")
    print("  - PRIORITY_B_LEADS.csv (large metros)")
    print("  - PRIORITY_C_LEADS.csv (medium metros)")
    print("  - ENRICHMENT_REPORT.txt")
    print()

if __name__ == "__main__":
    main()
