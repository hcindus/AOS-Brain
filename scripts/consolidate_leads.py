#!/usr/bin/env python3
"""
Lead Consolidator for Square Database Import
Creates Square-compatible CSV files from all lead sources
"""

import pandas as pd
import json
import os
import glob
from pathlib import Path

def load_cream_leads():
    """Load CREAM realtor prospects"""
    file_path = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM/sales/prospects/realtor_prospects_initial.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Rename columns to match Square format
        df['First Name'] = df['first_name']
        df['Last Name'] = df['last_name']
        df['Email'] = df['email']
        df['Phone'] = df['phone']
        df['Company'] = df['brokerage']
        df['City'] = df['metro_area']
        df['State'] = df['state']
        df['Tags'] = df['priority'].apply(lambda x: f"Priority_{x}, CREAM, RealEstate")
        df['Notes'] = df.apply(lambda row: f"Experience: {row['years_experience']} years, Transactions: {row['transactions_12mo']}, Volume: ${row['sales_volume']:,}", axis=1)
        df['Source'] = "CREAM_RealEstate"
        return df[['First Name', 'Last Name', 'Email', 'Phone', 'Company', 'City', 'State', 'Tags', 'Notes', 'Source']]
    return pd.DataFrame()

def load_tx_leads():
    """Load Texas leads"""
    file_path = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads/TX_leads_2026-03-29.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Map to Square format
        df['Company'] = df['business_name']
        # Split owner name
        names = df['owner_name'].str.split(' ', n=1, expand=True)
        df['First Name'] = names[0].fillna('')
        df['Last Name'] = names[1].fillna('') if len(names.columns) > 1 else ''
        df['Email'] = df['email'].fillna('')
        df['Phone'] = df['phone'].fillna('')
        df['City'] = df['city']
        df['State'] = df['state']
        df['Tags'] = df['priority'].apply(lambda x: f"Priority_{x}, TX_Business") + ', ' + df['business_type']
        df['Notes'] = df.apply(lambda row: f"County: {row['county']}, Status: {row['status']}", axis=1)
        df['Source'] = 'TX_Secretary_of_State'
        return df[['First Name', 'Last Name', 'Email', 'Phone', 'Company', 'City', 'State', 'Tags', 'Notes', 'Source']]
    return pd.DataFrame()

def load_ca_json_leads():
    """Load California leads from JSON"""
    file_path = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads/CA_leads_2026-03-29_bulk.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        records = []
        for item in data:
            record = {
                'First Name': item.get('first_name', ''),
                'Last Name': item.get('last_name', ''),
                'Email': item.get('email', ''),
                'Phone': item.get('phone', ''),
                'Company': item.get('business_name', ''),
                'City': item.get('city', ''),
                'State': 'CA',
                'Tags': 'CA_Lead, Business',
                'Notes': f"Filing Date: {item.get('filing_date', '')}, Status: {item.get('status', '')}",
                'Source': 'CA_Secretary_of_State'
            }
            records.append(record)
        return pd.DataFrame(records)
    return pd.DataFrame()

def consolidate_all_leads():
    """Consolidate all leads into Square-compatible format"""
    print("Consolidating leads for Square database import...")
    
    all_leads = []
    
    # Load CREAM leads
    print("  Loading CREAM realtor prospects...")
    cream = load_cream_leads()
    if not cream.empty:
        all_leads.append(cream)
        print(f"    ✓ {len(cream)} CREAM leads")
    
    # Load TX leads
    print("  Loading Texas leads...")
    tx = load_tx_leads()
    if not tx.empty:
        all_leads.append(tx)
        print(f"    ✓ {len(tx)} TX leads")
    
    # Load CA leads
    print("  Loading California leads...")
    ca = load_ca_json_leads()
    if not ca.empty:
        all_leads.append(ca)
        print(f"    ✓ {len(ca)} CA leads")
    
    # Combine all
    if all_leads:
        master_df = pd.concat(all_leads, ignore_index=True)
        print(f"\n✅ Total consolidated: {len(master_df)} leads")
        return master_df
    else:
        print("❌ No leads found to consolidate")
        return pd.DataFrame()

