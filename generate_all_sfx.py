#!/usr/bin/env python3
"""
Performance Supply Depot - Universal 8-Bit SFX Generator
Generates retro chiptune-style sound effects for all games
"""

import numpy as np
import wave
import os
import sys
import shutil

SAMPLE_RATE = 44100

def save_wav(filepath, audio_data):
    """Save audio data as WAV file"""
    audio_data = np.int16(np.clip(audio_data, -1, 1) * 32767)
    
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_data.tobytes())
    
    print(f"  Created: {os.path.basename(filepath)}")

def generate_jump():
    """Jump - quick upward sweep"""
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 150 + 600 * (t / duration)
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 5)
    audio = wave * envelope
    return audio / np.max(np.abs(audio))

def generate_shoot():
    """Shoot - laser fire"""
    duration = 0.12
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 900 - 400 * (t / duration)
    wave = np.square(2 * np.pi * freq * t) * 0.5
    envelope = np.exp(-t * 15)
    audio = wave * envelope
    return audio / np.max(np.abs(audio))

def generate_hit():
    """Hit - impact"""
    duration = 0.1
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    wave = np.sin(2 * np.pi * 500 * t)
    envelope = np.exp(-t * 25)
    audio = wave * envelope
    return audio / np.max(np.abs(audio))

def generate_powerup():
    """Powerup - energy boost arpeggio"""
    duration = 0.4
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [523, 659, 783, 1046]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.08
        mask = (t >= start) & (t < start + 0.15)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * np.exp(-(t[mask] - start) * 6)
    return audio / np.max(np.abs(audio))

def generate_explosion():
    """Explosion - big boom with noise"""
    duration = 0.4
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    noise = np.random.normal(0, 1, len(t))
    rumble = np.sin(2 * np.pi * 60 * t) * 0.6
    envelope = np.exp(-t * 4)
    audio = (noise * 0.6 + rumble * 0.4) * envelope
    return audio / np.max(np.abs(audio))

def generate_ui_select():
    """UI selection - blip"""
    duration = 0.1
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 1200
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 15)
    return (wave * envelope) / np.max(np.abs(wave * envelope))

def generate_ui_confirm():
    """UI confirm - positive tone"""
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 800 + 400 * (t / duration)
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 10)
    return (wave * envelope) / np.max(np.abs(wave * envelope))

def generate_ui_cancel():
    """UI cancel - negative buzz"""
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 300 - 100 * (t / duration)
    wave = np.square(2 * np.pi * freq * t) * 0.5
    envelope = np.exp(-t * 8)
    return (wave * envelope) / np.max(np.abs(wave * envelope))

def generate_coin():
    """Coin pickup - chime"""
    duration = 0.2
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [880, 1760]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.06
        mask = (t >= start) & (t < start + 0.12)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * np.exp(-(t[mask] - start) * 10)
    return audio / np.max(np.abs(audio))

def generate_game_over():
    """Game over - descending tones"""
    duration = 0.6
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [523, 466, 415, 349]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.12
        mask = (t >= start) & (t < start + 0.2)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * 0.5
    return audio / np.max(np.abs(audio))

def generate_victory():
    """Victory - fanfare"""
    duration = 1.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [523, 659, 783, 1046, 1318]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.15
        mask = (t >= start) & (t < start + 0.3)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * 0.5
    return audio / np.max(np.abs(audio))

def generate_checkpoint():
    """Checkpoint - success ping"""
    duration = 0.25
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [880, 1100]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.08
        mask = (t >= start) & (t < start + 0.15)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * np.exp(-(t[mask] - start) * 8)
    return audio / np.max(np.abs(audio))

def generate_warp():
    """Warp - sci-fi warp effect"""
    duration = 0.5
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 400 + 2000 * (t / duration)
    wave = np.sin(2 * np.pi * freq * t)
    noise = np.random.normal(0, 0.1, len(t))
    envelope = np.exp(-t * 1.5)
    audio = (wave + noise) * envelope
    return audio / np.max(np.abs(audio))

def generate_ambient_loop():
    """Ambient loop - background drone"""
    duration = 2.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    drone = np.sin(2 * np.pi * 60 * t) * 0.3
    shimmer = np.sin(2 * np.pi * 240 * t + np.sin(2 * np.pi * 0.5 * t) * 10) * 0.2
    audio = drone + shimmer
    return audio / np.max(np.abs(audio))

