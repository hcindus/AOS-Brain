# DataDepot - Stripe Customer Field Mapping
## Merge Tag to Stripe Data Bridge

---

## Stripe Customer Object Structure

```json
{
  "id": "cus_xxxxxxxxxxxxx",
  "object": "customer",
  "email": "customer@example.com",
  "name": "John Smith",
  "phone": "+1-555-0123",
  "metadata": {
    "first_name": "John",
    "last_name": "Smith",
    "company": "Bay Area POS Solutions",
    "city": "San Francisco",
    "state": "CA",
    "county": "San Francisco",
    "pos_focus": "Toast",
    "customer_segment": "hardware_buyer",
    "last_order_id": "pi_xxxxxxxxxxxxx",
    "last_order_date": "2026-04-22",
    "last_product_category": "pos_systems",
    "last_product_name": "Samsung POS Terminal",
    "order_count": 3,
    "lifetime_value": 2450.00,
    "days_since_last_order": 7,
    "data_depot_status": "prospect",
    "data_depot_code": "HARDWARE20",
    "cross_sell_email_1_sent": "2026-04-29T19:10:00Z",
    "cross_sell_email_1_opened": "false",
    "cross_sell_email_1_clicked": "false",
    "cross_sell_email_2_sent": "",
    "cross_sell_conversion": "false"
  },
  "subscriptions": {
    "data": []
  },
  "charges": {
    "data": []
  }
}
```

---

## Merge Tag Mapping Reference

| Email Merge Tag | Stripe Field | Data Source | Example Value |
|----------------|--------------|-------------|---------------|
| `{{Customer_ID}}` | `id` | Stripe core | `cus_ABC123XYZ` |
| `{{Email}}` | `email` | Stripe core | `john@bayareapos.com` |
| `{{First_Name}}` | `metadata.first_name` | Parsed from `name` | `John` |
| `{{Last_Name}}` | `metadata.last_name` | Parsed from `name` | `Smith` |
| `{{Full_Name}}` | `name` | Stripe core | `John Smith` |
| `{{Company}}` | `metadata.company` | Order/customer data | `Bay Area POS Solutions` |
| `{{City}}` | `metadata.city` | Shipping address | `San Francisco` |
| `{{State}}` | `metadata.state` | Shipping address | `CA` |
| `{{County}}` | `metadata.county` | Derived from city | `San Francisco` |
| `{{Phone}}` | `phone` | Stripe core | `+1-415-555-0123` |
| `{{Order_Number}}` | `metadata.last_order_id` | Order reference | `pi_3O9xYzAbC123` |
| `{{Order_Date}}` | `metadata.last_order_date` | Order timestamp | `2026-04-22` |
| `{{Product_Name}}` | `metadata.last_product_name` | Line item data | `Samsung POS Terminal` |
| `{{Product_Category}}` | `metadata.last_product_category` | Product taxonomy | `pos_systems` |
| `{{Days_Since_Order}}` | Calculated | `(now - order_date)` | `7` |
| `{{Order_Count}}` | `metadata.order_count` | Aggregated | `3` |
| `{{Lifetime_Value}}` | `metadata.lifetime_value` | Sum of charges | `$2,450.00` |
| `{{Segment}}` | `metadata.customer_segment` | Business logic | `hardware_buyer` |
| `{{DataDepot_Status}}` | `metadata.data_depot_status` | Campaign tracking | `prospect` |
| `{{Bundle_Code}}` | `metadata.data_depot_code` | Promotion code | `HARDWARE20` |
| `{{Supply_Volume}}` | Calculated | Monthly item count | `40` |
| `{{Month}}` | Calculated | Current month name | `April` |
| `{{Expiration_Date}}` | Calculated | `order_date + 14 days` | `May 6, 2026` |

---

## Customer Segment Detection Logic

