#!/usr/bin/env python3
"""
Website Audit - Check all functionality
Tests: Links, wallet connect, phone lookup, cart, checkout
"""

import os
import re
from pathlib import Path
from typing import List, Dict

class WebsiteAudit:
    def __init__(self):
        self.sites = {
            "myl0nr0s.cloud": "/var/www/myl0nr0s.cloud",
            "tappylewis.cloud": "/var/www/tappylewis.cloud"
        }
        self.issues = []
        
    def audit_site(self, domain: str, path: str):
        """Audit a single website"""
        print(f"\n{'='*70}")
        print(f"AUDITING: {domain}")
        print(f"{'='*70}")
        
        # Check files exist
        html_files = list(Path(path).glob("*.html"))
        print(f"\n📄 HTML Files: {len(html_files)}")
        
        # Check critical pages
        critical = ["index.html", "cart.html", "checkout.html", "contact.html"]
        for page in critical:
            full_path = os.path.join(path, page)
            if os.path.exists(full_path):
                print(f"   ✅ {page}")
            else:
                print(f"   ❌ {page} - MISSING")
                self.issues.append(f"{domain}: {page} missing")
        
        # Check JavaScript files
        js_files = list(Path(path).glob("*.js"))
        print(f"\n📜 JavaScript Files: {len(js_files)}")
        
        # Check for wallet functionality
        has_wallet = self.check_wallet_functionality(path)
        print(f"\n💰 Wallet Integration: {'✅ Found' if has_wallet else '❌ Missing'}")
        if not has_wallet:
            self.issues.append(f"{domain}: Wallet connect missing")
        
        # Check for phone lookup
        has_phone = self.check_phone_functionality(path)
        print(f"\n📞 Phone Lookup: {'✅ Found' if has_phone else '❌ Missing'}")
        if not has_phone:
            self.issues.append(f"{domain}: Phone lookup missing")
        
        # Check cart functionality
        has_cart = self.check_cart_functionality(path)
        print(f"\n🛒 Cart System: {'✅ Found' if has_cart else '❌ Missing'}")
        if not has_cart:
            self.issues.append(f"{domain}: Cart system incomplete")
        
        # Check broken links
        broken = self.check_broken_links(path)
        if broken:
            print(f"\n🔗 Broken Links: {len(broken)}")
            for link in broken[:5]:
                print(f"   ❌ {link}")
                self.issues.append(f"{domain}: Broken link - {link}")
        else:
            print(f"\n🔗 Links: ✅ All internal links valid")
    
    def check_wallet_functionality(self, path: str) -> bool:
        """Check if wallet connection exists"""
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.html', '.js')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if any(x in content for x in ['metamask', 'walletconnect', 'web3', 'ethereum', 'ethers']):
                                return True
                    except:
                        pass
        return False
    
    def check_phone_functionality(self, path: str) -> bool:
        """Check if phone lookup exists"""
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.html', '.js', '.py')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if any(x in content for x in ['phone.*lookup', 'reverse.*phone', 'carrier', 'phonenumber']):
                                return True
                    except:
                        pass
        return False
    
    def check_cart_functionality(self, path: str) -> bool:
        """Check if cart is complete"""
        has_cart = False
        has_checkout = False
        has_stripe = False
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.html', '.js')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if 'cart' in file.lower():
                                has_cart = True
                            if 'checkout' in file.lower():
                                has_checkout = True
                            if 'stripe' in content or 'payment' in content:
                                has_stripe = True
                    except:
                        pass
        
        return has_cart and has_checkout and has_stripe
    
    def check_broken_links(self, path: str) -> List[str]:
        """Check for broken internal links"""
        broken = []
        html_files = list(Path(path).glob("*.html"))
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Find href links
                    links = re.findall(r'href=["\']([^"\']+)["\']', content)
                    for link in links:
                        if link.startswith('http'):
                            continue  # Skip external
                        if link.startswith('#'):
                            continue  # Skip anchors
                        if link.startswith('javascript'):
                            continue
                        
                        # Check if file exists
                        if link.endswith('.html') or link.endswith('.js') or link.endswith('.css'):
                            target = os.path.join(path, link)
                            if not os.path.exists(target):
                                broken.append(f"{html_file.name} -> {link}")
            except:
                pass
        
        return broken
    
    def run_full_audit(self):
        """Run complete audit"""
        print("=" * 70)
        print("WEBSITE AUDIT - FULL SYSTEM CHECK")
        print("=" * 70)
        
        for domain, path in self.sites.items():
            if os.path.exists(path):
                self.audit_site(domain, path)
            else:
                print(f"\n❌ {domain}: Path not found - {path}")
        
        # Summary
        print(f"\n{'='*70}")
        print("AUDIT SUMMARY")
        print(f"{'='*70}")
        
        if self.issues:
            print(f"\n❌ {len(self.issues)} issues found:")
            for issue in self.issues:
                print(f"   - {issue}")
        else:
            print("\n✅ All systems operational")
        
        return len(self.issues) == 0


if __name__ == "__main__":
    audit = WebsiteAudit()
    audit.run_full_audit()
