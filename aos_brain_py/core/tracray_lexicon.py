# core/tracray_lexicon.py
"""
Tracray: Spatial lexicon mapping concepts to 3D coordinates.

Concepts live in 3D space. Thinking is wave motion through that space.
"""

from typing import List, Dict, Any, Tuple, Optional

TRACRAY_LEXICON = {
    "concepts": {
        # Sensory cortices
        "vision": {
            "words": ["see", "look", "image", "picture", "visual", "watch"],
            "route": "visual_cortex",
            "coord": (2, 2, 1),
            "relations": {"is_a": ["perception"], "part_of": ["sensory_system"]},
        },
        "auditory": {
            "words": ["hear", "listen", "sound", "audio", "noise", "music"],
            "route": "auditory_cortex",
            "coord": (3, 2, 1),
            "relations": {"is_a": ["perception"], "part_of": ["sensory_system"]},
        },
        
        # Memory systems
        "memory": {
            "words": ["remember", "recall", "forget", "memory", "past"],
            "route": "hippocampus",
            "coord": (5, 5, 2),
            "relations": {"is_a": ["cognition"]},
        },
        "learn": {
            "words": ["learn", "study", "understand", "know", "knowledge"],
            "route": "hippocampus",
            "coord": (6, 5, 2),
            "relations": {"is_a": ["cognition"], "requires": ["memory"]},
        },
        
        # Emotional/affective
        "emotion": {
            "words": ["feel", "emotion", "mood", "affect"],
            "route": "limbic",
            "coord": (8, 3, 1),
            "relations": {"is_a": ["affect"]},
        },
        "fear": {
            "words": ["afraid", "scared", "fear", "terror", "anxiety"],
            "route": "limbic",
            "coord": (8, 2, 1),
            "relations": {"is_a": ["emotion"], "valence": "negative"},
        },
        "joy": {
            "words": ["happy", "joy", "glad", "pleased", "delighted"],
            "route": "limbic",
            "coord": (8, 4, 1),
            "relations": {"is_a": ["emotion"], "valence": "positive"},
        },
        
        # Executive function
        "plan": {
            "words": ["plan", "decide", "choose", "goal", "strategy"],
            "route": "pfc",
            "coord": (9, 9, 3),
            "relations": {"is_a": ["cognition"], "requires": ["memory"]},
        },
        "analyze": {
            "words": ["analyze", "think", "reason", "consider", "evaluate"],
            "route": "pfc",
            "coord": (9, 8, 3),
            "relations": {"is_a": ["cognition"]},
        },
        
        # Language
        "speech": {
            "words": ["say", "speak", "tell", "explain", "describe"],
            "route": "broca",
            "coord": (7, 8, 2),
            "relations": {"is_a": ["language"]},
        },
        "comprehend": {
            "words": ["understand", "comprehend", "grasp", "parse"],
            "route": "wernicke",
            "coord": (7, 7, 2),
            "relations": {"is_a": ["language"]},
        },
        
        # Spatial relations
        "left": {
            "words": ["left", "west", "to the left of"],
            "route": "parietal",
            "coord": (1, 6, 2),
            "relations": {"type": "spatial_relation", "direction": (-1, 0, 0)},
        },
        "right": {
            "words": ["right", "east", "to the right of"],
            "route": "parietal",
            "coord": (11, 6, 2),
            "relations": {"type": "spatial_relation", "direction": (1, 0, 0)},
        },
        "up": {
            "words": ["up", "above", "over", "north"],
            "route": "parietal",
            "coord": (6, 11, 3),
            "relations": {"type": "spatial_relation", "direction": (0, 1, 1)},
        },
        "down": {
            "words": ["down", "below", "under", "south"],
            "route": "parietal",
            "coord": (6, 1, 1),
            "relations": {"type": "spatial_relation", "direction": (0, -1, -1)},
        },
        
        # Distance/scale
        "near": {
            "words": ["close", "near", "adjacent", "beside"],
            "route": "parietal",
            "coord": (4, 4, 1),
            "relations": {"type": "distance", "scale": "small"},
        },
        "far": {
            "words": ["far", "distant", "remote", "away"],
            "route": "parietal",
            "coord": (8, 8, 1),
            "relations": {"type": "distance", "scale": "large"},
        },
        
        # Entities
        "agent": {
            "words": ["i", "me", "you", "they", "person", "human"],
            "route": "wernicke",
            "coord": (5, 7, 2),
            "relations": {"type": "entity", "is_a": ["animate"]},
        },
        "object": {
            "words": ["thing", "object", "item", "stuff"],
            "route": "parietal",
            "coord": (5, 6, 2),
            "relations": {"type": "entity", "is_a": ["inanimate"]},
        },
        
        # Actions
        "move": {
            "words": ["move", "go", "walk", "run", "travel"],
            "route": "pfc",
            "coord": (7, 9, 3),
            "relations": {"type": "action", "requires": ["agent"]},
        },
        "create": {
            "words": ["create", "make", "build", "construct"],
            "route": "pfc",
            "coord": (9, 10, 3),
            "relations": {"type": "action", "requires": ["agent"]},
        },
        "destroy": {
            "words": ["destroy", "break", "remove", "delete"],
            "route": "limbic",
            "coord": (8, 10, 2),
            "relations": {"type": "action", "valence": "negative"},
        },
    },
    
    # Simple grammar for parsing
    "grammar": {
        "S": ["NP VP"],
        "NP": ["Det N", "N", "Det Adj N"],
        "VP": ["V", "V NP", "V PP"],
        "PP": ["P NP"],
        "Det": ["the", "a", "an", "this", "that"],
        "Adj": ["big", "small", "happy", "sad", "red", "blue"],
        "N": ["agent", "object", "memory", "plan", "emotion"],
        "V": ["move", "create", "see", "hear", "remember", "plan"],
        "P": ["to", "from", "with", "above", "below", "left", "right"],
    },
}


def tracray_lookup(text: str) -> List[Dict[str, Any]]:
    """
    Look up concepts in Tracray lexicon.
    
    Returns list of matched concepts with their spatial coordinates.
    """
    text_lower = text.lower()
    hits = []
    
    for concept, spec in TRACRAY_LEXICON["concepts"].items():
        for word in spec["words"]:
            if word in text_lower:
                hits.append({
                    "concept": concept,
                    "coord": spec["coord"],
                    "route": spec["route"],
                    "relations": spec.get("relations", {}),
                })
                break  # Found one word for this concept, move to next
    
    return hits


def tracray_lookup_single(text: str) -> Optional[Dict[str, Any]]:
    """Return the best matching concept (first match)."""
    hits = tracray_lookup(text)
    return hits[0] if hits else None


def get_concept_coord(concept: str) -> Optional[Tuple[int, int, int]]:
    """Get the 3D coordinate for a specific concept."""
    spec = TRACRAY_LEXICON["concepts"].get(concept)
    return spec["coord"] if spec else None


def get_route_for_concept(concept: str) -> Optional[str]]:
    """Get which brain route a concept maps to."""
    spec = TRACRAY_LEXICON["concepts"].get(concept)
    return spec["route"] if spec else None


def list_all_concepts() -> List[str]:
    """List all available concepts in the lexicon."""
    return list(TRACRAY_LEXICON["concepts"].keys())
