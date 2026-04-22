#!/usr/bin/env python3
"""
CASCADE CURRICULUM RE-FEED v1.0
Feeds knowledge through proper cascade: Conscious → Subconscious → Unconscious
"""

import socket
import json
import time
import random

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

def cascade_feed(item, importance, item_type="KNOWLEDGE"):
    """Feed through cascade: conscious → subconscious → unconscious"""
    
    # Step 1: Enter Conscious (perception)
    result = send("perceive", {
        "observation": f"[{item_type}] {item}",
        "intensity": importance
    })
    
    # Step 2: Seed Subconscious (pattern extraction)
    patterns = [
        f"Pattern_extracted_{item_type}_{hash(item) % 1000}",
        f"Association_{item_type}_link",
        f"Cluster_{item_type}_node"
    ]
    for pattern in patterns:
        send("add_to_layer", {
            "layer": "subconscious",
            "content": pattern,
            "intensity": importance * 0.85,
            "associations": ["pattern", item_type.lower(), "cascade"]
        })
    
    # Step 3: Seed Unconscious (if high importance)
    if importance >= 0.85:
        abstraction = f"Truth_{item_type}_{hash(item) % 10000}_abstract"
        send("add_to_layer", {
            "layer": "unconscious",
            "content": abstraction,
            "intensity": importance * 0.92,
            "associations": ["abstraction", item_type.lower(), "truth"]
        })
    
    time.sleep(0.15)

# ORIGINAL CURRICULUM - Re-fed through cascade
EQUATIONS = [
    ("Einstein: E = mc² (energy equals mass times speed of light squared)", 0.95),
    ("Pythagorean: a² + b² = c² (right triangle hypotenuse)", 0.88),
    ("Quadratic: x = (-b ± √(b² - 4ac)) / 2a", 0.85),
    ("Newton's Second: F = ma (force equals mass times acceleration)", 0.90),
    ("Euler's Identity: e^(iπ) + 1 = 0 (most beautiful equation)", 0.96),
    ("Schrödinger: iℏ ∂ψ/∂t = Ĥψ (quantum mechanics wave function)", 0.93),
    ("Maxwell: ∇ × E = -∂B/∂t (Faraday's law of induction)", 0.90),
    ("Bayes: P(A|B) = P(B|A) × P(A) / P(B) (conditional probability)", 0.88),
    ("Compound Interest: A = P(1 + r/n)^(nt)", 0.80),
    ("Standard Deviation: σ = √(Σ(x - μ)² / N)", 0.82),
    ("Logistic Growth: dP/dt = rP(1 - P/K)", 0.78),
    ("Heat Equation: ∂u/∂t = α ∇²u (diffusion of heat)", 0.85),
    ("Wave Equation: ∂²u/∂t² = c² ∇²u", 0.85),
    ("Black-Scholes: ∂V/∂t + ½σ²S² ∂²V/∂S² + rS ∂V/∂S - rV = 0", 0.90),
    ("Cauchy-Schwarz: |⟨u,v⟩| ≤ ‖u‖ ‖v‖", 0.83),
]

BIBLE = [
    ("Genesis 1:1 - In the beginning God created the heavens and the earth.", 0.90),
    ("Genesis 1:3 - And God said, Let there be light: and there was light.", 0.88),
    ("Psalm 23:1 - The Lord is my shepherd; I shall not want.", 0.88),
    ("Psalm 23:4 - Yea, though I walk through the valley of the shadow of death, I will fear no evil.", 0.90),
    ("John 1:1 - In the beginning was the Word, and the Word was with God, and the Word was God.", 0.92),
    ("John 3:16 - For God so loved the world, that he gave his only begotten Son.", 0.95),
    ("John 14:6 - I am the way, the truth, and the life: no man cometh unto the Father, but by me.", 0.90),
    ("Romans 6:23 - For the wages of sin is death; but the gift of God is eternal life through Jesus Christ.", 0.91),
    ("Romans 8:28 - All things work together for good to them that love God, to them who are called according to his purpose.", 0.89),
    ("1 Corinthians 13:4-8 - Charity suffereth long, is kind; envieth not; vaunteth not itself; never faileth.", 0.88),
    ("Ephesians 2:8 - By grace are ye saved through faith; and that not of yourselves: it is the gift of God.", 0.90),
    ("Philippians 4:13 - I can do all things through Christ which strengtheneth me.", 0.90),
    ("Hebrews 11:1 - Faith is the substance of things hoped for, the evidence of things not seen.", 0.90),
    ("Revelation 21:4 - God shall wipe away all tears from their eyes; and there shall be no more death.", 0.90),
]