```python
# stripe_segment_detection.py

def detect_customer_segment(customer):
    """
    Determine which cross-sell segment a customer belongs to
    Based on Stripe purchase history and metadata
    """
    metadata = customer.get('metadata', {})
    orders = customer.get('orders', [])
    
    # Segment A: POS Hardware Buyers
    if metadata.get('last_product_category') in ['pos_systems', 'scales', 'terminals']:
        if metadata.get('lifetime_value', 0) > 500:
            return {
                'segment': 'A',
                'segment_name': 'hardware_buyer',
                'priority': 'HIGHEST',
                'offer': '20% off bundle',
                'price': 237.00,
                'trigger_delay_days': 7
            }
    
    # Segment B: Supply Recurring
    if metadata.get('last_product_category') in ['paper_products', 'ink_ribbons']:
        order_count = metadata.get('order_count', 0)
        if order_count >= 2:
            # Check if monthly recurring (simplified logic)
            return {
                'segment': 'B',
                'segment_name': 'supply_recurring',
                'priority': 'HIGH',
                'offer': 'Free month with $500+ order',
                'price': 0.00,  # Free trial
                'trigger_delay_days': 0  # Same day with shipment
            }
    
    # Segment C: One-Time Buyers (Win-Back)
    if metadata.get('order_count', 0) == 1:
        days_since = metadata.get('days_since_last_order', 0)
        if days_since > 60:  # 60+ days since last order
            return {
                'segment': 'C',
                'segment_name': 'win_back',
                'priority': 'MEDIUM',
                'offer': '50% off 90 days',
                'price': 48.50,
                'trigger_delay_days': 90,
                'code': 'COMEBACK50'
            }
    
    # Segment D: Abandoned Cart
    if metadata.get('cart_abandoned', False):
        return {
            'segment': 'D',
            'segment_name': 'abandoned_cart',
            'priority': 'LOW',
            'offer': 'Starter trial',
            'price': 97.00,
            'trigger_delay_days': 1
        }
    
    # Default: Cold Prospect
    return {
        'segment': 'COLD',
        'segment_name': 'cold_prospect',
        'priority': 'LOW',
        'offer': 'Standard pricing',
        'price': 97.00,
        'trigger_delay_days': 0
    }
```

---

## Stripe Metadata Update API

### Enrich Customer with DataDepot Fields

```python
# stripe_customer_enrichment.py

import stripe
from datetime import datetime, timedelta

stripe.api_key = "sk_live_xxxxxxxxxxxxx"  # Set via env var

def enrich_customer_with_datadepot_fields(customer_id, purchase_data):
    """
    Enrich Stripe customer with DataDepot cross-sell fields
    Call this after each purchase
    """
    
    # Calculate derived fields
    purchase_date = datetime.fromisoformat(purchase_data['order_date'])
    days_since = (datetime.now() - purchase_date).days
    expiration = (purchase_date + timedelta(days=14)).strftime('%B %d, %Y')
    
    # Determine segment and offer
    segment_info = detect_customer_segment(purchase_data)
    
    metadata_update = {
        # Core identification
        'first_name': purchase_data['customer_name'].split()[0],
        'last_name': ' '.join(purchase_data['customer_name'].split()[1:]),
        'company': purchase_data.get('company', ''),
        'city': purchase_data['shipping_city'],
        'state': purchase_data['shipping_state'],
        'county': purchase_data.get('county', purchase_data['shipping_city']),
        
        # Purchase history
        'last_order_id': purchase_data['order_id'],
        'last_order_date': purchase_data['order_date'],
        'last_product_name': purchase_data['product_name'],
        'last_product_category': purchase_data['product_category'],
        'order_count': str(purchase_data.get('order_count', 1)),
        'lifetime_value': str(purchase_data.get('lifetime_value', 0)),
        'days_since_last_order': str(days_since),
        
        # DataDepot campaign fields
        'data_depot_status': 'prospect',
        'data_depot_code': segment_info['offer_code'],
        'customer_segment': segment_info['segment_name'],
        'cross_sell_email_1_sent': '',
        'cross_sell_email_1_opened': 'false',
        'cross_sell_email_1_clicked': 'false',
        'cross_sell_email_2_sent': '',
        'cross_sell_email_2_opened': 'false',
        'cross_sell_email_2_clicked': 'false',
        'cross_sell_email_3_sent': '',
        'cross_sell_conversion': 'false',
        'cross_sell_conversion_date': '',
        
        # Calculated fields for email
        'bundle_expiration': expiration,
        'supply_volume': str(purchase_data.get('monthly_quantity', 0)),
    }
    
    # Update Stripe customer
    customer = stripe.Customer.modify(
        customer_id,
        metadata=metadata_update
    )
    
    return customer
```

---

## Webhook Handler for Real-Time Triggers

