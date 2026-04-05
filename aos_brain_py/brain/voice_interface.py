#!/usr/bin/env python3
"""
Voice Interface for Ternary Brain - TTS/STT Integration.

Provides:
- Text-to-Speech (TTS) output using system voices
- Speech-to-Text (STT) input using whisper or alternative
- Voice personality matching (Miles, Mortimer, Mylonen)
- Prosody control for natural speech
- Voice activity detection

Requirements:
- For TTS: pyttsx3 (cross-platform)
- For STT: whisper (optional), or system alternatives
"""

import os
import sys
import json
import time
import threading
import subprocess
from pathlib import Path
from typing import Optional, Callable, Dict, List
from dataclasses import dataclass


@dataclass
class VoiceConfig:
    """Voice configuration for agents."""
    name: str
    rate: int = 150  # Words per minute
    volume: float = 0.9
    pitch: int = 100  # Percentage
    language: str = "en"
    fill_words: List[str] = None  # "um", "uh", "like", etc.
    pause_probability: float = 0.1  # Chance to pause mid-sentence
    
    def __post_init__(self):
        if self.fill_words is None:
            self.fill_words = []


class TextToSpeech:
    """
    Text-to-Speech engine for the ternary brain.
    
    Features:
    - Multiple voice personalities
    - Prosody control (rate, pitch, volume)
    - Natural filler words and pauses
    - Agent-specific speaking styles
    """
    
    # Agent voice configurations
    AGENT_VOICES = {
        "miles": VoiceConfig(
            name="Miles",
            rate=165,
            volume=0.95,
            pitch=105,
            fill_words=["uhm", "so", "actually", "you know"],
            pause_probability=0.15
        ),
        "mortimer": VoiceConfig(
            name="Mortimer", 
            rate=140,
            volume=0.9,
            pitch=95,
            fill_words=["hmm", "let me see", "perhaps"],
            pause_probability=0.1
        ),
        "mylonen": VoiceConfig(
            name="Mylonen",
            rate=155,
            volume=0.92,
            pitch=100,
            fill_words=["uh", "like", "sort of"],
            pause_probability=0.12
        ),
        "mini": VoiceConfig(
            name="Mini",
            rate=180,
            volume=0.85,
            pitch=110,
            fill_words=[],
            pause_probability=0.05
        ),
    }
    
    def __init__(self):
        self.engine = None
        self.current_voice = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialize TTS engine."""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            print("[TTS] Engine initialized")
        except ImportError:
            print("[TTS] Warning: pyttsx3 not installed. Using fallback.")
            self.engine = None
        except Exception as e:
            print(f"[TTS] Error initializing: {e}")
            self.engine = None
    
    def _apply_voice_config(self, config: VoiceConfig):
        """Apply voice configuration to engine."""
        if self.engine:
            self.engine.setProperty('rate', config.rate)
            self.engine.setProperty('volume', config.volume)
            # Note: pyttsx3 doesn't support pitch directly
    
    def _add_naturalness(self, text: str, config: VoiceConfig) -> str:
        """Add natural filler words and pauses."""
        import random
        
        words = text.split()
        result = []
        
        for i, word in enumerate(words):
            result.append(word)
            
            # Add occasional filler
            if random.random() < config.pause_probability and config.fill_words:
                filler = random.choice(config.fill_words)
                result.append(f"... {filler},")
            
            # Add ellipsis for natural pauses
            elif random.random() < 0.05:
                result[-1] = result[-1] + ","
        
        return " ".join(result)
    
    def speak(self, text: str, agent: str = "default", block: bool = True):
        """
        Speak text with agent-specific voice.
        
        Args:
            text: Text to speak
            agent: Agent name for voice selection
            block: If True, wait for speech to complete
        """
        config = self.AGENT_VOICES.get(agent, VoiceConfig(name="Default"))
        
        # Add naturalness
        natural_text = self._add_naturalness(text, config)
        
        if self.engine:
            self._apply_voice_config(config)
            self.engine.say(natural_text)
            if block:
                self.engine.runAndWait()
        else:
            # Fallback: print to console
            print(f"[{config.name}] {natural_text}")
            if block:
                # Estimate speaking time
                word_count = len(natural_text.split())
                speak_time = word_count / (config.rate / 60)  # seconds
                time.sleep(speak_time)
    
    def speak_async(self, text: str, agent: str = "default") -> threading.Thread:
        """Speak asynchronously (non-blocking)."""
        thread = threading.Thread(target=self.speak, args=(text, agent, True))
        thread.start()
        return thread
    
    def save_to_file(self, text: str, filename: str, agent: str = "default"):
        """Save speech to audio file."""
        config = self.AGENT_VOICES.get(agent, VoiceConfig(name="Default"))
        natural_text = self._add_naturalness(text, config)
        
        if self.engine:
            self._apply_voice_config(config)
            self.engine.save_to_file(natural_text, filename)
            self.engine.runAndWait()
            print(f"[TTS] Saved to {filename}")
        else:
            print(f"[TTS] Cannot save: no engine. Text: {natural_text}")


class SpeechToText:
    """
    Speech-to-Text engine for the ternary brain.
    
    Supports multiple backends:
    - OpenAI Whisper (recommended)
    - system 'whisper' command
    - Alternative: speech_recognition with Google
    """
    
    def __init__(self, backend: str = "auto"):
        self.backend = backend
        self.whisper_available = self._check_whisper()
        self.recording = False
        
    def _check_whisper(self) -> bool:
        """Check if whisper is available."""
        try:
            subprocess.run(["whisper", "--help"], 
                          capture_output=True, check=True)
            return True
        except:
            try:
                import whisper
                return True
            except ImportError:
                return False
    
    def _record_audio(self, duration: int = 5, sample_rate: int = 16000) -> bytes:
        """Record audio from microphone."""
        try:
            import sounddevice as sd
            import numpy as np
            
            print(f"[STT] Recording for {duration} seconds...")
            recording = sd.rec(int(duration * sample_rate),
                             samplerate=sample_rate,
                             channels=1,
                             dtype='int16')
            sd.wait()
            
            # Convert to bytes
            audio_bytes = recording.tobytes()
            return audio_bytes
            
        except ImportError:
            print("[STT] Error: sounddevice not installed")
            return b""
    
    def transcribe_whisper(self, audio_path: str) -> Optional[str]:
        """Transcribe using OpenAI Whisper."""
        try:
            import whisper
            
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            return result["text"]
            
        except ImportError:
            # Try command-line whisper
            try:
                result = subprocess.run(
                    ["whisper", audio_path, "--model", "base", "--output_format", "txt"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Read output file
                output_file = audio_path.replace('.wav', '.txt')
                if os.path.exists(output_file):
                    with open(output_file) as f:
                        return f.read().strip()
                        
            except Exception as e:
                print(f"[STT] Whisper error: {e}")
                return None
    
    def transcribe_speech_recognition(self, audio_path: str = None) -> Optional[str]:
        """Transcribe using speech_recognition library."""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            if audio_path:
                with sr.AudioFile(audio_path) as source:
                    audio = recognizer.record(source)
            else:
                # Record from microphone
                with sr.Microphone() as source:
                    print("[STT] Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5)
            
            # Try Google Speech Recognition
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None
                
        except ImportError:
            print("[STT] speech_recognition not installed")
            return None
    
    def listen(self, duration: int = 5) -> Optional[str]:
        """
        Listen for speech and transcribe.
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Transcribed text or None
        """
        # Record audio
        audio_data = self._record_audio(duration)
        
        if not audio_data:
            return None
        
        # Save temporary file
        temp_file = "/tmp/stt_recording.wav"
        try:
            import wave
            with wave.open(temp_file, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio_data)
            
            # Try whisper first
            if self.whisper_available:
                return self.transcribe_whisper(temp_file)
            
            # Fallback to speech_recognition
            return self.transcribe_speech_recognition(temp_file)
            
        except Exception as e:
            print(f"[STT] Error: {e}")
            return None
        finally:
            # Cleanup
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def listen_continuous(self, callback: Callable[[str], None]):
        """Listen continuously and call callback for each utterance."""
        print("[STT] Continuous listening mode. Press Ctrl+C to stop.")
        
        try:
            while True:
                text = self.listen(duration=5)
                if text:
                    callback(text)
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("[STT] Stopped listening")


class VoiceInterface:
    """
    Complete voice interface combining TTS and STT.
    
    Provides bidirectional voice communication with the ternary brain.
    """
    
    def __init__(self):
        self.tts = TextToSpeech()
        self.stt = SpeechToText()
        self.active = False
        
    def speak_response(self, text: str, agent: str = "miles", block: bool = True):
        """Speak a response from the brain."""
        self.tts.speak(text, agent=agent, block=block)
    
    def listen_for_input(self, duration: int = 5) -> Optional[str]:
        """Listen for user input."""
        return self.stt.listen(duration)
    
    def interactive_session(self, brain, agent: str = "miles"):
        """
        Run interactive voice session.
        
        Loop:
        1. Listen for speech
        2. Send to brain
        3. Speak response
        """
        print("=" * 60)
        print(f"🎙️ VOICE SESSION with {agent.upper()}")
        print("=" * 60)
        print("Speak to interact. Press Ctrl+C to exit.")
        print()
        
        # Greeting
        greeting = f"Hi, this is {agent.capitalize()}. How can I help you?"
        self.tts.speak(greeting, agent=agent)
        
        try:
            while True:
                # Listen
                print("\n[Listening...]")
                user_input = self.stt.listen(duration=5)
                
                if user_input:
                    print(f"User: {user_input}")
                    
                    # Process through brain
                    from brain.seven_region import Observation
                    obs = Observation(source="voice", content=user_input)
                    result = brain.tick(obs)
                    
                    # Speak response
                    response = result.get("language", "I understand.")
                    print(f"{agent.capitalize()}: {response}")
                    self.tts.speak(response, agent=agent)
                else:
                    print("[No speech detected]")
                    
        except KeyboardInterrupt:
            print("\n\nEnding voice session.")
            self.tts.speak(f"Goodbye from {agent}.", agent=agent)


def demo_voice_interface():
    """Demo voice capabilities."""
    print("=" * 60)
    print("🎙️ VOICE INTERFACE DEMO")
    print("=" * 60)
    
    voice = VoiceInterface()
    
    # Demo TTS with different agents
    print("\n--- TTS Demo ---")
    
    test_text = "The ternary brain is now equipped with voice capabilities."
    
    for agent in ["miles", "mortimer", "mylonen"]:
        print(f"\n{agent.upper()}:")
        voice.tts.speak(test_text, agent=agent)
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("✅ Voice demo complete!")
    print()
    print("To use voice interface:")
    print("  from brain.voice_interface import VoiceInterface")
    print("  voice = VoiceInterface()")
    print("  voice.speak_response('Hello', agent='miles')")
    print("  text = voice.listen_for_input(duration=5)")
    print("=" * 60)


if __name__ == "__main__":
    demo_voice_interface()
