#!/usr/bin/env python3
"""
GROWING NEURAL NETWORK — neurogenesis + pruning + persistence
=============================================================
A self-modifying neural network that:
  • LEARNS via backpropagation (stochastic gradient descent)
  • GROWS  — adds neurons (and layers) when learning plateaus
  • PRUNES — removes weak connections and dead neurons
  • SAVES  — persists its full state (weights + topology + history)

Designed to augment the ternary brain (myl0n/brain/ternary_brain.py).
Runs comfortably in a few MB of RAM — no external model needed.

Author: Mortimer
"""

import json
import os
import time

import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# ACTIVATION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def _activation(name):
    if name == "tanh":
        return (lambda x: np.tanh(x),
                lambda x: 1.0 - np.tanh(x) ** 2)
    if name == "relu":
        return (lambda x: np.maximum(0.0, x),
                lambda x: (x > 0.0).astype(float))
    if name == "sigmoid":
        return (lambda x: 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500))),
                lambda x: (lambda s: s * (1.0 - s))(1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))))
    if name == "linear":
        return (lambda x: x, lambda x: np.ones_like(x))
    raise ValueError(f"Unknown activation: {name}")


# ─────────────────────────────────────────────────────────────────────────────
# THE GROWING NETWORK
# ─────────────────────────────────────────────────────────────────────────────

