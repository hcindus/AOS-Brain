# visualizer/brain_visualizer.py
"""
3D Brain Visualizer with Bob Ross-inspired color palette.

Renders:
- QMD mode as color overlay
- Semantic graph as node network  
- OODA state as activity indicators
- Ternary signals as waveform
"""

import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Import config colors
from config.colors import BOB_ROSS_PALETTE, REGION_COLORS, hex_to_rgb


@dataclass
class VizConfig:
    """Visualizer configuration."""
    width: int = 120
    height: int = 40
    use_ansi: bool = True


class BrainVisualizer:
    """
    Console-based brain activity visualizer.
    
    Features:
    - Mode indicator with Bob Ross colors
    - Graph node count
    - OODA state display
    - Ternary signal visualization
    """
    
    # Mode colors from Bob Ross palette
    MODE_COLORS = {
        "Analytical": BOB_ROSS_PALETTE["cerulean_blue"],      # Clear thinking
        "Creative": BOB_ROSS_PALETTE["phthalo_green"],       # Growth/creation  
        "Cautious": BOB_ROSS_PALETTE["yellow_ochre"],        # Careful/earthy
        "Exploratory": BOB_ROSS_PALETTE["cadmium_yellow"],   # Bright curiosity
        "Reflective": BOB_ROSS_PALETTE["prussian_blue"],     # Deep thought
        "Directive": BOB_ROSS_PALETTE["alizarin_crimson"],   # Action/decision
        "Emotional": BOB_ROSS_PALETTE["cadmium_red"],        # Strong feelings
        "Minimal": BOB_ROSS_PALETTE["paynes_grey"],          # Quiet/subdued
        "Verbose": BOB_ROSS_PALETTE["burnt_sienna"],       # Warm expression
    }
    
    # Ternary color mapping
    TERNARY_SYMBOLS = {
        -1: ("▼", BOB_ROSS_PALETTE["paynes_grey"]),    # Inhibit - cool shadow
        0:  ("○", BOB_ROSS_PALETTE["midnight_black"]), # Neutral - darkness  
        1:  ("▲", BOB_ROSS_PALETTE["cadmium_yellow"]), # Excite - warm light
    }
    
    def __init__(self, brain=None):
        self.brain = brain
        self.config = VizConfig()
        self.history: List[dict] = []
        self.max_history = 20
        
    def update(self, cognition: dict):
        """
        Update visualization with new cognition state.
        
        Args:
            cognition: Output from brain.cognition_cycle()
        """
        self.history.append(cognition)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        self._render(cognition)
    
    def _render(self, cognition: dict):
        """Render the brain state."""
        mode = cognition.get("mode", "Unknown")
        thought = cognition.get("thought", {})
        
        # Clear screen
        print("\033[2J\033[H" if self.config.use_ansi else "\n" * self.config.height)
        
        # Header
        self._draw_header(mode)
        
        # Mode indicator with color
        self._draw_mode_indicator(mode)
        
        # OODA state
        self._draw_ooda_state(thought)
        
        # Ternary signals
        ternary = thought.get("ternary_code", [0, 0, 0, 0, 0])
        self._draw_ternary_signals(ternary)
        
        # Graph stats (if available)
        if self.brain and hasattr(self.brain, 'substrate'):
            self._draw_graph_stats()
        
        # Activity history
        self._draw_history()
    
    def _draw_header(self, mode: str):
        """Draw header bar."""
        color = self.MODE_COLORS.get(mode, BOB_ROSS_PALETTE["titanium_white"])
        rgb = hex_to_rgb(color)
        
        # ANSI escape for background color
        if self.config.use_ansi:
            bg_code = f"\033[48;2;{int(rgb[0]*255)};{int(rgb[1]*255)};{int(rgb[2]*255)}m"
            reset = "\033[0m"
            print(f"{bg_code}╔══════════════════════════════════════════════════════════════════════════════╗{reset}")
            print(f"{bg_code}║                    🧠 TERNARY BRAIN VISUALIZER                               ║{reset}")
            print(f"{bg_code}╚══════════════════════════════════════════════════════════════════════════════╝{reset}")
        else:
            print("╔══════════════════════════════════════════════════════════════════════════════╗")
            print("║                    🧠 TERNARY BRAIN VISUALIZER                               ║")
            print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    def _draw_mode_indicator(self, mode: str):
        """Draw current QMD mode with Bob Ross color."""
        color = self.MODE_COLORS.get(mode, BOB_ROSS_PALETTE["titanium_white"])
        rgb = hex_to_rgb(color)
        
        # Mode description
        descriptions = {
            "Analytical": "Clear, logical reasoning",
            "Creative": "Divergent, associative thinking",
            "Cautious": "Risk-aware, safety-biased",
            "Exploratory": "Curious, novelty-seeking",
            "Reflective": "Memory-oriented, introspective",
            "Directive": "Action-focused, execution-ready",
            "Emotional": "Value-weighted, expressive",
            "Minimal": "Terse, low-energy",
            "Verbose": "Expanded, explanatory",
        }
        desc = descriptions.get(mode, "Unknown mode")
        
        if self.config.use_ansi:
            bg_code = f"\033[48;2;{int(rgb[0]*255)};{int(rgb[1]*255)};{int(rgb[2]*255)}m"
            fg_code = "\033[38;2;0;0;0m"  # Black text
            reset = "\033[0m"
            print(f"\n{bg_code}{fg_code}  QMD MODE: {mode:15}  {desc:50}  {reset}\n")
        else:
            print(f"\n  [MODE: {mode}] {desc}\n")
    
    def _draw_ooda_state(self, thought: dict):
        """Draw OODA loop state."""
        print("  📊 OODA STATE:")
        print("  " + "─" * 70)
        
        obs = thought.get("observation", {})
        dec = thought.get("decision", {})
        val = thought.get("value", {})
        gates = thought.get("gates", {})
        
        # Show key OODA elements
        print(f"    Observation: {str(obs)[:60]}")
        print(f"    Decision:    {str(dec)[:60]}")
        print(f"    Value:       importance={val.get('importance', 0):.2f}, valence={val.get('valence', 0):.2f}")
        print(f"    Gates:       {gates}")
        print()
    
    def _draw_ternary_signals(self, ternary: List[int]):
        """Draw ternary signal bars."""
        print("  ⚡ TERNARY SIGNALS:")
        print("  " + "─" * 70)
        
        labels = ["Novelty", "Value", "Action", "Risk", "Growth"]
        
        for label, val in zip(labels, ternary[:5]):
            symbol, color = self.TERNARY_SYMBOLS.get(val, ("?", "#FFFFFF"))
            rgb = hex_to_rgb(color)
            
            # Create visual bar
            bar_len = 20
            if val == 1:
                bar = "█" * bar_len
            elif val == -1:
                bar = "░" * bar_len
            else:
                bar = "▒" * bar_len
            
            if self.config.use_ansi:
                fg_code = f"\033[38;2;{int(rgb[0]*255)};{int(rgb[1]*255)};{int(rgb[2]*255)}m"
                reset = "\033[0m"
                print(f"    {label:12} {fg_code}{symbol}{reset} [{fg_code}{bar}{reset}] {val:2d}")
            else:
                print(f"    {label:12} {symbol} [{bar}] {val:2d}")
        print()
    
    def _draw_graph_stats(self):
        """Draw semantic graph statistics."""
        if not hasattr(self.brain.substrate, 'graph'):
            return
        
        graph = self.brain.substrate.graph
        stats = graph.get_stats()
        
        print("  🕸️  SEMANTIC GRAPH:")
        print("  " + "─" * 70)
        print(f"    Nodes: {stats['nodes']:<6} │ Avg Value: {stats['avg_node_value']:.2f}")
        print(f"    Edges: {stats['edges']:<6} │ Avg Weight: {stats['avg_edge_weight']:.2f}")
        
        # Show tagged nodes
        for tag in ["salient", "novel", "growing"]:
            nodes = graph.get_nodes_by_tag(tag)
            if nodes:
                print(f"    {tag.capitalize():12} {len(nodes)} nodes")
        print()
    
    def _draw_history(self):
        """Draw recent mode history."""
        if len(self.history) < 2:
            return
        
        print("  📈 RECENT MODES:")
        print("  " + "─" * 70)
        
        recent = self.history[-10:]
        mode_line = ""
        
        for h in recent:
            mode = h.get("mode", "?")
            color = self.MODE_COLORS.get(mode, "#FFFFFF")
            rgb = hex_to_rgb(color)
            
            # First letter of mode
            letter = mode[0] if mode else "?"
            
            if self.config.use_ansi:
                fg_code = f"\033[38;2;{int(rgb[0]*255)};{int(rgb[1]*255)};{int(rgb[2]*255)}m"
                reset = "\033[0m"
                mode_line += f"{fg_code}{letter}{reset} "
            else:
                mode_line += f"{letter} "
        
        print(f"    {mode_line}")
        print()
    
    def draw_mode_legend(self):
        """Print legend of all modes and their colors."""
        print("\n  🎨 BOB ROSS COLOR LEGEND:")
        print("  " + "─" * 70)
        
        for mode, color in self.MODE_COLORS.items():
            rgb = hex_to_rgb(color)
            if self.config.use_ansi:
                fg_code = f"\033[38;2;{int(rgb[0]*255)};{int(rgb[1]*255)};{int(rgb[2]*255)}m"
                reset = "\033[0m"
                print(f"    {fg_code}■{reset} {mode:15} {color}")
            else:
                print(f"    ■ {mode:15} {color}")


class SimpleVisualizer:
    """Minimal text visualizer for testing."""
    
    def update(self, cognition: dict):
        """Simple text output."""
        mode = cognition.get("mode", "Unknown")
        thought = cognition.get("thought", {})
        ternary = thought.get("ternary_code", [0, 0, 0, 0, 0])
        
        print(f"\n[Brain] Mode: {mode}")
        print(f"[Brain] Ternary: {ternary}")
        print(f"[Brain] Decision: {thought.get('decision', {})}")
