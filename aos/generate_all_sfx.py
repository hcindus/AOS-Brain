#!/usr/bin/env python3
"""
Daily SFX Generator for Performance Supply Depot Games
Generates 8-bit chiptune style WAV files for all games needing sound effects
"""

import numpy as np
import wave
import os
import subprocess
from datetime import datetime

SAMPLE_RATE = 44100

# Define games and their SFX needs
GAMES = {
    "quantum-defender": {
        "dir": "/root/.openclaw/workspace/aocros/projects/quantum-defender/assets/audio",
        "type": "space_shooter",
        "priority": True
    },
    "milkman-game": {
        "dir": "/root/.openclaw/workspace/aocros/projects/milkman-game/audio",
        "type": "platformer",
        "priority": True
    },
    "neon-courier": {
        "dir": "/root/.openclaw/workspace/aocros/projects/neon-courier/audio",
        "type": "racing",
        "priority": True
    },
    "ReggieStarr": {
        "dir": "/root/.openclaw/workspace/aocros/projects/ReggieStarr/audio",
        "type": "platformer",
        "priority": True
    }
}

# Standard SFX definitions
SFX_DEFINITIONS = {
    "jump": {
        "desc": "Jump - quick ascending tone",
        "generator": lambda: generate_jump()
    },
    "shoot": {
        "desc": "Shoot - pew pew laser",
        "generator": lambda: generate_shoot()
    },
    "hit": {
        "desc": "Hit - impact sound",
        "generator": lambda: generate_hit()
    },
    "powerup": {
        "desc": "Powerup - energy boost",
        "generator": lambda: generate_powerup()
    },
    "explosion": {
        "desc": "Explosion - boom",
        "generator": lambda: generate_explosion()
    },
    "coin": {
        "desc": "Coin collect - pleasant chime",
        "generator": lambda: generate_coin()
    },
    "ui_select": {
        "desc": "UI select - short blip",
        "generator": lambda: generate_ui_select()
    },
    "ui_confirm": {
        "desc": "UI confirm - positive tone",
        "generator": lambda: generate_ui_confirm()
    },
    "ui_cancel": {
        "desc": "UI cancel - negative tone",
        "generator": lambda: generate_ui_cancel()
    },
    "game_over": {
        "desc": "Game over - descending",
        "generator": lambda: generate_game_over()
    },
    "victory": {
        "desc": "Victory - fanfare",
        "generator": lambda: generate_victory()
    },
    "checkpoint": {
        "desc": "Checkpoint - success chime",
        "generator": lambda: generate_checkpoint()
    },
    "enemy_hit": {
        "desc": "Enemy hit - thud",
        "generator": lambda: generate_enemy_hit()
    }
}

# Game-specific SFX requirements
GAME_SFX = {
    "space_shooter": ["shoot", "explosion", "hit", "powerup", "enemy_hit", "ui_select", "ui_confirm", "game_over", "victory"],
    "platformer": ["jump", "shoot", "hit", "powerup", "coin", "explosion", "ui_select", "ui_confirm", "game_over", "victory", "checkpoint", "enemy_hit"],
    "racing": ["hit", "powerup", "coin", "checkpoint", "explosion", "ui_select", "ui_confirm", "game_over", "victory", "enemy_hit"]
}

def save_wav(filename, audio_data):
    audio_data = np.int16(audio_data * 32767)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_data.tobytes())

# === SFX GENERATORS ===

def generate_jump():
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 200 + 400 * (t / duration)
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 8)
    audio = wave * envelope
    return audio / np.max(np.abs(audio))

def generate_shoot():
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 800 - 400 * (t / duration)
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 10)
    audio = wave * envelope
    return audio / np.max(np.abs(audio))

def generate_hit():
    duration = 0.1
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    wave = np.sin(2 * np.pi * 600 * t)
    envelope = np.exp(-t * 20)
    audio = wave * envelope
    return audio / np.max(np.abs(audio))

def generate_powerup():
    duration = 0.4
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [440, 554, 659, 880]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.08
        mask = (t >= start) & (t < start + 0.15)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * np.exp(-(t[mask] - start) * 6)
    return audio / np.max(np.abs(audio))

