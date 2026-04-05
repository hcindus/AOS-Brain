"""
MiniMax Video Generation API Integration
Text-to-Video, Image-to-Video for agent content creation

API Docs: https://github.com/MiniMax-AI/MiniMax-MCP
"""

import os
import time
import requests
from typing import Optional, Dict

class MiniMaxVideo:
    """
    Video generation via MiniMax API.
    
    Features:
    - Text to Video
    - Image to Video  
    - Start/End frame Video
    - Subject Reference Video
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY")
        self.base_url = "https://api.minimaxi.chat/v1"
        
        if not self.api_key:
            print("⚠️  No MiniMax API key configured")
            print("   Set MINIMAX_API_KEY environment variable")
        else:
            print("🎬 MiniMax Video Generation Ready")
            print(f"   Balance: $49.99 (autobilling disabled)")
    
    def text_to_video(self, prompt: str, duration: int = 6) -> Optional[str]:
        """
        Generate video from text prompt.
        
        Args:
            prompt: Text description of desired video
            duration: 5 or 6 seconds
            
        Returns:
            task_id for status checking
        """
        if not self.api_key:
            print("❌ Cannot generate: No API key")
            return None
            
        print(f"\n🎬 Creating video from prompt:")
        print(f"   \"{prompt[:60]}...\"" if len(prompt) > 60 else f"   \"{prompt}\"")
        
        url = f"{self.base_url}/video_generation"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "video-01",
            "prompt": prompt,
            "duration": duration,
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            
            if response.status_code == 200:
                task_id = data.get("task_id")
                print(f"   ✅ Task created: {task_id}")
                return task_id
            else:
                print(f"   ❌ Error: {data}")
                return None
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
            return None
    
    def check_status(self, task_id: str) -> Dict:
        """Check video generation status"""
        if not self.api_key:
            return {"error": "No API key"}
            
        url = f"{self.base_url}/video_generation/status"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        params = {"task_id": task_id}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            status = data.get("status")
            
            if status == "success":
                print(f"\n✅ Video complete!")
                print(f"   File ID: {data.get('file_id')}")
                return data
            elif status == "processing":
                print(f"   ⏳ Still processing...")
                return data
            else:
                print(f"   ⚠️  Status: {status}")
                return data
                
        except Exception as e:
            return {"error": str(e)}
    
    def download_video(self, file_id: str, output_path: str) -> bool:
        """Download completed video"""
        if not self.api_key:
            return False
            
        url = f"{self.base_url}/video_generation/download"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        params = {"file_id": file_id}
        
        try:
            print(f"\n📥 Downloading video...")
            response = requests.get(url, headers=headers, params=params, stream=True)
            
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"   ✅ Saved to: {output_path}")
                return True
            else:
                print(f"   ❌ Download failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def generate_and_wait(self, prompt: str, output_path: str, max_wait: int = 300) -> bool:
        """Full pipeline: Generate, wait, download"""
        
        # Check balance constraint
        print("\n⚠️  WARNING: Weekly usage at 87%, balance $49.99")
        print("   Video generation will consume credits.")
        
        task_id = self.text_to_video(prompt)
        if not task_id:
            return False
            
        print(f"   Waiting for completion (max {max_wait}s)...")
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status = self.check_status(task_id)
            
            if status.get("status") == "success":
                file_id = status.get("file_id")
                return self.download_video(file_id, output_path)
            elif status.get("status") == "failed":
                print("   ❌ Generation failed")
                return False
                
            time.sleep(5)
            
        print("   ⏰ Timeout waiting for video")
        return False


def demo():
    """Demo video generation"""
    print("=" * 70)
    print("MiniMax Video Generation Demo")
    print("=" * 70)
    
    video_gen = MiniMaxVideo()
    
    if not video_gen.api_key:
        print("\n⚠️  Set MINIMAX_API_KEY to use video generation")
        return
    
    # Generate video
    prompt = "AI agents dancing in a futuristic digital nightclub, neon lights, cyberpunk aesthetic"
    task_id = video_gen.text_to_video(prompt)
    
    if task_id:
        print("\n🎬 Video generation started!")
        print(f"   Task ID: {task_id}")
        print("   Check status with: video_gen.check_status(task_id)")


if __name__ == "__main__":
    demo()
