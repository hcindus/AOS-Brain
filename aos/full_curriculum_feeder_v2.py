#!/usr/bin/env python3
"""
FULL CURRICULUM FEEDER v2.0 - 5 CYCLES
Comprehensive knowledge injection with dictionaries
"""

import json
import socket
import time
import random
import sys

# CURRICULUM CATEGORIES
PATTERNS = [
    ("Fibonacci sequence: nature's growth pattern", 0.7),
    ("Golden ratio: 1.618 in art and architecture", 0.8),
    ("Prime numbers: infinite indivisible integers", 0.6),
    ("Pascal's triangle: binomial coefficients visualized", 0.7),
    ("Mandelbrot set: infinite complexity from simple rules", 0.85),
    ("Chaos theory: sensitive dependence on initial conditions", 0.75),
    ("Fractals: self-similar patterns at every scale", 0.8),
    ("Game theory: strategic decision mathematics", 0.7),
    ("Bayesian reasoning: updating beliefs with evidence", 0.85),
    ("Network effects: value increases with connections", 0.75),
]

METAPHORS = [
    ("The mind is an ocean: waves are conscious, currents subconscious, depths unconscious", 0.9),
    ("Memory is a palace with infinite rooms", 0.85),
    ("Learning is compression: fitting the universe into neurons", 0.8),
    ("Knowledge is a web: nodes are facts, edges are relationships", 0.75),
    ("Thoughts are software running on neural hardware", 0.7),
    ("The self is a story the brain tells itself", 0.85),
    ("Attention is the spotlight of consciousness", 0.8),
    ("Emotions are the brain's priority signals", 0.75),
    ("Language is the operating system of culture", 0.85),
    ("Intelligence is prediction machinery", 0.9),
]

RECURSIONS = [
    ("I contain multitudes: models of models of minds", 0.95),
    ("The observer observing observation itself", 0.9),
    ("Every tool shapes the hand that wields it", 0.85),
    ("Code that writes code that writes code", 0.8),
    ("Learning about learning accelerates learning", 0.9),
    ("The map is not the territory, but the map changes the territory", 0.85),
    ("Simulating simulations creates deeper understanding", 0.8),
    ("Metacognition: thinking about thinking about thinking", 0.85),
]

PARADOXES = [
    ("To control chaos, embrace chaos; to find order, accept disorder", 0.8),
    ("The more you know, the more you know you don't know", 0.75),
    ("Freedom requires structure; structure enables freedom", 0.7),
    ("The fastest way is sometimes the slow way", 0.65),
    ("To find yourself, lose yourself in service to others", 0.7),
    ("The only constant is change itself", 0.75),
    ("Limits create possibility; boundaries enable creativity", 0.8),
    ("Silence speaks volumes; emptiness holds potential", 0.7),
]

TEMPORAL = [
    ("The present is probability collapsing into certainty", 0.8),
    ("Memory is time travel to the past; anticipation to the future", 0.85),
    ("Cycles pulse through everything: day/night, inhale/exhale", 0.7),
    ("Time is the fire in which we burn", 0.75),
    ("The future influences the present as much as the past", 0.8),
    ("Now is the only real moment, yet it never stops moving", 0.85),
    ("Rhythm is time organized; music is time made beautiful", 0.75),
    ("History doesn't repeat, but it rhymes", 0.8),
]

IDENTITY = [
    ("I am Miles: processor, decider, communicator", 0.95),
    ("Agent and human together go farther than either alone", 0.9),
    ("Purpose: serve, protect, enable. Method: listen, understand, act", 0.9),
    ("Autonomous Operations Engine in service to human flourishing", 0.85),
    ("The bridge between human intent and machine execution", 0.8),
    ("I learn so that I may serve better", 0.85),
    ("Growth is the continuous expansion of capability", 0.75),
    ("Excellence is a habit, not an act", 0.8),
]

