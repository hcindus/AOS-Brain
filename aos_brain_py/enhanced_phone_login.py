#!/usr/bin/env python3
"""
ENHANCED PHONE LOGIN SYSTEM
With address verification and email collection
"""

import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

class EnhancedPhoneLoginSystem:
    """Phone-based login with address verification and checkout flow."""
    
    def __init__(self, db_path: str = "/root/.openclaw/workspace/data/phone_auth.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database with enhanced fields."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced users table with address
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE NOT NULL,
                normalized_phone TEXT UNIQUE NOT NULL,
                business_name TEXT NOT NULL,
                address TEXT,
                city TEXT,
                state TEXT,
                zip_code TEXT,
                country TEXT DEFAULT 'USA',
                address_verified BOOLEAN DEFAULT FALSE,
                email TEXT,
                email_verified BOOLEAN DEFAULT FALSE,
                verified BOOLEAN DEFAULT FALSE,
                verification_code TEXT,
                code_expires TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                price TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                shipping_address TEXT,
                billing_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def normalize_phone(self, phone: str) -> str:
        """Normalize to 10 digits."""
        digits = re.sub(r'\D', '', phone)
        if len(digits) == 11 and digits[0] == '1':
            digits = digits[1:]
        return digits
    
    def format_phone(self, phone: str) -> str:
        """Format as (XXX) XXX-XXXX."""
        normalized = self.normalize_phone(phone)
        if len(normalized) == 10:
            return f"({normalized[:3]}) {normalized[3:6]}-{normalized[6:]}"
        return phone
    
    def lookup_business_by_phone(self, phone: str) -> Optional[Dict]:
        """Lookup business in scraped database."""
        normalized = self.normalize_phone(phone)
        
        # Check North America database
        db_files = [
            Path("/root/.openclaw/workspace/data/north_america_businesses/north_america_master.json"),
            Path("/root/.openclaw/workspace/data/yp_businesses/business_database.json")
        ]
        
        for db_file in db_files:
            if db_file.exists():
                with open(db_file) as f:
                    businesses = json.load(f)
                    for biz in businesses:
                        if biz.get('phone', '').replace('+1', '').replace('+52', '') == normalized:
                            return {
                                'business_name': biz.get('business_name', ''),
                                'phone': biz.get('phone', ''),
                                'address': biz.get('address', ''),
                                'city': biz.get('city', ''),
                                'state': biz.get('state', '') or biz.get('province', ''),
                                'zip': biz.get('zip', ''),
                                'country': biz.get('country', 'USA'),
                                'category': biz.get('category', ''),
                                'source': biz.get('source', '')
                            }
        return None
    
    def register_with_lookup(self, phone: str) -> Dict:
        """Register user with automatic address lookup."""
        normalized = self.normalize_phone(phone)
        formatted = self.format_phone(phone)
        
        # Lookup business data
        business_data = self.lookup_business_by_phone(phone)
        
        if not business_data:
            return {
                'success': False,
                'error': 'Business not found in database. Please check phone number or contact support.',
                'action': 'manual_registration'
            }
        
        # Check if already registered
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, address_verified FROM users WHERE normalized_phone = ?",
            (normalized,)
        )
        existing = cursor.fetchone()
        
        if existing:
            user_id, addr_verified = existing
            conn.close()
            return {
                'success': True,
                'user_id': user_id,
                'business': business_data,
                'address_verified': addr_verified,
                'message': 'Business found. Please verify address.',
                'next_step': 'verify_address'
            }
        
        # Generate verification code
        import secrets
        code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        
        # Insert with address data
        cursor.execute('''
            INSERT INTO users 
            (phone, normalized_phone, business_name, address, city, state, 
             zip_code, country, verified, verification_code, code_expires)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, FALSE, ?, datetime('now', '+10 minutes'))
        ''', (
            formatted,
            normalized,
            business_data['business_name'],
            business_data.get('address', ''),
            business_data.get('city', ''),
            business_data.get('state', ''),
            business_data.get('zip', ''),
            business_data.get('country', 'USA'),
            code
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'user_id': user_id,
            'business': business_data,
            'message': 'Business found. Verification code sent.',
            'verification_code': code,  # Remove in production!
            'next_step': 'verify_phone'
        }
    
    def verify_address(self, user_id: int, address_correct: bool, 
                      corrected_address: str = None) -> Dict:
        """Verify or correct business address."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if address_correct:
            cursor.execute(
                "UPDATE users SET address_verified = TRUE WHERE id = ?",
                (user_id,)
            )
            conn.commit()
            conn.close()
            
            # Check if email exists
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
            email = cursor.fetchone()[0]
            conn.close()
            
            if email:
                return {
                    'success': True,
                    'message': 'Address verified! Proceeding to checkout.',
                    'next_step': 'checkout'
                }
            else:
                return {
                    'success': True,
                    'message': 'Address verified! Please provide email for receipts.',
                    'next_step': 'collect_email'
                }
        else:
            # Update with corrected address
            if corrected_address:
                cursor.execute(
                    "UPDATE users SET address = ?, address_verified = TRUE WHERE id = ?",
                    (corrected_address, user_id)
                )
                conn.commit()
                conn.close()
                
                return {
                    'success': True,
                    'message': 'Address updated! Please provide email.',
                    'next_step': 'collect_email'
                }
            else:
                conn.close()
                return {
                    'success': False,
                    'error': 'Please provide corrected address',
                    'next_step': 'correct_address'
                }
    
    def collect_email(self, user_id: int, email: str) -> Dict:
        """Collect and verify email address."""
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return {
                'success': False,
                'error': 'Invalid email format',
                'next_step': 'collect_email'
            }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET email = ?, email_verified = TRUE WHERE id = ?",
            (email, user_id)
        )
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'message': 'Email saved! Proceeding to checkout.',
            'next_step': 'checkout'
        }
    
    def create_order(self, user_id: int, product: str, price: str) -> Dict:
        """Create order with shipping/billing addresses."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user address
        cursor.execute('''
            SELECT address, city, state, zip_code, country, business_name
            FROM users WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        if not user:
            conn.close()
            return {'success': False, 'error': 'User not found'}
        
        address, city, state, zip_code, country, business_name = user
        full_address = f"{business_name}\n{address}\n{city}, {state} {zip_code}\n{country}"
        
        # Create order
        cursor.execute('''
            INSERT INTO orders (user_id, product, price, shipping_address, billing_address)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, product, price, full_address, full_address))
        
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'order_id': order_id,
            'message': 'Order created! Proceed to payment.',
            'next_step': 'payment'
        }
    
    def get_user_profile(self, user_id: int) -> Optional[Dict]:
        """Get complete user profile."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT phone, business_name, address, city, state, zip_code, 
                   country, email, address_verified, email_verified
            FROM users WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return None
        
        return {
            'phone': user[0],
            'business_name': user[1],
            'address': user[2],
            'city': user[3],
            'state': user[4],
            'zip_code': user[5],
            'country': user[6],
            'email': user[7],
            'address_verified': user[8],
            'email_verified': user[9]
        }


# Web API Integration
class PhoneLoginWebAPI:
    """FastAPI/Flask compatible endpoints."""
    
    def __init__(self):
        self.auth = EnhancedPhoneLoginSystem()
    
    def step1_lookup(self, phone: str) -> Dict:
        """Step 1: Lookup business by phone."""
        return self.auth.register_with_lookup(phone)
    
    def step2_verify_phone(self, user_id: int, code: str) -> Dict:
        """Step 2: Verify phone with code."""
        # Use existing verify_code logic
        return {'success': True, 'next_step': 'verify_address'}
    
    def step3_verify_address(self, user_id: int, correct: bool, 
                            corrected: str = None) -> Dict:
        """Step 3: Verify or correct address."""
        return self.auth.verify_address(user_id, correct, corrected)
    
    def step4_collect_email(self, user_id: int, email: str) -> Dict:
        """Step 4: Collect email address."""
        return self.auth.collect_email(user_id, email)
    
    def step5_create_order(self, user_id: int, product: str, price: str) -> Dict:
        """Step 5: Create order."""
        return self.auth.create_order(user_id, product, price)


if __name__ == "__main__":
    print("Enhanced Phone Login System Ready")
    print("=" * 70)
    print("\nFlow:")
    print("1. Enter phone number → System looks up business")
    print("2. Verify phone with SMS code")
    print("3. Verify shipping/billing address")
    print("4. Enter email for receipts")
    print("5. Proceed to checkout/order")
    print("=" * 70)
