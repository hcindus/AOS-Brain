"""
Concept Translator
Translates between Minecraft world and brain concepts.
"""

from typing import Dict, List, Set


class ConceptTranslator:
    """
    Bidirectional translation:
    - Minecraft blocks/entities/events → brain concepts
    - Brain concepts → Minecraft actions
    """
    
    # Block types → concepts
    BLOCK_MAP = {
        # Wood types
        "oak_log": "wood",
        "spruce_log": "wood", 
        "birch_log": "wood",
        "jungle_log": "wood",
        "acacia_log": "wood",
        "dark_oak_log": "wood",
        
        # Stone types
        "stone": "stone",
        "cobblestone": "stone",
        "smooth_stone": "stone",
        
        # Ores
        "coal_ore": "coal",
        "iron_ore": "iron",
        "gold_ore": "gold",
        "diamond_ore": "diamond",
        "redstone_ore": "redstone",
        "lapis_ore": "lapis",
        
        # Plants
        "grass_block": "ground",
        "dirt": "ground",
        "sand": "ground",
        "gravel": "ground",
        
        # Crops
        "wheat": "food",
        "potatoes": "food",
        "carrots": "food",
        "beetroots": "food",
        "melon": "food",
        "pumpkin": "food",
        
        # Water
        "water": "water",
        "water_bucket": "water",
        
        # Danger
        "lava": "lava",
        "lava_bucket": "lava",
        "fire": "fire",
        "soul_fire": "fire",
        "cactus": "danger",
        "sweet_berry_bush": "danger",
        
        # Tools/Blocks
        "crafting_table": "craft",
        "furnace": "smelt",
        "blast_furnace": "smelt",
        "smoker": "cook",
        "chest": "storage",
        "barrel": "storage",
        
        # Building
        "bricks": "build",
        "planks": "build",
        "glass": "build",
        "torch": "light",
        
        # Beds
        "white_bed": "sleep",
        "red_bed": "sleep",
        "blue_bed": "sleep",
        # ... (all bed colors)
    }
    
    # Entities → concepts
    ENTITY_MAP = {
        # Hostile
        "zombie": "danger",
        "skeleton": "danger",
        "creeper": "danger",
        "spider": "danger",
        "cave_spider": "danger",
        "witch": "danger",
        "phantom": "danger",
        "drowned": "danger",
        "husk": "danger",
        "stray": "danger",
        
        # Neutral
        "enderman": "strange",
        "piglin": "trade",
        "zombified_piglin": "danger",
        "bee": "resource",
        "wolf": "ally",
        "fox": "wild",
        
        # Passive/Food
        "cow": "food",
        "pig": "food",
        "chicken": "food",
        "sheep": "wool",
        "rabbit": "food",
        "salmon": "food",
        "cod": "food",
        "pufferfish": "danger_food",
        
        # Villagers
        "villager": "trade",
        "wandering_trader": "trade",
        "iron_golem": "protector",
        
        # Other
        "player": "other_player",
        "bat": "harmless",
        "squid": "ocean",
        "dolphin": "ocean_friend",
    }
    
    # Biomes → concepts
    BIOME_MAP = {
        "forest": "forest",
        "birch_forest": "forest",
        "dark_forest": "forest",
        "flower_forest": "forest",
        
        "plains": "plains",
        "sunflower_plains": "plains",
        
        "desert": "desert",
        "beach": "beach",
        "ocean": "ocean",
        "deep_ocean": "ocean",
        "river": "river",
        
        "jungle": "jungle",
        "bamboo_jungle": "jungle",
        
        "taiga": "cold_forest",
        "snowy_taiga": "cold_forest",
        
        "savanna": "savanna",
        "savanna_plateau": "savanna",
        
        "badlands": "badlands",
        "eroded_badlands": "badlands",
        "wooded_badlands": "badlands",
        
        "mountains": "mountains",
        "snowy_slopes": "mountains",
        "jagged_peaks": "mountains",
        
        "swamp": "swamp",
        "mangrove_swamp": "swamp",
        
        "mushroom_fields": "rare_biome",
        "ice_spikes": "rare_biome",
    }
    
    # Events → concepts
    EVENT_MAP = {
        # Combat
        "took_damage": "pain",
        "killed_mob": "victory",
        "player_death": "death",
        
        # Discovery
        "found_ore": "discovery",
        "found_dungeon": "discovery",
        "found_village": "discovery",
        "found_temple": "discovery",
        
        # Survival
        "ate_food": "satiation",
        "starving": "hunger",
        "slept": "rest",
        "used_bed": "sleep_trigger",
        
        # Crafting
        "crafted_item": "creation",
        "smelted_ore": "creation",
        "enchanted_item": "power",
        
        # Building
        "placed_block": "build",
        "broke_block": "gather",
        
        # Trading
        "traded": "commerce",
        "found_trade": "opportunity",
        
        # Exploration
        "entered_new_biome": "exploration",
        "found_new_dimension": "dimension",
    }
    
    # Time → concepts
    TIME_CONCEPTS = {
        "day": (0, 12000),
        "sunset": (12000, 13000),
        "night": (13000, 23000),
        "sunrise": (23000, 24000),
    }
    
    def __init__(self):
        self.seen_concepts = set()
        self.novelty_tracker = {}
        
    def translate_observation(self, obs: Dict) -> List[str]:
        """
        Translate Minecraft observation to brain concepts.
        
        Args:
            obs: Dict with blocks, entities, biome, events, player state
            
        Returns:
            List of concept names
        """
        concepts = set()
        
        # Block concepts
        for block in obs.get("blocks", []):
            block_id = block.get("id", "")
            if block_id in self.BLOCK_MAP:
                concepts.add(self.BLOCK_MAP[block_id])
                
        # Entity concepts
        for entity in obs.get("entities", []):
            entity_id = entity.get("id", "")
            if entity_id in self.ENTITY_MAP:
                concepts.add(self.ENTITY_MAP[entity_id])
                
        # Biome concept
        biome = obs.get("biome", "")
        if biome in self.BIOME_MAP:
            concepts.add(self.BIOME_MAP[biome])
            
        # Event concepts
        for event in obs.get("events", []):
            if event in self.EVENT_MAP:
                concepts.add(self.EVENT_MAP[event])
                
        # Player state concepts
        player = obs.get("player", {})
        if player.get("health", 20) < 10:
            concepts.add("low_health")
        if player.get("hunger", 20) < 8:
            concepts.add("hunger")
        if player.get("time_of_day") == "night":
            concepts.add("night")
        if player.get("inventory_size", 0) > 20:
            concepts.add("inventory_full")
            
        # Track seen concepts
        for c in concepts:
            self.seen_concepts.add(c)
            self.novelty_tracker[c] = self.novelty_tracker.get(c, 0) + 1
            
        return list(concepts)
        
    def compute_novelty(self, concepts: List[str]) -> float:
        """Compute novelty score for current concepts"""
        if not concepts:
            return 0.0
            
        novelty_sum = 0.0
        for c in concepts:
            # Less seen = more novel
            times_seen = self.novelty_tracker.get(c, 0)
            novelty_sum += 1.0 / (1 + times_seen * 0.1)
            
        return novelty_sum / len(concepts)
        
    def calculate_valence(self, obs: Dict, concepts: List[str]) -> float:
        """Calculate emotional valence from observation"""
        valence = 0.0
        
        # Player state
        player = obs.get("player", {})
        health_pct = player.get("health", 20) / 20.0
        hunger_pct = player.get("hunger", 20) / 20.0
        
        valence += (health_pct - 0.5) * 0.4
        valence += (hunger_pct - 0.5) * 0.3
        
        # Concepts
        positive = {"discovery", "victory", "satiation", "rest", "creation", "commerce", "exploration"}
        negative = {"pain", "hunger", "death", "danger"}
        
        for c in concepts:
            if c in positive:
                valence += 0.3
            if c in negative:
                valence -= 0.4
                
        return max(-1.0, min(1.0, valence))
        
    def calculate_threat(self, obs: Dict, concepts: List[str]) -> float:
        """Calculate threat level"""
        threat = 0.0
        
        # Health threat
        player = obs.get("player", {})
        if player.get("health", 20) < 5:
            threat += 0.5
        elif player.get("health", 20) < 10:
            threat += 0.3
            
        # Entity threat
        for entity in obs.get("entities", []):
            entity_id = entity.get("id", "")
            distance = entity.get("distance", 100)
            
            if entity_id in ["zombie", "skeleton", "creeper", "spider"]:
                if distance < 5:
                    threat += 0.4
                elif distance < 15:
                    threat += 0.2
                    
        # Concept threat
        for c in concepts:
            if c == "danger":
                threat += 0.3
            if c == "lava":
                threat += 0.4
            if c == "low_health":
                threat += 0.3
                
        return min(1.0, threat)


if __name__ == "__main__":
    print("Concept Translator")
    print("=" * 50)
    
    translator = ConceptTranslator()
    
    # Test observation
    test_obs = {
        "blocks": [
            {"id": "oak_log", "rel_pos": [0, -1, 0]},
            {"id": "stone", "rel_pos": [1, 0, 0]},
            {"id": "coal_ore", "rel_pos": [0, 1, 0]},
        ],
        "entities": [
            {"id": "zombie", "rel_pos": [5, 0, 3], "distance": 5},
            {"id": "cow", "rel_pos": [-10, 0, 5], "distance": 12},
        ],
        "biome": "forest",
        "events": ["found_ore"],
        "player": {
            "health": 15,
            "hunger": 12,
            "pos": [100, 64, 200],
            "time_of_day": "day",
        },
    }
    
    concepts = translator.translate_observation(test_obs)
    print(f"\nTest Observation:")
    print(f"  Concepts: {concepts}")
    print(f"  Novelty: {translator.compute_novelty(concepts):.2f}")
    print(f"  Valence: {translator.calculate_valence(test_obs, concepts):+.2f}")
    print(f"  Threat: {translator.calculate_threat(test_obs, concepts):.2f}")
    
    print("\n" + "=" * 50)
    print("Translator ready")
