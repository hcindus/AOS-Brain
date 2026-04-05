"""
Minecraft Observer Module
Reads world state and converts to brain concepts.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class WorldObservation:
    """Snapshot of Minecraft world state"""
    # Spatial
    x: float
    y: float
    z: float
    yaw: float
    pitch: float
    
    # Blocks around player (3x3x3)
    nearby_blocks: Dict[str, str]  # "dx,dy,dz" -> block_type
    
    # Entities
    nearby_entities: List[Dict]  # [{"type": "zombie", "distance": 5.2}, ...]
    
    # Player state
    health: float
    hunger: float
    inventory: Dict[str, int]  # item -> count
    
    # Environment
    biome: str
    time_of_day: int  # 0-24000
    light_level: int
    
    # Recent events
    events: List[Dict]  # [{"type": "damage", "source": "zombie", "amount": 2.0}, ...]
    
    # Biome/atmosphere
    is_raining: bool
    is_underground: bool


class MinecraftObserver:
    """
    Observes Minecraft world and converts to concepts.
    
    Connects to Minecraft via:
    - RCON (remote console)
    - Data packs
    - Or reads from log files / API
    """
    
    def __init__(self, connection_type: str = "file"):
        self.connection_type = connection_type
        self.last_observation = None
        
        # Block type → concept mapping
        self.block_concepts = {
            # Resources
            "oak_log": "wood",
            "birch_log": "wood",
            "spruce_log": "wood",
            "stone": "stone",
            "coal_ore": "coal",
            "iron_ore": "iron",
            "gold_ore": "gold",
            "diamond_ore": "diamond",
            
            # Tools
            "crafting_table": "craft",
            "furnace": "smelt",
            "chest": "storage",
            
            # Danger
            "lava": "danger",
            "fire": "danger",
            "cactus": "pain",
            
            # Food
            "wheat": "food",
            "potatoes": "food",
            "carrots": "food",
            
            # Environment
            "water": "water",
            "grass_block": "ground",
            "dirt": "ground",
            "sand": "ground",
            "bedrock": "deep",
        }
        
        # Entity → concept mapping
        self.entity_concepts = {
            # Dangerous
            "zombie": "danger",
            "skeleton": "danger",
            "creeper": "danger",
            "spider": "danger",
            "witch": "danger",
            
            # Neutral
            "cow": "food",
            "pig": "food",
            "chicken": "food",
            "sheep": "wool",
            
            # Friendly
            "villager": "trade",
            "wandering_trader": "trade",
            
            # Rare
            "diamond": "treasure",
            "emerald": "treasure",
        }
        
    def observe(self) -> Optional[WorldObservation]:
        """
        Get current world observation.
        
        Returns:
            WorldObservation or None if no data
        """
        # In real implementation, this would:
        # - Query Minecraft server via RCON
        # - Read from data pack output
        # - Parse log files
        # - Connect to mod API
        
        # For now, return mock observation
        return self._get_mock_observation()
        
    def _get_mock_observation(self) -> WorldObservation:
        """Generate mock observation for testing"""
        return WorldObservation(
            x=100.5,
            y=64.0,
            z=200.3,
            yaw=45.0,
            pitch=0.0,
            nearby_blocks={
                "0,0,0": "grass_block",
                "0,1,0": "oak_log",
                "1,0,0": "stone",
                "-1,0,0": "dirt",
                "0,0,1": "coal_ore",
            },
            nearby_entities=[
                {"type": "cow", "distance": 5.2},
                {"type": "zombie", "distance": 12.5},
            ],
            health=18.5,
            hunger=16.0,
            inventory={
                "wood": 12,
                "cobblestone": 8,
                "coal": 4,
            },
            biome="forest",
            time_of_day=8000,
            light_level=12,
            events=[
                {"type": "step", "block": "grass"},
            ],
            is_raining=False,
            is_underground=False,
        )
        
    def to_concepts(self, observation: WorldObservation) -> Dict:
        """
        Convert observation to brain concepts.
        
        Returns:
            Dict with:
            - concepts: List of active concept names
            - valence: Emotional valence (-1 to 1)
            - threat: Threat level (0 to 1)
            - novelty: Novelty level (0 to 1)
        """
        concepts = []
        
        # Block concepts
        for block in observation.nearby_blocks.values():
            if block in self.block_concepts:
                concepts.append(self.block_concepts[block])
                
        # Entity concepts
        for entity in observation.nearby_entities:
            entity_type = entity.get("type", "")
            if entity_type in self.entity_concepts:
                concepts.append(self.entity_concepts[entity_type])
                
        # Biome concept
        concepts.append(observation.biome)
        
        # Time concept
        if observation.time_of_day < 12000:
            concepts.append("day")
        else:
            concepts.append("night")
            
        # Environment
        if observation.is_underground:
            concepts.append("cave")
        if observation.is_raining:
            concepts.append("rain")
            
        # State concepts
        if observation.health < 10:
            concepts.append("danger")  # Low health
        if observation.hunger < 6:
            concepts.append("hungry")
        if observation.inventory.get("wood", 0) > 10:
            concepts.append("prepared")
            
        # Calculate valence from state
        valence = 0.0
        if observation.health > 15:
            valence += 0.3
        if observation.hunger > 15:
            valence += 0.2
        if any(c == "danger" for c in concepts):
            valence -= 0.5
        if any(c == "treasure" for c in concepts):
            valence += 0.8
            
        # Calculate threat
        threat = 0.0
        for entity in observation.nearby_entities:
            if entity.get("type") in ["zombie", "skeleton", "creeper", "spider"]:
                dist = entity.get("distance", 100)
                if dist < 10:
                    threat += 0.5
                    
        # Calculate novelty (simplified)
        novelty = 0.3  # Base novelty
        if "cave" in concepts:
            novelty += 0.3
        if len(set(concepts)) > 5:
            novelty += 0.2
            
        return {
            "concepts": list(set(concepts)),
            "valence": max(-1.0, min(1.0, valence)),
            "threat": min(1.0, threat),
            "novelty": min(1.0, novelty),
            "position": (observation.x, observation.y, observation.z),
        }
        
    def get_reward_signal(self, observation: WorldObservation) -> Dict:
        """
        Generate reward signal for brain.
        
        Returns:
            Dict with dopamine, serotonin, acetylcholine, norepinephrine
        """
        concepts_data = self.to_concepts(observation)
        
        # Dopamine: reward + novelty
        dopamine = concepts_data["valence"] * 0.5 + concepts_data["novelty"] * 0.3
        
        # Serotonin: calm vs anxious
        serotonin = 0.5 - concepts_data["threat"] * 0.5
        if observation.health > 15:
            serotonin += 0.2
            
        # Acetylcholine: attention to novelty
        acetylcholine = concepts_data["novelty"] * 0.8
        
        # Norepinephrine: alertness
        norepinephrine = concepts_data["threat"] * 0.8
        if "danger" in concepts_data["concepts"]:
            norepinephrine += 0.3
            
        return {
            "dopamine": max(-1.0, min(1.0, dopamine)),
            "serotonin": max(-1.0, min(1.0, serotonin)),
            "acetylcholine": max(-1.0, min(1.0, acetylcholine)),
            "norepinephrine": max(-1.0, min(1.0, norepinephrine)),
        }


if __name__ == "__main__":
    print("Minecraft Observer Module")
    print("=" * 50)
    
    observer = MinecraftObserver()
    
    # Get observation
    obs = observer.observe()
    print("\nWorld Observation:")
    print(f"  Position: ({obs.x}, {obs.y}, {obs.z})")
    print(f"  Biome: {obs.biome}")
    print(f"  Health: {obs.health}/20")
    print(f"  Nearby blocks: {list(obs.nearby_blocks.values())}")
    print(f"  Nearby entities: {[e['type'] for e in obs.nearby_entities]}")
    
    # Convert to concepts
    concepts = observer.to_concepts(obs)
    print("\nBrain Concepts:")
    print(f"  Active: {concepts['concepts']}")
    print(f"  Valence: {concepts['valence']:+.2f}")
    print(f"  Threat: {concepts['threat']:.2f}")
    print(f"  Novelty: {concepts['novelty']:.2f}")
    
    # Get reward
    reward = observer.get_reward_signal(obs)
    print("\nNeurochemical Reward:")
    for chem, val in reward.items():
        print(f"  {chem}: {val:+.2f}")
        
    print("\n" + "=" * 50)
    print("Observer ready")
