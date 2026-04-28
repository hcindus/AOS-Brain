#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Content Review Script for X Marketing
Ensures all content meets ethical standards before posting.

ETHICAL CHECKLIST:
✓ No false claims or exaggerated savings
✓ Actual prices and services offered
✓ Educational value for small businesses
✓ Respectful tone (no pressure tactics)
✓ Clear contact information
✓ Accurate phone number (888-881-6834)
✓ Correct website (psdepot.com)
✓ Under 280 characters (X limit)
"""

import sys
import re

def review_content(file_path=None, text=None):
    """Review content against ethical guidelines"""
    
    if file_path:
        with open(file_path, 'r') as f:
            text = f.read()
    
    if not text:
        print("❌ No content provided")
        return False
    
    issues = []
    warnings = []
    
    # Check 1: Phone number accuracy
    if "888-881-6834" not in text:
        issues.append("❌ Missing or incorrect phone number (should be 888-881-6834)")
    
    # Check 2: Website accuracy
    if "psdepot.com" not in text:
        issues.append("❌ Missing or incorrect website (should be psdepot.com)")
    
    # Check 3: Character limit
    if len(text) > 280:
        issues.append(f"❌ Exceeds X character limit: {len(text)} chars (max 280)")
    
    # Check 4: No false claims
    false_claims = [
        r"save \d+%",
        r"guaranteed.*savings",
        r"best.*price",
        r"lowest.*cost",
        r"#1.*supplier",
    ]
    for pattern in false_claims:
        if re.search(pattern, text, re.IGNORECASE):
            warnings.append(f"⚠️ Possible subjective claim detected: '{pattern}'")
    
    # Check 5: No pressure tactics
    pressure_words = ["act now", "limited time", "urgent", "don't miss", "hurry", "last chance"]
    for word in pressure_words:
        if word.lower() in text.lower():
            warnings.append(f"⚠️ Pressure tactic detected: '{word}'")
    
    # Check 6: Has educational or service value
    value_indicators = ["tip", "help", "service", "repair", "install", "question", "quote", "available", "starting at"]
    has_value = any(indicator in text.lower() for indicator in value_indicators)
    if not has_value:
        warnings.append("⚠️ Content may lack educational or service value")
    
    # Report
    print("=" * 60)
    print("CONTENT ETHICS REVIEW")
    print("=" * 60)
    print(f"\nContent:\n{text}\n")
    print(f"Character count: {len(text)}/280")
    print(f"\nIssues found: {len(issues)}")
    print(f"Warnings: {len(warnings)}")
    
    if issues:
        print("\n❌ CRITICAL ISSUES:")
        for issue in issues:
            print(f"   {issue}")
    
    if warnings:
        print("\n⚠️ WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
    
    if not issues and not warnings:
        print("\n✅ Content passed ethical review")
        return True
    
    if not issues:
        print("\n✅ Content passed (with warnings)")
        return True
    
    print("\n❌ Content failed ethical review")
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: review_content.py <text_file>")
        print("       review_content.py --test")
        return
    
    if sys.argv[1] == "--test":
        # Test with sample content
        test_content = """Tip: Thermal paper darkens when exposed to heat. Store properly to extend life. Questions? 888-881-6834 | psdepot.com"""
        review_content(text=test_content)
    else:
        review_content(file_path=sys.argv[1])

if __name__ == "__main__":
    main()
