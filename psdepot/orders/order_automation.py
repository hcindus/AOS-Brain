#!/usr/bin/env python3
"""
PSDepot Order Automation System
Parse customer orders from various formats and generate invoices
"""

import json
import re
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import uuid

# Database setup
DB_PATH = Path("/root/.openclaw/workspace/data/psdepot_orders.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

class OrderAutomation:
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        """Initialize orders database"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                order_id TEXT UNIQUE,
                customer_name TEXT,
                company TEXT,
                email TEXT,
                phone TEXT,
                status TEXT DEFAULT 'RECEIVED',
                subtotal REAL,
                tax_rate REAL DEFAULT 0.0775,
                tax_amount REAL,
                shipping REAL,
                total REAL,
                source_type TEXT,
                source_data TEXT,
                tracking_number TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT,
                sku TEXT,
                description TEXT,
                quantity INTEGER,
                unit_price REAL,
                line_total REAL,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS order_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT,
                status TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def parse_text_order(self, text: str) -> Dict:
        """Parse order from plain text"""
        order = {
            'order_id': None,
            'customer_name': '',
            'company': '',
            'email': '',
            'phone': '',
            'items': [],
            'subtotal': 0.0,
            'tax_rate': 0.0775,
            'tax_amount': 0.0,
            'shipping': 0.0,
            'total': 0.0
        }
        
        lines = text.strip().split('\n')
        
        # Extract order ID - look for # followed by numbers
        for line in lines:
            if 'order' in line.lower():
                match = re.search(r'#\s*([A-Z0-9\-]+)', line)
                if match:
                    order['order_id'] = match.group(1)
                    break
        
        # Generate order ID if not found
        if not order['order_id']:
            order['order_id'] = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"
        
        # Parse line by line for structured data
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Skip empty lines and section headers
            if not line_lower or line_lower in ['items:', 'order:']:
                continue
            
            # Customer name
            if 'customer:' in line_lower:
                order['customer_name'] = line.split(':', 1)[1].strip()
            
            # Company
            elif 'company:' in line_lower:
                order['company'] = line.split(':', 1)[1].strip()
            
            # Email
            elif 'email:' in line_lower:
                order['email'] = line.split(':', 1)[1].strip()
            elif not order['email']:
                email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line)
                if email_match:
                    order['email'] = email_match.group()
            
            # Phone
            elif 'phone:' in line_lower:
                order['phone'] = line.split(':', 1)[1].strip()
            
            # Totals
            elif 'subtotal' in line_lower and ':' in line:
                try:
                    val = re.search(r'[\d,]+\.?\d*', line.split(':')[1])
                    if val:
                        order['subtotal'] = float(val.group().replace(',', ''))
                except:
                    pass
            
            elif 'tax' in line_lower and ':' in line and '%' in line:
                try:
                    rate_match = re.search(r'([\d.]+)%', line)
                    if rate_match:
                        order['tax_rate'] = float(rate_match.group(1)) / 100
                    val = re.search(r'[\d,]+\.?\d*', line.split(':')[1])
                    if val:
                        order['tax_amount'] = float(val.group().replace(',', ''))
                except:
                    pass
            
            elif 'shipping' in line_lower and ':' in line:
                try:
                    val = re.search(r'[\d,]+\.?\d*', line.split(':')[1])
                    if val:
                        order['shipping'] = float(val.group().replace(',', ''))
                except:
                    pass
            
            elif 'total' in line_lower and ':' in line and 'sub' not in line_lower:
                try:
                    val = re.search(r'[\d,]+\.?\d*', line.split(':')[1])
                    if val:
                        order['total'] = float(val.group().replace(',', ''))
                except:
                    pass
        
        # Parse items - look for qty x description @ price pattern
        for line in lines:
            item = self._parse_item_line(line)
            if item:
                order['items'].append(item)
        
        # Calculate if totals not provided
        if not order['subtotal'] and order['items']:
            order['subtotal'] = sum(item['line_total'] for item in order['items'])
        if not order['tax_amount'] and order['subtotal']:
            order['tax_amount'] = order['subtotal'] * order['tax_rate']
        if not order['total']:
            order['total'] = order['subtotal'] + order['tax_amount'] + order['shipping']
        
        return order
    
    def _parse_item_line(self, line: str) -> Optional[Dict]:
        """Parse a single item line - must have quantity x pattern"""
        line = line.strip()
        if not line or line.startswith('-') or line.startswith('='):
            return None
        
        # Skip header/total lines
        line_lower = line.lower()
        if any(skip in line_lower for skip in ['subtotal', 'tax', 'shipping', 'total', 'order', 'customer', 'company', 'email', 'phone', 'date', 'note']):
            return None
        
        item = {
            'sku': '',
            'description': '',
            'quantity': 1,
            'unit_price': 0.0,
            'line_total': 0.0
        }
        
        # Pattern: 2 x Receipt Paper @ $45.00 = $90.00
        qty_price_match = re.search(r'(\d+)\s*x\s*(.+?)\s*@?\s*\$?([\d,]+\.?\d*)', line, re.IGNORECASE)
        if qty_price_match:
            item['quantity'] = int(qty_price_match.group(1))
            item['description'] = qty_price_match.group(2).strip()
            item['unit_price'] = float(qty_price_match.group(3).replace(',', ''))
            item['line_total'] = item['quantity'] * item['unit_price']
            return item
        
        # Pattern: SKU-123 | Description | 2 | $45.00
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 3:
            item['sku'] = parts[0]
            item['description'] = parts[1]
            try:
                item['quantity'] = int(parts[2])
            except:
                pass
            if len(parts) >= 4:
                price_match = re.search(r'[\d,]+\.?\d*', parts[3])
                if price_match:
                    item['unit_price'] = float(price_match.group().replace(',', ''))
            item['line_total'] = item['quantity'] * item['unit_price']
            return item
        
        return None
    
    def save_order(self, order: Dict, source_type: str = 'text') -> str:
        """Save order to database"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Generate UUID
        order_uuid = str(uuid.uuid4())
        
        # Insert order
        c.execute('''
            INSERT INTO orders 
            (id, order_id, customer_name, company, email, phone, status, 
             subtotal, tax_rate, tax_amount, shipping, total, source_type, source_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_uuid, order['order_id'], order.get('customer_name', ''),
            order.get('company', ''), order.get('email', ''), order.get('phone', ''),
            'RECEIVED', order['subtotal'], order['tax_rate'],
            order['tax_amount'], order.get('shipping', 0), order['total'],
            source_type, json.dumps(order)
        ))
        
        # Insert items
        for item in order['items']:
            c.execute('''
                INSERT INTO order_items 
                (order_id, sku, description, quantity, unit_price, line_total)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                order_uuid, item.get('sku', ''), item['description'],
                item['quantity'], item['unit_price'], item['line_total']
            ))
        
        # Add history entry
        c.execute('''
            INSERT INTO order_history (order_id, status, notes)
            VALUES (?, ?, ?)
        ''', (order_uuid, 'RECEIVED', 'Order received and parsed'))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Order saved: {order['order_id']} (ID: {order_uuid})")
        return order_uuid
    
    def update_status(self, order_id: str, status: str, notes: str = ''):
        """Update order status"""
        valid_statuses = ['RECEIVED', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'ISSUE', 'CANCELLED']
        
        if status.upper() not in valid_statuses:
            print(f"❌ Invalid status. Valid options: {', '.join(valid_statuses)}")
            return False
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? OR order_id = ?
        ''', (status.upper(), order_id, order_id))
        
        c.execute('''
            INSERT INTO order_history (order_id, status, notes)
            VALUES ((SELECT id FROM orders WHERE id = ? OR order_id = ?), ?, ?)
        ''', (order_id, order_id, status.upper(), notes))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Order {order_id} status updated to: {status.upper()}")
        return True
    
    def add_tracking(self, order_id: str, tracking_number: str, carrier: str = ''):
        """Add tracking number to order"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            UPDATE orders SET tracking_number = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? OR order_id = ?
        ''', (tracking_number, order_id, order_id))
        
        notes = f"Tracking added: {tracking_number}"
        if carrier:
            notes += f" ({carrier})"
        
        c.execute('''
            INSERT INTO order_history (order_id, status, notes)
            VALUES ((SELECT id FROM orders WHERE id = ? OR order_id = ?), 'SHIPPED', ?)
        ''', (order_id, order_id, notes))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Tracking added to order {order_id}: {tracking_number}")
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        """Get order by ID"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('SELECT * FROM orders WHERE id = ? OR order_id = ?', (order_id, order_id))
        order_row = c.fetchone()
        
        if not order_row:
            conn.close()
            return None
        
        order = dict(order_row)
        
        # Get items
        c.execute('SELECT * FROM order_items WHERE order_id = ?', (order['id'],))
        order['items'] = [dict(row) for row in c.fetchall()]
        
        # Get history
        c.execute('''
            SELECT * FROM order_history 
            WHERE order_id = ? 
            ORDER BY created_at DESC
        ''', (order['id'],))
        order['history'] = [dict(row) for row in c.fetchall()]
        
        conn.close()
        return order
    
    def list_orders(self, status: str = None, limit: int = 50) -> List[Dict]:
        """List orders with optional status filter"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        if status:
            c.execute('''
                SELECT * FROM orders 
                WHERE status = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (status.upper(), limit))
        else:
            c.execute('''
                SELECT * FROM orders 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
        
        orders = [dict(row) for row in c.fetchall()]
        conn.close()
        return orders
    
    def generate_invoice_html(self, order_id: str) -> str:
        """Generate HTML invoice"""
        order = self.get_order(order_id)
        if not order:
            return "Order not found"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Invoice #{order['order_id']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
        .header {{ border-bottom: 2px solid #00E0FF; padding-bottom: 20px; margin-bottom: 30px; }}
        .company {{ font-size: 24px; font-weight: bold; color: #00E0FF; }}
        .invoice-title {{ font-size: 18px; color: #666; margin-top: 10px; }}
        .customer-info {{ margin: 20px 0; }}
        .info-row {{ margin: 5px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #00E0FF; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        .total-section {{ margin-top: 30px; border-top: 2px solid #00E0FF; padding-top: 20px; }}
        .total-row {{ display: flex; justify-content: space-between; margin: 5px 0; }}
        .grand-total {{ font-size: 18px; font-weight: bold; color: #00E0FF; }}
        .status {{ display: inline-block; padding: 5px 15px; border-radius: 15px; font-weight: bold; }}
        .status-RECEIVED {{ background: #FFD700; color: #333; }}
        .status-PROCESSING {{ background: #00BFFF; color: white; }}
        .status-SHIPPED {{ background: #32CD32; color: white; }}
        .status-DELIVERED {{ background: #00E0FF; color: white; }}
        .status-ISSUE {{ background: #FF4444; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="company">Performance Supply Depot</div>
        <div class="invoice-title">INVOICE #{order['order_id']}</div>
        <div style="margin-top: 10px;">
            <span class="status status-{order['status']}">{order['status']}</span>
        </div>
    </div>
    
    <div class="customer-info">
        <div class="info-row"><strong>Customer:</strong> {order.get('customer_name', 'N/A')}</div>
        <div class="info-row"><strong>Company:</strong> {order.get('company', 'N/A')}</div>
        <div class="info-row"><strong>Email:</strong> {order.get('email', 'N/A')}</div>
        <div class="info-row"><strong>Phone:</strong> {order.get('phone', 'N/A')}</div>
        <div class="info-row"><strong>Order Date:</strong> {order.get('created_at', 'N/A')}</div>
        <div class="info-row"><strong>Tracking:</strong> {order.get('tracking_number', 'N/A')}</div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>SKU</th>
                <th>Description</th>
                <th>Qty</th>
                <th>Unit Price</th>
                <th>Line Total</th>
            </tr>
        </thead>
        <tbody>
"""
        
        for item in order.get('items', []):
            html += f"""
            <tr>
                <td>{item.get('sku', 'N/A')}</td>
                <td>{item.get('description', 'N/A')}</td>
                <td>{item.get('quantity', 0)}</td>
                <td>${item.get('unit_price', 0):.2f}</td>
                <td>${item.get('line_total', 0):.2f}</td>
            </tr>
"""
        
        html += f"""
        </tbody>
    </table>
    
    <div class="total-section">
        <div class="total-row">
            <span>Subtotal:</span>
            <span>${order.get('subtotal', 0):.2f}</span>
        </div>
        <div class="total-row">
            <span>Tax ({order.get('tax_rate', 0.0775)*100:.2f}%):</span>
            <span>${order.get('tax_amount', 0):.2f}</span>
        </div>
        <div class="total-row">
            <span>Shipping:</span>
            <span>${order.get('shipping', 0):.2f}</span>
        </div>
        <div class="total-row grand-total">
            <span>TOTAL:</span>
            <span>${order.get('total', 0):.2f}</span>
        </div>
    </div>
    
    <div style="margin-top: 40px; padding: 20px; background: #f5f5f5; border-radius: 5px;">
        <strong>Payment Terms:</strong> Net 30<br>
        <strong>Questions?</strong> Contact us at info@psdepot.com or 888-881-6834
    </div>
</body>
</html>
"""
        return html
    
    def export_invoice(self, order_id: str, output_path: str = None) -> str:
        """Export invoice to HTML file"""
        if not output_path:
            output_path = f"/var/www/psdepot.com/invoices/invoice_{order_id}.html"
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        html = self.generate_invoice_html(order_id)
        with open(output_path, 'w') as f:
            f.write(html)
        
        print(f"✅ Invoice exported: {output_path}")
        return output_path


def main():
    """CLI interface"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python order_automation.py init")
        print("  python order_automation.py parse <text_file>")
        print("  python order_automation.py list [status]")
        print("  python order_automation.py status <order_id> <status>")
        print("  python order_automation.py track <order_id> <tracking_number>")
        print("  python order_automation.py invoice <order_id>")
        return
    
    cmd = sys.argv[1]
    automation = OrderAutomation()
    
    if cmd == 'init':
        print("Database initialized")
    
    elif cmd == 'parse' and len(sys.argv) >= 3:
        with open(sys.argv[2], 'r') as f:
            text = f.read()
        order = automation.parse_text_order(text)
        order_id = automation.save_order(order, 'file')
        print(f"\nParsed order:")
        print(f"  Order ID: {order['order_id']}")
        print(f"  Customer: {order.get('customer_name', 'N/A')}")
        print(f"  Items: {len(order['items'])}")
        print(f"  Total: ${order['total']:.2f}")
    
    elif cmd == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        orders = automation.list_orders(status)
        print(f"\n{'Order ID':<20} {'Customer':<25} {'Status':<12} {'Total':>10}")
        print("-" * 70)
        for order in orders:
            print(f"{order['order_id']:<20} {order.get('customer_name', 'N/A')[:24]:<25} {order['status']:<12} ${order['total']:>9.2f}")
    
    elif cmd == 'status' and len(sys.argv) >= 4:
        automation.update_status(sys.argv[2], sys.argv[3])
    
    elif cmd == 'track' and len(sys.argv) >= 4:
        automation.add_tracking(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else '')
    
    elif cmd == 'invoice' and len(sys.argv) >= 3:
        path = automation.export_invoice(sys.argv[2])
        print(f"Invoice URL: https://psdepot.com/invoices/{path.split('/')[-1]}")
    
    else:
        print("Unknown command")


if __name__ == '__main__':
    main()
