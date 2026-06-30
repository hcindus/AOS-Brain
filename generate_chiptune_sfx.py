#!/usr/bin/env python3
"""
8-bit Chiptune SFX Generator for Performance Supply Depot Games
Generates retro game sounds using synthetic waveforms
"""

import numpy as np
import wave
import struct
import os
from pathlib import Path

SAMPLE_RATE = 44100
AMPLITUDE = 0.5

def save_wav(samples, filename, sample_rate=SAMPLE_RATE):
    """Save numpy array as WAV file"""
    samples = np.clip(samples, -1.0, 1.0)
    samples = (samples * 32767).astype(np.int16)

    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(samples.tobytes())

def generate_jump(duration=0.3):
    """Rising pitch slide - classic jump sound"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq_start = 150
    freq_end = 600
    freq = np.linspace(freq_start, freq_end, len(t))
    samples = AMPLITUDE * np.sin(2 * np.pi * freq * t) * np.exp(-t * 2)
    return samples

def generate_shoot(duration=0.2):
    """Quick high pitch pulse - laser/pew sound"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 800
    samples = AMPLITUDE * np.sin(2 * np.pi * freq * t) * np.exp(-t * 15)
    # Add square wave overtone for 8-bit feel
    samples += AMPLITUDE * 0.3 * np.sign(np.sin(2 * np.pi * freq * t * 2)) * np.exp(-t * 15)
    return samples

def generate_hit(duration=0.15):
    """Short noise burst - impact sound"""
    samples = np.random.uniform(-AMPLITUDE, AMPLITUDE, int(SAMPLE_RATE * duration))
    # Lowpass filter effect using exponential decay
    t = np.linspace(0, duration, len(samples))
    samples *= np.exp(-t * 20)
    # Add some tone
    tone = AMPLITUDE * 0.5 * np.sin(2 * np.pi * 200 * t) * np.exp(-t * 15)
    return samples + tone

def generate_powerup(duration=0.4):
    """Ascending arpeggio - powerup collect sound"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    # Arpeggio: C-E-G-C
    notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
    samples = np.zeros_like(t)
    segment = len(t) // len(notes)

    for i, freq in enumerate(notes):
        start = i * segment
        end = (i + 1) * segment if i < len(notes) - 1 else len(t)
        t_seg = t[start:end]
        envelope = np.exp(-(t_seg - t_seg[0]) * 5) if len(t_seg) > 0 else np.array([])
        samples[start:end] = AMPLITUDE * np.sin(2 * np.pi * freq * t_seg) * envelope

    return samples

def generate_explosion(duration=0.5):
    """Noise with descending pitch - explosion sound"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    # White noise
    noise = np.random.uniform(-AMPLITUDE, AMPLITUDE, len(t))
    # Descending pitch rumble
    freq = 200 * np.exp(-t * 3)
    rumble = AMPLITUDE * 0.7 * np.sin(2 * np.pi * freq * t)
    # Exponential decay
    envelope = np.exp(-t * 4)
    return (noise * 0.6 + rumble) * envelope

def generate_coin(duration=0.15):
    """High pitched bing - coin collect"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 1200
    samples = AMPLITUDE * np.sin(2 * np.pi * freq * t) * np.exp(-t * 10)
    # Add higher harmonic
    samples += AMPLITUDE * 0.3 * np.sin(2 * np.pi * freq * 2 * t) * np.exp(-t * 12)
    return samples

def generate_ui_select(duration=0.08):
    """Short blip - menu selection"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 600
    samples = AMPLITUDE * 0.7 * np.sin(2 * np.pi * freq * t) * np.exp(-t * 15)
    return samples

def generate_ui_confirm(duration=0.12):
    """Two-tone success - menu confirm"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    # Rising two tones
    samples = np.zeros_like(t)
    half = len(t) // 2
    t1, t2 = t[:half], t[half:]
    samples[:half] = AMPLITUDE * 0.6 * np.sin(2 * np.pi * 600 * t1) * np.exp(-t1 * 10)
    samples[half:] = AMPLITUDE * 0.8 * np.sin(2 * np.pi * 900 * t2) * np.exp(-(t2 - t2[0]) * 10)
    return samples

def generate_ui_cancel(duration=0.12):
    """Falling tone - menu cancel/back"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq_start = 400
    freq_end = 200
    freq = np.linspace(freq_start, freq_end, len(t))
    samples = AMPLITUDE * 0.6 * np.sin(2 * np.pi * freq * t) * np.exp(-t * 8)
    return samples

def generate_ambient_loop(duration=2.0):
    """Subtle background drone - ambient atmosphere"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    # Multiple low frequency oscillators
    base = 0.2 * np.sin(2 * np.pi * 60 * t)
    base += 0.15 * np.sin(2 * np.pi * 65 * t)
    base += 0.1 * np.sin(2 * np.pi * 55 * t)
    # Slow modulation
    lfo = 1 + 0.3 * np.sin(2 * np.pi * 0.5 * t)
    samples = AMPLITUDE * base * lfo * 0.5
    return samples

def generate_game_over(duration=1.5):
    """Descending sad melody - game over"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    # Sad descending: G-F-E-D-C
    notes = [392, 349.23, 329.63, 293.66, 261.63]
    samples = np.zeros_like(t)
    segment = len(t) // len(notes)

    for i, freq in enumerate(notes):
        start = i * segment
        end = (i + 1) * segment if i < len(notes) - 1 else len(t)
        t_seg = t[start:end]
        # Square wave for retro feel
        samples[start:end] = AMPLITUDE * 0.4 * np.sign(np.sin(2 * np.pi * freq * t_seg))

    return samples * np.exp(-t * 0.5)

