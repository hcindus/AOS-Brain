#!/usr/bin/env python3
"""
TERNARY CORTEX — a growing neural network wired into the ternary brain
=====================================================================
The ternary brain (ternary_brain.py) reasons symbolically with -1/0/1
qbits. This module gives it a LEARNABLE cortex: a growing neural
network that:
  • LEARNS patterns from ternary qbit states
  • GROWS  (adds neurons/layers) as knowledge increases
  • PRUNES dead neurons
  • SAVES/LOADS its full state

The cortex encodes ternary qbits (-1/0/1) as network inputs, learns to
map them to outcomes, and provides "intuition" the symbolic logic can't.

Author: Mortimer
"""

import numpy as np

from growing_brain import GrowingNetwork
from ternary_brain import TernaryQbit, TernaryState


class TernaryCortex:
    """A growing neural network that learns ternary (-1/0/1) patterns."""

    def __init__(self, n_qbits, output_size=1, hidden_sizes=None,
                 lr=0.1, seed=None):
        self.n_qbits = int(n_qbits)
        self.output_size = int(output_size)
        self.net = GrowingNetwork(
            self.n_qbits, self.output_size,
            hidden_sizes=hidden_sizes,
            activation="tanh", lr=lr, seed=seed,
        )

    # ── Ternary ↔ network encoding ─────────────────────────────────────────

    def encode(self, qbits):
        """Encode a list of -1/0/1 qbits (or TernaryQbit objects) → vector."""
        vals = []
        for q in qbits:
            vals.append(q.value if isinstance(q, TernaryQbit) else int(q))
        return np.array(vals, dtype=float)

    def decode(self, output):
        """Decode a network output → TernaryQbit (-1/0/1)."""
        o = float(np.asarray(output).ravel()[0])
        if o > 0.33:
            return TernaryQbit(1)
        if o < -0.33:
            return TernaryQbit(-1)
        return TernaryQbit(0)

    # ── Learning ───────────────────────────────────────────────────────────

    def learn(self, experiences, epochs=200, patience=30, grow=True,
              verbose=False):
        """
        Learn from experiences: list of (qbit_state, outcome) pairs.
        qbit_state is a list of -1/0/1; outcome is -1/0/1 (or a float).
        """
        X = np.array([self.encode(q) for q, _ in experiences], dtype=float)
        y = np.array([[float(o)] for _, o in experiences], dtype=float)
        return self.net.train(X, y, epochs=epochs, patience=patience,
                              grow=grow, verbose=verbose)

    def infer(self, qbits):
        """Predict the ternary outcome for a qbit state."""
        return self.decode(self.net.predict(self.encode(qbits)))

    # ── Lifecycle ───────────────────────────────────────────────────────────

    def grow(self, mode="node"):
        return self.net.grow(mode)

    def prune(self, threshold=0.01):
        return self.net.prune(threshold)

    def save(self, path):
        return self.net.save(path)

    @classmethod
    def load(cls, path):
        net = GrowingNetwork.load(path)
        cortex = cls(net.input_size, net.output_size)
        cortex.net = net
        return cortex

    def stats(self):
        return self.net.stats()


# ─────────────────────────────────────────────────────────────────────────────
# INTEGRATION WITH THE TERNARY BRAIN
# ─────────────────────────────────────────────────────────────────────────────

def attach_cortex(brain, n_qbits=8, output_size=1, hidden_sizes=None,
                  lr=0.1, seed=None):
    """Attach a learnable TernaryCortex to an existing TernaryBrain."""
    brain.cortex = TernaryCortex(n_qbits, output_size,
                                 hidden_sizes=hidden_sizes, lr=lr, seed=seed)
    return brain.cortex


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═" * 60)
    print("TERNARY CORTEX — growing network learns a ternary function")
    print("═" * 60)

    # Task: majority vote over 3 qbits → sign(sum)
    # This is a natural ternary aggregation the cortex must learn.
    def majority(q):
        s = sum(q)
        return 1 if s > 0 else (-1 if s < 0 else 0)

    # All 27 combinations of 3 ternary qbits
    import itertools
    states = list(itertools.product([-1, 0, 1], repeat=3))
    experiences = [(list(s), majority(s)) for s in states]

    cortex = TernaryCortex(n_qbits=3, output_size=1, hidden_sizes=[2],
                           lr=0.2, seed=42)
    print(f"\nStarting topology: {cortex.stats()['topology']}  "
          f"({cortex.stats()['parameters']} params)")
    print("Task: majority vote over 3 qbits (27 training examples)\n")

    cortex.learn(experiences, epochs=300, patience=25, grow=True, verbose=True)

    print("\n" + "─" * 60)
    print("After learning:")
    for k, v in cortex.stats().items():
        print(f"  {k}: {v}")

    # Test predictions
    print("\nPredictions (qbits → majority):")
    correct = 0
    for s in states:
        pred = cortex.infer(list(s)).value
        truth = majority(s)
        ok = pred == truth
        correct += ok
        print(f"  {s} → {pred:+d}  (truth {truth:+d})  {'✓' if ok else '✗'}")
    print(f"\nAccuracy: {correct}/{len(states)} = {100*correct/len(states):.0f}%")

    # Save + reload
    base = cortex.save("/data/data/com.termux/files/home/myl0n/brain/cortex")
    print(f"\nSaved → {base}.npz + {base}.json")

    cortex2 = TernaryCortex.load(base)
    print(f"Reloaded: topology {cortex2.stats()['topology']}, "
          f"generation {cortex2.stats()['generation']}")
    print(f"Reloaded predicts [1,-1,1] → {cortex2.infer([1,-1,1]).value:+d}")

    # ── Integration with the actual ternary brain ──────────────────────────
    print("\n" + "═" * 60)
    print("INTEGRATION — attaching the cortex to the ternary brain")
    print("═" * 60)
    from ternary_brain import TernaryBrain
    brain = TernaryBrain()
    attach_cortex(brain, n_qbits=3, output_size=1, hidden_sizes=[2], seed=1)
    print(f"Brain: {brain.name}")
    print(f"  symbolic organs: {list(brain.state().keys())}")
    print(f"  + learnable cortex: {brain.cortex.stats()['topology']} "
          f"({brain.cortex.stats()['parameters']} params)")
    print("\nThe ternary brain now has BOTH:")
    print("  • symbolic reasoning (qbits, organs, routing)")
    print("  • a learnable, growing, self-pruning neural cortex")
