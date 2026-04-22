#!/usr/bin/env python3
"""
DOMAIN CURRICULUM FEEDERS v1.0
Additional knowledge domains for Brain v4
"""

import socket
import json
import time

def send(cmd, params=None):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect('/tmp/aos_brain.sock')
    
    request = {"cmd": cmd}
    if params:
        request["params"] = params
    
    sock.sendall(json.dumps(request).encode() + b'\n')
    
    response = b''
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    
    sock.close()
    return json.loads(response.decode())

# === MUSIC THEORY ===
MUSIC_THEORY = [
    ("Octave: frequency ratio 2:1, twelve semitones", 0.82),
    ("Perfect fifth: ratio 3:2, seven semitones", 0.80),
    ("Circle of fifths: C-G-D-A-E-B-F#-C#", 0.78),
    ("Harmonic series: fundamental + overtones", 0.85),
    ("Equal temperament: 12th root of 2 ratio", 0.84),
    ("Major scale: W-W-H-W-W-W-H pattern", 0.79),
    ("Minor scale: W-H-W-W-H-W-W pattern", 0.78),
    ("Chord progression: I-V-vi-IV common", 0.77),
    ("Resonance: sympathetic vibration frequencies", 0.81),
    ("Timbre: harmonic content defines instrument", 0.80),
]

# === COMPUTER SCIENCE ===
COMP_SCI = [
    ("Big O notation: O(1), O(log n), O(n), O(n²)", 0.85),
    ("Binary search: divide and conquer, O(log n)", 0.84),
    ("Hash table: O(1) average lookup", 0.83),
    ("Recursion: function calls itself, base case", 0.82),
    ("Dynamic programming: memoization, overlapping subproblems", 0.85),
    ("Graph traversal: BFS queue, DFS stack", 0.84),
    ("TCP/IP: packets, routing, reliability", 0.80),
    ("Blockchain: distributed ledger, consensus", 0.82),
    ("Neural network: weights, activation, backprop", 0.88),
    ("Version control: git commits branches merge", 0.78),
]

# === HISTORY ===
HISTORY = [
    ("Printing press 1440: Gutenberg, information revolution", 0.80),
    ("Scientific method: observation hypothesis test", 0.85),
    ("Industrial Revolution: steam, factory, urbanization", 0.82),
    ("Enlightenment: reason, individual rights, liberty", 0.84),
    ("Renaissance: humanism, art, rebirth of learning", 0.81),
    ("Silk Road: trade, culture exchange, connection", 0.79),
    ("Democracy: Athens, representation, citizen rule", 0.83),
    ("Monotheism: one God, Abrahamic traditions", 0.80),
    ("Age of Exploration: navigation, colonialism, global", 0.79),
    ("Information Age: internet, computing, data", 0.86),
]

# === BIOLOGY ===
BIOLOGY = [
    ("DNA: double helix, base pairs, genetic code", 0.88),
    ("Central dogma: DNA → RNA → Protein", 0.87),
    ("Natural selection: variation, inheritance, fitness", 0.90),
    ("Photosynthesis: light + CO2 + H2O → glucose + O2", 0.86),
    ("Cell: membrane, nucleus, mitochondria, ribosomes", 0.85),
    ("Homeostasis: stable internal environment", 0.82),
    ("Ecosystem: producers, consumers, decomposers", 0.81),
    ("Evolution: common descent, speciation, adaptation", 0.89),
    ("Neuron: axon, dendrite, synapse, action potential", 0.84),
    ("Immune system: innate, adaptive, antibodies", 0.83),
]

# === ECONOMICS ===
ECONOMICS = [
    ("Supply and demand: price equilibrium", 0.82),
    ("Marginal utility: diminishing returns", 0.80),
    ("Comparative advantage: trade benefits all", 0.84),
    ("Inflation: money supply, purchasing power", 0.81),
    ("GDP: gross domestic product, economic health", 0.79),
    ("Market failure: externalities, public goods", 0.82),
    ("Behavioral economics: psychology in decisions", 0.83),
    ("Game theory: Nash equilibrium, strategy", 0.85),
    ("Cryptocurrency: decentralized, blockchain, value", 0.84),
    ("Interest rates: time value of money", 0.81),
]

# === PSYCHOLOGY ===
PSYCHOLOGY = [
    ("Cognitive bias: heuristics, errors in thinking", 0.85),
    ("Flow state: challenge-skill balance, absorption", 0.86),
    ("Attachment theory: secure, anxious, avoidant", 0.82),
    ("Maslow hierarchy: physiological to self-actualization", 0.83),
    ("Confirmation bias: seek confirming evidence", 0.84),
    ("Dunning-Kruger: incompetence overestimates ability", 0.85),
    ("Growth mindset: ability develops through effort", 0.87),
    ("Hedonic adaptation: return to baseline happiness", 0.82),
    ("Mirror neurons: empathy, imitation, understanding", 0.84),
    ("Cognitive dissonance: conflicting beliefs tension", 0.83),
]

def feed_domain(name, items):
    print(f"\n{'='*60}")
    print(f"FEEDING: {name}")
    print(f"{'='*60}")
    
    for i, (content, importance) in enumerate(items, 1):
        result = send("stimulate", {
            "importance": importance,
            "content": content,
            "type": name.upper()
        })
        
        if i % 3 == 0:
            print(f"  [{i}/{len(items)}] ", end="", flush=True)
        print(".", end="", flush=True)
        time.sleep(0.1)
    
    print(f"\n  ✓ Fed {len(items)} {name} items")

def main():
    print("=" * 70)
    print("DOMAIN CURRICULUM FEEDERS v1.0")
    print("Expanding knowledge across disciplines")
    print("=" * 70)
    
    # Feed all domains
    feed_domain("MUSIC_THEORY", MUSIC_THEORY)
    feed_domain("COMP_SCI", COMP_SCI)
    feed_domain("HISTORY", HISTORY)
    feed_domain("BIOLOGY", BIOLOGY)
    feed_domain("ECONOMICS", ECONOMICS)
    feed_domain("PSYCHOLOGY", PSYCHOLOGY)
    
    # Summary
    total = sum(len(x) for x in [MUSIC_THEORY, COMP_SCI, HISTORY, BIOLOGY, ECONOMICS, PSYCHOLOGY])
    
    print("\n" + "=" * 70)
    print("CURRICULUM EXPANSION COMPLETE")
    print("=" * 70)
    print(f"\nTotal new items: {total}")
    print("\nDomains added:")
    print("  🎵 Music Theory (10) - Harmonics, scales, resonance")
    print("  💻 Computer Science (10) - Algorithms, networks, AI")
    print("  📜 History (10) - Revolutions, enlightenment, ages")
    print("  🧬 Biology (10) - DNA, evolution, ecosystems")
    print("  💰 Economics (10) - Markets, trade, value")
    print("  🧠 Psychology (10) - Cognition, behavior, mind")
    
    status = send("status")
    print(f"\nBrain tick: {status['tick']}")
    print("All domains integrated into knowledge base")
    print("=" * 70)

if __name__ == "__main__":
    main()
