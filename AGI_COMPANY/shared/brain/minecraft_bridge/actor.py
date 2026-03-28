"""
Minecraft Actor Module
Converts brain actions to Minecraft commands.
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
import time


class ActionType(Enum):
    """Types of actions the brain can take"""
    MOVE = "move"  # forward, back, left, right
    LOOK = "look"  # yaw, pitch
    JUMP = "jump"
    MINE = "mine"  # block at cursor
    PLACE = "place"  # place held block
    USE = "use"  # right-click
    ATTACK = "attack"  # left-click entity
    CRAFT = "craft"  # open crafting
    EAT = "eat"  # consume food
    SLEEP = "sleep"  # enter bed
    

class MinecraftActor:
    """
    Executes actions in Minecraft based on brain outputs.
    
    Converts brain intentions to Minecraft commands:
    - RCON commands
    - Data pack functions
    - Or key/mouse simulation
    """
    
    def __init__(self, connection_type: str = "mock"):
        self.connection_type = connection_type
        self.last_action = None
        self.action_cooldown = 0
        
        # Concept → action mapping
        self.concept_actions = {
            # Movement
            "forward": (ActionType.MOVE, {"direction": "forward"}),
            "back": (ActionType.MOVE, {"direction": "back"}),
            "left": (ActionType.MOVE, {"direction": "left"}),
            "right": (ActionType.MOVE, {"direction": "right"}),
            "jump": (ActionType.JUMP, {}),
            
            # Interaction
            "mine": (ActionType.MINE, {}),
            "place": (ActionType.PLACE, {}),
            "craft": (ActionType.CRAFT, {}),
            "eat": (ActionType.EAT, {}),
            "attack": (ActionType.ATTACK, {}),
            "sleep": (ActionType.SLEEP, {}),
            
            # Goals
            "explore": (ActionType.MOVE, {"direction": "forward", "duration": 10}),
            "flee": (ActionType.MOVE, {"direction": "back", "sprint": True}),
        }
        
    def execute(self, action: Dict) -> bool:
        """
        Execute an action in Minecraft.
        
        Args:
            action: Dict with 'type' and parameters
            
        Returns:
            True if executed, False otherwise
        """
        if self.action_cooldown > 0:
            self.action_cooldown -= 1
            return False
            
        action_type = action.get("type")
        params = action.get("params", {})
        
        # Execute based on type
        if action_type == ActionType.MOVE.value:
            return self._move(params)
        elif action_type == ActionType.LOOK.value:
            return self._look(params)
        elif action_type == ActionType.JUMP.value:
            return self._jump()
        elif action_type == ActionType.MINE.value:
            return self._mine()
        elif action_type == ActionType.PLACE.value:
            return self._place()
        elif action_type == ActionType.USE.value:
            return self._use()
        elif action_type == ActionType.ATTACK.value:
            return self._attack()
        elif action_type == ActionType.EAT.value:
            return self._eat()
        elif action_type == ActionType.SLEEP.value:
            return self._sleep()
            
        self.last_action = action
        return True
        
    def _move(self, params: Dict) -> bool:
        """Move in a direction"""
        direction = params.get("direction", "forward")
        duration = params.get("duration", 1)
        sprint = params.get("sprint", False)
        
        # In real implementation:
        # - Send RCON command
        # - Or simulate key press
        # - Or call data pack function
        
        print(f"  [ACT] Move {direction}" + (" (sprint)" if sprint else ""))
        self.action_cooldown = duration
        return True
        
    def _look(self, params: Dict) -> bool:
        """Look in a direction"""
        yaw = params.get("yaw", 0)
        pitch = params.get("pitch", 0)
        
        print(f"  [ACT] Look yaw={yaw}, pitch={pitch}")
        return True
        
    def _jump(self) -> bool:
        """Jump"""
        print("  [ACT] Jump")
        self.action_cooldown = 2
        return True
        
    def _mine(self) -> bool:
        """Mine block at cursor"""
        print("  [ACT] Mine")
        self.action_cooldown = 5  # Mining takes time
        return True
        
    def _place(self) -> bool:
        """Place block"""
        print("  [ACT] Place block")
        self.action_cooldown = 2
        return True
        
    def _use(self) -> bool:
        """Use/interact"""
        print("  [ACT] Use")
        return True
        
    def _attack(self) -> bool:
        """Attack"""
        print("  [ACT] Attack")
        self.action_cooldown = 3
        return True
        
    def _eat(self) -> bool:
        """Eat food"""
        print("  [ACT] Eat")
        self.action_cooldown = 3
        return True
        
    def _sleep(self) -> bool:
        """Enter bed (trigger dream mode)"""
        print("  [ACT] Sleep (entering dream mode)")
        self.action_cooldown = 100  # Sleep takes a while
        return True
        
    def from_brain_concepts(self, concepts: List[str], intensity: float = 1.0) -> Optional[Dict]:
        """
        Convert brain concepts to action.
        
        Args:
            concepts: Active brain concepts
            intensity: Activation intensity
            
        Returns:
            Action dict or None
        """
        # Priority mapping
        priority_actions = [
            ("sleep", 10),  # High priority - triggers dream mode
            ("flee", 9),    # Danger
            ("attack", 8),  # Combat
            ("eat", 7),     # Survival
            ("mine", 6),    # Resource
            ("craft", 5),   # Building
            ("place", 4),   # Building
            ("jump", 3),    # Mobility
            ("explore", 2), # Curiosity
            ("forward", 1), # Default
        ]
        
        for concept, priority in priority_actions:
            if concept in concepts:
                if concept in self.concept_actions:
                    action_type, params = self.concept_actions[concept]
                    return {
                        "type": action_type.value,
                        "params": {**params, "intensity": intensity},
                        "priority": priority,
                    }
                    
        return None
        
    def from_cortical_activation(self, 
                                  active_region: Tuple[int, int, int],
                                  wave_direction: Tuple[float, float, float]) -> Optional[Dict]:
        """
        Convert cortical sheet activation to action.
        
        Args:
            active_region: (x, y, z) of active cortical region
            wave_direction: Direction of wave propagation
            
        Returns:
            Action dict or None
        """
        x, y, z = active_region
        dx, dy, dz = wave_direction
        
        # Map cortical regions to actions
        # Front (high y) = forward/movement
        # Back (low y) = retreat
        # Left/Right = turn
        
        if y > 40:  # Frontal - move forward
            return {
                "type": ActionType.MOVE.value,
                "params": {"direction": "forward"},
                "source": "cortical_frontal",
            }
        elif y < 24:  # Posterior - retreat
            return {
                "type": ActionType.MOVE.value,
                "params": {"direction": "back", "sprint": True},
                "source": "cortical_posterior",
            }
        elif x < 28:  # Left hemisphere - turn left
            return {
                "type": ActionType.LOOK.value,
                "params": {"yaw": -30},
                "source": "cortical_left",
            }
        elif x > 36:  # Right hemisphere - turn right
            return {
                "type": ActionType.LOOK.value,
                "params": {"yaw": 30},
                "source": "cortical_right",
            }
        elif z > 10:  # Upper = look up/jump
            return {
                "type": ActionType.JUMP.value,
                "params": {},
                "source": "cortical_upper",
            }
            
        return None


if __name__ == "__main__":
    print("Minecraft Actor Module")
    print("=" * 50)
    
    actor = MinecraftActor()
    
    # Test concept-to-action
    test_concepts = [
        ["wood", "forward", "explore"],
        ["zombie", "danger", "flee"],
        ["hungry", "eat"],
        ["night", "sleep"],
    ]
    
    for concepts in test_concepts:
        print(f"\nConcepts: {concepts}")
        action = actor.from_brain_concepts(concepts)
        if action:
            print(f"  Selected action: {action['type']}")
            actor.execute(action)
        else:
            print("  No action")
            
    print("\n" + "=" * 50)
    print("Actor ready")
