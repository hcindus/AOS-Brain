#!/usr/bin/env python3
"""
AOS Brain TUI - Simple Terminal Interface
Feed inputs, check status, monitor brain activity
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime

# Colors for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

STATE_FILE = os.path.expanduser("~/.aos/brain/state/brain_state.json")
INPUT_QUEUE = os.path.expanduser("~/.aos/brain/input/queue.jsonl")
FEED_SCRIPT = "/root/.openclaw/workspace/AOS/brain/feed_brain.py"

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header():
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║              AOS BRAIN TUI v2.3.0                        ║")
    print("║         Terminal Interface for Brain Control             ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

def get_brain_status():
    """Get current brain status"""
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
        return state
    except:
        return None

def get_queue_count():
    """Get number of items in queue"""
    try:
        with open(INPUT_QUEUE, 'r') as f:
            return len(f.readlines())
    except:
        return 0

def show_status():
    """Display brain status"""
    clear()
    print_header()
    
    state = get_brain_status()
    queue_count = get_queue_count()
    
    if state:
        print(f"{Colors.GREEN}✓ Brain Status: ONLINE{Colors.END}")
        print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        print(f"  Tick:           {state.get('tick', 'N/A')}")
        print(f"  Phase:          {state.get('phase', 'N/A')}")
        print(f"  Nodes:          {state.get('policy_nn', {}).get('total_nodes', 'N/A')}")
        print(f"  Layers:         {state.get('policy_nn', {}).get('layers', 'N/A')}")
        print(f"  Novelty:        {state.get('growingnn', {}).get('novelty', 'N/A')}")
        print(f"  Memory Clusters:{state.get('memory_nn', {}).get('clusters', 'N/A')}")
        print(f"  Queue Items:    {queue_count}")
        print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        
        last_input = state.get('obs', {}).get('input', 'N/A')
        if len(last_input) > 50:
            last_input = last_input[:50] + "..."
        print(f"  Last Input:     {last_input}")
    else:
        print(f"{Colors.FAIL}✗ Brain Status: OFFLINE or No State File{Colors.END}")
    
    print(f"\n{Colors.WARNING}Press Enter to continue...{Colors.END}")
    input()

def feed_input_menu():
    """Menu for feeding inputs"""
    while True:
        clear()
        print_header()
        print(f"{Colors.CYAN}Feed Input to Brain{Colors.END}")
        print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        print("  1. Quick Input (type your own)")
        print("  2. Mathematical Equation")
        print("  3. Periodic Table Element")
        print("  4. Custom Text")
        print("  5. Back to Main Menu")
        print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        
        choice = input(f"\n{Colors.CYAN}Select option (1-5): {Colors.END}").strip()
        
        if choice == '1':
            text = input(f"\n{Colors.CYAN}Enter your input: {Colors.END}").strip()
            if text:
                feed_to_brain(text)
        elif choice == '2':
            equation_menu()
        elif choice == '3':
            element_menu()
        elif choice == '4':
            text = input(f"\n{Colors.CYAN}Enter custom text: {Colors.END}").strip()
            if text:
                feed_to_brain(text)
        elif choice == '5':
            break

def equation_menu():
    """Quick equations"""
    clear()
    print_header()
    print(f"{Colors.CYAN}Select Equation:{Colors.END}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    equations = [
        ("1", "Logistic Map", "xₙ₊₁ = r·xₙ(1-xₙ)"),
        ("2", "Bayesian Update", "P(H|E) = P(E|H)·P(H)/P(E)"),
        ("3", "Gradient Descent", "θₙ₊₁ = θₙ - α·∇J(θ)"),
        ("4", "Lotka-Volterra", "dx/dt = αx - βxy"),
        ("5", "Markov Chain", "P(Xₙ₊₁|Xₙ)"),
        ("6", "Fibonacci", "Fₙ = Fₙ₋₁ + Fₙ₋₂"),
        ("7", "Wave Equation", "∂²u/∂t² = c²∇²u"),
    ]
    
    for num, name, eq in equations:
        print(f"  {num}. {name}: {eq}")
    print(f"  8. Back")
    
    choice = input(f"\n{Colors.CYAN}Select (1-8): {Colors.END}").strip()
    
    for num, name, eq in equations:
        if choice == num:
            feed_to_brain(f"EQ{num}: {name} - {eq}")
            return

def element_menu():
    """Quick elements"""
    clear()
    print_header()
    print(f"{Colors.CYAN}Select Element:{Colors.END}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    elements = [
        ("1", "H", "Hydrogen", "1", "1.008", "Nonmetal"),
        ("2", "He", "Helium", "2", "4.0026", "Noble Gas"),
        ("3", "Li", "Lithium", "3", "6.94", "Alkali Metal"),
        ("4", "Be", "Beryllium", "4", "9.0122", "Alkaline Earth"),
        ("5", "B", "Boron", "5", "10.81", "Metalloid"),
        ("6", "C", "Carbon", "6", "12.011", "Nonmetal"),
        ("7", "N", "Nitrogen", "7", "14.007", "Nonmetal"),
        ("8", "O", "Oxygen", "8", "15.999", "Nonmetal"),
        ("9", "F", "Fluorine", "9", "18.998", "Halogen"),
        ("10", "Ne", "Neon", "10", "20.180", "Noble Gas"),
    ]
    
    for num, sym, name, an, mass, group in elements:
        print(f"  {num}. {sym} ({name}) - Atomic {an}, {group}")
    print(f"  11. Back")
    
    choice = input(f"\n{Colors.CYAN}Select (1-11): {Colors.END}").strip()
    
    for num, sym, name, an, mass, group in elements:
        if choice == num:
            feed_to_brain(f"PT{num}: {sym} ({name}) - Atomic {an}, Mass {mass}, {group}")
            return

def feed_to_brain(text):
    """Feed text to brain"""
    try:
        result = subprocess.run(
            ['python3', FEED_SCRIPT, text],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(f"\n{Colors.GREEN}✓ {result.stdout.strip()}{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.FAIL}✗ Error: {e}{Colors.END}")
    
    print(f"\n{Colors.WARNING}Press Enter to continue...{Colors.END}")
    input()

def show_queue():
    """Show queue contents"""
    clear()
    print_header()
    print(f"{Colors.CYAN}Input Queue Contents{Colors.END}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    try:
        with open(INPUT_QUEUE, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            print(f"  {Colors.WARNING}Queue is empty{Colors.END}")
        else:
            print(f"  {Colors.GREEN}{len(lines)} item(s) in queue:{Colors.END}\n")
            for i, line in enumerate(lines[:5], 1):  # Show first 5
                try:
                    data = json.loads(line)
                    text = data.get('text', 'N/A')
                    if len(text) > 60:
                        text = text[:60] + "..."
                    print(f"  {i}. {text}")
                except:
                    print(f"  {i}. [Invalid entry]")
            
            if len(lines) > 5:
                print(f"\n  ... and {len(lines) - 5} more")
    except:
        print(f"  {Colors.FAIL}Could not read queue{Colors.END}")
    
    print(f"\n{Colors.WARNING}Press Enter to continue...{Colors.END}")
    input()

def clear_queue():
    """Clear the input queue"""
    clear()
    print_header()
    
    confirm = input(f"{Colors.WARNING}Clear all items from queue? (yes/no): {Colors.END}").strip().lower()
    
    if confirm == 'yes':
        try:
            with open(INPUT_QUEUE, 'w') as f:
                f.write('')
            print(f"\n{Colors.GREEN}✓ Queue cleared{Colors.END}")
        except:
            print(f"\n{Colors.FAIL}✗ Could not clear queue{Colors.END}")
    else:
        print(f"\n{Colors.CYAN}Cancelled{Colors.END}")
    
    print(f"\n{Colors.WARNING}Press Enter to continue...{Colors.END}")
    input()

def main():
    """Main TUI loop"""
    while True:
        clear()
        print_header()
        
        # Show quick status
        state = get_brain_status()
        if state:
            print(f"{Colors.GREEN}● Brain Online{Colors.END} | Tick: {state.get('tick', 'N/A')} | Queue: {get_queue_count()}")
        else:
            print(f"{Colors.FAIL}● Brain Offline{Colors.END}")
        
        print(f"\n{Colors.CYAN}Main Menu{Colors.END}")
        print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        print("  1. 📊 Show Brain Status")
        print("  2. 📝 Feed Input to Brain")
        print("  3. 📋 View Input Queue")
        print("  4. 🗑️  Clear Input Queue")
        print("  5. 🚪 Exit")
        print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        
        choice = input(f"\n{Colors.CYAN}Select option (1-5): {Colors.END}").strip()
        
        if choice == '1':
            show_status()
        elif choice == '2':
            feed_input_menu()
        elif choice == '3':
            show_queue()
        elif choice == '4':
            clear_queue()
        elif choice == '5':
            clear()
            print(f"{Colors.GREEN}Goodbye!{Colors.END}")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(f"\n{Colors.GREEN}Goodbye!{Colors.END}")
        sys.exit(0)
