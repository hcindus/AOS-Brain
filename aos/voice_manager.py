#!/usr/bin/env python3
"""
AOS Voice Manager - ElevenLabs Integration
Ported from legacy brain to Ternary System
"""

import os
import json
import time
import requests
import tempfile
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass

# ElevenLabs Configuration
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"


@dataclass
class VoiceConfig:
    """Voice configuration"""
    name: str
    voice_id: str
    description: str
    stability: float = 0.5
    similarity_boost: float = 0.75


class ElevenLabsVoiceManager:
    """
    ElevenLabs Voice Integration for Ternary Brain.
    Ported from legacy brain architecture.
    """
    
    # Voice library from legacy system
    VOICES = {
        "adam": VoiceConfig("Adam", "pNInz6obpgDQGcFmaJgB", "Deep, professional", 0.5, 0.75),
        "antoni": VoiceConfig("Antoni", "ErXwobYiHyaRYGkd4X9r", "Well-rounded", 0.5, 0.75),
        "arnold": VoiceConfig("Arnold", "VR6AewLTigWG4xSOukaG", "Crisp, news anchor", 0.5, 0.75),
        "bella": VoiceConfig("Bella", "EXAVITQu4vr4xnSDxMaL", "Warm, engaging", 0.5, 0.75),
        "josh": VoiceConfig("Josh", "TxGEqnHWrfWFTfGW9XjX", "Deep, narrator", 0.5, 0.75),
        "rachel": VoiceConfig("Rachel", "21m00Tcm4TlvDq8ikWAM", "Calm, soothing", 0.5, 0.75),
        "sam": VoiceConfig("Sam", "yoZ06aMxZJJ28mfd3POB", "Youthful, energetic", 0.5, 0.75),
    }
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path.home() / ".aos" / "cache" / "voice"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        })
        
        self.current_voice = self.VOICES["adam"]  # Default
        self.request_count = 0
        self.cache_hits = 0
        
        print(f"[VoiceManager] Initialized with {len(self.VOICES)} voices")
    
    def set_voice(self, voice_key: str):
        """Set current voice"""
        if voice_key in self.VOICES:
            self.current_voice = self.VOICES[voice_key]
            print(f"[VoiceManager] Voice set to: {self.current_voice.name}")
        else:
            print(f"[VoiceManager] Unknown voice: {voice_key}, using default")
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text"""
        import hashlib
        return hashlib.md5(f"{self.current_voice.voice_id}:{text}".encode()).hexdigest()
    
    def speak(self, text: str, voice: Optional[str] = None, 
              play: bool = True) -> Optional[Path]:
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            voice: Voice key (or use current)
            play: Whether to play audio
            
        Returns:
            Path to audio file or None
        """
        if not ELEVENLABS_API_KEY:
            print("[VoiceManager] No API key set, using text only")
            return None
        
        if voice and voice in self.VOICES:
            voice_config = self.VOICES[voice]
        else:
            voice_config = self.current_voice
        
        # Check cache
        cache_key = self._get_cache_key(text)
        cache_path = self.cache_dir / f"{cache_key}.mp3"
        
        if cache_path.exists():
            self.cache_hits += 1
            print(f"[VoiceManager] Cache hit: {text[:30]}...")
            if play:
                self._play_audio(cache_path)
            return cache_path
        
        # Generate speech
        try:
            url = f"{ELEVENLABS_API_URL}/text-to-speech/{voice_config.voice_id}"
            
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": voice_config.stability,
                    "similarity_boost": voice_config.similarity_boost
                }
            }
            
            response = self.session.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                # Save to cache
                with open(cache_path, "wb") as f:
                    f.write(response.content)
                
                self.request_count += 1
                print(f"[VoiceManager] Generated: {text[:30]}...")
                
                if play:
                    self._play_audio(cache_path)
                
                return cache_path
            else:
                print(f"[VoiceManager] API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[VoiceManager] Error: {e}")
            return None
    
    def _play_audio(self, audio_path: Path):
        """Play audio file"""
        try:
            import subprocess
            subprocess.run(["aplay", str(audio_path)], 
                         capture_output=True, check=False)
        except:
            pass  # Audio playback not critical
    
    def get_stats(self) -> Dict:
        """Get voice manager statistics"""
        return {
            "requests": self.request_count,
            "cache_hits": self.cache_hits,
            "current_voice": self.current_voice.name,
            "cache_size": len(list(self.cache_dir.glob("*.mp3")))
        }


class VoiceInterface:
    """
    High-level voice interface for Ternary Brain
    """
    
    def __init__(self):
        self.voice_manager = ElevenLabsVoiceManager()
        self.enabled = ELEVENLABS_API_KEY != ""
        
    def announce(self, message: str, priority: str = "normal"):
        """Announce message via voice"""
        if not self.enabled:
            print(f"[Voice] {message}")
            return
        
        # Only speak important messages
        if priority in ["high", "critical"]:
            self.voice_manager.speak(message, play=True)
        else:
            print(f"[Voice] {message}")
    
    def set_emotional_tone(self, tone: str):
        """Set voice based on emotional tone"""
        voice_map = {
            "calm": "rachel",
            "energetic": "sam",
            "professional": "adam",
            "warm": "bella",
            "serious": "arnold"
        }
        
        if tone in voice_map:
            self.voice_manager.set_voice(voice_map[tone])


if __name__ == "__main__":
    print("=" * 70)
    print("  AOS Voice Manager - Test")
    print("=" * 70)
    
    voice = VoiceInterface()
    
    print("\nAvailable voices:")
    for key, config in ElevenLabsVoiceManager.VOICES.items():
        print(f"  {key}: {config.name} - {config.description}")
    
    print("\nVoice interface ready")
    print("Note: Requires ELEVENLABS_API_KEY environment variable for TTS")
    print("=" * 70)
