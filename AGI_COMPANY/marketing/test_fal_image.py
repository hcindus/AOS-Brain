#!/usr/bin/env python3
"""
Test FAL.AI Image Generation
Uses credentials from Hermes vault
"""

import requests
import json

# Miles credentials
FAL_KEY_ID = "13565e4b-b0ec-46cf-aa68-2abdc0abc6ad"
FAL_KEY_SECRET = "ccc1524b64bd146258cd4ab3b1dcbaad"

def test_fal_image_generation():
    """Test FAL.AI image generation with credentials"""
    
    print("=" * 70)
    print("FAL.AI IMAGE GENERATION TEST")
    print("=" * 70)
    
    # FAL.AI API endpoint
    url = "https://fal.run/fal-ai/fast-sdxl"
    
    headers = {
        "Authorization": f"Key {FAL_KEY_ID}:{FAL_KEY_SECRET}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": "AGI company logo, futuristic, neon blue and orange, digital brain, minimalist, high quality, 4k",
        "image_size": "square",  # or "landscape", "portrait"
        "num_inference_steps": 30,
        "guidance_scale": 7.5
    }
    
    print(f"\n🎨 Generating image...")
    print(f"   Prompt: {payload['prompt'][:50]}...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS!")
            print(f"   Image URL: {result.get('images', [{}])[0].get('url', 'N/A')[:60]}...")
            print(f"   Seed: {result.get('seed', 'N/A')}")
            
            # Save result
            with open("/tmp/fal_test_result.json", "w") as f:
                json.dump(result, f, indent=2)
            print(f"   💾 Result saved: /tmp/fal_test_result.json")
            
            return True
        else:
            print(f"\n❌ FAILED")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


if __name__ == "__main__":
    success = test_fal_image_generation()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ FAL.AI IMAGE GENERATION: WORKING")
        print("Ready for marketing team to use")
    else:
        print("❌ FAL.AI IMAGE GENERATION: FAILED")
        print("Check credentials or endpoint")
    print("=" * 70)
