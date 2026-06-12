#!/usr/bin/env python3
"""
Bar Search Tool - 50 States + Mexico
Searches for bars/restaurants with specific keywords
"""

import csv
import os
import json
from datetime import datetime

# Configuration
KEYWORDS = ['nickel', 'nickle', 'pickle', 'peso', 'dollar', 'wooden', 'silver']
BAR_TYPES = ['bar', 'pub', 'tavern', 'lounge', 'nightclub', 'brewery', 'winery', 
             'cantina', 'speakeasy', 'saloon', 'cocktail', 'grill', 'roadhouse']

# US States to search
US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

# Mexico states
MEXICO_STATES = [
    'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche',
    'Chiapas', 'Chihuahua', 'CDMX', 'Coahuila', 'Colima', 'Durango',
    'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'Mexico State',
    'Michoacan', 'Morelos', 'Nayarit', 'Nuevo Leon', 'Oaxaca',
    'Puebla', 'Queretaro', 'Quintana Roo', 'San Luis Potosi', 'Sinaloa',
    'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz',
    'Yucatan', 'Zacatecas'
]

class BarSearcher:
    def __init__(self):
        self.results = []
        self.output_dir = '/root/.openclaw/workspace/bar_search_results'
        os.makedirs(self.output_dir, exist_ok=True)
        
    def search_existing_databases(self):
        """Search all existing databases for matches"""
        print("Searching existing databases...")
        
        data_paths = [
            '/root/.openclaw/workspace/AGI_COMPANY/data/restaurants/',
            '/root/.openclaw/workspace/AGI_COMPANY/data/leads_final/',
            '/root/.openclaw/workspace/datadepot/data/',
        ]
        
        matches = []
        for base_path in data_paths:
            if os.path.exists(base_path):
                for root, dirs, files in os.walk(base_path):
                    for file in files:
                        if file.endswith('.csv'):
                            filepath = os.path.join(root, file)
                            try:
                                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                    reader = csv.DictReader(f)
                                    for row in reader:
                                        company = str(row.get('Company', '')).lower()
                                        for kw in KEYWORDS:
                                            if kw in company:
                                                is_bar = any(bt in str(row.get('Business Type', '')).lower() 
                                                            for bt in BAR_TYPES)
                                                matches.append({
                                                    'name': row.get('Company'),
                                                    'type': row.get('Business Type'),
                                                    'address': row.get('Address'),
                                                    'city': row.get('City'),
                                                    'state': row.get('State'),
                                                    'phone': row.get('Phone'),
                                                    'keyword': kw,
                                                    'is_bar': is_bar,
                                                    'source': file
                                                })
                                                break
                            except:
                                pass
        
        return matches
    
    def save_results(self, matches):
        """Save results to CSV and JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # CSV output
        csv_file = os.path.join(self.output_dir, f'bar_search_results_{timestamp}.csv')
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if matches:
                writer = csv.DictWriter(f, fieldnames=matches[0].keys())
                writer.writeheader()
                writer.writerows(matches)
        
        # JSON output
        json_file = os.path.join(self.output_dir, f'bar_search_results_{timestamp}.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=2)
        
        # Summary
        summary = {
            'total_matches': len(matches),
            'bars': len([m for m in matches if m.get('is_bar')]),
            'by_keyword': {},
            'by_state': {}
        }
        
        for kw in KEYWORDS:
            summary['by_keyword'][kw] = len([m for m in matches if m['keyword'] == kw])
        
        states = {}
        for m in matches:
            state = m.get('state', 'Unknown')
            states[state] = states.get(state, 0) + 1
        summary['by_state'] = states
        
        summary_file = os.path.join(self.output_dir, f'summary_{timestamp}.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        return summary

if __name__ == '__main__':
    searcher = BarSearcher()
    matches = searcher.search_existing_databases()
    summary = searcher.save_results(matches)
    
    print(f"\nSearch Complete!")
    print(f"Total matches: {summary['total_matches']}")
    print(f"Bars/Pubs: {summary['bars']}")
    print(f"\nBy Keyword:")
    for kw, count in summary['by_keyword'].items():
        if count > 0:
            print(f"  {kw}: {count}")
    print(f"\nBy State (top 10):")
    for state, count in sorted(summary['by_state'].items(), key=lambda x: -x[1])[:10]:
        print(f"  {state}: {count}")
