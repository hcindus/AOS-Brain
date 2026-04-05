#!/usr/bin/env python3
"""
Brain Visualizer Live - Pretty Colors & Real-time Display
Bob Ross Palette + Mandelbrot Backgrounds
"""

import json
import os
import sys
import time
import math
from pathlib import Path
import numpy as np

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyBboxPatch, Wedge
from matplotlib.colors import LinearSegmentedColormap

# Bob Ross Palette (the colors you remembered!)
BOB_ROSS = {
    "Alizarin Crimson": "#E32636",
    "Bright Red": "#FF6347",
    "Cadmium Yellow": "#FFD700",
    "Dark Sienna": "#3C1414",
    "Indian Yellow": "#FFB347",
    "Midnight Black": "#000000",
    "Phthalo Blue": "#000F89",
    "Phthalo Green": "#123524",
    "Prussian Blue": "#003153",
    "Sap Green": "#507D2A",
    "Van Dyke Brown": "#664228",
    "Yellow Ochre": "#F0BB5E",
    "Titanium White": "#FDF5E6",
    "Crimson Lake": "#DC143C"
}

# Phase colors
PHASE_COLORS = {
    "Observe": BOB_ROSS["Phthalo Blue"],
    "Orient": BOB_ROSS["Sap Green"],
    "Decide": BOB_ROSS["Bright Red"],
    "Act": BOB_ROSS["Cadmium Yellow"],
    "Rest": BOB_ROSS["Van Dyke Brown"]
}

STATE_FILE = Path.home() / ".aos/brain/state/brain_v31_state.json"

def mandelbrot_zoom(width=100, height=100, max_iter=50, zoom=1.0, offset_x=0, offset_y=0):
    """Generate mandelbrot for background"""
    img = np.zeros((height, width))
    for x in range(width):
        for y in range(height):
            zx = 1.5 * (x - width/2) / (0.5 * zoom * width) + offset_x
            zy = (y - height/2) / (0.5 * zoom * height) + offset_y
            c_x, c_y = zx, zy
            iter_count = 0
            while zx*zx + zy*zy < 4 and iter_count < max_iter:
                tmp = zx*zx - zy*zy + c_x
                zy = 2.0*zx*zy + c_y
                zx = tmp
                iter_count += 1
            img[y, x] = iter_count / max_iter
    return img

