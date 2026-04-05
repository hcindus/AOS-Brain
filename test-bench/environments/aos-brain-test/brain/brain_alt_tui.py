#!/usr/bin/env python3
"""
AOS Brain ALT TUI v2.3.0 - Enhanced Terminal Interface
Layout: Visualizer | Brain Status | System Info | Controls
"""

import os
import sys
import json
import time
import subprocess
import psutil
from datetime import datetime

# Colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

STATE_FILE = os.path.expanduser("~/.aos/brain/state/brain_state.json")
INPUT_QUEUE = os.path.expanduser("~/.aos/brain/input/queue.jsonl")
FEED_SCRIPT = "/root/.openclaw/workspace/AOS/brain/feed_brain.py"

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def draw_mandelbrot_line(y, width=60):
    """Generate a line of Mandelbrot pattern"""
    line = ""
    for x in range(width):
        # Simplified Mandelbrot-ish pattern for ASCII
        x0 = (x / width) * 3.5 - 2.5
        y0 = (y / 10) * 2.0 - 1.0
        
        x_val, y_val = 0.0, 0.0
        iteration = 0
        max_iter = 20
        
        while x_val*x_val + y_val*y_val <= 4 and iteration < max_iter:
            xtemp = x_val*x_val - y_val*y_val + x0
            y_val = 2*x_val*y_val + y0
            x_val = xtemp
            iteration += 1
        
        # Bob Ross palette colors
        chars = [' ', '·', '•', '◆', '▪', '█']
        char_idx = min(iteration // 4, len(chars) - 1)
        
        if iteration == max_iter:
            line += Colors.BLUE + '█' + Colors.END
        else:
            colors = [Colors.DIM, Colors.CYAN, Colors.GREEN, Colors.WARNING, Colors.HEADER]
            color = colors[min(char_idx, len(colors) - 1)]
            line += color + chars[char_idx] + Colors.END
    
    return line

def draw_brain_visualizer():
    """Draw ASCII brain visualizer"""
    print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}║              BRAIN VISUALIZER v2.3.0                     ║{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.END}")
    
    # Mandelbrot background (8 lines)
    for y in range(8):
        print(f"  {draw_mandelbrot_line(y)}")
    
    # Neural nodes overlay
    state = get_brain_status()
    if state:
        nodes = state.get('policy_nn', {}).get('nodes', [8, 12, 40])
        total = sum(nodes)
        phase = state.get('phase', 'UNKNOWN')
        
        print(f"\n  {Colors.GREEN}● Neural Activity:{Colors.END}")
        print(f"    Layers: {len(nodes)} | Nodes: {nodes} | Total: {total}")
        print(f"    Phase: {Colors.WARNING}{phase}{Colors.END}")
        
        # Simple node visualization
        viz = "    "
        for i, n in enumerate(nodes):
            size = min(n // 5, 20)
            viz += Colors.BLUE + "█" * (size // 4) + Colors.END + " "
        print(viz)
    else:
        print(f"\n  {Colors.FAIL}● Brain Offline{Colors.END}")
    
    print()

def get_brain_status():
    """Get current brain status"""
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return None

def get_queue_count():
    """Get number of items in queue"""
    try:
        with open(INPUT_QUEUE, 'r') as f:
            return len(f.readlines())
    except:
        return 0

def draw_system_info():
    """Draw system information"""
    print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}║              SYSTEM INFORMATION                          ║{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.END}")
    
    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count()
    print(f"  {Colors.GREEN}CPU:{Colors.END} {cpu_percent}% usage | {cpu_count} cores")
    
    # Memory
    mem = psutil.virtual_memory()
    mem_used_gb = mem.used / (1024**3)
    mem_total_gb = mem.total / (1024**3)
    mem_percent = mem.percent
    print(f"  {Colors.GREEN}RAM:{Colors.END} {mem_used_gb:.1f}GB / {mem_total_gb:.1f}GB ({mem_percent}%)")
    
    # Disk
    disk = psutil.disk_usage('/')
    disk_used_gb = disk.used / (1024**3)
    disk_total_gb = disk.total / (1024**3)
    disk_percent = disk.percent
    print(f"  {Colors.GREEN}Disk:{Colors.END} {disk_used_gb:.1f}GB / {disk_total_gb:.1f}GB ({disk_percent}%)")
    
    # Swap
    swap = psutil.swap_memory()
    swap_used_gb = swap.used / (1024**3)
    swap_total_gb = swap.total / (1024**3)
    print(f"  {Colors.GREEN}Swap:{Colors.END} {swap_used_gb:.1f}GB / {swap_total_gb:.1f}GB")
    
    # Network
    net_io = psutil.net_io_counters()
    net_sent_mb = net_io.bytes_sent / (1024**2)
    net_recv_mb = net_io.bytes_recv / (1024**2)
    print(f"  {Colors.GREEN}Network:{Colors.END} ↑{net_sent_mb:.0f}MB ↓{net_recv_mb:.0f}MB")
    
    # Load Average
    try:
        load1, load5, load15 = os.getloadavg()
        print(f"  {Colors.GREEN}Load:{Colors.END} {load1:.2f} {load5:.2f} {load15:.2f}")
    except:
        pass
    
    print()

def draw_brain_status():
    """Draw brain status panel"""
    print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}║              BRAIN STATUS                              ║{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.END}")
    
    state = get_brain_status()
    queue_count = get_queue_count()
    
    if state:
        print(f"  {Colors.GREEN}● Status: ONLINE{Colors.END}")
        print(f"  {Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        print(f"    Tick:            {state.get('tick', 'N/A')}")
        print(f"    Phase:           {state.get('phase', 'N/A')}")
        print(f"    Nodes:           {state.get('policy_nn', {}).get('total_nodes', 'N/A')}")
        print(f"    Layers:          {state.get('policy_nn', {}).get('layers', 'N/A')}")
        print(f"    Distribution:    {state.get('policy_nn', {}).get('nodes', 'N/A')}")
        print(f"    Novelty:         {state.get('growingnn', {}).get('novelty', 'N/A')}")
        print(f"    Error Rate:      {state.get('growingnn', {}).get('error_rate', 'N/A')}")
        print(f"    Memory Clusters: {state.get('memory_nn', {}).get('clusters', 'N/A')}")
        print(f"    Queue Items:     {queue_count}")
        print(f"  {Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        
        last_input = state.get('obs', {}).get('input', 'N/A')
        if len(last_input) > 55:
            last_input = last_input[:55] + "..."
        print(f"    Last Input:      {last_input}")
    else:
        print(f"  {Colors.FAIL}● Status: OFFLINE{Colors.END}")
        print(f"  {Colors.FAIL}  No state file found{Colors.END}")
    
    print()

def draw_menu():
    """Draw control menu"""
    print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}║              CONTROLS                                  ║{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.END}")
    print(f"  {Colors.GREEN}1.{Colors.END} 📝 Feed Quick Input")
    print(f"  {Colors.GREEN}2.{Colors.END} 🔢 Feed Mathematical Equation")
    print(f"  {Colors.GREEN}3.{Colors.END} 🧪 Feed Periodic Table Element")
    print(f"  {Colors.GREEN}4.{Colors.END} 📋 View Queue ({get_queue_count()} items)")
    print(f"  {Colors.GREEN}5.{Colors.END} 🗑️  Clear Queue")
    print(f"  {Colors.GREEN}6.{Colors.END} 🔄 Refresh Display")
    print(f"  {Colors.GREEN}7.{Colors.END} 🚪 Exit")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")

def feed_input(text):
    """Feed text to brain"""
    try:
        result = subprocess.run(
            ['python3', FEED_SCRIPT, text],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def quick_input():
    """Quick input dialog"""
    print(f"\n{Colors.CYAN}Enter your input:{Colors.END}")
    text = input("> ").strip()
    if text:
        result = feed_input(text)
        print(f"{Colors.GREEN}✓ {result}{Colors.END}")
        input(f"{Colors.WARNING}Press Enter...{Colors.END}")

def equation_input():
    """Equation selection"""
    equations = [
        ("1", "Logistic Map", "xₙ₊₁ = r·xₙ(1-xₙ)"),
        ("2", "Bayesian Update", "P(H|E) = P(E|H)·P(H)/P(E)"),
        ("3", "Gradient Descent", "θₙ₊₁ = θₙ - α·∇J(θ)"),
        ("4", "Lotka-Volterra", "dx/dt = αx - βxy"),
        ("5", "Markov Chain", "P(Xₙ₊₁|Xₙ)"),
        ("6", "Fibonacci", "Fₙ = Fₙ₋₁ + Fₙ₋₂"),
        ("7", "Wave Equation", "∂²u/∂t² = c²∇²u"),
    ]
    
    print(f"\n{Colors.CYAN}Select Equation:{Colors.END}")
    for num, name, eq in equations:
        print(f"  {num}. {name}: {eq}")
    print(f"  8. Back")
    
    choice = input(f"\n{Colors.CYAN}Select (1-8): {Colors.END}").strip()
    for num, name, eq in equations:
        if choice == num:
            result = feed_input(f"EQ{num}: {name} - {eq}")
            print(f"{Colors.GREEN}✓ {result}{Colors.END}")
            input(f"{Colors.WARNING}Press Enter...{Colors.END}")
            return

def element_input():
    """Element selection"""
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
    
    print(f"\n{Colors.CYAN}Select Element:{Colors.END}")
    for num, sym, name, an, mass, group in elements:
        print(f"  {num}. {sym} ({name}) - Atomic {an}, {group}")
    print(f"  11. Back")
    
    choice = input(f"\n{Colors.CYAN}Select (1-11): {Colors.END}").strip()
    for num, sym, name, an, mass, group in elements:
        if choice == num:
            result = feed_input(f"PT{num}: {sym} ({name}) - Atomic {an}, Mass {mass}, {group}")
            print(f"{Colors.GREEN}✓ {result}{Colors.END}")
            input(f"{Colors.WARNING}Press Enter...{Colors.END}")
            return

def view_queue():
    """View queue contents"""
    print(f"\n{Colors.CYAN}Input Queue:{Colors.END}")
    try:
        with open(INPUT_QUEUE, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            print(f"  {Colors.WARNING}Queue is empty{Colors.END}")
        else:
            print(f"  {Colors.GREEN}{len(lines)} item(s):{Colors.END}\n")
            for i, line in enumerate(lines[:5], 1):
                try:
                    data = json.loads(line)
                    text = data.get('text', 'N/A')
                    if len(text) > 50:
                        text = text[:50] + "..."
                    print(f"  {i}. {text}")
                except:
                    print(f"  {i}. [Invalid]")
            if len(lines) > 5:
                print(f"\n  ... and {len(lines) - 5} more")
    except:
        print(f"  {Colors.FAIL}Could not read queue{Colors.END}")
    
    input(f"\n{Colors.WARNING}Press Enter...{Colors.END}")

def clear_queue():
    """Clear queue"""
    print(f"\n{Colors.WARNING}Clear all items from queue? (yes/no):{Colors.END}")
    confirm = input("> ").strip().lower()
    
    if confirm == 'yes':
        try:
            with open(INPUT_QUEUE, 'w') as f:
                f.write('')
            print(f"{Colors.GREEN}✓ Queue cleared{Colors.END}")
        except:
            print(f"{Colors.FAIL}✗ Could not clear{Colors.END}")
    else:
        print(f"{Colors.CYAN}Cancelled{Colors.END}")
    
    input(f"{Colors.WARNING}Press Enter...{Colors.END}")

def main():
    """Main loop"""
    while True:
        clear()
        
        # Layout: Visualizer | Brain Status | System Info | Controls
        draw_brain_visualizer()
        draw_brain_status()
        draw_system_info()
        draw_menu()
        
        choice = input(f"\n{Colors.CYAN}Select option (1-7): {Colors.END}").strip()
        
        if choice == '1':
            quick_input()
        elif choice == '2':
            equation_input()
        elif choice == '3':
            element_input()
        elif choice == '4':
            view_queue()
        elif choice == '5':
            clear_queue()
        elif choice == '6':
            continue  # Just refresh
        elif choice == '7':
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
