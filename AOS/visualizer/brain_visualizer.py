import json
import os
import time
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pathlib import Path

STATE_PATH = Path.home() / ".aos" / "brain" / "state" / "brain_state.json"

bob_ross_palette = {
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
    "Titanium White": "#FDF5E6"
}

phase_colors = {
    "Observe": bob_ross_palette["Phthalo Blue"],
    "Orient": bob_ross_palette["Sap Green"],
    "Decide": bob_ross_palette["Bright Red"],
    "Act": bob_ross_palette["Cadmium Yellow"]
}

def load_state():
    if not os.path.exists(STATE_PATH):
        return None
    try:
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return None

def mandelbrot_background(width=400, height=300, max_iter=50, zoom=1.0, offset=(0.0, 0.0)):
    img = np.zeros((height, width))
    for x in range(width):
        for y in range(height):
            zx = 1.5 * (x - width / 2) / (0.5 * zoom * width) + offset[0]
            zy = (y - height / 2) / (0.5 * zoom * height) + offset[1]
            c_x, c_y = zx, zy
            iter_count = 0
            while zx*zx + zy*zy < 4 and iter_count < max_iter:
                tmp = zx*zx - zy*zy + c_x
                zy = 2.0*zx*zy + c_y
                zx = tmp
                iter_count += 1
            img[y, x] = iter_count / max_iter
    return img

class BrainVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        plt.ion()
        self.zoom = 1.0
        self.offset = (0.0, 0.0)
        self.last_layer_counts = None

    def draw(self, state):
        self.ax.clear()
        self.ax.set_axis_off()

        phase = state.get("phase", "Observe")
        limbic = state.get("limbic", {})
        policy_nn = state.get("policy_nn", {})
        memory_nn = state.get("memory_nn", {})

        reward = limbic.get("reward", 0.0)
        novelty = limbic.get("novelty", 0.0)

        self.draw_background(phase, reward, novelty)
        self.draw_policy_network(policy_nn, reward, novelty)
        self.draw_memory_map(memory_nn, reward, novelty)
        self.draw_phase_indicator(phase)
        self.draw_signature()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def draw_background(self, phase, reward, novelty):
        self.zoom = 1.0 + novelty * 2.0
        self.offset = (math.sin(reward * math.pi), math.cos(reward * math.pi))
        mb = mandelbrot_background(400, 300, max_iter=40, zoom=self.zoom, offset=self.offset)
        self.ax.imshow(mb, extent=[-1, 1, -1, 1], cmap="inferno", alpha=0.6)

        sky_color = phase_colors.get(phase, bob_ross_palette["Midnight Black"])
        self.ax.set_facecolor(sky_color)

    def draw_policy_network(self, policy_nn, reward, novelty):
        layers = policy_nn.get("layers", 0)
        nodes = policy_nn.get("nodes", [])
        activations = policy_nn.get("activations", [])

        if not layers or not nodes:
            return

        max_nodes = max(nodes)
        y_step = 2.0 / (layers + 1)
        x_step = 2.0 / (max_nodes + 1)

        growth_pulse = False
        if self.last_layer_counts is not None and len(nodes) > len(self.last_layer_counts):
            growth_pulse = True
        self.last_layer_counts = nodes[:]

        for li in range(layers):
            n = nodes[li] if li < len(nodes) else 0
            for ni in range(n):
                x = -1.0 + (ni + 1) * x_step
                y = 0.8 - (li + 1) * y_step

                act = 0.0
                if activations and li < len(activations) and ni < len(activations[li]):
                    act = activations[li][ni]

                size = 0.03 + act * 0.07
                color = self.activation_color(act, reward)

                circ = Circle((x, y), size, color=color, alpha=0.9)
                self.ax.add_patch(circ)

                if growth_pulse and li == layers - 1:
                    pulse = Circle((x, y), size * 1.8,
                                   edgecolor=bob_ross_palette["Indian Yellow"],
                                   facecolor="none", linewidth=1.5, alpha=0.7)
                    self.ax.add_patch(pulse)

    def activation_color(self, act, reward):
        if reward > 0.6:
            base = bob_ross_palette["Bright Red"]
        elif reward < -0.3:
            base = bob_ross_palette["Prussian Blue"]
        else:
            base = bob_ross_palette["Sap Green"]

        r = int(int(base[1:3], 16) * (0.5 + act / 2))
        g = int(int(base[3:5], 16) * (0.5 + act / 2))
        b = int(int(base[5:7], 16) * (0.5 + act / 2))
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        return f"#{r:02X}{g:02X}{b:02X}"

    def draw_memory_map(self, memory_nn, reward, novelty):
        clusters = memory_nn.get("clusters", 0)
        if clusters <= 0:
            return

        for _ in range(clusters):
            cx = random.uniform(-0.9, 0.9)
            cy = random.uniform(-0.9, -0.2)
            size = 0.03 + random.random() * 0.04
            color = bob_ross_palette["Yellow Ochre"] if novelty > 0.5 else bob_ross_palette["Titanium White"]
            circ = Circle((cx, cy), size, color=color, alpha=0.6)
            self.ax.add_patch(circ)

    def draw_phase_indicator(self, phase):
        text = f"OODA: {phase}"
        self.ax.text(-0.95, 0.9, text,
                     fontsize=14,
                     color=bob_ross_palette["Titanium White"],
                     ha="left", va="center",
                     bbox=dict(boxstyle="round,pad=0.3",
                               facecolor=bob_ross_palette["Dark Sienna"],
                               alpha=0.7))

    def draw_signature(self):
        self.ax.text(0.95, -0.95, "OpenClaw Brain",
                     fontsize=10,
                     color=bob_ross_palette["Titanium White"],
                     ha="right", va="center",
                     alpha=0.8)

def main():
    viz = BrainVisualizer()
    while True:
        state = load_state()
        if state:
            viz.draw(state)
        else:
            time.sleep(0.2)
        plt.pause(0.05)

if __name__ == "__main__":
    main()
