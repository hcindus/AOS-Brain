#!/usr/bin/env python3
"""
Adapter: Convert Leads to MASTER_CLIENTS.csv Format
Maps standard lead format to Performance Supply Depot client database
"""

import pandas as pd
import os
from datetime import datetime
from pathlib import Path

# Configuration
LEADS_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/data/leads_consolidated")
OUTPUT_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/data/clients_adapted")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# MASTER_CLIENTS.csv columns (23 total)
CLIENT_COLUMNS = [
    "Client",           # Business name
    "Type",             # Service type (derived from Tags)
    "Rep",              # Sales rep (assigned)
    "System",           # POS system (if known)
    "HW_Maint",         # Hardware maintenance (YES/NO)
    "Revenue_Tracking", # Revenue number
    "Primary_Contact",  # Full name
    "Phone",            # Phone number
    "Cell",             # Cell number (same as phone)
    "Tax_Pct",          # Tax percentage
    "Tax_Pct2",         # Secondary tax
    "Tax_District",     # Tax jurisdiction
    "Store_Address",    # Street address
    "City",             # City
    "State",            # State
    "Zip",              # ZIP code
    "Email",            # Primary email
    "Ops_Email",        # Operations email
    "Billing_Email",    # Billing email
    "Notes",            # Additional notes
    "Country",          # Country code
    "Source",           # Lead source
    "Import_Date"       # When imported
]

def map_type_from_tags(tags):
    """Map tags to client Type"""
    if pd.isna(tags):
        return "UNKNOWN"
    
    tags_lower = str(tags).lower()
    
    type_mapping = {
        "realestate": "REAL ESTATE",
        "restaurant": "SUPPLY ONLY",
        "technology": "TECH",
        "manufacturing": "INDUSTRIAL",
        "finance": "FINANCE",
        "healthcare": "HEALTHCARE",
        "retail": "RETAIL",
        "agriculture": "AGRICULTURE"
    }
    
    for keyword, client_type in type_mapping.items():
        if keyword in tags_lower:
            return client_type
    
    return "GENERAL"

def map_rep_from_state(state):
    """Map state to sales rep"""
    rep_map = {
        "CA": "AH",  # California
        "TX": "LG",  # Texas
        "FL": "RA",  # Florida
        "NY": "MB",  # New York
        "WA": "DK",  # Washington
        "OR": "DK",  # Oregon
        "NV": "LG",  # Nevada
        "AZ": "LG",  # Arizona
        "ON": "AH",  # Ontario
        "BC": "AH",  # British Columbia
        "CDMX": "LG",  # Mexico City
        "JAL": "LG",  # Jalisco
    }
    return rep_map.get(str(state).upper(), "AH")  # Default to AH

def map_tax_district(state, country):
    """Map to tax district"""
    if country == "US":
        tax_map = {
            "CA": "SF",      # San Francisco
            "TX": "TEX",     # Texas
            "FL": "FLA",     # Florida
            "NY": "NYC",     # New York
            "WA": "SEA",     # Seattle
        }
        return tax_map.get(str(state).upper(), "GEN")
    elif country == "CA":
        return str(state).upper()
    elif country == "MX":
        return str(state).upper()
    return "GEN"

def get_tax_pct(state, country):
    """Get tax percentage based on location"""
    if country == "US":
        tax_rates = {
            "CA": 0.0925,    # California ~9.25%
            "TX": 0.0825,    # Texas ~8.25%
            "FL": 0.065,     # Florida ~6.5%
            "NY": 0.085,     # New York ~8.5%
            "WA": 0.065,     # Washington ~6.5%
            "NV": 0.0685,    # Nevada ~6.85%
        }
        return tax_rates.get(str(state).upper(), 0.08)
    elif country == "CA":
        return 0.13  # Ontario HST
    elif country == "MX":
        return 0.16  # Mexico IVA
    return 0.08