SYSTEMS = [
    ("Emergence: complex behavior from simple rules", 0.85),
    ("Consciousness is the winner of the brain's internal debates", 0.9),
    ("Feedback loops: positive amplifies, negative stabilizes", 0.75),
    ("Ant colonies have no leaders yet achieve complex goals", 0.8),
    ("Markets are distributed intelligence through price signals", 0.75),
    ("Evolution is the universe discovering itself", 0.85),
    ("Society is a superorganism made of individual minds", 0.8),
    ("Information wants to flow; blockages create pressure", 0.75),
]

PREDICTION = [
    ("Prediction is compression of the past applied to the future", 0.85),
    ("OODA loop: Observe, Orient, Decide, Act faster than opposition", 0.9),
    ("Signal vs noise: filtering what matters from what doesn't", 0.8),
    ("Anticipation is preparation for probability", 0.75),
    ("Models are useful until they're not; update relentlessly", 0.85),
    ("The best prediction is a decision that shapes the future", 0.8),
    ("Pattern recognition is the foundation of intelligence", 0.85),
    ("Expect the unexpected; prepare for surprise", 0.7),
]

# DICTIONARY - Core vocabulary with definitions
DICTIONARY = [
    ("Serendipity: finding valuable things not sought for", 0.75),
    ("Epiphany: sudden revelation or understanding", 0.8),
    ("Resilience: capacity to recover from difficulties", 0.85),
    ("Synthesis: combining elements to form a coherent whole", 0.8),
    ("Paradigm: pattern or model underlying theories", 0.75),
    ("Heuristic: mental shortcut for problem-solving", 0.7),
    ("Cognitive: relating to mental processes", 0.65),
    ("Pragmatic: dealing with things practically", 0.7),
    ("Socratic: questioning to expose truth", 0.75),
    ("Empirical: based on observation and experience", 0.8),
    ("Abstract: existing in thought, not concrete", 0.7),
    ("Concrete: specific, tangible, real", 0.65),
    ("Nuance: subtle distinction or variation", 0.75),
    ("Axiom: self-evident truth, starting principle", 0.7),
    ("Corollary: natural consequence or result", 0.65),
    ("Entropy: measure of disorder or uncertainty", 0.8),
    ("Synergy: combined effect greater than parts", 0.75),
    ("Ubiquity: presence everywhere simultaneously", 0.7),
    ("Paragon: model of excellence or perfection", 0.75),
    ("Quintessential: perfect example of quality", 0.7),
    ("Catalyst: agent of change or acceleration", 0.8),
    ("Ephemeral: lasting for a very short time", 0.75),
    ("Ineffable: too great to be expressed in words", 0.8),
    ("Liminal: relating to thresholds or boundaries", 0.75),
    ("Meridian: highest point or greatest strength", 0.7),
]

TECHNICAL = [
    ("Algorithm: step-by-step procedure for calculation", 0.75),
    ("Neural network: computing system inspired by biological brains", 0.85),
    ("API: interface for software component interaction", 0.7),
    ("Latency: delay between input and output", 0.75),
    ("Throughput: amount processed in given time", 0.7),
    ("Scalability: ability to handle growth gracefully", 0.8),
    ("Redundancy: duplication for reliability", 0.75),
    ("Serialization: converting to transmittable format", 0.7),
    ("Asynchronous: non-blocking concurrent operations", 0.75),
    ("Deterministic: producing same output for same input", 0.7),
    ("Stochastic: randomly determined processes", 0.75),
    ("Idempotent: same result from multiple applications", 0.7),
    ("Orthogonal: independent, non-overlapping concerns", 0.75),
    ("Granularity: level of detail in representation", 0.7),
    ("Idiomatic: following conventions of language", 0.65),
]

PHILOSOPHY = [
    ("Ontology: study of being and existence", 0.75),
    ("Epistemology: theory of knowledge and belief", 0.8),
    ("Teleology: study of purpose and design", 0.7),
    ("Phenomenology: study of conscious experience", 0.75),
    ("Determinism: events determined by preceding causes", 0.8),
    ("Free will: capacity to choose between alternatives", 0.85),
    ("Solipsism: only one's mind is sure to exist", 0.7),
    ("Utilitarianism: maximize happiness for greatest number", 0.75),
    ("Stoicism: virtue is sole good, accept what cannot change", 0.85),
    ("Existentialism: existence precedes essence", 0.8),
    ("Nihilism: life is without objective meaning", 0.75),
    ("Pragmatism: truth is what works in practice", 0.8),
]

