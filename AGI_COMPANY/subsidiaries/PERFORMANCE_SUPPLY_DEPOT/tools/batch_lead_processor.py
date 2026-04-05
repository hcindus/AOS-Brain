#!/usr/bin/env python3
"""
Batch Lead Enrichment Processor
Processes all PSD lead files and generates *_COMPLETED.xlsx outputs
"""

import os
import sys
import glob
from pathlib import Path
import pandas as pd

sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/tools')

from lead_enrichment_system import Lead, Planner, EnrichmentPipeline

LEADS_DIR = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads"
OUTPUT_DIR = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads/completed"

def extract_county_from_filename(filename: str) -> str:
    """Extract county name from filename like 'Adams_WA_County_Leads.xlsx'"""
    base = Path(filename).stem
    parts = base.replace('_County_Leads', '').split('_')
    
    # Handle different naming patterns
    if len(parts) >= 2:
        # Adams_WA or CA_Santa_Barbara
        if parts[0] in ['CA', 'WA', 'OR'] and len(parts) > 2:
            return ' '.join(parts[1:])
        else:
            return parts[0]
    return ""

def extract_state_from_filename(filename: str) -> str:
    """Extract state from filename"""
    base = Path(filename).stem
    if '_WA_' in base:
        return 'WA'
    elif '_OR_' in base:
        return 'OR'
    elif 'CA_' in base:
        return 'CA'
    return ""

def process_excel_file(filepath: str, planner: Planner, pipeline: EnrichmentPipeline) -> str:
    """Process a single Excel file and generate _COMPLETED version"""
    filename = os.path.basename(filepath)
    print(f"\n{'='*70}")
    print(f"Processing: {filename}")
    print(f"{'='*70}")
    
    try:
        # Read Excel
        df = pd.read_excel(filepath)
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
        
        # Detect column mapping
        col_mapping = {}
        for col in df.columns:
            col_lower = str(col).lower()
            if 'business' in col_lower or 'name' in col_lower:
                col_mapping['business_name'] = col
            elif 'city' in col_lower:
                col_mapping['city'] = col
            elif 'state' in col_lower:
                col_mapping['state'] = col
            elif 'zip' in col_lower:
                col_mapping['zip'] = col
            elif 'county' in col_lower:
                col_mapping['county'] = col
            elif 'address' in col_lower:
                col_mapping['address'] = col
            elif 'phone' in col_lower:
                col_mapping['phone'] = col
            elif 'email' in col_lower:
                col_mapping['email'] = col
        
        print(f"  Mapping: {col_mapping}")
        
        # Ensure output columns exist
        if 'Address' not in df.columns:
            df['Address'] = ""
        if 'Phone' not in df.columns:
            df['Phone'] = ""
        if 'Email' not in df.columns:
            df['Email'] = ""
        
        # Get state/county from filename
        file_state = extract_state_from_filename(filename)
        file_county = extract_county_from_filename(filename)
        
        # Process each row
        enriched_count = 0
        for idx, row in df.iterrows():
            business = str(row.get(col_mapping.get('business_name', 'Business Name'), '')).strip()
            if business and business != 'nan':
                city = str(row.get(col_mapping.get('city', 'City'), '')).strip()
                state = str(row.get(col_mapping.get('state', 'State'), file_state)).strip()
                zip_code = str(row.get(col_mapping.get('zip', 'Zip'), '')).strip()
                county = str(row.get(col_mapping.get('county', 'County'), file_county)).strip()
                
                if not business or business.lower() in ['nan', 'none', '']:
                    continue
                
                print(f"  [{idx+1}/{len(df)}] {business[:40]}...", end=" ")
                
                # Create lead
                lead = Lead(
                    business_name=business,
                    city=city if city and city != 'nan' else "",
                    state=state if state and state != 'nan' else file_state,
                    zip=zip_code if zip_code and zip_code != 'nan' else "",
                    county=county if county and county != 'nan' else ""
                )
                
                # Run enrichment (simplified - no real browser)
                result = pipeline.process_lead(lead)
                
                # Update dataframe
                if result.get('address'):
                    df.at[idx, 'Address'] = result['address']
                if result.get('phone'):
                    df.at[idx, 'Phone'] = result['phone']
                if result.get('email'):
                    df.at[idx, 'Email'] = result['email']
                    enriched_count += 1
                
                if result.get('enriched'):
                    print("✓")
                else:
                    print("○")
        
        # Generate output filename
        base, ext = os.path.splitext(filename)
        output_name = f"{base}_COMPLETED{ext}"
        output_path = os.path.join(OUTPUT_DIR, output_name)
        
        # Save
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        df.to_excel(output_path, index=False)
        
        print(f"\n  ✓ Saved: {output_name}")
        print(f"  ✓ Enriched: {enriched_count}/{len(df)}")
        
        return output_path
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return ""

def main():
    """Process all lead files"""
    print("=" * 70)
    print("BATCH LEAD ENRICHMENT PROCESSOR")
    print("=" * 70)
    print(f"\nInput: {LEADS_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    
    # Find all xlsx files
    pattern = os.path.join(LEADS_DIR, "*.xlsx")
    files = glob.glob(pattern)
    
    # Exclude already completed and enriched files
    files = [f for f in files if '_COMPLETED' not in f and 'enriched' not in f.lower()]
    
    print(f"\nFound {len(files)} files to process")
    
    if not files:
        print("No files found!")
        return
    
    # Initialize enrichment
    planner = Planner()
    pipeline = EnrichmentPipeline(planner)
    
    # Process each file
    completed = []
    for filepath in files[:10]:  # Process first 10 for demo
        output = process_excel_file(filepath, planner, pipeline)
        if output:
            completed.append(output)
    
    # Summary
    print("\n" + "=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)
    print(f"Files processed: {len(completed)}")
    print(f"\nCompleted files:")
    for f in completed:
        print(f"  • {os.path.basename(f)}")

if __name__ == "__main__":
    main()
