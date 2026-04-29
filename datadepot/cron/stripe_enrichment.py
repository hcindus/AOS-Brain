#!/usr/bin/env python3
"""
DataDepot Stripe Customer Enrichment
Checks for new purchases, enriches with segment data, queues cross-sell sequences
Triggered by cron: 0 7 * * * (daily 7 AM)
"""

import json
import os
import sys
from datetime import datetime, timedelta

# Mock stripe module (replace with actual when ready)
class MockStripe:
    @staticmethod
    def Customer():
        class Customer:
            @staticmethod
            def list(**kwargs):
                # Return mock data for testing
                return type('obj', (object,), {
                    'data': [
                        {
                            'id': 'cus_test123',
                            'email': 'test@example.com',
                            'name': 'Test Customer',
                            'metadata': {
                                'last_order_date': (datetime.now() - timedelta(days=1)).isoformat(),
                                'order_count': '1',
                                'last_product_category': 'pos_systems'
                            }
                        }
                    ]
                })()
        return Customer()

try:
    import stripe
except ImportError:
    stripe = MockStripe()

LOG_FILE = '/var/log/datadepot/enrichment.log'
QUEUE_FILE = '/root/.openclaw/workspace/datadepot/queue/pending_emails.json'

def log(message, level='INFO'):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [{level}] {message}")
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] [{level}] {message}\n")

def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, 'r') as f:
        return json.load(f)

def save_queue(queue):
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)

def detect_segment(customer):
    """Determine customer segment based on purchase history"""
    metadata = customer.get('metadata', {})
    
    category = metadata.get('last_product_category', '')
    order_count = int(metadata.get('order_count', 0))
    
    if category in ['pos_systems', 'scales', 'terminals']:
        return {
            'segment': 'A',
            'segment_name': 'hardware_buyer',
            'priority': 'HIGHEST',
            'offer': 'HARDWARE20',
            'delay_days': 7,
            'template': 'segment_a_email_1',
            'price': 237.00
        }
    elif category in ['paper_products', 'ink_ribbons'] and order_count >= 2:
        return {
            'segment': 'B',
            'segment_name': 'supply_recurring',
            'priority': 'HIGH',
            'offer': 'SUPPLY_FREE',
            'delay_days': 0,
            'template': 'segment_b_email_1',
            'price': 0.00
        }
    elif order_count == 1:
        return {
            'segment': 'C',
            'segment_name': 'one_time_buyer',
            'priority': 'MEDIUM',
            'offer': 'COMEBACK50',
            'delay_days': 90,
            'template': 'segment_c_email_1',
            'price': 48.50
        }
    else:
        return None

def queue_sequence(customer, segment_info):
    """Add customer to email sequence queue"""
    queue = load_queue()
    
    scheduled_time = datetime.now() + timedelta(days=segment_info['delay_days'])
    
    email_job = {
        'customer_id': customer['id'],
        'to_email': customer['email'],
        'to_name': customer.get('name', 'Valued Customer'),
        'template': segment_info['template'],
        'campaign_id': f"cross_sell_{segment_info['segment_name']}_{datetime.now().strftime('%Y%m')}",
        'scheduled_time': scheduled_time.isoformat(),
        'segment': segment_info['segment'],
        'offer_code': segment_info['offer'],
        'created_at': datetime.now().isoformat(),
        'subject': None,  # Will be extracted from template
        'html_body': None,  # Will be rendered at send time
        'from': 'Miles - Performance Supply Depot <miles@psdepot.com>',
        'merge_data': {
            '{{Customer_ID}}': customer['id'],
            '{{Email}}': customer['email'],
            '{{Full_Name}}': customer.get('name', ''),
            '{{First_Name}}': customer.get('name', '').split()[0] if customer.get('name') else 'there',
            '{{Company}}': customer.get('metadata', {}).get('company', ''),
            '{{Order_Number}}': customer.get('metadata', {}).get('last_order_id', ''),
            '{{Product_Name}}': customer.get('metadata', {}).get('last_product_name', ''),
            '{{Days_Since_Order}}': '0',
            '{{Bundle_Code}}': segment_info['offer'],
            '{{Expiration_Date}}': (datetime.now() + timedelta(days=14)).strftime('%B %d, %Y')
        }
    }
    
    # Check if already in queue
    existing = [e for e in queue if e['customer_id'] == customer['id'] and e['template'] == segment_info['template']]
    
    if existing:
        log(f"Customer {customer['id']} already queued for {segment_info['template']}, skipping")
        return False
    
    queue.append(email_job)
    save_queue(queue)
    
    log(f"✓ Queued {segment_info['segment_name']} sequence for {customer['email']} (send: {scheduled_time.strftime('%Y-%m-%d')})")
    return True

def main():
    log("=" * 60)
    log("STRIPE CUSTOMER ENRICHMENT - STARTING")
    log("=" * 60)
    
    # Check for customers needing enrichment
    # In production: stripe.Customer.list(created={'gte': yesterday_timestamp})
    
    customers = stripe.Customer.list(limit=100)
    
    log(f"Checking {len(customers.data)} customers for enrichment")
    
    enriched = 0
    queued = 0
    
    for customer in customers.data:
        metadata = customer.get('metadata', {})
        
        # Skip if already enriched with DataDepot fields
        if metadata.get('data_depot_status'):
            continue
        
        # Detect segment
        segment = detect_segment(customer)
        
        if segment:
            # Queue sequence
            if queue_sequence(customer, segment):
                queued += 1
            
            enriched += 1
    
    log("")
    log("=" * 60)
    log("ENRICHMENT COMPLETE")
    log("=" * 60)
    log(f"Customers checked: {len(customers.data)}")
    log(f"Segments detected: {enriched}")
    log(f"Sequences queued: {queued}")
    log("=" * 60)

if __name__ == '__main__':
    main()
