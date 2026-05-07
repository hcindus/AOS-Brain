#!/usr/bin/env python3
"""
California ABC License Scraper
Scrapes active ABC license holders for specific license types across all 58 California counties
"""

import requests
import csv
import json
import sqlite3
import time
import zipfile
import io
from datetime import datetime
from pathlib import Path
import re

# Configuration
OUTPUT_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated")
DB_PATH = Path("/root/.openclaw/workspace/data/depot_chaos/unified.db")

# License types to scrape
TARGET_LICENSE_TYPES = {
    '41': 'On-Sale Beer & Wine - Eating Place',
    '47': 'On-Sale General - Restaurant', 
    '48': 'On-Sale General - Bar/Tavern',
    '20': 'Off-Sale Beer & Wine',
    '21': 'Off-Sale General',
    '58': "Caterer's Beer & Wine",
    '75': 'Event Permit Holder'
}

# All 58 California counties
CALIFORNIA_COUNTIES = [
    'Alameda', 'Alpine', 'Amador', 'Butte', 'Calaveras', 'Colusa', 'Contra Costa',
    'Del Norte', 'El Dorado', 'Fresno', 'Glenn', 'Humboldt', 'Imperial', 'Inyo',
    'Kern', 'Kings', 'Lake', 'Lassen', 'Los Angeles', 'Madera', 'Marin',
    'Mariposa', 'Mendocino', 'Merced', 'Modoc', 'Mono', 'Monterey', 'Napa',
    'Nevada', 'Orange', 'Placer', 'Plumas', 'Riverside', 'Sacramento', 'San Benito',
    'San Bernardino', 'San Diego', 'San Francisco', 'San Joaquin', 'San Luis Obispo',
    'San Mateo', 'Santa Barbara', 'Santa Clara', 'Santa Cruz', 'Shasta', 'Sierra',
    'Siskiyou', 'Solano', 'Sonoma', 'Stanislaus', 'Sutter', 'Tehama', 'Trinity',
    'Tulare', 'Tuolumne', 'Ventura', 'Yolo', 'Yuba'
]

# ABC Weekly Data Export URL (publicly available)
ABC_DATA_EXPORT_URL = "https://www.abc.ca.gov/wp-content/uploads/weekly-data-export/weekly_export.zip"


