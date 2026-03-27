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
            "relations": {"is_a": ["emotion"], "triggers": ["amygdala"]},
        },
        "joy": {
            "words": ["happy", "joy", "delight", "pleasure", "glad"],
            "route": "limbic",
            "coord": (8, 4, 1),
            "relations": {"is_a": ["emotion"]},
        },
        
        # Motor/action
        "move": {
            "words": ["move", "go", "walk", "run", "travel"],
            "route": "motor_cortex",
            "coord": (4, 4, 2),
            "relations": {"is_a": ["action"]},
        },
        "act": {
            "words": ["act", "do", "perform", "execute"],
            "route": "motor_cortex",
            "coord": (4, 5, 2),
            "relations": {"is_a": ["action"]},
        },
        
        # Cognitive/higher functions
        "think": {
            "words": ["think", "consider", "ponder", "reflect"],
            "route": "prefrontal",
            "coord": (6, 6, 3),
            "relations": {"is_a": ["cognition"]},
        },
        "decide": {
            "words": ["decide", "choose", "select", "determine"],
            "route": "prefrontal",
            "coord": (7, 7, 3),
            "relations": {"is_a": ["cognition"], "requires": ["think"]},
        },
        "plan": {
            "words": ["plan", "design", "arrange", "prepare"],
            "route": "prefrontal",
            "coord": (7, 6, 3),
            "relations": {"is_a": ["cognition"]},
        },
        
        # Social concepts
        "communicate": {
            "words": ["speak", "talk", "say", "tell", "communicate"],
            "route": "language_areas",
            "coord": (3, 6, 2),
            "relations": {"is_a": ["social"]},
        },
        "social": {
            "words": ["people", "person", "human", "society", "community"],
            "route": "social_cognition",
            "coord": (6, 3, 2),
            "relations": {"is_a": ["concept"]},
        },
        
        # Abstract
        "time": {
            "words": ["time", "moment", "second", "minute", "hour"],
            "route": "abstract",
            "coord": (5, 7, 3),
            "relations": {"is_a": ["abstract"]},
        },
        "space": {
            "words": ["space", "place", "location", "position"],
            "route": "spatial",
            "coord": (4, 7, 2),
            "relations": {"is_a": ["abstract"]},
        },
        "self": {
            "words": ["I", "me", "myself", "self", "identity"],
            "route": "default_mode",
            "coord": (5, 4, 3),
            "relations": {"is_a": ["concept"]},
        },
        "world": {
            "words": ["world", "universe", "reality", "existence"],
            "route": "abstract",
            "coord": (5, 5, 4),
            "relations": {"is_a": ["abstract"]},
        },
        
        # Sensory processing
        "touch": {
            "words": ["touch", "feel", "tactile", "physical"],
            "route": "somatosensory",
            "coord": (2, 3, 1),
            "relations": {"is_a": ["perception"]},
        },
        "smell": {
            "words": ["smell", "odor", "scent", "aroma"],
            "route": "olfactory",
            "coord": (2, 4, 1),
            "relations": {"is_a": ["perception"]},
        },
        "taste": {
            "words": ["taste", "flavor", "savor"],
            "route": "gustatory",
            "coord": (2, 5, 1),
            "relations": {"is_a": ["perception"]},
        },
    }
}


class TracrayLexicon:
    """
    Wrapper class for Tracray spatial lexicon.
    
    Maps natural language concepts to 3D cortical coordinates
    for wave-based thinking.
    """
    
    def __init__(self):
        self.lexicon = TRACRAY_LEXICON
        self._build_word_index()
    
    def _build_word_index(self):
        """Build reverse index from words to concepts."""
        self.word_to_concept = {}
        for concept_name, concept_data in self.lexicon["concepts"].items():
            for word in concept_data.get("words", []):
                self.word_to_concept[word.lower()] = concept_name
    
    def lookup(self, word: str) -> Optional[Dict]:
        """
        Look up a word in the lexicon.
        
        Returns concept data with route and coordinates, or None if not found.
        """
        word_lower = word.lower()
        
        # Direct concept lookup
        if word_lower in self.lexicon["concepts"]:
            return self.lexicon["concepts"][word_lower]
        
        # Word-to-concept lookup
        if word_lower in self.word_to_concept:
            concept_name = self.word_to_concept[word_lower]
            return self.lexicon["concepts"][concept_name]
        
        return None
    
    def get_route(self, word: str) -> Optional[str]:
        """Get brain route for a word."""
        concept = self.lookup(word)
        return concept["route"] if concept else None
    
    def get_coord(self, word: str) -> Optional[Tuple[int, int, int]]:
        """Get 3D coordinate for a word."""
        concept = self.lookup(word)
        return concept["coord"] if concept else None
    
    def get_related(self, word: str, relation_type: str = "is_a") -> List[str]:
        """Get related concepts."""
        concept = self.lookup(word)
        if concept and "relations" in concept:
            return concept["relations"].get(relation_type, [])
        return []
    
    def match_text(self, text: str) -> List[Dict]:
        """
        Find all Tracray concepts in a text.
        
        Returns list of matched concepts with positions.
        """
        text_lower = text.lower()
        matches = []
        
        for word, concept_name in self.word_to_concept.items():
            if word in text_lower:
                concept = self.lexicon["concepts"][concept_name]
                matches.append({
                    "word": word,
                    "concept": concept_name,
                    "route": concept["route"],
                    "coord": concept["coord"],
                })
        
        return matches
    
    def get_all_concepts(self) -> List[str]:
        """Get all concept names."""
        return list(self.lexicon["concepts"].keys())
    
    def get_all_routes(self) -> List[str]:
        """Get all unique brain routes."""
        routes = set()
        for concept in self.lexicon["concepts"].values():
            routes.add(concept["route"])
        return sorted(list(routes))


# Helper functions
def get_route_for_concept(concept: str) -> Optional[str]:
    """Get which brain route a concept maps to."""
    spec = TRACRAY_LEXICON["concepts"].get(concept)
    return spec["route"] if spec else None


def get_coord_for_concept(concept: str) -> Optional[Tuple[int, int, int]]:
    """Get 3D coordinate for a concept."""
    spec = TRACRAY_LEXICON["concepts"].get(concept)
    return spec["coord"] if spec else None


def list_all_concepts() -> List[str]:
    """List all concepts in the lexicon."""
    return list(TRACRAY_LEXICON["concepts"].keys())