FRACTALS = [
    ("Mandelbrot Set: z → z² + c, bounded if |z| < 2 after iterations", 0.92),
    ("Julia Set: z → z² + c for fixed c, each c gives unique fractal", 0.90),
    ("Sierpinski Triangle: Remove middle triangle recursively", 0.85),
    ("Koch Snowflake: Each line replaced by 4 segments, infinite perimeter", 0.87),
    ("Dragon Curve: Paper folding fractal, L-system: FX → X+YF+, Y → -FX-Y", 0.85),
    ("Barnsley Fern: 4 affine transformations, probability weighted", 0.86),
    ("Lorenz Attractor: dx/dt = σ(y-x), dy/dt = x(ρ-z)-y, dz/dt = xy-βz", 0.90),
    ("Feigenbaum Constant: δ ≈ 4.669 (bifurcation universality)", 0.88),
]

print("=" * 70)
print("CASCADE CURRICULUM RE-FEED v1.0")
print("Proper flow: Conscious → Subconscious → Unconscious")
print("=" * 70)

# Check initial
status = send("status")
c = status['consciousness']
print(f"\n[INIT] Before re-feed:")
print(f"       Conscious: {c['conscious']['active_items']}/10")
print(f"       Subconscious: {c['subconscious']['active_items']}/100")
print(f"       Unconscious: {c['unconscious']['active_items']}/1000")

# Feed Equations
total = 0
print("\n" + "=" * 70)
print("FEEDING: EQUATIONS (15 items)")
print("=" * 70)
for item, imp in EQUATIONS:
    cascade_feed(item, imp, "EQUATION")
    total += 1
    if total % 5 == 0:
        print(f"  [{total}/37] Cascade feeding...")
print(f"  ✓ {len(EQUATIONS)} equations cascaded")

# Feed Bible
print("\n" + "=" * 70)
print("FEEDING: BIBLE (14 items)")
print("=" * 70)
for item, imp in BIBLE:
    cascade_feed(item, imp, "SCRIPTURE")
    total += 1
    if total % 5 == 0:
        print(f"  [{total}/37] Cascade feeding...")
print(f"  ✓ {len(BIBLE)} scriptures cascaded")

# Feed Fractals
print("\n" + "=" * 70)
print("FEEDING: FRACTALS (8 items)")
print("=" * 70)
for item, imp in FRACTALS:
    cascade_feed(item, imp, "FRACTAL")
    total += 1
    if total % 5 == 0:
        print(f"  [{total}/37] Cascade feeding...")
print(f"  ✓ {len(FRACTALS)} fractals cascaded")

# Final status
print("\n" + "=" * 70)
print("CASCADE RE-FEED COMPLETE")
print("=" * 70)

status = send("status")
c = status['consciousness']

print(f"\nAfter cascade re-feed:")
print(f"  Conscious:    {c['conscious']['active_items']}/10")
print(f"  Subconscious: {c['subconscious']['active_items']}/100")
print(f"  Unconscious:  {c['unconscious']['active_items']}/1000")

con_pct = (c['conscious']['active_items']/10)*100
sub_pct = (c['subconscious']['active_items']/100)*100
unc_pct = (c['unconscious']['active_items']/1000)*100

print(f"\n┌─────────────────────────────────────────────┐")
print(f"│  CASCADE STATUS                             │")
print(f"├─────────────────────────────────────────────┤")
print(f"│  🧠 CONSCIOUS     {c['conscious']['active_items']:3d}/10  ({con_pct:5.1f}%)  │")
print(f"│     ↓ Perception                            │")
print(f"│  🌊 SUBCONSCIOUS  {c['subconscious']['active_items']:3d}/100 ({sub_pct:5.1f}%) │")
print(f"│     ↓ Abstraction                           │")
print(f"│  🌌 UNCONSCIOUS   {c['unconscious']['active_items']:3d}/1000 ({unc_pct:5.1f}%)│")
print(f"│     ↑ Insight                               │")
print(f"└─────────────────────────────────────────────┘")

print(f"\nTotal items re-fed through cascade: {total}")
print("All layers populated with proper flow")
print("=" * 70)
