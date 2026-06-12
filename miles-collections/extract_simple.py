#!/usr/bin/env python3
"""
Simple Excel Text Extractor for Collections Import
Reads xlsx files as zip and extracts readable text
"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import json
import re

def extract_text_from_xlsx(filepath):
    """Extract text from xlsx by reading shared strings"""
    texts = []
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            # Read shared strings
            if 'xl/sharedStrings.xml' in z.namelist():
                shared_xml = z.read('xl/sharedStrings.xml')
                root = ET.fromstring(shared_xml)
                for elem in root.iter():
                    if elem.text and elem.text.strip():
                        texts.append(elem.text.strip())
            
            # Read sheet data
            sheet_texts = []
            for name in z.namelist():
                if name.startswith('xl/worksheets/sheet') and name.endswith('.xml'):
                    sheet_xml = z.read(name)
                    root = ET.fromstring(sheet_xml)
                    for elem in root.iter():
                        if elem.text and elem.text.strip():
                            sheet_texts.append(elem.text.strip())
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []
    
    return texts + sheet_texts

def parse_collections_data(texts):
    """Parse extracted text for collection data"""
    accounts = []
    
    # Look for patterns like names, amounts, days
    name_pattern = re.compile(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)')
    amount_pattern = re.compile(r'\$?([0-9,]+\.\d{2})')
    days_pattern = re.compile(r'(\d+)\s*(?:days|day)')
    
    current_account = {}
    
    for text in texts:
        # Skip headers and common non-data text
        if any(x in text.lower() for x in ['total', 'summary', 'page', 'date:', 'report']):
            continue
        
        # Look for names
        name_match = name_pattern.search(text)
        if name_match and len(text) < 100:
            if current_account and 'name' in current_account:
                accounts.append(current_account)
                current_account = {}
            current_account['name'] = name_match.group(1)
        
        # Look for amounts
        amount_match = amount_pattern.search(text)
        if amount_match:
            try:
                amount = float(amount_match.group(1).replace(',', ''))
                if amount > 100:  # Reasonable balance
                    current_account['balance'] = amount
            except:
                pass
        
        # Look for days
        days_match = days_pattern.search(text)
        if days_match:
            try:
                days = int(days_match.group(1))
                current_account['days'] = days
            except:
                pass
    
    # Add last account
    if current_account and 'name' in current_account:
        accounts.append(current_account)
    
    return accounts

def main():
    print("="*60)
    print("PENDO EXCEL EXTRACTOR")
    print("="*60)
    
    vendor_dir = Path("/root/.openclaw/workspace/data/vendor_attachments")
    
    # Find Excel files
    files = []
    if vendor_dir.exists():
        for f in vendor_dir.iterdir():
            if f.suffix == '.xlsx' and ('pendo' in f.name.lower() or 'unpaid' in f.name.lower()):
                files.append(f)
    
    files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not files:
        print("No Excel files found")
        return
    
    print(f"\nFound {len(files)} Excel files:")
    for i, f in enumerate(files[:5], 1):
        size = f.stat().st_size / 1024
        print(f"  {i}. {f.name} ({size:.1f} KB)")
    
    # Process most recent
    target = files[0]
    print(f"\nProcessing: {target.name}")
    
    texts = extract_text_from_xlsx(target)
    print(f"Extracted {len(texts)} text fragments")
    
    # Show sample
    print("\nSample text fragments:")
    for i, t in enumerate(texts[:10], 1):
        print(f"  {i}. {t[:50]}...")
    
    accounts = parse_collections_data(texts)
    print(f"\nFound {len(accounts)} potential accounts")
    
    # Show parsed
    if accounts:
        print("\nParsed accounts:")
        for i, acc in enumerate(accounts[:5], 1):
            print(f"  {i}. {acc}")

if __name__ == '__main__':
    main()