def generate_level_complete():
    """Level complete - success melody"""
    duration = 0.5
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    notes = [880, 1100, 1320, 1760]
    audio = np.zeros_like(t)
    for i, freq in enumerate(notes):
        start = i * 0.1
        mask = (t >= start) & (t < start + 0.15)
        audio[mask] += np.sin(2 * np.pi * freq * t[mask]) * 0.4
    return audio / np.max(np.abs(audio))

def generate_boss_alarm():
    """Boss alarm - warning pulse"""
    duration = 0.3
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 300
    pulse = np.sin(2 * np.pi * freq * t) * (np.sin(2 * np.pi * 8 * t) > 0).astype(float)
    envelope = np.exp(-t * 3)
    audio = pulse * envelope
    return audio / np.max(np.abs(audio))

def generate_enemy_shoot():
    """Enemy shoot - lower pitch laser"""
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 400 - 200 * (t / duration)
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 12)
    audio = wave * envelope
    return audio / np.max(np.abs(audio))

def generate_enemy_hit():
    """Enemy hit - metallic clank"""
    duration = 0.1
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 600
    wave = np.square(2 * np.pi * freq * t) * 0.3
    noise = np.random.normal(0, 0.3, len(t))
    envelope = np.exp(-t * 20)
    audio = (wave + noise) * envelope
    return audio / np.max(np.abs(audio))

def main():
    print("=" * 60)
    print("PERFORMANCE SUPPLY DEPOT - SFX GENERATOR")
    print("=" * 60)
    
    # Games to process
    games = [
        ("neon-courier", "/root/.openclaw/workspace/aocros/projects/neon-courier/assets/audio"),
        ("portal", "/root/.openclaw/workspace/aocros/projects/portal/assets/audio"),
        ("quantum-defender", "/root/.openclaw/workspace/aocros/projects/quantum-defender/assets/audio"),
        ("ronstrapp", "/root/.openclaw/workspace/aocros/projects/ronstrapp/assets/audio"),
        ("tappys-online", "/root/.openclaw/workspace/aocros/projects/tappys-online/assets/audio"),
        ("teleport", "/root/.openclaw/workspace/aocros/projects/teleport/assets/audio"),
        ("nog", "/root/.openclaw/workspace/aocros/projects/upcoming/nog/assets/audio"),
        ("milkman-game", "/root/.openclaw/workspace/aocros/projects/milkman-game/audio"),
        ("laser-pistol", "/root/.openclaw/workspace/aocros/projects/laser-pistol/assets/audio"),
    ]
    
    generators = {
        "jump.wav": (generate_jump, "Jump"),
        "shoot.wav": (generate_shoot, "Shoot"),
        "hit.wav": (generate_hit, "Hit"),
        "powerup.wav": (generate_powerup, "Powerup"),
        "explosion.wav": (generate_explosion, "Explosion"),
        "ui_select.wav": (generate_ui_select, "UI Select"),
        "ui_confirm.wav": (generate_ui_confirm, "UI Confirm"),
        "ui_cancel.wav": (generate_ui_cancel, "UI Cancel"),
        "coin.wav": (generate_coin, "Coin"),
        "game_over.wav": (generate_game_over, "Game Over"),
        "victory.wav": (generate_victory, "Victory"),
        "checkpoint.wav": (generate_checkpoint, "Checkpoint"),
        "warp.wav": (generate_warp, "Warp"),
        "ambient_loop.wav": (generate_ambient_loop, "Ambient Loop"),
        "level_complete.wav": (generate_level_complete, "Level Complete"),
        "boss_alarm.wav": (generate_boss_alarm, "Boss Alarm"),
        "enemy_shoot.wav": (generate_enemy_shoot, "Enemy Shoot"),
        "enemy_hit.wav": (generate_enemy_hit, "Enemy Hit"),
    }
    
    total_created = 0
    
    for game_name, audio_dir in games:
        print(f"\n[{game_name}]")
        
        # Create directory if needed
        os.makedirs(audio_dir, exist_ok=True)
        
        # Copy generator script to directory
        try:
            shutil.copy('/root/.openclaw/workspace/generate_all_sfx.py', os.path.join(audio_dir, 'generate_sfx.py'))
        except:
            pass
        
        # Generate each SFX if missing
        for filename, (generator, desc) in generators.items():
            filepath = os.path.join(audio_dir, filename)
            if not os.path.exists(filepath):
                try:
                    audio = generator()
                    save_wav(filepath, audio)
                    total_created += 1
                except Exception as e:
                    print(f"  ERROR creating {filename}: {e}")
        
        print(f"  Updated: {audio_dir}")
    
    print("\n" + "=" * 60)
    print(f"TOTAL SFX FILES CREATED: {total_created}")
    print("=" * 60)

if __name__ == "__main__":
    main()
