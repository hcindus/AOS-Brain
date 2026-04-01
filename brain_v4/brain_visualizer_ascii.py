#!/usr/bin/env python3
"""
Brain Visualizer - ASCII Art Version (No Display Required)
Pretty colors in terminal using ANSI codes
"""

import json
import os
import sys
import time
import math
from pathlib import Path

STATE_FILE = Path.home() / ".aos/brain/state/brain_v31_state.json"

# ANSI Colors (for terminal pretty printing)
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Bob Ross Colors
    PHTHALO_BLUE = '\033[38;5;27m'
    SAP_GREEN = '\033[38;5;28m'
    BRIGHT_RED = '\033[38;5;196m'
    CADMIUM_YELLOW = '\033[38;5;220m'
    INDIAN_YELLOW = '\033[38;5;214m'
    DARK_SIENNA = '\033[38;5;94m'
    MIDNIGHT = '\033[38;5;232m'
    PRUSSIAN = '\033[38;5;24m'
    VAN_DYKE = '\033[38;5;58m'
    YELLOW_OCHRE = '\033[38;5;178m'
    TITANIUM_WHITE = '\033[38;5;255m'
    ALIZARIN_CRIMSON = '\033[38;5;161m'
    CRIMSON_LAKE = '\033[38;5;160m'
    
    # Backgrounds
    BG_BLUE = '\033[48;5;27m'
    BG_GREEN = '\033[48;5;28m'
    BG_RED = '\033[48;5;196m'
    BG_YELLOW = '\033[48;5;220m'
    BG_DARK = '\033[48;5;232m'

PHASE_COLORS = {
    "Observe": Colors.PHTHALO_BLUE,
    "Orient": Colors.SAP_GREEN,
    "Decide": Colors.BRIGHT_RED,
    "Act": Colors.CADMIUM_YELLOW
}

def clear_screen():
    os.system('clear')

def draw_box(title, width=60):
    """Draw a pretty box"""
    print(f"{Colors.BRIGHT_RED}╔{'═' * width}╗{Colors.RESET}")
    padding = (width - len(title)) // 2
    print(f"{Colors.BRIGHT_RED}║{' ' * padding}{Colors.BOLD}{Colors.CADMIUM_YELLOW}{title}{Colors.RESET}{Colors.BRIGHT_RED}{' ' * (width - len(title) - padding)}║{Colors.RESET}")
    print(f"{Colors.BRIGHT_RED}╚{'═' * width}╝{Colors.RESET}")

def draw_status_line(label, value, color, width=30):
    """Draw a status line with color"""
    value_str = str(value)
    padding = width - len(label) - len(value_str) - 2
    print(f"{color}{Colors.BOLD}{label}:{Colors.RESET} {Colors.TITANIUM_WHITE}{value_str}{Colors.RESET}")

def draw_neural_ascii(tick):
    """Draw ASCII neural network"""
    print(f"\n{Colors.PHTHALO_BLUE}{'─' * 70}{Colors.RESET}")
    print(f"{Colors.CADMIUM_YELLOW}{Colors.BOLD}     🧠 7-REGION OODA NEURAL NETWORK{Colors.RESET}")
    print(f"{Colors.PHTHALO_BLUE}{'─' * 70}{Colors.RESET}\n")
    
    # Pulsing effect based on tick
    pulse = (tick % 20) // 5
    
    regions = [
        ("SENSORY", Colors.PHTHALO_BLUE, pulse == 0),
        ("  PFC   ", Colors.BRIGHT_RED, pulse == 1),
        ("HIPPO", Colors.SAP_GREEN, pulse == 2),
        ("LIMBIC", Colors.INDIAN_YELLOW, pulse == 3),
        (" BASAL ", Colors.CADMIUM_YELLOW, pulse == 0),
        ("CEREB", Colors.SAP_GREEN, pulse == 1),
        ("BRAINSTEM", Colors.CRIMSON_LAKE, pulse == 2)
    ]
    
    # Draw connections
    print(f"{Colors.VAN_DYKE}           ╱    ╲    ╱    ╲{Colors.RESET}")
    print(f"{Colors.VAN_DYKE}          ╱      ╲  ╱      ╲{Colors.RESET}")
    
    # Draw nodes row
    nodes_str = ""
    for name, color, active in regions[:4]:
        if active:
            nodes_str += f"{Colors.BOLD}{color}[{name}]{Colors.RESET}  "
        else:
            nodes_str += f"{color}({name}){Colors.RESET}  "
    print(f"{nodes_str}")
    
    print(f"{Colors.VAN_DYKE}           ╲    ╱    ╲    ╱{Colors.RESET}")
    
    # Lower nodes
    nodes_str2 = "     "
    for name, color, active in regions[4:]:
        if active:
            nodes_str2 += f"{Colors.BOLD}{color}[{name}]{Colors.RESET} "
        else:
            nodes_str2 += f"{color}({name}){Colors.RESET} "
    print(f"{nodes_str2}")

