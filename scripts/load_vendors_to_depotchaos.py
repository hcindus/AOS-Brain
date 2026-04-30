#!/usr/bin/env python3
"""
Load vendor data from email attachments into DepotChaos database.
Extracts vendor names, phone numbers, emails, and addresses.
"""

import pandas as pd
import sqlite3
import os
import re
import json
from datetime import datetime
from pathlib import Path

# Source files
VENDOR_ATTACHMENTS_DIR = "/root/.openclaw/workspace/data/vendor_attachments"

# Target databases
DEPOTCHAOS_DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
DATADEPOT_DB = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/database/datadepot.db"

def ensure_vendor_tables(conn):
    """Create vendor tables if they don't exist."""
    cursor = conn.cursor()
    
    # Main vendors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dba_name TEXT,
            contact_name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            territory TEXT,
            vendor_type TEXT,
            status TEXT DEFAULT 'active',
            source_file TEXT,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_contact_at TIMESTAMP,
            notes TEXT
        )
    """)
    
    # Vendor interactions tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendor_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id INTEGER,
            interaction_type TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vendor_id) REFERENCES vendors(id)
        )
    """)
    
    conn.commit()
    print("✅ Vendor tables ready")

def extract_phone_numbers(text):
    """Extract phone numbers from text."""
    if pd.isna(text):
        return None
    text = str(text)
    # Match various phone formats
    patterns = [
        r'(\d{3})[-.]?(\d{3})[-.]?(\d{4})',
        r'\((\d{3})\)\s*(\d{3})[-.]?(\d{4})',
        r'(\d{3})\s+(\d{3})\s+(\d{4})',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return '-'.join(matches[0])
    return None

def extract_emails(text):
    """Extract emails from text."""
    if pd.isna(text):
        return None
    text = str(text)
    pattern = r'[\w.+-]+@[\w-]+\.[\w.-]+'
    matches = re.findall(pattern, text)
    return matches[0] if matches else None

def process_pendo_file(filepath):
    """Process Pendo Excel files - these contain customer/vendor data."""
    vendors = []
    try:
        df = pd.read_excel(filepath, header=None)
        filename = os.path.basename(filepath)
        
        # Pendo files have date in first column
        # Look for rows with business info
        for idx, row in df.iterrows():
            row_data = row.dropna().astype(str).tolist()
            if len(row_data) >= 3:
                # Try to extract business info
                potential_name = str(row_data[1]) if len(row_data) > 1 else None
                potential_contact = str(row_data[2]) if len(row_data) > 2 else None
                
                if potential_name and len(potential_name) > 2:
                    # Skip header rows
                    if 'customer' in potential_name.lower() or 'name' in potential_name.lower():
                        continue
                    
                    vendor = {
                        'name': potential_name.strip(),
                        'contact_name': potential_contact.strip() if potential_contact else None,
                        'phone': extract_phone_numbers(' '.join(row_data)),
                        'email': extract_emails(' '.join(row_data)),
                        'address': None,
                        'city': None,
                        'state': None,
                        'zip': None,
                        'source_file': filename,
                        'vendor_type': 'customer'
                    }
                    vendors.append(vendor)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    
    return vendors

def process_client_file(filepath):
    """Process Client Excel files."""
    vendors = []
    try:
        df = pd.read_excel(filepath, header=None)
        filename = os.path.basename(filepath)
        
        # Look for address patterns and business names
        for idx, row in df.iterrows():
            row_text = ' '.join(row.dropna().astype(str).tolist())
            
            # Look for address patterns (contains Suite, Ave, St, etc.)
            if any(x in row_text.lower() for x in ['suite', 'st', 'ave', 'blvd', 'rd', 'dr']):
                # This might be an address line
                # Try to find associated business name from previous rows
                vendor = {
                    'name': None,  # Will need manual extraction
                    'address': row_text.strip(),
                    'phone': extract_phone_numbers(row_text),
                    'email': extract_emails(row_text),
                    'source_file': filename,
                    'vendor_type': 'client'
                }
                vendors.append(vendor)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    
    return vendors

def process_po_file(filepath):
    """Process PO files for vendor information."""
    vendors = []
    try:
        df = pd.read_excel(filepath, header=None)
        filename = os.path.basename(filepath)
        
        # PO files often have vendor names
        for idx, row in df.iterrows():
            row_data = row.dropna().astype(str).tolist()
            for cell in row_data:
                cell_str = str(cell)
                # Look for company indicators
                if any(x in cell_str.lower() for x in ['llc', 'inc', 'corp', 'ltd', 'company']):
                    vendor = {
                        'name': cell_str.strip(),
                        'phone': extract_phone_numbers(' '.join(row_data)),
                        'email': extract_emails(' '.join(row_data)),
                        'source_file': filename,
                        'vendor_type': 'supplier'
                    }
                    vendors.append(vendor)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    
    return vendors

def load_vendors_to_db(vendors, conn):
    """Load extracted vendors into database."""
    cursor = conn.cursor()
    inserted = 0
    skipped = 0
    
    for vendor in vendors:
        # Skip if no name
        if not vendor.get('name'):
            skipped += 1
            continue
        
        try:
            cursor.execute("""
                INSERT INTO vendors 
                (name, dba_name, contact_name, phone, email, address, city, state, zip, 
                 territory, vendor_type, status, source_file, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                vendor.get('name'),
                vendor.get('dba_name'),
                vendor.get('contact_name'),
                vendor.get('phone'),
                vendor.get('email'),
                vendor.get('address'),
                vendor.get('city'),
                vendor.get('state'),
                vendor.get('zip'),
                vendor.get('territory'),
                vendor.get('vendor_type', 'unknown'),
                'active',
                vendor.get('source_file'),
                json.dumps(vendor) if vendor else None
            ))
            inserted += 1
        except sqlite3.IntegrityError:
            skipped += 1
    
    conn.commit()
    return inserted, skipped

def main():
    print("=" * 60)
    print("DepotChaos Vendor Data Loader")
    print("=" * 60)
    
    # Connect to DepotChaos database
    conn = sqlite3.connect(DEPOTCHAOS_DB)
    ensure_vendor_tables(conn)
    
    # Process all files
    total_vendors = []
    files_processed = 0
    
    for filename in os.listdir(VENDOR_ATTACHMENTS_DIR):
        filepath = os.path.join(VENDOR_ATTACHMENTS_DIR, filename)
        
        if 'Pendo' in filename:
            vendors = process_pendo_file(filepath)
            total_vendors.extend(vendors)
            files_processed += 1
            print(f"📄 {filename}: {len(vendors)} records")
        elif 'Client' in filename or 'client' in filename.lower():
            vendors = process_client_file(filepath)
            total_vendors.extend(vendors)
            files_processed += 1
            print(f"📄 {filename}: {len(vendors)} records")
        elif any(x in filename for x in ['PO', 'po', 'purchase']):
            vendors = process_po_file(filepath)
            total_vendors.extend(vendors)
            files_processed += 1
            print(f"📄 {filename}: {len(vendors)} records")
    
    print(f"\n📊 Total records extracted: {len(total_vendors)}")
    print(f"📁 Files processed: {files_processed}")
    
    # Load into database
    inserted, skipped = load_vendors_to_db(total_vendors, conn)
    
    print(f"\n✅ Inserted: {inserted}")
    print(f"⏭️  Skipped: {skipped}")
    
    # Show summary
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM vendors")
    total_in_db = cursor.fetchone()[0]
    
    cursor.execute("SELECT vendor_type, COUNT(*) FROM vendors GROUP BY vendor_type")
    by_type = cursor.fetchall()
    
    print(f"\n📈 Database Summary:")
    print(f"   Total vendors: {total_in_db}")
    for vtype, count in by_type:
        print(f"   - {vtype}: {count}")
    
    conn.close()
    print("\n✅ Vendor data loaded into DepotChaos!")

if __name__ == "__main__":
    main()
