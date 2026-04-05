#!/usr/bin/env python3
"""
Identify which API service this key belongs to
"""

API_KEY = "sk-api-TX-XTNb1QOfiC0DmcpFU6rfGKJ6iiRMVsQjMsC8nnIBFWqNMKGd8Dg8tzQMmmSxLdgLD12Y1YO9azhrrYDRAihxR-fHwcNYvopauDyeR8ZppkTb3IpTaS0Q"

print("API Key Analysis:")
print(f"Key prefix: {API_KEY[:20]}...")
print(f"Key length: {len(API_KEY)}")
print()

# Check patterns
if API_KEY.startswith("sk-"):
    print("Pattern: OpenAI-style key (sk-)")
    print("  - Could be: OpenAI, or OpenAI-compatible service")
    
if "api" in API_KEY.lower():
    print("  - Contains 'api' - may indicate API-specific format")
    
if len(API_KEY) > 100:
    print(f"  - Long key ({len(API_KEY)} chars) - typical for modern APIs")

print()
print("Services to test:")
print("  1. OpenAI (api.openai.com)")
print("  2. Anthropic Claude (api.anthropic.com)")
print("  3. Custom/OpenAI-compatible proxy")
print("  4. MiniMax (if using OpenAI-compatible endpoint)")