def draw_mandelbrot_ascii(tick):
    """Draw ASCII mandelbrot approximation"""
    chars = " .:-=+*#%@"
    zoom = 1.0 + (tick % 100) / 50.0
    
    print(f"\n{Colors.PRUSSIAN}{Colors.BOLD}     🌀 MANDELBROT BACKGROUND{Colors.RESET}")
    
    # Simple pattern based on tick
    pattern = ""
    for i in range(40):
        idx = int((math.sin(i/5 + tick/10) + 1) * 4.5) % len(chars)
        pattern += chars[idx]
    
    # Colorize the pattern
    colored = ""
    for char in pattern:
        if char in "@%":
            colored += f"{Colors.ALIZARIN_CRIMSON}{char}{Colors.RESET}"
        elif char in "#*":
            colored += f"{Colors.BRIGHT_RED}{char}{Colors.RESET}"
        elif char in "+=":
            colored += f"{Colors.CADMIUM_YELLOW}{char}{Colors.RESET}"
        elif char in "-:":
            colored += f"{Colors.SAP_GREEN}{char}{Colors.RESET}"
        else:
            colored += f"{Colors.PHTHALO_BLUE}{char}{Colors.RESET}"
    
    print(f"{Colors.PRUSSIAN}     {colored}{Colors.RESET}")

def draw_progress_bar(label, percent, width=50):
    """Draw ASCII progress bar"""
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    
    # Color gradient
    if percent < 0.3:
        color = Colors.PHTHALO_BLUE
    elif percent < 0.6:
        color = Colors.SAP_GREEN
    elif percent < 0.8:
        color = Colors.CADMIUM_YELLOW
    else:
        color = Colors.BRIGHT_RED
    
    print(f"\n{Colors.YELLOW_OCHRE}{label}:{Colors.RESET}")
    print(f"{color}|{bar}|{Colors.RESET} {Colors.BOLD}{percent*100:.1f}%{Colors.RESET}")

def draw_brain_ascii(state):
    """Draw complete ASCII brain visualizer"""
    clear_screen()
    
    tick = state.get('tick', 0) if state else 0
    phase = state.get('phase', 'Decide') if state else 'Decide'
    memories = state.get('memories', 0) if state else 0
    
    # Header box
    draw_box(f"🧠 AOS BRAIN v4.0 - TICK {tick:,}", 66)
    
    # Status section
    print(f"\n{Colors.PHTHALO_BLUE}{'─' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}  STATUS{Colors.RESET}")
    print(f"{Colors.PHTHALO_BLUE}{'─' * 70}{Colors.RESET}")
    
    draw_status_line("Phase", phase, PHASE_COLORS.get(phase, Colors.PHTHALO_BLUE))
    draw_status_line("Memories", f"{memories:,}", Colors.SAP_GREEN)
    draw_status_line("Nodes", "141", Colors.CADMIUM_YELLOW)
    draw_status_line("Mode", "AOSv3-7Region", Colors.INDIAN_YELLOW)
    
    # Neural network
    draw_neural_ascii(tick)
    
    # Mandelbrot
    draw_mandelbrot_ascii(tick)
    
    # Curriculum progress
    progress = min(tick / 20000, 1.0)
    draw_progress_bar("📚 Curriculum Progress", progress)
    
    # Footer
    print(f"\n{Colors.VAN_DYKE}{'─' * 70}{Colors.RESET}")
    print(f"{Colors.YELLOW_OCHRE}     🎨 Colors by Bob Ross | Neural patterns active{Colors.RESET}")
    print(f"{Colors.VAN_DYKE}{'─' * 70}{Colors.RESET}\n")
    
    print(f"{Colors.DARK_SIENNA}     Press Ctrl+C to stop visualizer{Colors.RESET}")

def load_state():
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                return json.load(f)
    except:
        pass
    return {"tick": 19647, "memories": 19647, "phase": "Decide"}

def main():
    print(f"{Colors.BOLD}{Colors.CADMIUM_YELLOW}")
    print("=" * 70)
    print("  🎨 AOS BRAIN VISUALIZER - ASCII ART MODE")
    print("  No display required! Pretty terminal colors!")
    print("=" * 70)
    print(f"{Colors.RESET}")
    print("\nStarting visualizer...")
    time.sleep(1)
    
    try:
        while True:
            state = load_state()
            draw_brain_ascii(state)
            time.sleep(2)
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{Colors.SAP_GREEN}👋 Visualizer stopped. Brain continues running!{Colors.RESET}\n")

if __name__ == "__main__":
    main()
