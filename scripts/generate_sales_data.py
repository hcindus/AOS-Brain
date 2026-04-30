#!/usr/bin/env python3
"""Generate realistic sales data for PSD dashboard based on customer annual projections"""

import sqlite3
import random
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path('/root/.openclaw/workspace/data/depot_chaos/unified.db')

# Revenue categories by system type (rough estimates)
REVENUE_MULTIPLIERS = {
    'ECR': 1.2,
    'NCC': 1.0,
    'SUPPLY ONLY': 0.5,
    'CASIO': 0.8,
    'MAITRE\'D': 1.5,
    'ALOHA': 1.3,
    'TOAST': 1.8,
    'CLOVER': 1.4,
    'SQUARE': 1.2,
    'REVEL': 1.6,
    'MICROSALE': 1.0,
    'SPOT ON': 0.9,
    'NCR': 1.1,
    'MICROS': 1.2,
    'SYMPHONY': 0.9,
    'COMTREX': 0.8,
    'SQUIRREL': 0.7,
    'PANASONIC': 0.6,
    'CAKE': 1.0,
    'DIGITAL DINING': 0.8,
    'CRS': 0.9,
    'REPAIR ONLY': 0.3,
    'TP+NS': 0.4,
    'SCALE': 0.5
}

def generate_monthly_distribution(annual):
    """Generate realistic monthly revenue with seasonal patterns"""
    # Higher sales in Dec, Nov, and summer months
    weights = [0.08, 0.07, 0.08, 0.08, 0.09, 0.09, 0.09, 0.08, 0.08, 0.09, 0.09, 0.10]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Add some randomness
    adjusted_weights = [w * (0.8 + random.random() * 0.4) for w in weights]
    total = sum(adjusted_weights)
    adjusted_weights = [w/total for w in adjusted_weights]
    
    return {months[i]: annual * adjusted_weights[i] for i in range(12)}

def main():
    print("Generating sales data for PSD dashboard...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clear existing sales data
    cursor.execute("DELETE FROM psd_customer_sales")
    
    # Get all customers with their category and system type
    cursor.execute("""
        SELECT id, system_type, category, annual_projection 
        FROM psd_customers 
        WHERE status = 'active'
    """)
    
    customers = cursor.fetchall()
    print(f"Processing {len(customers)} customers...")
    
    records_created = 0
    
    for customer_id, system_type, category, annual_proj in customers:
        # Use annual projection if available, otherwise estimate based on category
        if annual_proj and annual_proj > 0:
            base_annual = annual_proj
        else:
            # Default projections by category
            if category == 'Top 165':
                base_annual = random.randint(15000, 50000)
            elif category == 'Spot On Target':
                base_annual = random.randint(8000, 20000)
            elif category == 'Prime':
                base_annual = random.randint(5000, 12000)
            elif category == 'PPCL':
                base_annual = random.randint(3000, 8000)
            else:
                base_annual = random.randint(5000, 15000)
        
        # Apply system multiplier
        system_mult = REVENUE_MULTIPLIERS.get(system_type, 1.0)
        annual = base_annual * system_mult
        
        # Generate monthly breakdown
        monthly = generate_monthly_distribution(annual)
        
        # Insert for 2022, 2023, 2024, 2025
        for year in [2022, 2023, 2024, 2025]:
            # Add some year-over-year growth
            growth = 1.0 + (year - 2022) * 0.05  # 5% annual growth
            for month, amount in monthly.items():
                final_amount = amount * growth * (0.9 + random.random() * 0.2)
                cursor.execute("""
                    INSERT INTO psd_customer_sales (customer_id, year, month, amount)
                    VALUES (?, ?, ?, ?)
                """, (customer_id, year, month, round(final_amount, 2)))
                records_created += 1
    
    conn.commit()
    conn.close()
    
    print(f"Created {records_created} sales records")
    
    # Show summary
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT year, SUM(amount) as total FROM psd_customer_sales GROUP BY year
    """)
    print("\nYearly Revenue Summary:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: ${row[1]:,.2f}")
    
    conn.close()

if __name__ == "__main__":
    main()
