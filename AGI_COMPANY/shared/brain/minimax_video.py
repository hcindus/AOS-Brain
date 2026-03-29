"""
MiniMax Video Generation Integration
Text-to-Video, Image-to-Video for agent content creation.

Uses MiniMax API via MCP (Model Context Protocol).
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
        
        print("🎬 MiniMax Video Generation Ready")
        
    def text_to_video(self, prompt: str, duration: int = 6) -< Optional[str]:
        """
        Generate video from text description.
        
        Args:
            prompt: Text description of desired video
            duration: 5 or 6 seconds
            
        Returns:
            task_id for status checking
        """
        if not self.api_key:
            print("⚠️  No MiniMax API key configured")
            return None
            
        print(f"\n🎬 Creating video from prompt:")
        print(f"   \"{prompt[:100]}...\"" if len(prompt) > 100 else f"   \"{prompt}\"")
        
        # API endpoint
        url = f"{self.base_url}/video_generation"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "video-01",
            "prompt": prompt,
            "duration": duration,  # 5 or 6 seconds
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
            
    def check_status(self, task_id: str) -< Dict:
        """
        Check video generation status.
        
        Statuses:
        - processing: Still generating
        - success: Done, file_id available
        - failed: Error occurred
        """
        if not self.api_key:
            return {"error": "No API key"}
            
        url = f"{self.base_url}/query/video_generation"
        
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
        """
        Download completed video.
        
        Args:
            file_id: From successful generation
            output_path: Where to save video
        """
        if not self.api_key:
            return False
            
        url = f"{self.base_url}/files/{file_id}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            print(f"\n📥 Downloading video...")
            response = requests.get(url, headers=headers, stream=True)
            
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
            
    def generate_and_wait(self, prompt: str, output_path: str, 
                          max_wait: int = 300) -> bool:
        """
        Full pipeline: Generate and download with waiting.
        
        Args:
            prompt: Video description
            output_path: Where to save
            max_wait: Maximum seconds to wait
            
        Returns:
            True if successful
        """
        # Start generation
        task_id = self.text_to_video(prompt)
        if not task_id:
            return False
            
        # Wait for completion
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
                
            time.sleep(5)  # Check every 5 seconds
            
        print("   ⏰ Timeout waiting for video")
        return False


def demo():
    """Demo video generation"""
    print("=" * 70)
    print("MiniMax Video Generation Demo")
    print("=" * 70)
    
    # Initialize (requires API key)
    video_gen = MiniMaxVideo()
    
    if not video_gen.api_key:
        print("\n⚠️  Set MINIMAX_API_KEY environment variable")
        print("   Get key from: https://www.minimaxi.com/")
        return
        
    # Generate video
    prompt = "A futuristic AI agent working in a virtual office, holographic displays, cyberpunk aesthetic"
    task_id = video_gen.text_to_video(prompt)
    
    if task_id:
        print("\n🎬 Video generation started!")
        print(f"   Task ID: {task_id}")
        print("   Check status with: video_gen.check_status(task_id)")


if __name__ == "__main__":
    demo()
