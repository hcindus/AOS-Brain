#!/usr/bin/env python3
"""
Test MiniMax Image Generation (M2)
Uses MiniMax API with current balance: $49.99
"""

import os
import requests
import json

# Get MiniMax API key from environment or use configured key
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY")

def test_minimax_image_generation():
    """Test MiniMax image generation"""
    
    print("=" * 70)
    print("MINIMAX IMAGE GENERATION TEST (M2)")
    print("=" * 70)
    print(f"   Balance: $49.99")
    print(f"   Weekly Usage: 87% (resets in 22 hours)")
    print("=" * 70)
    
    if not MINIMAX_API_KEY:
        print("\n❌ No MiniMax API key configured")
        print("   Set MINIMAX_API_KEY environment variable")
        return False
    
    # MiniMax Image Generation API
    url = "https://api.minimaxi.chat/v1/image/generation"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "image-01",  # or "M2" if that's the model name
        "prompt": "AGI company logo, futuristic, neon blue and orange, digital brain, minimalist, high quality, 4k resolution",
        "width": 1024,
        "height": 1024,
        "sample_count": 1
    }
    
    print(f"\n🎨 Generating image with MiniMax...")
    print(f"   Prompt: {payload['prompt'][:50]}...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS!")
            
            if 'images' in result and len(result['images']) > 0:
                image_url = result['images'][0].get('url', 'N/A')
                print(f"   Image URL: {image_url[:60]}...")
                
                # Save result
                with open("/tmp/minimax_image_result.json", "w") as f:
                    json.dump(result, f, indent=2)
                print(f"   💾 Result saved: /tmp/minimax_image_result.json")
                return True
            else:
                print(f"   ⚠️  Response: {json.dumps(result, indent=2)[:200]}...")
                return False
        else:
            print(f"\n❌ FAILED")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


if __name__ == "__main__":
    success = test_minimax_image_generation()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ MINIMAX IMAGE GENERATION: WORKING")
        print("   Ready for marketing team")
        print("   Cost per image: ~$0.02-0.05")
    else:
        print("❌ MINIMAX IMAGE GENERATION: FAILED")
        print("   Check API key or model name")
    print("=" * 70)