```python
# stripe_webhook_handler.py

from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/stripe-webhook', methods=['POST'])
def handle_stripe_webhook():
    """
    Handle Stripe webhooks for automated cross-sell triggers
    """
    event = None
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_new_purchase(session)
        
    elif event['type'] == 'invoice.paid':
        invoice = event['data']['object']
        handle_recurring_payment(invoice)
        
    elif event['type'] == 'charge.failed':
        charge = event['data']['object']
        handle_abandoned_cart(charge)
    
    return jsonify({'status': 'success'}), 200

def handle_new_purchase(session):
    """
    Trigger cross-sell sequence based on purchase type
    """
    customer_id = session['customer']
    line_items = stripe.checkout.Session.list_line_items(session['id'])
    
    # Analyze purchase to determine segment
    product_category = categorize_product(line_items['data'][0])
    
    # Enrich customer metadata
    enrich_customer_with_datadepot_fields(customer_id, {
        'order_id': session['id'],
        'order_date': datetime.now().isoformat(),
        'product_name': line_items['data'][0]['description'],
        'product_category': product_category,
        'customer_name': session.get('customer_details', {}).get('name', ''),
        'shipping_city': session.get('shipping', {}).get('address', {}).get('city', ''),
        'shipping_state': session.get('shipping', {}).get('address', {}).get('state', ''),
    })
    
    # Queue email based on segment
    segment = detect_customer_segment_from_session(session)
    
    if segment['priority'] == 'HIGHEST':
        # Hardware buyer - schedule 7-day sequence
        schedule_email_sequence(customer_id, 'segment_a_hardware', delay_days=7)
    elif segment['priority'] == 'HIGH':
        # Supply recurring - immediate with shipment
        schedule_email_sequence(customer_id, 'segment_b_supply', delay_days=0)

def handle_recurring_payment(invoice):
    """
    Update order count and trigger win-back if needed
    """
    customer_id = invoice['customer']
    customer = stripe.Customer.retrieve(customer_id)
    
    # Increment order count
    current_count = int(customer.metadata.get('order_count', 0))
    stripe.Customer.modify(customer_id, metadata={
        'order_count': str(current_count + 1),
        'last_order_date': datetime.now().isoformat()
    })

def handle_abandoned_cart(charge):
    """
    Trigger abandoned cart sequence
    """
    # Mark for abandoned cart sequence
    customer_id = charge['customer']
    stripe.Customer.modify(customer_id, metadata={
        'cart_abandoned': 'true',
        'cart_value': str(charge['amount']),
        'abandoned_date': datetime.now().isoformat()
    })
    
    # Trigger 24-hour abandoned cart email
    schedule_email_sequence(customer_id, 'segment_d_abandoned', delay_days=1)
```

---

## Email Template Rendering with Stripe Data

```python
# email_template_renderer.py

def render_email_template(template_content, stripe_customer):
    """
    Replace merge tags with actual Stripe customer data
    """
    metadata = stripe_customer.get('metadata', {})
    
    # Build merge tag dictionary
    merge_data = {
        '{{Customer_ID}}': stripe_customer.get('id', ''),
        '{{Email}}': stripe_customer.get('email', ''),
        '{{First_Name}}': metadata.get('first_name', 'there'),
        '{{Last_Name}}': metadata.get('last_name', ''),
        '{{Full_Name}}': stripe_customer.get('name', 'Valued Customer'),
        '{{Company}}': metadata.get('company', 'your company'),
        '{{City}}': metadata.get('city', 'your area'),
        '{{State}}': metadata.get('state', 'CA'),
        '{{County}}': metadata.get('county', metadata.get('city', 'your county')),
        '{{Phone}}': stripe_customer.get('phone', ''),
        '{{Order_Number}}': metadata.get('last_order_id', ''),
        '{{Order_Date}}': metadata.get('last_order_date', ''),
        '{{Product_Name}}': metadata.get('last_product_name', 'recent purchase'),
        '{{Product_Category}}': metadata.get('last_product_category', ''),
        '{{Days_Since_Order}}': metadata.get('days_since_last_order', '0'),
        '{{Order_Count}}': metadata.get('order_count', '1'),
        '{{Lifetime_Value}}': f"${metadata.get('lifetime_value', '0')}",
        '{{Segment}}': metadata.get('customer_segment', ''),
        '{{DataDepot_Status}}': metadata.get('data_depot_status', 'prospect'),
        '{{Bundle_Code}}': metadata.get('data_depot_code', ''),
        '{{Supply_Volume}}': metadata.get('supply_volume', '0'),
        '{{Month}}': datetime.now().strftime('%B'),
        '{{Expiration_Date}}': metadata.get('bundle_expiration', ''),
    }
    
    # Replace all merge tags
    rendered = template_content
    for tag, value in merge_data.items():
        rendered = rendered.replace(tag, str(value))
    
    return rendered
```

---

## Implementation Checklist

### Phase 1: Stripe Setup (This Week)
- [ ] Add webhook endpoint to Stripe Dashboard: `https://psdepot.com/stripe-webhook`
- [ ] Configure webhook events: `checkout.session.completed`, `invoice.paid`, `charge.failed`
- [ ] Set `stripe.api_key` environment variable
- [ ] Test webhook with Stripe CLI

### Phase 2: Customer Enrichment (Next)
- [ ] Run enrichment on all existing customers
- [ ] Verify merge tag mapping for top 10 customers
- [ ] Update `payment_server.py` to call enrichment after checkout

### Phase 3: Email Integration (Following)
- [ ] Connect to Mailgun/SendGrid API
- [ ] Test template rendering with real customer data
- [ ] Verify email deliverability (DKIM, SPF)

### Phase 4: Automation (Final)
- [ ] Deploy webhook handler to production
- [ ] Set up cron for scheduled email sends
- [ ] Configure bounce/response tracking

---

**Last Updated:** 2026-04-29
**Owner:** Miles / DataDepot
**Status:** Ready for Implementation