def generate_explosion():
    duration = 0.3
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    noise = np.random.normal(0, 1, len(t))
    rumble = np.sin(2 * np.pi * 100 * t) * 0.5
    envelope = np.exp(-t * 6)
    audio = (noise * 0.7 + rumble * 0.3) * envelope
    return audio / np.max(np.abs(audio))

def generate_coin():
    duration = 0.3
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [987, 1318]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.1
        mask = (t >= start) & (t < start + 0.15)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * np.exp(-(t[mask] - start) * 8)
    return audio / np.max(np.abs(audio))

def generate_ui_select():
    duration = 0.05
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    wave = np.sin(2 * np.pi * 1000 * t)
    envelope = np.exp(-t * 30)
    audio = wave * envelope
    return audio / np.max(np.abs(audio))

def generate_ui_confirm():
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [880, 1108]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.05
        mask = (t >= start) & (t < start + 0.1)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * np.exp(-(t[mask] - start) * 10)
    return audio / np.max(np.abs(audio))

def generate_ui_cancel():
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 440 - 220 * (t / duration)
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 8)
    audio = wave * envelope
    return audio / np.max(np.abs(audio))

def generate_game_over():
    duration = 0.6
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [523, 466, 415, 349]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.12
        mask = (t >= start) & (t < start + 0.15)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * 0.5
    return audio / np.max(np.abs(audio))

def generate_victory():
    duration = 0.8
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [523, 659, 783, 1046, 1318]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.12
        mask = (t >= start) & (t < start + 0.2)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * np.exp(-(t[mask] - start) * 3)
    return audio / np.max(np.abs(audio))

def generate_checkpoint():
    duration = 0.3
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [659, 880]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.1
        mask = (t >= start) & (t < start + 0.15)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * np.exp(-(t[mask] - start) * 8)
    return audio / np.max(np.abs(audio))

def generate_enemy_hit():
    duration = 0.08
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 300 - 150 * (t / duration)
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 25)
    audio = wave * envelope
    return audio / np.max(np.abs(audio))

def main():
    print("=" * 70)
    print("🎮 PERFORMANCE SUPPLY DEPOT - DAILY SFX GENERATOR")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 70)
    
    created_files = []
    
    for game_name, game_config in GAMES.items():
        print(f"\n🔍 Checking {game_name}...")
        
        audio_dir = game_config["dir"]
        game_type = game_config["type"]
        
        # Ensure directory exists
        os.makedirs(audio_dir, exist_ok=True)
        
        # Get required SFX for this game type
        required_sfx = GAME_SFX.get(game_type, [])
        
        for sfx_name in required_sfx:
            sfx_file = f"{sfx_name}.wav"
            sfx_path = os.path.join(audio_dir, sfx_file)
            
            # Skip if file already exists
            if os.path.exists(sfx_path):
                print(f"   ✓ {sfx_file} (exists)")
                continue
            
            # Generate the SFX
            if sfx_name in SFX_DEFINITIONS:
                try:
                    audio_data = SFX_DEFINITIONS[sfx_name]["generator"]()
                    save_wav(sfx_path, audio_data)
                    print(f"   🆕 {sfx_file}")
                    created_files.append({
                        "game": game_name,
                        "file": sfx_file,
                        "desc": SFX_DEFINITIONS[sfx_name]["desc"],
                        "path": sfx_path
                    })
                except Exception as e:
                    print(f"   ❌ Error creating {sfx_file}: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 GENERATION SUMMARY")
    print("=" * 70)
    
    if created_files:
        print(f"\n✅ Created {len(created_files)} new SFX files:\n")
        
        current_game = None
        for item in created_files:
            if item["game"] != current_game:
                current_game = item["game"]
                print(f"\n📁 {current_game}/")
            print(f"   → {item['file']:<20} {item['desc']}")
    else:
        print("\n📭 No new files needed - all SFX already present!")
    
    print("\n" + "=" * 70)
    
    return created_files

if __name__ == "__main__":
    main()