class GrowingNetwork:
    """A feedforward network that grows, prunes, and persists itself."""

    def __init__(self, input_size, output_size, hidden_sizes=None,
                 activation="tanh", lr=0.05, seed=None):
        if seed is not None:
            np.random.seed(seed)
        self.input_size = int(input_size)
        self.output_size = int(output_size)
        self.sizes = [self.input_size] + list(hidden_sizes or [4]) + [self.output_size]
        self.lr = float(lr)
        self.activation_name = activation
        self.act, self.act_deriv = _activation(activation)

        # He initialization
        self.weights = []
        self.biases = []
        for i in range(len(self.sizes) - 1):
            self.weights.append(
                np.random.randn(self.sizes[i], self.sizes[i + 1])
                * np.sqrt(2.0 / self.sizes[i])
            )
            self.biases.append(np.zeros(self.sizes[i + 1]))

        # Lifecycle bookkeeping
        self.generation = 0          # number of growth events
        self.total_epochs = 0        # total training epochs seen
        self.loss_history = []       # per-epoch loss
        self.born = time.time()

    # ── Forward / backward ──────────────────────────────────────────────────

    def forward(self, x):
        """Return the list of layer activations (acts[0] == input)."""
        acts = [np.asarray(x, dtype=float)]
        for i in range(len(self.weights)):
            z = acts[-1] @ self.weights[i] + self.biases[i]
            acts.append(self.act(z))
        return acts

    def predict(self, x):
        return self.forward(x)[-1]

    def _train_step(self, x, y):
        """One SGD step. Returns the squared loss for this sample."""
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        acts = [x]
        zs = []
        for i in range(len(self.weights)):
            z = acts[-1] @ self.weights[i] + self.biases[i]
            zs.append(z)
            acts.append(self.act(z))

        loss = float(np.sum((acts[-1] - y) ** 2))

        # Backprop
        delta = (acts[-1] - y) * self.act_deriv(zs[-1])
        dW = [None] * len(self.weights)
        db = [None] * len(self.biases)
        dW[-1] = np.outer(acts[-2], delta)
        db[-1] = delta
        for i in range(len(self.weights) - 2, -1, -1):
            delta = (delta @ self.weights[i + 1].T) * self.act_deriv(zs[i])
            dW[i] = np.outer(acts[i], delta)
            db[i] = delta

        for i in range(len(self.weights)):
            self.weights[i] -= self.lr * dW[i]
            self.biases[i] -= self.lr * db[i]

        return loss

    # ── Training loop with growth ───────────────────────────────────────────

    def train(self, X, y, epochs=200, patience=30, grow=True,
              prune_every=0, prune_threshold=0.01, verbose=True):
        """
        Train on (X, y). When loss plateaus for `patience` epochs, grow.
        Optionally prune every `prune_every` epochs.
        """
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        n = len(X)

        best = float("inf")
        stall = 0

        for ep in range(epochs):
            # Shuffle
            idx = np.random.permutation(n)
            total = 0.0
            for i in idx:
                total += self._train_step(X[i], y[i])
            avg = total / n
            self.loss_history.append(avg)
            self.total_epochs += 1

            if avg < best - 1e-6:
                best = avg
                stall = 0
            else:
                stall += 1

            if verbose and (ep % max(1, epochs // 10) == 0 or ep == epochs - 1):
                print(f"  epoch {ep:4d}  loss {avg:.6f}  "
                      f"topology {self.topology_str()}")

            # Growth trigger
            if grow and stall >= patience and avg > 1e-4:
                self.grow()
                stall = 0
                best = avg
                if verbose:
                    print(f"  🌱 grew → topology {self.topology_str()}")

            # Pruning trigger
            if prune_every and ep > 0 and ep % prune_every == 0:
                removed = self.prune(prune_threshold)
                if removed and verbose:
                    print(f"  ✂️  pruned {removed} connection(s)")

        return best

    # ── Growth (neurogenesis) ───────────────────────────────────────────────

    def grow(self, mode="node"):
        """Add capacity. 'node' adds a neuron; 'layer' adds a hidden layer."""
        if mode == "layer":
            return self._grow_layer()
        return self._grow_node()

    def _grow_node(self):
        """Add one neuron to the last hidden layer."""
        k = len(self.sizes) - 2          # index of last hidden layer
        if k < 1:
            # No hidden layer yet — insert one
            return self._grow_layer()

        # New neuron's incoming weights (a new column)
        new_in = np.random.randn(self.sizes[k - 1], 1) * 0.1
        self.weights[k - 1] = np.hstack([self.weights[k - 1], new_in])
        # New neuron's outgoing weights (a new row)
        new_out = np.random.randn(1, self.sizes[k + 1]) * 0.1
        self.weights[k] = np.vstack([self.weights[k], new_out])
        # New neuron's bias
        self.biases[k - 1] = np.append(self.biases[k - 1], 0.0)
        self.sizes[k] += 1
        self.generation += 1
        return self.sizes[k]

    def _grow_layer(self):
        """Insert a new hidden layer (size 4) before the output."""
        new_size = 4
        last_hidden = self.sizes[-2]
        out = self.sizes[-1]

        # Replace the last weight matrix (hidden→out) with two:
        #   hidden→new  and  new→out
        w_in = np.random.randn(last_hidden, new_size) * np.sqrt(2.0 / last_hidden)
        w_out = np.random.randn(new_size, out) * np.sqrt(2.0 / new_size)
        b_new = np.zeros(new_size)

        self.weights = self.weights[:-1] + [w_in, w_out]
        self.biases = self.biases[:-1] + [b_new, self.biases[-1]]
        self.sizes.insert(-1, new_size)
        self.generation += 1
        return new_size

    # ── Pruning ─────────────────────────────────────────────────────────────

    def prune(self, threshold=0.01):
        """Zero weak connections and remove dead neurons. Returns count removed."""
        removed = 0

        # 1) Zero weak connections
        for i in range(len(self.weights)):
            mask = np.abs(self.weights[i]) < threshold
            removed += int(mask.sum())
            self.weights[i][mask] = 0.0

        # 2) Remove dead neurons (hidden layers only)
        for k in range(1, len(self.sizes) - 1):
            incoming = np.abs(self.weights[k - 1]).sum(axis=0)   # per-neuron
            outgoing = np.abs(self.weights[k]).sum(axis=1)       # per-neuron
            activity = incoming + outgoing
            dead = np.where(activity < threshold)[0]

            if len(dead) == 0:
                continue
            if len(dead) >= self.sizes[k]:
                # Never remove the entire layer
                dead = dead[: max(0, self.sizes[k] - 1)]

            keep = np.ones(self.sizes[k], dtype=bool)
            keep[dead] = False

            self.weights[k - 1] = self.weights[k - 1][:, keep]
            self.weights[k] = self.weights[k][keep, :]
            self.biases[k - 1] = self.biases[k - 1][keep]
            self.sizes[k] = int(keep.sum())
            removed += len(dead)

        return removed

    # ── Persistence ─────────────────────────────────────────────────────────

    def save(self, path):
        """Save weights + topology + history to disk."""
        base = os.path.splitext(path)[0]
        np.savez(
            base + ".npz",
            **{f"w{i}": w for i, w in enumerate(self.weights)},
            **{f"b{i}": b for i, b in enumerate(self.biases)},
        )
        meta = {
            "input_size": self.input_size,
            "output_size": self.output_size,
            "sizes": self.sizes,
            "activation": self.activation_name,
            "lr": self.lr,
            "generation": self.generation,
            "total_epochs": self.total_epochs,
            "loss_history": self.loss_history,
            "born": self.born,
            "saved": time.time(),
        }
        with open(base + ".json", "w") as f:
            json.dump(meta, f, indent=2)
        return base

    @classmethod
    def load(cls, path):
        """Reconstruct a network from a saved state."""
        base = os.path.splitext(path)[0]
        with open(base + ".json") as f:
            meta = json.load(f)
        net = cls(
            meta["input_size"], meta["output_size"],
            hidden_sizes=meta["sizes"][1:-1],
            activation=meta["activation"], lr=meta["lr"],
        )
        data = np.load(base + ".npz")
        net.weights = [data[f"w{i}"] for i in range(len(net.weights))]
        net.biases = [data[f"b{i}"] for i in range(len(net.biases))]
        net.sizes = list(meta["sizes"])
        net.generation = meta["generation"]
        net.total_epochs = meta["total_epochs"]
        net.loss_history = meta["loss_history"]
        net.born = meta["born"]
        return net

    # ── Introspection ───────────────────────────────────────────────────────

    def topology_str(self):
        return "→".join(str(s) for s in self.sizes)

    def param_count(self):
        return sum(w.size for w in self.weights) + sum(b.size for b in self.biases)

    def stats(self):
        return {
            "topology": self.topology_str(),
            "parameters": self.param_count(),
            "generation": self.generation,
            "total_epochs": self.total_epochs,
            "final_loss": self.loss_history[-1] if self.loss_history else None,
            "age_seconds": round(time.time() - self.born, 1),
        }


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═" * 60)
    print("GROWING NEURAL NETWORK — neurogenesis demo")
    print("═" * 60)

    # XOR: a single hidden neuron CANNOT solve it — the network must grow.
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([[0], [1], [1], [0]], dtype=float)

    net = GrowingNetwork(input_size=2, output_size=1, hidden_sizes=[1],
                         activation="tanh", lr=0.3, seed=42)
    print(f"\nStarting topology: {net.topology_str()}  "
          f"({net.param_count()} params)")
    print("Task: XOR (needs ≥2 hidden neurons — forces growth)\n")

    net.train(X, y, epochs=400, patience=25, grow=True, verbose=True)

    print("\n" + "─" * 60)
    print("After training:")
    for s in net.stats().items():
        print(f"  {s[0]}: {s[1]}")

    print("\nPredictions:")
    for xi, yi in zip(X, y):
        p = net.predict(xi)[0]
        print(f"  {xi[0]:.0f} XOR {xi[1]:.0f} = {yi[0]:.0f}  →  {p:+.3f}  "
              f"({'✓' if round(p) == yi[0] else '✗'})")

    # Save + reload
    base = net.save("/data/data/com.termux/files/home/myl0n/brain/cortex_demo")
    print(f"\nSaved state → {base}.npz + {base}.json")

    net2 = GrowingNetwork.load(base)
    print(f"Reloaded: topology {net2.topology_str()}, "
          f"{net2.param_count()} params, generation {net2.generation}")
    print(f"Reloaded predicts [1,0] XOR = {net2.predict([1, 0])[0]:+.3f}")