class BrainVisualizerLive:
    """Live brain visualizer with pretty colors"""
    
    def __init__(self):
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.fig.patch.set_facecolor(BOB_ROSS["Midnight Black"])
        self.ax.set_facecolor(BOB_ROSS["Prussian Blue"])
        
        plt.ion()
        plt.show()
        
        self.tick = 0
        print("=" * 70)
        print("  🎨 BRAIN VISUALIZER LIVE")
        print("  Bob Ross Colors + Mandelbrot Backgrounds")
        print("=" * 70)
    
    def load_state(self):
        """Load brain state from file"""
        try:
            if STATE_FILE.exists():
                with open(STATE_FILE) as f:
                    return json.load(f)
        except:
            pass
        return None
    
    def draw_brain(self, state):
        """Draw the brain visualization"""
        self.ax.clear()
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.axis('off')
        
        if not state:
            self.ax.text(50, 50, "NO BRAIN STATE", 
                        ha='center', va='center', 
                        fontsize=20, color=BOB_ROSS["Alizarin Crimson"])
            return
        
        tick = state.get('tick', 0)
        self.tick = tick
        
        # Background mandelbrot
        zoom = 1.0 + (tick % 1000) / 500  # Dynamic zoom based on tick
        mb = mandelbrot_zoom(100, 100, max_iter=40, zoom=zoom, 
                            offset_x=math.sin(tick/1000), 
                            offset_y=math.cos(tick/1000))
        self.ax.imshow(mb, extent=[0, 100, 0, 100], 
                       cmap='inferno', alpha=0.3, aspect='auto')
        
        # Title area
        title = f"🧠 AOS Brain v4.0 - Tick {tick:,}"
        self.ax.text(50, 95, title, ha='center', va='center',
                    fontsize=24, fontweight='bold', 
                    color=BOB_ROSS["Titanium White"],
                    bbox=dict(boxstyle='round,pad=0.5', 
                             facecolor=BOB_ROSS["Phthalo Blue"], 
                             edgecolor=BOB_ROSS["Cadmium Yellow"], 
                             linewidth=3, alpha=0.9))
        
        # Status boxes
        self.draw_status_box(5, 75, "Memories", state.get('memories', 0), 
                           BOB_ROSS["Sap Green"])
        self.draw_status_box(35, 75, "Nodes", state.get('nodes', 141), 
                           BOB_ROSS["Phthalo Blue"])
        self.draw_status_box(65, 75, "Phase", state.get('phase', 'Decide'), 
                           PHASE_COLORS.get(state.get('phase', 'Decide'), 
                           BOB_ROSS["Phthalo Blue"]))
        
        # Neural network visualization
        self.draw_neural_network(10, 10, 80, 50, tick)
        
        # Curriculum progress bar
        self.draw_progress_bar(10, 3, 80, 4, "Curriculum Progress", 
                              min(tick / 20000, 1.0), 
                              BOB_ROSS["Indian Yellow"])
        
        # Footer
        self.ax.text(50, 1, "🎨 Colors by Bob Ross | Fractals by Mandelbrot", 
                    ha='center', va='center', fontsize=10, 
                    color=BOB_ROSS["Yellow Ochre"], alpha=0.7)
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def draw_status_box(self, x, y, label, value, color):
        """Draw a status box"""
        # Box background
        rect = FancyBboxPatch((x, y), 25, 15, 
                             boxstyle="round,pad=0.02", 
                             facecolor=BOB_ROSS["Midnight Black"], 
                             edgecolor=color, linewidth=2, alpha=0.8)
        self.ax.add_patch(rect)
        
        # Label
        self.ax.text(x + 12.5, y + 11, label, ha='center', va='center',
                    fontsize=10, color=BOB_ROSS["Yellow Ochre"])
        
        # Value
        val_str = f"{value:,}" if isinstance(value, int) else str(value)
        self.ax.text(x + 12.5, y + 5, val_str, ha='center', va='center',
                    fontsize=14, fontweight='bold', color=color)
    
    def draw_neural_network(self, x, y, width, height, tick):
        """Draw animated neural network"""
        # Background
        rect = FancyBboxPatch((x, y), width, height,
                             boxstyle="round,pad=0.01",
                             facecolor=BOB_ROSS["Dark Sienna"],
                             edgecolor=BOB_ROSS["Van Dyke Brown"],
                             linewidth=2, alpha=0.6)
        self.ax.add_patch(rect)
        
        # Title
        self.ax.text(x + width/2, y + height - 3, "7-Region OODA Network",
                    ha='center', va='center', fontsize=12,
                    color=BOB_ROSS["Cadmium Yellow"])
        
        # Regions
        regions = [
            ("Sensory", x + 10, y + 35, BOB_ROSS["Phthalo Blue"]),
            ("PFC", x + 40, y + 35, BOB_ROSS["Bright Red"]),
            ("Hippocampus", x + 70, y + 35, BOB_ROSS["Sap Green"]),
            ("Limbic", x + 25, y + 15, BOB_ROSS["Indian Yellow"]),
            ("Basal", x + 55, y + 15, BOB_ROSS["Cadmium Yellow"]),
            ("Cerebellum", x + 40, y + 5, BOB_ROSS["Phthalo Green"]),
            ("Brainstem", x + 10, y + 15, BOB_ROSS["Crimson Lake"])
        ]
        
        # Draw connections (animated)
        for i, (name1, x1, y1, c1) in enumerate(regions):
            for name2, x2, y2, c2 in regions[i+1:]:
                # Pulsing connections
                pulse = (math.sin(tick/100 + i) + 1) / 2
                alpha = 0.2 + pulse * 0.4
                self.ax.plot([x1, x2], [y1, y2], 
                           color=BOB_ROSS["Titanium White"], 
                           alpha=alpha, linewidth=1)
        
        # Draw nodes
        for name, nx, ny, color in regions:
            # Pulsing effect
            pulse = (math.sin(tick/50 + ord(name[0])) + 1) / 2
            size = 800 + pulse * 400
            
            # Node circle
            circle = Circle((nx, ny), 4, facecolor=color, 
                          edgecolor=BOB_ROSS["Titanium White"], 
                          linewidth=2, alpha=0.8 + pulse * 0.2)
            self.ax.add_patch(circle)
            
            # Label
            self.ax.text(nx, ny - 7, name, ha='center', va='top',
                      fontsize=8, color=BOB_ROSS["Titanium White"])
    
    def draw_progress_bar(self, x, y, width, height, label, progress, color):
        """Draw a progress bar"""
        # Background
        rect = FancyBboxPatch((x, y), width, height,
                             boxstyle="round,pad=0.01",
                             facecolor=BOB_ROSS["Dark Sienna"],
                             edgecolor=BOB_ROSS["Van Dyke Brown"],
                             linewidth=1, alpha=0.6)
        self.ax.add_patch(rect)
        
        # Progress fill
        fill_width = width * progress
        fill = FancyBboxPatch((x, y), fill_width, height,
                             boxstyle="round,pad=0.01",
                             facecolor=color,
                             edgecolor='none', alpha=0.8)
        self.ax.add_patch(fill)
        
        # Label
        self.ax.text(x + width/2, y + height/2, 
                    f"{label}: {progress*100:.1f}%",
                    ha='center', va='center', fontsize=9,
                    color=BOB_ROSS["Titanium White"], fontweight='bold')
    
    def run(self):
        """Main visualization loop"""
        print("\n🎨 Starting Brain Visualizer...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                state = self.load_state()
                self.draw_brain(state)
                time.sleep(2)  # Update every 2 seconds
                
        except KeyboardInterrupt:
            print("\n👋 Visualizer stopped")
            plt.close()

if __name__ == "__main__":
    viz = BrainVisualizerLive()
    viz.run()