def adapt_lead_to_client(lead_row):
    """Convert a single lead row to client format"""
    
    # Build primary contact name
    first_name = str(lead_row.get('First Name', ''))
    last_name = str(lead_row.get('Last Name', ''))
    primary_contact = f"{first_name} {last_name}".strip()
    
    # Client name (Company)
    client = str(lead_row.get('Company', ''))
    if not client or client == 'nan':
        client = f"{first_name} {last_name} Business"
    
    # Get location data
    city = str(lead_row.get('City', ''))
    state = str(lead_row.get('State', ''))
    country = str(lead_row.get('Country', 'US'))
    
    # Map fields
    return {
        "Client": client,
        "Type": map_type_from_tags(lead_row.get('Tags', '')),
        "Rep": map_rep_from_state(state),
        "System": "",  # Unknown
        "HW_Maint": "NO",
        "Revenue_Tracking": "",
        "Primary_Contact": primary_contact,
        "Phone": str(lead_row.get('Phone', '')),
        "Cell": str(lead_row.get('Phone', '')),
        "Tax_Pct": get_tax_pct(state, country),
        "Tax_Pct2": "",
        "Tax_District": map_tax_district(state, country),
        "Store_Address": "",  # Not in leads
        "City": city,
        "State": state,
        "Zip": str(lead_row.get('Postal Code', '')),
        "Email": str(lead_row.get('Email', '')),
        "Ops_Email": "",
        "Billing_Email": "",
        "Notes": str(lead_row.get('Notes', '')),
        "Country": country,
        "Source": str(lead_row.get('Source', '')),
        "Import_Date": datetime.now().strftime("%Y-%m-%d")
    }

def process_all_leads():
    """Process all consolidated leads"""
    print("=" * 70)
    print("ADAPTER: Leads → MASTER_CLIENTS Format")
    print("=" * 70)
    print()
    
    # Find all leads files
    lead_files = [
        LEADS_DIR / "COMPLETED_ALL_STATES.csv",
        LEADS_DIR / "COMPLETED_CA_ALL.csv",
        LEADS_DIR / "COMPLETED_MX_ALL.csv"
    ]
    
    all_clients = []
    
    for leads_file in lead_files:
        if not leads_file.exists():
            print(f"⚠️ File not found: {leads_file}")
            continue
        
        print(f"Processing: {leads_file.name}")
        
        # Load leads
        df = pd.read_csv(leads_file)
        print(f"  Loaded {len(df)} leads")
        
        # Convert each row
        for _, row in df.iterrows():
            client = adapt_lead_to_client(row)
            all_clients.append(client)
        
        print(f"  ✓ Converted {len(df)} to client format")
        print()
    
    if not all_clients:
        print("❌ No leads to process")
        return
    
    # Create DataFrame
    clients_df = pd.DataFrame(all_clients)
    
    # Save master file
    output_file = OUTPUT_DIR / "ADAPTED_MASTER_CLIENTS.csv"
    clients_df.to_csv(output_file, index=False)
    print(f"✅ Saved {len(clients_df)} clients to: {output_file}")
    print()
    
    # Save by country
    for country in ['US', 'CA', 'MX']:
        country_clients = clients_df[clients_df['Country'] == country]
        if len(country_clients) > 0:
            country_file = OUTPUT_DIR / f"ADAPTED_CLIENTS_{country}.csv"
            country_clients.to_csv(country_file, index=False)
            print(f"  ✓ {country}: {len(country_clients)} clients → {country_file.name}")
    
    # Summary
    print()
    print("=" * 70)
    print("ADAPTATION COMPLETE")
    print("=" * 70)
    print(f"Total clients adapted: {len(clients_df)}")
    print(f"Countries: {clients_df['Country'].nunique()}")
    print(f"Client types: {clients_df['Type'].nunique()}")
    print()
    print(f"Output location: {OUTPUT_DIR}")
    print()
    print("Next steps:")
    print("  1. Review ADAPTED_MASTER_CLIENTS.csv")
    print("  2. Compare to existing MASTER_CLIENTS.csv")
    print("  3. Merge if format matches")
    print()

def main():
    process_all_leads()

if __name__ == "__main__":
    main()