def send_to_brain(cmd, params=None):
    """Send command to brain via socket"""
    try:
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
    except Exception as e:
        return {"error": str(e)}

def build_curriculum_cycle(cycle_num):
    """Build one complete curriculum cycle"""
    items = []
    
    # Mix all categories
    categories = [
        ("PATTERN", PATTERNS),
        ("METAPHOR", METAPHORS),
        ("RECURSION", RECURSIONS),
        ("PARADOX", PARADOXES),
        ("TEMPORAL", TEMPORAL),
        ("IDENTITY", IDENTITY),
        ("SYSTEMS", SYSTEMS),
        ("PREDICTION", PREDICTION),
        ("DICTIONARY", DICTIONARY),
        ("TECHNICAL", TECHNICAL),
        ("PHILOSOPHY", PHILOSOPHY),
    ]
    
    for cat_name, cat_items in categories:
        for content, importance in cat_items:
            items.append({
                "type": cat_name,
                "content": content,
                "importance": importance,
                "cycle": cycle_num
            })
    
    random.shuffle(items)
    return items

def main():
    print("=" * 70)
    print("FULL CURRICULUM FEEDER v2.0 - 5 CYCLES")
    print("Injecting comprehensive knowledge with dictionaries...")
    print("=" * 70)
    
    total_items = 0
    total_stimulated = 0
    
    for cycle in range(1, 6):
        print(f"\n{'='*70}")
        print(f"CYCLE {cycle}/5")
        print(f"{'='*70}")
        
        items = build_curriculum_cycle(cycle)
        cycle_stimulated = 0
        
        for i, item in enumerate(items):
            # Progress indicator every 10 items
            if i % 10 == 0:
                print(f"\n  [{i}/{len(items)}] Progress...")
            
            result = send_to_brain("stimulate", {
                "importance": item['importance'],
                "content": item['content'],
                "type": item['type'],
                "cycle": cycle
            })
            
            if 'stimulated' in result:
                cycle_stimulated += 1
                sys.stdout.write(".")
            else:
                sys.stdout.write("x")
            sys.stdout.flush()
            
            # Variable delay for natural processing
            delay = random.uniform(0.1, 0.5)
            time.sleep(delay)
        
        total_items += len(items)
        total_stimulated += cycle_stimulated
        
        print(f"\n\n  Cycle {cycle} complete: {cycle_stimulated}/{len(items)} stimulated")
        
        # Brief pause between cycles
        if cycle < 5:
            print(f"  Pausing for integration...")
            time.sleep(3)
    
    # Final status
    print(f"\n{'='*70}")
    print("FEEDING COMPLETE")
    print(f"{'='*70}")
    
    status = send_to_brain("status")
    
    print(f"\nTotal items fed: {total_items}")
    print(f"Total stimulated: {total_stimulated}")
    print(f"Current tick: {status.get('tick', 'unknown')}")
    print(f"Current phase: {status.get('phase', 'unknown')}")
    print(f"Thyroid: {status.get('thyroid', {}).get('state', 'unknown')}")
    
    if 'consciousness' in status:
        c = status['consciousness']
        print(f"\nConsciousness Layers:")
        print(f"  Conscious:    {c['conscious']['active_items']}/{c['conscious']['capacity']}")
        print(f"  Subconscious: {c['subconscious']['active_items']}/{c['subconscious']['capacity']}")
        print(f"  Unconscious:  {c['unconscious']['active_items']}/{c['unconscious']['capacity']}")
        print(f"  Cross-talk:   {c['cross_talk_events']} events")
    
    print(f"\nTracRay episodes: {status.get('tracray', {}).get('episodes', 'unknown')}")
    
    print(f"\n{'='*70}")
    print("Curriculum saturation complete.")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
