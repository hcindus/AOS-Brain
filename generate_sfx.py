#!/usr/bin/env python3
"""
8-bit Chiptune SFX Generator
Generates retro game sound effects using mathematical waveforms
"""

import wave
import struct
import math
import os

# Audio settings
SAMPLE_RATE = 22050
BIT_DEPTH = 16
CHANNELS = 1

def generate_silence(duration):
    """Generate silence"""
    samples = int(SAMPLE_RATE * duration)
    return [0] * samples

def generate_square_wave(frequency, duration, volume=0.5):
    """Generate square wave (classic 8-bit sound)"""
    samples = int(SAMPLE_RATE * duration)
    data = []
    for i in range(samples):
        value = volume * 32767 if math.sin(2 * math.pi * frequency * i / SAMPLE_RATE) > 0 else -volume * 32767
        data.append(int(value))
    return data

def generate_sawtooth_wave(frequency, duration, volume=0.5):
    """Generate sawtooth wave"""
    samples = int(SAMPLE_RATE * duration)
    data = []
    period = SAMPLE_RATE / frequency
    for i in range(samples):
        value = volume * 32767 * (2 * (i % period) / period - 1)
        data.append(int(value))
    return data

def generate_triangle_wave(frequency, duration, volume=0.5):
    """Generate triangle wave"""
    samples = int(SAMPLE_RATE * duration)
    data = []
    period = SAMPLE_RATE / frequency
    for i in range(samples):
        phase = (i % period) / period
        if phase < 0.25:
            value = 4 * phase
        elif phase < 0.75:
            value = 2 - 4 * phase
        else:
            value = 4 * phase - 4
        data.append(int(volume * 32767 * value))
    return data

def generate_noise(duration, volume=0.3):
    """Generate white noise"""
    import random
    samples = int(SAMPLE_RATE * duration)
    data = []
    for _ in range(samples):
        value = volume * 32767 * (random.random() * 2 - 1)
        data.append(int(value))
    return data

def apply_envelope(data, attack=0.01, decay=0.1, sustain=0.7, release=0.2, duration=None):
    """Apply ADSR envelope to sound data"""
    if duration is None:
        duration = len(data) / SAMPLE_RATE
    
    total_samples = len(data)
    attack_samples = int(SAMPLE_RATE * attack)
    decay_samples = int(SAMPLE_RATE * decay)
    release_samples = int(SAMPLE_RATE * release)
    sustain_samples = total_samples - attack_samples - decay_samples - release_samples
    
    result = []
    for i in range(total_samples):
        if i < attack_samples:
            envelope = i / attack_samples
        elif i < attack_samples + decay_samples:
            envelope = 1 - (1 - sustain) * (i - attack_samples) / decay_samples
        elif i < attack_samples + decay_samples + sustain_samples:
            envelope = sustain
        else:
            envelope = sustain * (1 - (i - attack_samples - decay_samples - sustain_samples) / release_samples)
        
        result.append(int(data[i] * envelope))
    return result

def apply_fade_out(data, fade_duration):
    """Apply fade out to data"""
    samples = len(data)
    fade_samples = int(SAMPLE_RATE * fade_duration)
    result = []
    for i in range(samples):
        if i >= samples - fade_samples:
            fade = (samples - i) / fade_samples
        else:
            fade = 1.0
        result.append(int(data[i] * fade))
    return result

def frequency_sweep(start_freq, end_freq, duration, wave_type='square'):
    """Generate frequency sweep"""
    samples = int(SAMPLE_RATE * duration)
    data = []
    for i in range(samples):
        progress = i / samples
        freq = start_freq + (end_freq - start_freq) * progress
        phase = 2 * math.pi * freq * i / SAMPLE_RATE
        
        if wave_type == 'square':
            value = 0.5 * 32767 if math.sin(phase) > 0 else -0.5 * 32767
        elif wave_type == 'sawtooth':
            value = 0.5 * 32767 * (2 * (i * freq / SAMPLE_RATE % 1) - 1)
        else:
            value = 0.5 * 32767 * math.sin(phase)
        
        data.append(int(value))
    return data

def arpeggio(frequencies, duration_per_note, total_duration):
    """Generate arpeggio pattern"""
    samples_per_note = int(SAMPLE_RATE * duration_per_note)
    total_samples = int(SAMPLE_RATE * total_duration)
    data = []
    
    sample_idx = 0
    note_idx = 0
    while sample_idx < total_samples:
        freq = frequencies[note_idx % len(frequencies)]
        for _ in range(samples_per_note):
            if sample_idx >= total_samples:
                break
            phase = 2 * math.pi * freq * sample_idx / SAMPLE_RATE
            value = 0.5 * 32767 if math.sin(phase) > 0 else -0.5 * 32767
            data.append(int(value))
            sample_idx += 1
        note_idx += 1
    
    return data[:total_samples]

