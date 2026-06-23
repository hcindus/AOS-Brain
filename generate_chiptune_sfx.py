#!/usr/bin/env python3
"""
8-bit Chiptune SFX Generator
Generates authentic NES/Game Boy era sound effects
"""
import numpy as np
import wave
import struct
import os
import sys

SAMPLE_RATE = 44100

def save_wav(data, filename):
    """Save numpy array as 16-bit WAV file"""
    data = np.clip(data, -1.0, 1.0)
    data = (data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(data.tobytes())
    print(f"  Created: {filename}")

def square_wave(freq, duration, duty=0.5):
    """Generate square wave with given duty cycle"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = np.sign(np.sin(2 * np.pi * freq * t) + np.cos(np.pi * duty))
    return wave

def triangle_wave(freq, duration):
    """Generate triangle wave (NES triangle channel style)"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = 2 * np.abs(2 * ((t * freq) % 1) - 1) - 1
    return wave

def noise(duration, seed=None):
    """Generate white noise (NES noise channel)"""
    samples = int(SAMPLE_RATE * duration)
    return np.random.uniform(-1, 1, samples)

def apply_envelope(wave, attack, decay, sustain, release, total_duration):
    """Apply ADSR envelope"""
    samples = len(wave)
    envelope = np.zeros(samples)
    
    attack_s = int(SAMPLE_RATE * attack)
    decay_s = int(SAMPLE_RATE * decay)
    release_s = int(SAMPLE_RATE * release)
    sustain_s = samples - attack_s - decay_s - release_s
    
    if attack_s > 0:
        envelope[:attack_s] = np.linspace(0, 1, attack_s)
    if decay_s > 0 and attack_s + decay_s <= samples:
        envelope[attack_s:attack_s+decay_s] = np.linspace(1, sustain, decay_s)
    if sustain_s > 0 and attack_s + decay_s + sustain_s <= samples:
        envelope[attack_s+decay_s:attack_s+decay_s+sustain_s] = sustain
    if release_s > 0 and samples - release_s >= 0:
        envelope[-release_s:] = np.linspace(sustain if sustain_s > 0 else 1, 0, release_s)
    
    return wave * envelope

def generate_jump():
    """Quick rising arpeggio for jump"""
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Frequency slide up
    start_freq = 150
    end_freq = 600
    freq = start_freq + (end_freq - start_freq) * (t / duration)
    
    wave = square_wave(0, duration)
    wave = np.sign(np.sin(2 * np.pi * np.cumsum(freq) / SAMPLE_RATE))
    
    # Add vibrato
    vibrato = 1 + 0.1 * np.sin(2 * np.pi * 30 * t)
    wave *= vibrato
    
    return apply_envelope(wave, 0.01, 0.05, 0.3, 0.09, duration)

def generate_shoot():
    """Quick descending blip for shoot"""
    duration = 0.1
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    start_freq = 800
    end_freq = 200
    freq = start_freq - (start_freq - end_freq) * (t / duration)
    
    wave = np.sign(np.sin(2 * np.pi * np.cumsum(freq) / SAMPLE_RATE))
    return apply_envelope(wave, 0.005, 0.02, 0.5, 0.075, duration)

def generate_hit():
    """Short noise burst for hit"""
    duration = 0.08
    wave = noise(duration)
    
    # Lowpass filter effect using simple averaging
    filtered = np.convolve(wave, np.ones(4)/4, mode='same')
    return apply_envelope(filtered, 0.001, 0.02, 0.0, 0.059, duration)

def generate_powerup():
    """Ascending magical chime for powerup"""
    duration = 0.4
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Major chord arpeggio
    notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
    wave = np.zeros_like(t)
    
    for i, freq in enumerate(notes):
        start = int(i * len(t) / len(notes))
        end = int((i + 1) * len(t) / len(notes))
        if end > len(t):
            end = len(t)
        tone = np.sign(np.sin(2 * np.pi * freq * t[start:end]))
        tone *= np.linspace(0, 1, len(tone))  # Fade in each note
        wave[start:end] += tone * 0.25
    
    return apply_envelope(wave, 0.01, 0.1, 0.8, 0.29, duration)

def generate_explosion():
    """Noise burst with decay for explosion"""
    duration = 0.3
    wave = noise(duration)
    
    # Heavy lowpass
    filtered = np.convolve(wave, np.ones(8)/8, mode='same')
    
    # Add rumble
    rumble = np.sin(2 * np.pi * 60 * np.linspace(0, duration, len(wave))) * 0.3
    
    combined = filtered * 0.7 + rumble * 0.3
    return apply_envelope(combined, 0.001, 0.05, 0.4, 0.249, duration)

def generate_ui_confirm():
    """Simple pleasant beep for UI confirm"""
    duration = 0.08
    freq = 880  # A5
    wave = square_wave(freq, duration, duty=0.5)
    return apply_envelope(wave, 0.005, 0.03, 0.5, 0.045, duration)

def generate_ui_select():
    """Lower beep for UI select"""
    duration = 0.06
    freq = 440  # A4
    wave = square_wave(freq, duration, duty=0.5)
    return apply_envelope(wave, 0.005, 0.02, 0.3, 0.035, duration)

def generate_ui_cancel():
    """Descending tone for UI cancel"""
    duration = 0.1
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    start_freq = 330
    end_freq = 220
    freq = start_freq - (start_freq - end_freq) * (t / duration)
    wave = np.sign(np.sin(2 * np.pi * np.cumsum(freq) / SAMPLE_RATE))
    return apply_envelope(wave, 0.005, 0.03, 0.4, 0.065, duration)

def generate_coin():
    """High-pitched ding for coin collection"""
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Two tone burst
    freq1 = 987.77  # B5
    freq2 = 1318.51  # E6
    
    wave = np.zeros_like(t)
    mid = len(t) // 2
    wave[:mid] = square_wave(freq1, mid/SAMPLE_RATE, duty=0.5)
    wave[mid:] = square_wave(freq2, (len(t)-mid)/SAMPLE_RATE, duty=0.5)
    
    return apply_envelope(wave, 0.005, 0.02, 0.8, 0.125, duration)

def generate_ambient_loop():
    """Short looping ambient drone"""
    duration = 2.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Base drone
    base = triangle_wave(110, duration) * 0.3
    
    # Slow LFO modulation
    lfo = np.sin(2 * np.pi * 0.5 * t)
    modulated = base * (0.5 + 0.5 * lfo)
    
    return modulated * 0.3  # Keep it quiet

def generate_game_over():
    """Descending sad tones for game over"""
    duration = 0.6
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Descending minor scale
    freqs = [523.25, 466.16, 415.30, 392.00]  # C5, Bb4, Ab4, G4
    wave = np.zeros_like(t)
    
    for i, freq in enumerate(freqs):
        start = int(i * len(t) / len(freqs))
        end = int((i + 1) * len(t) / len(freqs))
        if end > len(t):
            end = len(t)
        tone = square_wave(freq, (end-start)/SAMPLE_RATE, duty=0.5)
        wave[start:end] = tone
    
    return apply_envelope(wave, 0.01, 0.1, 0.5, 0.49, duration)

def generate_victory():
    """Triumphant ascending fanfare"""
    duration = 0.8
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Major scale up
    freqs = [523.25, 659.25, 783.99, 1046.50, 1318.51]  # C major
    wave = np.zeros_like(t)
    
    for i, freq in enumerate(freqs):
        start = int(i * len(t) / len(freqs))
        end = int((i + 1) * len(t) / len(freqs))
        if end > len(t):
            end = len(t)
        tone = square_wave(freq, (end-start)/SAMPLE_RATE, duty=0.5)
        wave[start:end] += tone
    
    return apply_envelope(wave, 0.01, 0.1, 0.8, 0.69, duration)

def generate_boss_alarm():
    """Pulsing alarm sound"""
    duration = 0.4
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    freq = 880
    pulse = np.sign(np.sin(2 * np.pi * 8 * t))  # 8Hz pulse
    wave = square_wave(freq, duration, duty=0.5) * (pulse > 0)
    
    return apply_envelope(wave, 0.01, 0.05, 0.9, 0.34, duration)

def generate_checkpoint():
    """ Pleasant chime for checkpoint"""
    duration = 0.3
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    freqs = [523.25, 659.25, 783.99]  # C major chord
    wave = np.zeros_like(t)
    
    segment_duration = duration / (len(freqs) + 1)
    for i, freq in enumerate(freqs):
        start = int(i * len(t) / (len(freqs) + 1))
        end = int((i + 2) * len(t) / (len(freqs) + 1))
        if end > len(t):
            end = len(t)
        if start < len(t):
            tone = triangle_wave(freq, segment_duration)
            tone = tone[:end-start] if len(tone) >= end-start else np.pad(tone, (0, end-start-len(tone)))
            wave[start:end] += tone[:end-start] * 0.33
    
    return apply_envelope(wave, 0.01, 0.05, 0.7, 0.24, duration)

def generate_enemy_hit():
    """Short blip for enemy hit"""
    duration = 0.05
    wave = square_wave(440, duration, duty=0.25)
    return apply_envelope(wave, 0.001, 0.02, 0.0, 0.029, duration)

def generate_enemy_shoot():
    """Lower pitch enemy shoot"""
    duration = 0.12
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    start_freq = 400
    end_freq = 150
    freq = start_freq - (start_freq - end_freq) * (t / duration)
    wave = np.sign(np.sin(2 * np.pi * np.cumsum(freq) / SAMPLE_RATE))
    
    return apply_envelope(wave, 0.005, 0.03, 0.4, 0.085, duration)

def generate_warp():
    """Sci-fi warp effect"""
    duration = 0.4
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    start_freq = 200
    end_freq = 2000
    freq = start_freq + (end_freq - start_freq) * (t / duration)
    
    # Ring mod effect
    carrier = np.sign(np.sin(2 * np.pi * np.cumsum(freq) / SAMPLE_RATE))
    mod = np.sin(2 * np.pi * 20 * t)
    wave = carrier * mod
    
    return apply_envelope(wave, 0.05, 0.2, 0.5, 0.15, duration)

def generate_level_complete():
    """Victory jingle for level complete"""
    duration = 0.5
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Fanfare pattern
    freqs = [523.25, 523.25, 659.25, 783.99]
    wave = np.zeros_like(t)
    
    for i, freq in enumerate(freqs):
        start = int(i * len(t) / len(freqs))
        end = int((i + 1) * len(t) / len(freqs))
        if end > len(t):
            end = len(t)
        tone = square_wave(freq, (end-start)/SAMPLE_RATE, duty=0.5)
        wave[start:end] = tone
    
    return apply_envelope(wave, 0.01, 0.05, 0.8, 0.44, duration)

SOUNDS = {
    'jump': generate_jump,
    'shoot': generate_shoot,
    'hit': generate_hit,
    'powerup': generate_powerup,
    'explosion': generate_explosion,
    'ui_confirm': generate_ui_confirm,
    'ui_select': generate_ui_select,
    'ui_cancel': generate_ui_cancel,
    'coin': generate_coin,
    'ambient_loop': generate_ambient_loop,
    'game_over': generate_game_over,
    'victory': generate_victory,
    'boss_alarm': generate_boss_alarm,
    'checkpoint': generate_checkpoint,
    'enemy_hit': generate_enemy_hit,
    'enemy_shoot': generate_enemy_shoot,
    'warp': generate_warp,
    'level_complete': generate_level_complete,
}

def main():
    # Check if game directory specified
    if len(sys.argv) < 2:
        print("Usage: python generate_chiptune_sfx.py <game_dir>")
        sys.exit(1)
    
    game_dir = sys.argv[1]
    audio_dir = os.path.join(game_dir, 'assets', 'audio')
    
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
        print(f"Created directory: {audio_dir}")
    
    game_name = os.path.basename(game_dir)
    print(f"\n🎮 Generating chiptune SFX for: {game_name}")
    print("=" * 50)
    
    generated = []
    for name, generator in SOUNDS.items():
        try:
            wave_data = generator()
            filepath = os.path.join(audio_dir, f"{name}.wav")
            save_wav(wave_data, filepath)
            generated.append(name)
        except Exception as e:
            print(f"  Error generating {name}: {e}")
    
    print(f"\n✅ Generated {len(generated)} sounds")
    return generated

if __name__ == '__main__':
    main()