def download_abc_data():
    """Download the ABC weekly data export"""
    print("[*] Downloading ABC weekly data export...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(ABC_DATA_EXPORT_URL, headers=headers, timeout=60)
        response.raise_for_status()
        print(f"[*] Downloaded {len(response.content)} bytes")
        return response.content
    except Exception as e:
        print(f"[!] Error downloading ABC data: {e}")
        return None


def extract_csv_from_zip(zip_content):
    """Extract CSV data from the downloaded zip file"""
    try:
        with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
            csv_files = [f for f in z.namelist() if f.endswith('.csv')]
            if not csv_files:
                print("[!] No CSV files found in zip")
                return None
            
            # Read the first CSV file
            with z.open(csv_files[0]) as f:
                content = f.read().decode('utf-8', errors='ignore')
                return content
    except Exception as e:
        print(f"[!] Error extracting zip: {e}")
        return None


def parse_abc_csv(csv_content):
    """Parse ABC CSV data and extract license information"""
    licenses = []
    lines = csv_content.strip().split('\n')
    
    if not lines:
        return licenses
    
    # Parse header
    reader = csv.DictReader(lines)
    
    for row in reader:
        try:
            license_type = row.get('License_Type', '').strip()
            status = row.get('Status', '').strip().upper()
            
            # Filter for target license types and active status
            if license_type in TARGET_LICENSE_TYPES and status == 'ACTIVE':
                license_data = {
                    'license_number': row.get('License_Number', ''),
                    'license_type': license_type,
                    'license_type_name': TARGET_LICENSE_TYPES.get(license_type, 'Unknown'),
                    'status': status,
                    'business_name': row.get('Doing_Business_As', '') or row.get('Business_Name', ''),
                    'owner_name': row.get('Licensee_Name', ''),
                    'address': row.get('Address', ''),
                    'city': row.get('City', ''),
                    'state': row.get('State', 'CA'),
                    'zip': row.get('Zip', ''),
                    'county': row.get('County', ''),
                    'phone': row.get('Phone_Number', ''),
                    'issue_date': row.get('Issue_Date', ''),
                    'expiration_date': row.get('Expiration_Date', ''),
                }
                licenses.append(license_data)
        except Exception as e:
            continue
    
    return licenses


def save_to_csv(licenses, filename):
    """Save licenses to CSV file"""
    output_path = OUTPUT_DIR / filename
    
    if not licenses:
        print(f"[!] No licenses to save to {filename}")
        return None
    
    fieldnames = [
        'license_number', 'license_type', 'license_type_name', 'status',
        'business_name', 'owner_name', 'address', 'city', 'state', 'zip', 'county',
        'phone', 'issue_date', 'expiration_date'
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(licenses)
    
    print(f"[+] Saved {len(licenses)} records to {output_path}")
    return output_path


def save_by_license_type(licenses):
    """Save licenses grouped by license type"""
    by_type = {}
    for lic in licenses:
        lt = lic['license_type']
        if lt not in by_type:
            by_type[lt] = []
        by_type[lt].append(lic)
    
    saved_files = []
    for license_type, type_licenses in by_type.items():
        filename = f"CA_ABC_Type{license_type}_{datetime.now().strftime('%Y-%m-%d')}.csv"
        path = save_to_csv(type_licenses, filename)
        if path:
            saved_files.append(path)
    
    return saved_files


def save_by_county(licenses):
    """Save licenses grouped by county"""
    by_county = {}
    for lic in licenses:
        county = lic['county'] or 'Unknown'
        if county not in by_county:
            by_county[county] = []
        by_county[county].append(lic)
    
    saved_files = []
    for county, county_licenses in by_county.items():
        # Clean county name for filename
        county_clean = re.sub(r'[^\w]', '_', county).replace('__', '_')
        filename = f"CA_ABC_{county_clean}_{datetime.now().strftime('%Y-%m-%d')}.csv"
        path = save_to_csv(county_licenses, filename)
        if path:
            saved_files.append(path)
    
    return saved_files


def upload_to_database(licenses):
    """Upload licenses to the unified database"""
    print(f"[*] Uploading {len(licenses)} licenses to database...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ca_abc_licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_number TEXT UNIQUE,
            license_type TEXT,
            license_type_name TEXT,
            status TEXT,
            business_name TEXT,
            owner_name TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            county TEXT,
            phone TEXT,
            issue_date TEXT,
            expiration_date TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create index on license number
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_abc_license_number ON ca_abc_licenses(license_number)
    ''')
    
    # Create index on county for faster queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_abc_county ON ca_abc_licenses(county)
    ''')
    
    # Insert or update licenses
    inserted = 0
    updated = 0
    errors = 0
    
    for lic in licenses:
        try:
            cursor.execute('''
                INSERT INTO ca_abc_licenses 
                (license_number, license_type, license_type_name, status, business_name, 
                 owner_name, address, city, state, zip, county, phone, issue_date, expiration_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(license_number) DO UPDATE SET
                    status = excluded.status,
                    business_name = excluded.business_name,
                    owner_name = excluded.owner_name,
                    address = excluded.address,
                    city = excluded.city,
                    zip = excluded.zip,
                    county = excluded.county,
                    phone = excluded.phone,
                    scraped_at = CURRENT_TIMESTAMP
            ''', (
                lic['license_number'], lic['license_type'], lic['license_type_name'],
                lic['status'], lic['business_name'], lic['owner_name'], lic['address'],
                lic['city'], lic['state'], lic['zip'], lic['county'], lic['phone'],
                lic['issue_date'], lic['expiration_date']
            ))
            
            if cursor.rowcount == 1:
                if cursor.lastrowid:
                    inserted += 1
                else:
                    updated += 1
        except Exception as e:
            errors += 1
            continue
    
    conn.commit()
    conn.close()
    
    print(f"[+] Database upload complete: {inserted} inserted, {updated} updated, {errors} errors")
    return {'inserted': inserted, 'updated': updated, 'errors': errors}


def get_license_counts_by_type(licenses):
    """Get summary counts by license type"""
    counts = {}
    for lic in licenses:
        lt = lic['license_type']
        counts[lt] = counts.get(lt, 0) + 1
    return counts


def get_license_counts_by_county(licenses):
    """Get summary counts by county"""
    counts = {}
    for lic in licenses:
        county = lic['county'] or 'Unknown'
        counts[county] = counts.get(county, 0) + 1
    return counts


def main():
    """Main entry point"""
    print("=" * 70)
    print("California ABC License Scraper")
    print("=" * 70)
    print(f"[*] Target license types: {list(TARGET_LICENSE_TYPES.keys())}")
    print(f"[*] Target counties: All 58 California counties")
    print()
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Download ABC data
    zip_content = download_abc_data()
    if not zip_content:
        print("[!] Failed to download ABC data. Exiting.")
        return 1
    
    # Step 2: Extract CSV from zip
    csv_content = extract_csv_from_zip(zip_content)
    if not csv_content:
        print("[!] Failed to extract CSV from zip. Exiting.")
        return 1
    
    # Step 3: Parse CSV and filter for target licenses
    print("[*] Parsing CSV data...")
    licenses = parse_abc_csv(csv_content)
    print(f"[*] Found {len(licenses)} matching active licenses")
    
    if not licenses:
        print("[!] No licenses found matching criteria")
        return 1
    
    # Step 4: Print summary
    print("\n[+] License Counts by Type:")
    type_counts = get_license_counts_by_type(licenses)
    for lt, count in sorted(type_counts.items()):
        print(f"    Type {lt}: {count} licenses")
    
    print("\n[+] License Counts by County (top 10):")
    county_counts = get_license_counts_by_county(licenses)
    for county, count in sorted(county_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"    {county}: {count} licenses")
    print(f"    ... and {len(county_counts) - 10} more counties")
    
    # Step 5: Save to CSV files
    print("\n[*] Saving to CSV files...")
    
    # Save consolidated file
    consolidated_file = save_to_csv(licenses, f"CA_ABC_CONSOLIDATED_{datetime.now().strftime('%Y-%m-%d')}.csv")
    
    # Save by license type
    type_files = save_by_license_type(licenses)
    
    # Save by county
    county_files = save_by_county(licenses)
    
    # Step 6: Upload to database
    print("\n[*] Uploading to database...")
    db_stats = upload_to_database(licenses)
    
    # Step 7: Summary
    print("\n" + "=" * 70)
    print("SCRAPING COMPLETE")
    print("=" * 70)
    print(f"[+] Total licenses scraped: {len(licenses)}")
    print(f"[+] Consolidated file: {consolidated_file}")
    print(f"[+] License type files: {len(type_files)}")
    print(f"[+] County files: {len(county_files)}")
    print(f"[+] Database: {DB_PATH}")
    print(f"    - Inserted: {db_stats['inserted']}")
    print(f"    - Updated: {db_stats['updated']}")
    print(f"    - Errors: {db_stats['errors']}")
    print("=" * 70)
    
    return 0


if __name__ == '__main__':
    exit(main())