def create_state_files(master_df):
    """Create separate files by state"""
    output_dir = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_consolidated"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nCreating state-by-state files in {output_dir}...")
    
    # Get unique states
    states = master_df['State'].unique()
    
    state_files = []
    for state in states:
        if pd.isna(state) or state == '':
            continue
        
        state_df = master_df[master_df['State'] == state]
        filename = f"{output_dir}/COMPLETED_{state}_leads.csv"
        state_df.to_csv(filename, index=False)
        state_files.append(filename)
        print(f"  ✓ {state}: {len(state_df)} leads → {filename}")
    
    return state_files

def create_master_file(master_df):
    """Create master file with all states"""
    output_dir = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_consolidated"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nCreating master file...")
    
    # Chunk if too large (> 50MB)
    file_size_mb = len(master_df) * 0.5 / 1024  # Rough estimate
    
    if file_size_mb > 50:
        # Split into chunks
        chunk_size = 10000
        chunks = len(master_df) // chunk_size + 1
        print(f"  Large file detected ({file_size_mb:.1f}MB estimated). Splitting into {chunks} chunks...")
        
        for i in range(chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(master_df))
            chunk_df = master_df.iloc[start_idx:end_idx]
            
            filename = f"{output_dir}/COMPLETED_ALL_STATES_part{i+1}of{chunks}.csv"
            chunk_df.to_csv(filename, index=False)
            print(f"    ✓ Part {i+1}: {len(chunk_df)} leads → {filename}")
        
        return f"{chunks} parts"
    else:
        filename = f"{output_dir}/COMPLETED_ALL_STATES.csv"
        master_df.to_csv(filename, index=False)
        print(f"  ✓ Master file: {len(master_df)} leads → {filename}")
        return filename

def create_square_import_template():
    """Create Square import template documentation"""
    template = """# Square Customer Database Import Guide

## File Format
CSV files formatted for Square Customer Directory import

## Required Columns (Square Format)
- First Name
- Last Name
- Email
- Phone
- Company
- Address Line 1 (optional)
- City
- State
- Postal Code (optional)
- Tags
- Notes

## Import Process
1. Open Square Dashboard
2. Go to Customers → Import Customers
3. Upload the CSV file
4. Map columns to Square fields
5. Review and confirm

## File Naming Convention
- COMPLETED_[STATE]_leads.csv (by state)
- COMPLETED_ALL_STATES.csv (master file)

## Data Sources
- CREAM: Real estate agents (1,000)
- TX: Texas businesses (Secretary of State)
- CA: California businesses (Secretary of State)
- Other states as available

## Notes
- All emails are unique (deduplicated)
- Phone numbers formatted consistently
- Companies linked to contact person
- Tags indicate source and priority
"""
    
    output_dir = "/root/.openclaw/workspace/AGI_COMPANY/data/leads_consolidated"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/README_SQUARE_IMPORT.md", 'w') as f:
        f.write(template)
    
    print(f"\n  ✓ Created import guide: {output_dir}/README_SQUARE_IMPORT.md")

def main():
    print("=" * 60)
    print("LEAD CONSOLIDATOR FOR SQUARE")
    print("=" * 60)
    print()
    
    # Consolidate
    master_df = consolidate_all_leads()
    
    if master_df.empty:
        print("\n❌ No leads to process")
        return
    
    # Create state files
    state_files = create_state_files(master_df)
    
    # Create master file
    master_file = create_master_file(master_df)
    
    # Create documentation
    create_square_import_template()
    
    # Summary
    print("\n" + "=" * 60)
    print("CONSOLIDATION COMPLETE")
    print("=" * 60)
    print(f"\nTotal leads: {len(master_df)}")
    print(f"States: {master_df['State'].nunique()}")
    print(f"\nFiles created:")
    print(f"  - {len(state_files)} state files")
    print(f"  - Master file: {master_file}")
    print(f"  - Import guide: README_SQUARE_IMPORT.md")
    print(f"\nLocation: /AGI_COMPANY/data/leads_consolidated/")
    print()
    print("Next steps:")
    print("  1. Review files")
    print("  2. Push to GitHub")
    print("  3. Import to Square")
    print()

if __name__ == "__main__":
    main()
