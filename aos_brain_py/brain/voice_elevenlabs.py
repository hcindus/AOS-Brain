#!/usr/bin/env python3
"""
ElevenLabs Voice Integration for Ternary Brain.

Voice IDs from vault:
- Adam: pNInz6obpgDQGcFmaJgB (Deep, professional)
- Antoni: ErXwobYiHyaRYGkd4X9r (Well-rounded)
- Arnold: VR6AewLTigWG4xSOukaG (Crisp, news anchor)
- Bella: EXAVITQu4vr4xnSDxMaL (Warm, engaging)
- Dorothy: ThT5KcBeLxXkiuQ8jT1 (Natural, soft)
- Elli: MF3mGyEYCl7XYWbV9V6 (Friendly, casual)
- Josh: TxGEqnHWrfWFTfGW9XjX (Deep, narrator)
- Rachel: 21m00Tcm4TlvDq8ikWAM (Calm, soothing)
- Sam: yoZ06aMxZJJ28mfd3POB (Youthful, energetic)
- Torable: ThT5KcBeLxXkiuQ8jT1 (Warm, natural)
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass

# ElevenLabs Configuration
ELEVENLABS_API_KEY = "sk_deca3c774b72a1dad75bd3028f0d36bac49ef76a4bcb573f"
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"


@dataclass
class ElevenLabsVoice:
    """Voice configuration for agents."""
    name: str
    voice_id: str
    description: str
    agent: str  # Which agent uses this voice


class ElevenLabsVoiceManager:
    """
    Manages ElevenLabs voices for all agents.
    
    Voices from vault available to brain agents.
    """
    
    # Voice library from vault
    VOICES = {
        "adam": ElevenLabsVoice(
            "Adam", 
            "pNInz6obpgDQGcFmaJgB",
            "Deep, energetic, professional - perfect for sales",
            "miles"
        ),
        "antoni": ElevenLabsVoice(
            "Antoni",
            "ErXwobYiHyaRYGkd4X9r", 
            "Well-rounded, versatile narrator",
            "mylonen"
        ),
        "arnold": ElevenLabsVoice(
            "Arnold",
            "VR6AewLTigWG4xSOukaG",
            "Crisp, news-anchor delivery",
            "pulp"
        ),
        "bella": ElevenLabsVoice(
            "Bella",
            "EXAVITQu4vr4xnSDxMaL",
            "Warm, engaging, approachable",
            "jane"
        ),
        "dorothy": ElevenLabsVoice(
            "Dorothy",
            "ThT5KcBeLxXkiuQ8jT1",
            "Natural, soft, comforting",
            "greet"
        ),
        "elli": ElevenLabsVoice(
            "Elli",
            "MF3mGyEYCl7XYWbV9V6",
            "Friendly, casual, conversational",
            "clippy"
        ),
        "josh": ElevenLabsVoice(
            "Josh",
            "TxGEqnHWrfWFTfGW9XjX",
            "Deep, authoritative narrator",
            "mortimer"
        ),
        "rachel": ElevenLabsVoice(
            "Rachel",
            "21m00Tcm4TlvDq8ikWAM",
            "Calm, soothing, professional",
            "closester"
        ),
        "sam": ElevenLabsVoice(
            "Sam",
            "yoZ06aMxZJJ28mfd3POB",
            "Youthful, energetic, vibrant",
            "hume"
        ),
        "miles_special": ElevenLabsVoice(
            "Miles Special",
            "ztnpYzQJyWffPj1VC5Uw",
            "Energetic, professional sales voice",
            "miles_primary"
        ),
    }
    
    def __init__(self):
        self.api_key = ELEVENLABS_API_KEY
        self.api_url = ELEVENLABS_API_URL
        self.audio_dir = Path.home() / ".aos" / "brain" / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
    def get_voice_for_agent(self, agent_name: str) -> ElevenLabsVoice:
        """Get appropriate voice for agent."""
        agent_lower = agent_name.lower()
        
        # Direct match
        if agent_lower in self.VOICES:
            return self.VOICES[agent_lower]
        
        # Search by assigned agent
        for voice in self.VOICES.values():
            if voice.agent == agent_lower:
                return voice
        
        # Default to Adam (Miles)
        return self.VOICES["adam"]
    
    def speak(self, text: str, voice_id: str = None, agent: str = None) -> Optional[str]:
        """
        Convert text to speech using ElevenLabs.
        
        Args:
            text: Text to speak
            voice_id: Specific voice ID or None for agent default
            agent: Agent name to get appropriate voice
            
        Returns:
            Path to audio file or None if failed
        """
        if not text.strip():
            return None
        
        # Get voice
        if agent and not voice_id:
            voice = self.get_voice_for_agent(agent)
            voice_id = voice.voice_id
        elif not voice_id:
            voice_id = self.VOICES["adam"].voice_id
        
        # Clean text
        text = self._clean_text(text)
        
        # Generate audio
        url = f"{self.api_url}/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Save audio
                timestamp = int(time.time() * 1000)
                audio_path = self.audio_dir / f"speech_{timestamp}.mp3"
                
                with open(audio_path, "wb") as f:
                    f.write(response.content)
                
                return str(audio_path)
            else:
                print(f"[ElevenLabs] Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"[ElevenLabs] Exception: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean text for TTS."""
        # Remove markdown
        text = text.replace("**", "").replace("*", "")
        text = text.replace("`", "").replace("#", "")
        
        # Limit length
        if len(text) > 5000:
            text = text[:5000] + "..."
        
        return text.strip()
    
    def list_voices(self) -> List[Dict]:
        """List all available voices."""
        return [
            {
                "name": v.name,
                "voice_id": v.voice_id,
                "description": v.description,
                "agent": v.agent
            }
            for v in self.VOICES.values()
        ]


