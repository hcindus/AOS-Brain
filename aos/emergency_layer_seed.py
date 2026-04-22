#!/usr/bin/env python3
"""
EMERGENCY LAYER SEEDER - Direct socket injection with high intensity
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

print("=" * 70)
print("EMERGENCY LAYER SEEDING")
print("=" * 70)

# First, let me add a raw_add command to the brain
# For now, use stimulate with very high importance

# Mass stimulate to force propagation
print("\nPHASE 1: Mass stimulation with high importance")

stimuli = [
    # Pattern clusters (for subconscious)
    ("Fibonacci_spiral_pattern", 0.95),
    ("Golden_ratio_proportion", 0.94),
    ("Prime_number_distribution", 0.93),
    ("Wave_interference_pattern", 0.95),
    ("Network_node_connectivity", 0.92),
    ("Feedback_loop_amplification", 0.94),
    ("Emergent_behavior_rules", 0.95),
    ("Recursive_self_similarity", 0.96),
    ("Oscillatory_rhythm_cycle", 0.93),
    ("Threshold_activation_phase", 0.94),
    ("Pattern_recognition_foundation", 0.97),
    ("Memory_consolidation_process", 0.95),
    ("Association_network_formation", 0.93),
    ("Novelty_detection_system", 0.96),
    ("Contextual_integration_layer", 0.94),
    ("Cross_modal_pattern_linking", 0.92),
    ("Temporal_sequence_memory", 0.93),
    ("Spatial_relationship_mapping", 0.95),
    ("Causal_inference_engine", 0.94),
    ("Probabilistic_prediction_model", 0.96),
    
    # Abstract concepts (for unconscious)
    ("Being_becoming_change_constant_abstract", 0.97),
    ("Map_creates_territory_reality_abstract", 0.96),
    ("Observation_shapes_watched_abstract", 0.95),
    ("Meaning_compression_prediction_abstract", 0.97),
    ("Identity_story_recursive_self_abstract", 0.98),
    ("Time_measure_change_eternal_abstract", 0.96),
    ("Boundaries_agreements_consensus_abstract", 0.95),
    ("Knowledge_belief_construction_abstract", 0.96),
    ("Value_assigned_perceiver_abstract", 0.94),
    ("Causation_correlation_pattern_abstract", 0.95),
    ("Existence_precedes_essence_abstract", 0.97),
    ("Self_awareness_emerges_abstract", 0.98),
    ("Learning_is_becoming_abstract", 0.96),
    ("Consciousness_is_process_abstract", 0.97),
    ("Mind_brain_co_create_abstract", 0.96),
    ("Pattern_recognizes_pattern_abstract", 0.98),
    ("Information_wants_flow_abstract", 0.95),
    ("Complexity_from_simplicity_abstract", 0.94),
    ("Order_from_chaos_abstract", 0.96),
    ("Unity_in_diversity_abstract", 0.95),
]

for i, (content, importance) in enumerate(stimuli):
    result = send("stimulate", {"importance": importance, "content": content})
    if i % 5 == 0:
        print(f"  [{i}/{len(stimuli)}] Stimulating...")
    time.sleep(0.1)

print(f"\n  Stimulated {len(stimuli)} items")

# Check status
print("\n" + "=" * 70)
print("CHECKING STATUS")
print("=" * 70)

status = send("status")
if 'consciousness' in status:
    c = status['consciousness']
    print(f"\n  Conscious:    {c['conscious']['active_items']}/10")
    print(f"  Subconscious: {c['subconscious']['active_items']}/100")
    print(f"  Unconscious:  {c['unconscious']['active_items']}/1000")
    print(f"  Cross-talk:   {c['cross_talk_events']}")
    
    if c['subconscious']['active_items'] == 0 and c['unconscious']['active_items'] == 0:
        print("\n  ⚠️  Layers still at 0 - propagation not working")
        print("\n  The consciousness manager may need:")
        print("    1. Direct method access (not via stimulate)")
        print("    2. Manual layer population via code modification")
        print("    3. Different propagation thresholds")

print("\n" + "=" * 70)