def save_wav(filename, data):
    """Save data to WAV file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.setnframes(len(data))
        
        # Convert to bytes
        packed_data = struct.pack('<%dh' % len(data), *data)
        wav_file.writeframes(packed_data)

# SFX Generation Functions
def create_jump():
    """Rising square wave arpeggio for jump"""
    data = frequency_sweep(150, 600, 0.15, 'square')
    data = apply_envelope(data, attack=0.01, decay=0.05, sustain=0.3, release=0.1, duration=0.15)
    return data

def create_shoot():
    """Short noise burst or pulse for shooting"""
    data = frequency_sweep(800, 400, 0.1, 'square')
    data = apply_envelope(data, attack=0.001, decay=0.05, sustain=0.2, release=0.05, duration=0.1)
    return data

def create_hit():
    """Low pitch decay for impact"""
    data = frequency_sweep(200, 50, 0.1, 'square')
    noise = generate_noise(0.05, 0.2)
    data = [d + n for d, n in zip(data[:len(noise)], noise)]
    data = apply_envelope(data, attack=0.001, decay=0.05, sustain=0.1, release=0.1, duration=0.1)
    return data

def create_powerup():
    """Ascending major triad for powerup"""
    freqs = [523.25, 659.25, 783.99, 1046.50]  # C major: C5, E5, G5, C6
    data = arpeggio(freqs, 0.05, 0.3)
    data = apply_envelope(data, attack=0.01, decay=0.1, sustain=0.8, release=0.15, duration=0.3)
    return data

def create_explosion():
    """Noise sweep with decay"""
    data = generate_noise(0.4, 0.8)
    data = apply_fade_out(data, 0.3)
    return data

def create_ui_confirm():
    """High blip for menu select"""
    data = generate_square_wave(880, 0.08, 0.4)
    data = apply_envelope(data, attack=0.001, decay=0.02, sustain=0.5, release=0.05, duration=0.08)
    return data

def create_ui_cancel():
    """Lower blip for menu back"""
    data = generate_square_wave(440, 0.08, 0.4)
    data = apply_envelope(data, attack=0.001, decay=0.02, sustain=0.5, release=0.05, duration=0.08)
    return data

def create_ui_select():
    """Short tick for hover/focus"""
    data = generate_square_wave(1760, 0.03, 0.3)
    data = apply_envelope(data, attack=0.001, decay=0.01, sustain=0.3, release=0.02, duration=0.03)
    return data

def create_coin():
    """Classic coin ding"""
    freqs = [987.77, 1318.51]  # B5, E6
    data = arpeggio(freqs, 0.08, 0.2)
    data = apply_envelope(data, attack=0.001, decay=0.05, sustain=0.9, release=0.1, duration=0.2)
    return data

def create_enemy_hit():
    """Thud for damaging enemy"""
    data = frequency_sweep(150, 80, 0.1, 'square')
    data = apply_envelope(data, attack=0.001, decay=0.03, sustain=0.2, release=0.08, duration=0.1)
    return data

def create_enemy_shoot():
    """Lower pitch shoot for enemy"""
    data = frequency_sweep(400, 200, 0.12, 'square')
    data = apply_envelope(data, attack=0.001, decay=0.05, sustain=0.3, release=0.1, duration=0.12)
    return data

def create_boss_alarm():
    """Warning/alert with alternating tones"""
    freqs = [800, 600, 800, 600]
    data = arpeggio(freqs, 0.15, 0.6)
    data = apply_envelope(data, attack=0.01, decay=0.05, sustain=0.9, release=0.1, duration=0.6)
    return data

def create_checkpoint():
    """Fanfare fragment for progress save"""
    freqs = [523.25, 659.25, 783.99, 1046.50]
    data = arpeggio(freqs, 0.1, 0.5)
    data = apply_envelope(data, attack=0.01, decay=0.1, sustain=0.9, release=0.2, duration=0.5)
    return data

def create_level_complete():
    """Victory arpeggio for stage clear"""
    freqs = [523.25, 659.25, 783.99, 1046.50, 1318.51, 1567.98]
    data = arpeggio(freqs, 0.1, 0.8)
    data = apply_envelope(data, attack=0.01, decay=0.2, sustain=0.9, release=0.3, duration=0.8)
    return data

def create_game_over():
    """Descending tone for failure"""
    data = frequency_sweep(600, 100, 1.0, 'square')
    data = apply_envelope(data, attack=0.01, decay=0.3, sustain=0.5, release=0.7, duration=1.0)
    return data

def create_warp():
    """Phaser sweep for teleport/transition"""
    data = frequency_sweep(200, 2000, 0.5, 'sawtooth')
    data = apply_envelope(data, attack=0.05, decay=0.1, sustain=0.7, release=0.3, duration=0.5)
    return data

def create_ambient_space():
    """Dark ambient drone for background"""
    data = generate_sawtooth_wave(60, 3.0, 0.2)
    data = apply_fade_out(data, 0.5)
    return data

# SFX catalog
SFX_CATALOG = {
    'jump.wav': create_jump,
    'shoot.wav': create_shoot,
    'hit.wav': create_hit,
    'powerup.wav': create_powerup,
    'explosion.wav': create_explosion,
    'ui_confirm.wav': create_ui_confirm,
    'ui_cancel.wav': create_ui_cancel,
    'ui_select.wav': create_ui_select,
    'coin.wav': create_coin,
    'enemy_hit.wav': create_enemy_hit,
    'enemy_shoot.wav': create_enemy_shoot,
    'boss_alarm.wav': create_boss_alarm,
    'checkpoint.wav': create_checkpoint,
    'level_complete.wav': create_level_complete,
    'game_over.wav': create_game_over,
    'warp.wav': create_warp,
    'ambient_space.wav': create_ambient_space,
}

def generate_for_game(game_path, existing_files=None):
    """Generate SFX for a specific game"""
    audio_dir = os.path.join(game_path, 'assets', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    
    created = []
    skipped = []
    
    for filename, generator in SFX_CATALOG.items():
        filepath = os.path.join(audio_dir, filename)
        
        # Skip if file already exists
        if existing_files and filename in existing_files:
            skipped.append(filename)
            continue
        
        try:
            data = generator()
            save_wav(filepath, data)
            created.append(filename)
        except Exception as e:
            print(f"Error creating {filename}: {e}")
    
    return created, skipped

def main():
    """Main entry point"""
    games = [
        '/root/.openclaw/workspace/aocros/projects/MilkMan',
        '/root/.openclaw/workspace/aocros/projects/quantum-defender',
        '/root/.openclaw/workspace/aocros/projects/teleport',
        '/root/.openclaw/workspace/aocros/projects/milkman-game',
        '/root/.openclaw/workspace/aocros/projects/laser-pistol',
        '/root/.openclaw/workspace/aocros/projects/neon-courier',
        '/root/.openclaw/workspace/aocros/projects/ReggieStarr',
        '/root/.openclaw/workspace/aocros/projects/dusty',
        '/root/.openclaw/workspace/aocros/projects/ronstrapp',
        '/root/.openclaw/workspace/aocros/projects/portal',
        '/root/.openclaw/workspace/aocros/projects/tappys-online',
        '/root/.openclaw/workspace/aocros/projects/upcoming/nog',
    ]
    
    report = []
    total_created = 0
    
    for game_path in games:
        game_name = os.path.basename(game_path)
        
        if not os.path.exists(game_path):
            report.append(f"\n⚠️  {game_name}: Game directory does not exist")
            continue
        
        # Check existing files
        audio_dir = os.path.join(game_path, 'assets', 'audio')
        existing = set()
        if os.path.exists(audio_dir):
            existing = set(f for f in os.listdir(audio_dir) if f.endswith('.wav'))
        
        created, skipped = generate_for_game(game_path, existing)
        
        report.append(f"\n🎮 {game_name}:")
        report.append(f"   📁 {audio_dir}")
        if created:
            report.append(f"   ✅ Created ({len(created)}): {', '.join(created)}")
        if skipped:
            report.append(f"   ⏭️  Skipped (already exists): {len(skipped)} files")
        if not created and not skipped:
            report.append(f"   ℹ️  No action needed")
        
        total_created += len(created)
    
    report.append(f"\n{'='*50}")
    report.append(f"📊 SUMMARY: {total_created} new SFX files generated")
    report.append(f"{'='*50}")
    
    return '\n'.join(report)

if __name__ == '__main__':
    result = main()
    print(result)
    
    # Save report
    with open('/root/.openclaw/workspace/sfx_report.txt', 'w') as f:
        f.write(result)