class SkillLearningProfile:
    """
    Profile that updates when agents learn new skills.
    
    Tracks:
    - Skills learned
    - Knowledge accumulated  
    - Experience gained
    - Profile auto-updates
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.profile_path = Path.home() / ".aos" / "brain" / "profiles" / f"{agent_name}_profile.json"
        self.profile_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing or create new
        self.profile = self._load_profile()
    
    def _load_profile(self) -> Dict:
        """Load profile from disk."""
        if self.profile_path.exists():
            try:
                with open(self.profile_path) as f:
                    return json.load(f)
            except:
                pass
        
        # Default profile
        return {
            "name": self.agent_name,
            "created": time.time(),
            "skills": [],
            "knowledge_domains": [],
            "experiences": [],
            "level": 1,
            "total_learnings": 0,
            "last_updated": time.time(),
        }
    
    def _save_profile(self):
        """Save profile to disk."""
        self.profile["last_updated"] = time.time()
        with open(self.profile_path, 'w') as f:
            json.dump(self.profile, f, indent=2)
    
    def learn_skill(self, skill_name: str, skill_description: str, category: str = "general"):
        """Record new skill learned."""
        skill = {
            "name": skill_name,
            "description": skill_description,
            "category": category,
            "learned_at": time.time(),
        }
        
        # Check if already known
        existing = [s for s in self.profile["skills"] if s["name"] == skill_name]
        if not existing:
            self.profile["skills"].append(skill)
            self.profile["total_learnings"] += 1
            
            # Update knowledge domains
            if category not in self.profile["knowledge_domains"]:
                self.profile["knowledge_domains"].append(category)
            
            # Level up every 10 skills
            if self.profile["total_learnings"] % 10 == 0:
                self.profile["level"] += 1
                print(f"[SkillProfile] {self.agent_name} leveled up to {self.profile['level']}!")
            
            self._save_profile()
            print(f"[SkillProfile] {self.agent_name} learned: {skill_name}")
    
    def add_experience(self, experience: str, result: str = "success"):
        """Record experience."""
        exp = {
            "description": experience,
            "result": result,
            "timestamp": time.time(),
        }
        self.profile["experiences"].append(exp)
        
        # Keep only last 100 experiences
        if len(self.profile["experiences"]) > 100:
            self.profile["experiences"] = self.profile["experiences"][-100:]
        
        self._save_profile()
    
    def get_profile_summary(self) -> str:
        """Get profile summary."""
        return f"""{self.agent_name} Profile:
  Level: {self.profile['level']}
  Skills: {len(self.profile['skills'])}
  Knowledge: {', '.join(self.profile['knowledge_domains'])}
  Total Learnings: {self.profile['total_learnings']}
  Experiences: {len(self.profile['experiences'])}
"""


# Integration with brain
class EnhancedVoiceInterface:
    """Voice interface with ElevenLabs and skill tracking."""
    
    def __init__(self, agent_name: str = "miles"):
        self.voice_manager = ElevenLabsVoiceManager()
        self.profile = SkillLearningProfile(agent_name)
        self.agent_name = agent_name
    
    def speak(self, text: str) -> Optional[str]:
        """Speak text with agent's voice."""
        audio_path = self.voice_manager.speak(text, agent=self.agent_name)
        
        if audio_path:
            self.profile.add_experience(f"Spoke: {text[:50]}...")
        
        return audio_path
    
    def learn_skill(self, skill_name: str, description: str, category: str = "general"):
        """Learn new skill and update profile."""
        self.profile.learn_skill(skill_name, description, category)
    
    def get_profile(self) -> str:
        """Get current profile."""
        return self.profile.get_profile_summary()


if __name__ == "__main__":
    # Test voices
    print("=" * 70)
    print("🎙️ ELEVENLABS VOICE SYSTEM")
    print("=" * 70)
    print()
    
    voice_mgr = ElevenLabsVoiceManager()
    
    print("Available Voices:")
    for voice in voice_mgr.list_voices():
        print(f"  - {voice['name']}: {voice['description']}")
    
    print()
    print("Testing voice for Miles...")
    
    # Test with Miles
    miles_voice = EnhancedVoiceInterface("miles")
    
    # Learn some skills
    miles_voice.learn_skill("sales", "Professional sales techniques", "business")
    miles_voice.learn_skill("consulting", "Strategic business consulting", "business")
    
    print()
    print(miles_voice.get_profile())
    
    print("✅ Voice system ready!")
