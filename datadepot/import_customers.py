#!/usr/bin/env python3
"""
Performance Supply Depot Customer Import Script
Imports AH_PPL_2022 customer data into DepotChaos with duplicate detection
"""

import pandas as pd
import sqlite3
import json
import re
from datetime import datetime
from pathlib import Path
import sys

# Configuration
DB_PATH = Path('/root/.openclaw/workspace/data/depot_chaos/unified.db')
EXCEL_FILE = Path('/tmp/AH_PPL_2022.xlsx')
IMPORT_LOG = Path('/root/.openclaw/workspace/datadepot/import_ah_ppl_2022.log')

class CustomerImporter:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.stats = {
            'total_processed': 0,
            'imported': 0,
            'duplicates': 0,
            'multi_location': 0,
            'needs_verification': 0,
            'errors': 0
        }
        self.ensure_tables()
        
    def ensure_tables(self):
        """Create necessary tables if they don't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS psd_customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT NOT NULL,
                contact_name TEXT,
                phone TEXT,
                phone2 TEXT,
                email TEXT,
                street_address TEXT,
                city TEXT,
                state TEXT,
                zipcode TEXT,
                system_type TEXT,
                category TEXT,
                annual_projection REAL,
                status TEXT DEFAULT 'active',
                source_sheet TEXT,
                import_date TEXT,
                last_contact TEXT,
                next_predicted_contact TEXT,
                needs_verification BOOLEAN DEFAULT 0,
                verification_notes TEXT,
                duplicate_of INTEGER,
                UNIQUE(business_name, city, street_address)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS psd_customer_sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                year INTEGER,
                month TEXT,
                amount REAL,
                FOREIGN KEY (customer_id) REFERENCES psd_customers(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS import_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                import_date TEXT,
                source_file TEXT,
                sheet_name TEXT,
                records_processed INTEGER,
                records_imported INTEGER,
                duplicates_found INTEGER,
                errors TEXT
            )
        ''')
        
        self.conn.commit()
    
    def normalize_phone(self, phone):
        """Normalize phone number for comparison"""
        if pd.isna(phone) or phone is None:
            return None
        phone = str(phone)
        # Remove all non-numeric characters
        digits = re.sub(r'\D', '', phone)
        # Standard format
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        return phone
    
    def normalize_name(self, name):
        """Normalize business name for duplicate checking"""
        if pd.isna(name) or name is None:
            return None
        name = str(name).strip().upper()
        # Remove common suffixes
        name = re.sub(r'\s+(LLC|INC|CORP|LTD|DBA).*$', '', name)
        # Remove extra spaces and special chars
        name = re.sub(r'[^A-Z0-9]', '', name)
        return name
    
    def check_duplicate(self, business_name, city, street=None):
        """Check if customer already exists"""
        norm_name = self.normalize_name(business_name)
        
        # Check exact match on name + city
        self.cursor.execute('''
            SELECT id, business_name, city, street_address, phone 
            FROM psd_customers 
            WHERE UPPER(REPLACE(REPLACE(business_name, ' ', ''), "'", '')) = ?
            AND UPPER(city) = UPPER(?)
        ''', (norm_name, city))
        
        exact_match = self.cursor.fetchone()
        if exact_match:
            return exact_match[0], 'exact'
        
        # Check phone match
        if street:
            # Check for multi-location (same name, different address)
            self.cursor.execute('''
                SELECT id, business_name, city, street_address 
                FROM psd_customers 
                WHERE UPPER(REPLACE(REPLACE(business_name, ' ', ''), "'", '')) = ?
                AND UPPER(city) != UPPER(?)
            ''', (norm_name, city))
            
            multi = self.cursor.fetchone()
            if multi:
                return multi[0], 'multi_location'
        
        return None, None
    
    def extract_address_components(self, address_str):
        """Extract street, city, state, zip from address string"""
        if pd.isna(address_str):
            return None, None, None, None
        
        # Try common patterns
        # Pattern: "123 Main St, City, CA 12345"
        match = re.match(r'(.+?)\s*,\s*([^,]+)\s*,\s*([A-Za-z]{2})\s*(\d{5})', str(address_str))
        if match:
            return match.group(1), match.group(2), match.group(3), match.group(4)
        
        # Pattern: "123 Main St, City CA 12345"
        match = re.match(r'(.+?)\s*,\s*([^,]+)\s+([A-Za-z]{2})\s*(\d{5})', str(address_str))
        if match:
            return match.group(1), match.group(2), match.group(3), match.group(4)
        
        return address_str, None, None, None
    
    def extract_sales_data(self, row):
        """Extract monthly sales data from row"""
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        sales = {}
        for month in months:
            if month in row.index and pd.notna(row[month]):
                try:
                    # Handle format like "54220 $55" - extract the dollar amount
                    val = str(row[month])
                    match = re.search(r'\$(\d+)', val)
                    if match:
                        sales[month] = int(match.group(1))
                    else:
                        sales[month] = float(row[month])
                except:
                    pass
        return sales
    
    def process_top165(self, df):
        """Process Top 165 sheet"""
        print(f"\n📊 Processing Top 165 sheet ({len(df)} rows)...")
        
        for idx, row in df.iterrows():
            try:
                if pd.isna(row.get('GROUP 1')) or str(row.get('GROUP 1')).strip() == '':
                    continue
                
                business = str(row.get('GROUP 1', '')).strip()
                system = str(row.get('SYSTEM', '')).strip() if pd.notna(row.get('SYSTEM')) else None
                contact = str(row.get('Contact', '')).strip() if pd.notna(row.get('Contact')) else None
                phone = self.normalize_phone(row.get('Phone'))
                phone2 = self.normalize_phone(row.get('2nd Phone'))
                
                # Address parsing
                street = city = state = zipcode = None
                if pd.notna(row.get('Unnamed: 7')):
                    street = str(row.get('Unnamed: 7')).strip()
                if pd.notna(row.get('Unnamed: 8')):
                    city = str(row.get('Unnamed: 8')).strip()
                if pd.notna(row.get('Unnamed: 9')):
                    state = str(row.get('Unnamed: 9')).strip()
                
                # Email (usually in column 10)
                email = None
                if 'Unnamed: 10' in row.index and pd.notna(row.get('Unnamed: 10')):
                    email = str(row.get('Unnamed: 10')).strip()
                
                # Check for duplicate
                dup_id, dup_type = self.check_duplicate(business, city, street)
                
                if dup_type == 'exact':
                    self.stats['duplicates'] += 1
                    continue
                elif dup_type == 'multi_location':
                    self.stats['multi_location'] += 1
                
                # Extract sales data
                sales = self.extract_sales_data(row)
                
                # Insert customer
                self.cursor.execute('''
                    INSERT INTO psd_customers 
                    (business_name, contact_name, phone, phone2, email, street_address, 
                     city, state, system_type, category, source_sheet, import_date,
                     needs_verification, duplicate_of)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    business, contact, phone, phone2, email, street,
                    city, state, system, 'Top 165', 'Top 165', 
                    datetime.now().isoformat(),
                    0 if dup_type != 'multi_location' else 1,
                    dup_id if dup_type == 'multi_location' else None
                ))
                
                customer_id = self.cursor.lastrowid
                
                # Insert sales data
                for month, amount in sales.items():
                    self.cursor.execute('''
                        INSERT INTO psd_customer_sales (customer_id, year, month, amount)
                        VALUES (?, ?, ?, ?)
                    ''', (customer_id, 2022, month, amount))
                
                self.stats['imported'] += 1
                self.stats['total_processed'] += 1
                
            except Exception as e:
                self.stats['errors'] += 1
                print(f"  ⚠️  Error on row {idx}: {e}")
        
        self.conn.commit()
        print(f"  ✅ Imported {self.stats['imported']} from Top 165")
    
    def process_spot_on_targets(self, df):
        """Process Spot On Target List sheet"""
        print(f"\n📊 Processing Spot On Target List ({len(df)} rows)...")
        
        imported_before = self.stats['imported']
        
        for idx, row in df.iterrows():
            try:
                if pd.isna(row.get('Account Name')):
                    continue
                
                business = str(row.get('Account Name')).strip()
                if business.startswith('***'):
                    continue
                
                # Check for duplicates
                dup_id, dup_type = self.check_duplicate(business, 'Unknown')
                
                if dup_type == 'exact':
                    self.stats['duplicates'] += 1
                    continue
                
                # Extract sales if available
                sales = self.extract_sales_data(row)
                
                self.cursor.execute('''
                    INSERT INTO psd_customers 
                    (business_name, system_type, category, source_sheet, import_date, needs_verification)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    business, 
                    row.get('Primary tech') if pd.notna(row.get('Primary tech')) else None,
                    'Spot On Target',
                    'Spot On Target List',
                    datetime.now().isoformat(),
                    1  # Needs verification - minimal data
                ))
                
                customer_id = self.cursor.lastrowid
                
                for month, amount in sales.items():
                    self.cursor.execute('''
                        INSERT INTO psd_customer_sales (customer_id, year, month, amount)
                        VALUES (?, ?, ?, ?)
                    ''', (customer_id, 2022, month, amount))
                
                self.stats['imported'] += 1
                self.stats['total_processed'] += 1
                
            except Exception as e:
                self.stats['errors'] += 1
        
        self.conn.commit()
        print(f"  ✅ Imported {self.stats['imported'] - imported_before} from Spot On Targets")
    
    def process_prime_accounts(self, df):
        """Process Prime sheet"""
        print(f"\n📊 Processing Prime accounts ({len(df)} rows)...")
        
        imported_before = self.stats['imported']
        
        # Skip header row
        for idx, row in df.iloc[1:].iterrows():
            try:
                if pd.isna(row.get('Unnamed: 4')):
                    continue
                
                business = str(row.get('Unnamed: 4')).strip()
                system = str(row.get('Unnamed: 2')).strip() if pd.notna(row.get('Unnamed: 2')) else None
                contact = str(row.get('Unnamed: 5')).strip() if pd.notna(row.get('Unnamed: 5')) else None
                phone = self.normalize_phone(row.get('Unnamed: 6'))
                
                street = str(row.get('Unnamed: 9')).strip() if pd.notna(row.get('Unnamed: 9')) else None
                city = str(row.get('Unnamed: 10')).strip() if pd.notna(row.get('Unnamed: 10')) else None
                state = str(row.get('Unnamed: 11')).strip() if pd.notna(row.get('Unnamed: 11')) else None
                zipcode = str(row.get('Unnamed: 12')).strip() if pd.notna(row.get('Unnamed: 12')) else None
                
                # Check duplicates
                dup_id, dup_type = self.check_duplicate(business, city, street)
                
                if dup_type == 'exact':
                    self.stats['duplicates'] += 1
                    continue
                
                self.cursor.execute('''
                    INSERT INTO psd_customers 
                    (business_name, contact_name, phone, street_address, city, state, zipcode,
                     system_type, category, source_sheet, import_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    business, contact, phone, street, city, state, zipcode,
                    system, 'Prime', 'Prime',
                    datetime.now().isoformat()
                ))
                
                self.stats['imported'] += 1
                self.stats['total_processed'] += 1
                
            except Exception as e:
                self.stats['errors'] += 1
        
        self.conn.commit()
        print(f"  ✅ Imported {self.stats['imported'] - imported_before} from Prime")
    
    def process_ppcl(self, df):
        """Process PPCL_2022 sheet"""
        print(f"\n📊 Processing PPCL_2022 ({len(df)} rows)...")
        
        imported_before = self.stats['imported']
        
        for idx, row in df.iterrows():
            try:
                if pd.isna(row.get('2 Star Market')):
                    continue
                
                business = str(row.get('2 Star Market')).strip()
                system = str(row.get('CASIO')).strip() if pd.notna(row.get('CASIO')) else None
                
                # Contact info
                contact = None
                phone = None
                if pd.notna(row.get('Ali')):
                    contact = str(row.get('Ali')).strip()
                if pd.notna(row.get('510-531-3576')):
                    phone = self.normalize_phone(row.get('510-531-3576'))
                
                # Address
                street = city = state = zipcode = None
                if pd.notna(row.get('2020 MacArthur Blvd')):
                    street = str(row.get('2020 MacArthur Blvd')).strip()
                if pd.notna(row.get('Oakland')):
                    city = str(row.get('Oakland')).strip()
                if pd.notna(row.get('Ca')):
                    state = str(row.get('Ca')).strip()
                if pd.notna(row.get('94602')):
                    zipcode = str(int(row.get('94602')))
                
                dup_id, dup_type = self.check_duplicate(business, city, street)
                
                if dup_type == 'exact':
                    self.stats['duplicates'] += 1
                    continue
                
                self.cursor.execute('''
                    INSERT INTO psd_customers 
                    (business_name, contact_name, phone, street_address, city, state, zipcode,
                     system_type, category, source_sheet, import_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    business, contact, phone, street, city, state, zipcode,
                    system, 'PPCL', 'PPCL_2022',
                    datetime.now().isoformat()
                ))
                
                self.stats['imported'] += 1
                self.stats['total_processed'] += 1
                
            except Exception as e:
                self.stats['errors'] += 1
        
        self.conn.commit()
        print(f"  ✅ Imported {self.stats['imported'] - imported_before} from PPCL")
    
    def generate_report(self):
        """Generate import report"""
        print("\n" + "="*60)
        print("📋 IMPORT SUMMARY")
        print("="*60)
        print(f"Total records processed: {self.stats['total_processed']}")
        print(f"✅ Successfully imported: {self.stats['imported']}")
        print(f"⚠️  Duplicates skipped: {self.stats['duplicates']}")
        print(f"🏢 Multi-location detected: {self.stats['multi_location']}")
        print(f"🔍 Needs verification: {self.stats['needs_verification']}")
        print(f"❌ Errors: {self.stats['errors']}")
        print("="*60)
        
        # Log to file
        with open(IMPORT_LOG, 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Import Date: {datetime.now().isoformat()}\n")
            f.write(f"Source: {EXCEL_FILE}\n")
            f.write(json.dumps(self.stats, indent=2))
            f.write(f"\n{'='*60}\n")
    
    def run(self):
        """Main import process"""
        print("="*60)
        print("🏭 Performance Supply Depot Customer Import")
        print("="*60)
        print(f"Source: {EXCEL_FILE}")
        print(f"Database: {DB_PATH}")
        print("="*60)
        
        if not EXCEL_FILE.exists():
            print(f"❌ Error: Excel file not found at {EXCEL_FILE}")
            sys.exit(1)
        
        # Load Excel file
        xl = pd.ExcelFile(EXCEL_FILE)
        print(f"\n📁 Found {len(xl.sheet_names)} sheets: {xl.sheet_names}")
        
        # Process each relevant sheet
        if 'Top 165' in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name='Top 165')
            self.process_top165(df)
        
        if 'SPOT ON TARGET LIST' in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name='SPOT ON TARGET LIST')
            self.process_spot_on_targets(df)
        
        if 'Prime' in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name='Prime', header=None)
            self.process_prime_accounts(df)
        
        if 'PPCL_2022' in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name='PPCL_2022')
            self.process_ppcl(df)
        
        self.generate_report()
        self.conn.close()
        print(f"\n✅ Import complete! Log saved to: {IMPORT_LOG}")

if __name__ == '__main__':
    importer = CustomerImporter()
    importer.run()