def generate_level_complete(duration=1.0):
    """Victory fanfare - level complete"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    # Victory pattern: C-E-G-C-G
    notes = [523.25, 659.25, 783.99, 1046.50, 783.99]
    samples = np.zeros_like(t)
    segment = len(t) // len(notes)

    for i, freq in enumerate(notes):
        start = i * segment
        end = (i + 1) * segment if i < len(notes) - 1 else len(t)
        t_seg = t[start:end]
        # Mix square and sine
        sq = np.sign(np.sin(2 * np.pi * freq * t_seg))
        sin = np.sin(2 * np.pi * freq * t_seg)
        samples[start:end] = AMPLITUDE * 0.3 * (sq * 0.6 + sin * 0.4)

    return samples

def generate_checkpoint(duration=0.3):
    """Positive chime - checkpoint reached"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    # Rising ping
    freq = 800 + 400 * t / duration
    samples = AMPLITUDE * 0.7 * np.sin(2 * np.pi * freq * t) * np.exp(-t * 8)
    return samples

def generate_boss_alarm(duration=0.4):
    """Urgent alternating tones"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    samples = np.zeros_like(t)
    segment = len(t) // 4
    for i in range(4):
        start = i * segment
        end = (i + 1) * segment
        t_seg = t[start:end]
        freq = 500 if i % 2 == 0 else 700
        samples[start:end] = AMPLITUDE * 0.5 * np.sin(2 * np.pi * freq * t_seg)
    return samples * np.exp(-t * 3)

def generate_enemy_hit(duration=0.1):
    """Short grunt - enemy damage"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    noise = np.random.uniform(-AMPLITUDE * 0.5, AMPLITUDE * 0.5, len(t))
    tone = AMPLITUDE * 0.3 * np.sin(2 * np.pi * 150 * t)
    envelope = np.exp(-t * 30)
    return (noise + tone) * envelope

def generate_enemy_shoot(duration=0.15):
    """Lower pitch shot - enemy projectile"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 400
    samples = AMPLITUDE * np.sin(2 * np.pi * freq * t) * np.exp(-t * 12)
    return samples

def generate_laser(duration=0.2):
    """Sci-fi laser with frequency sweep"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = 1000 * np.exp(-t * 8)
    samples = AMPLITUDE * np.sin(2 * np.pi * freq * t) * np.exp(-t * 5)
    return samples

# Map of sound types to generator functions
SFX_GENERATORS = {
    'jump.wav': generate_jump,
    'shoot.wav': generate_shoot,
    'hit.wav': generate_hit,
    'powerup.wav': generate_powerup,
    'explosion.wav': generate_explosion,
    'coin.wav': generate_coin,
    'ui_select.wav': generate_ui_select,
    'ui_confirm.wav': generate_ui_confirm,
    'ui_cancel.wav': generate_ui_cancel,
    'ui_back.wav': generate_ui_cancel,
    'ambient_loop.wav': generate_ambient_loop,
    'game_over.wav': generate_game_over,
    'level_complete.wav': generate_level_complete,
    'checkpoint.wav': generate_checkpoint,
    'boss_alarm.wav': generate_boss_alarm,
    'boss_hit.wav': generate_hit,
    'enemy_hit.wav': generate_enemy_hit,
    'enemy_shoot.wav': generate_enemy_shoot,
    'laser.wav': generate_laser,
}

# Games to process (exclude __pycache__)
GAMES = [
    'MilkMan', 'ReggieStarr', 'TEC-MA79-Digital', 'censys',
    'dusty', 'issia_property', 'laser-pistol', 'memory-technology',
    'milkman-game', 'neon-courier', 'netprobe-droidscript', 'netprobe',
    'portal', 'quantum-defender', 'ronstrapp', 'socket-arsenal',
    'tappys-online', 'teleport', 'tshirts', 'upcoming',
    'venues', 'voice-system', 'websites'
]

def main():
    base_path = Path('/root/.openclaw/workspace/aocros/projects')
    generated_count = 0
    updated_games = []

    for game in GAMES:
        audio_dir = base_path / game / 'assets' / 'audio'

        if not audio_dir.exists():
            print(f"⚠️  {game}: No audio directory, skipping")
            continue

        print(f"\n🎮 Processing: {game}")
        game_sfx_count = 0

        for filename, generator in SFX_GENERATORS.items():
            filepath = audio_dir / filename

            try:
                samples = generator()
                save_wav(samples, str(filepath))
                game_sfx_count += 1
                generated_count += 1
                print(f"  ✓ {filename}")
            except Exception as e:
                print(f"  ✗ {filename}: {e}")

        if game_sfx_count > 0:
            updated_games.append((game, game_sfx_count))

    print(f"\n{'='*50}")
    print(f"✅ GENERATION COMPLETE!")
    print(f"📊 Total files generated: {generated_count}")
    print(f"🎮 Games updated: {len(updated_games)}")
    print(f"\nPer-game breakdown:")
    for game, count in updated_games:
        print(f"  • {game}: {count} files")

    return updated_games

if __name__ == '__main__':
    main()
