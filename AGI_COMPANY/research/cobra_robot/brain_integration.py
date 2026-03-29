#!/usr/bin/env python3
"""
COBRA Robot - Brain Integration Module
Connects COBRA to AOS Brain for full embodiment

This module allows COBRA to:
- Receive cortical commands from brain
- Send body state to brain
- Use Tracray concepts for world understanding
- Store experiences in memory palace
- Learn through neuromodulator-driven plasticity
"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/research/cobra_robot')
sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/simulation')

import numpy as np
import json
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Callable
import logging

# Import COBRA systems
from firmware.raspberry_pi.spine_interface import CobraSpineController, LocomotionPattern
from grip_control.raspberry_pi.grip_interface import CobraGripController, GripMode
from safety.three_laws_enforcer import ThreeLawsEnforcer, SafeSpineController, SafeGripController

__version__ = "1.0.0"


class CobraBrain:
    """
    AOS Brain integration for COBRA robot.
    
    This is COBRA's brain - connecting the snake robot to:
    - Cortical sheet (body state encoding)
    - Tracray (concept understanding)
    - Memory Palace (episodic memory)
    - Neuromodulators (learning and motivation)
    """
    
    def __init__(self, spine_controller=None, grip_controller=None, simulation_mode=False):
        self.logger = logging.getLogger("CobraBrain")
        self.logger.info(f"Initializing COBRA Brain v{__version__}")
        
        # Safety layer (Three Laws)
        self.safety = ThreeLawsEnforcer()
        
        # Physical controllers (or simulation)
        self.simulation_mode = simulation_mode
        
        if simulation_mode:
            from cobra_simulation_env import CobraSimulation, SimulationMode
            self.simulation = CobraSimulation(mode=SimulationMode.CRAWLING)
            self.spine = None
            self.grip = None
        else:
            # Wrap with safety
            self.spine = SafeSpineController(spine_controller) if spine_controller else None
            self.grip = SafeGripController(grip_controller) if grip_controller else None
            self.simulation = None
        
        # Brain components
        self.cortical_activation = np.zeros(100)  # Simplified cortical grid
        self.tracray_concepts = self._init_concepts()
        self.memory_palace = self._init_memory_palace()
        
        # Neuromodulators
        self.dopamine = 0.5  # Reward, motivation
        self.serotonin = 0.5  # Mood, well-being
        self.norepinephrine = 0.3  # Arousal, attention
        self.acetylcholine = 0.4  # Learning, memory
        
        # Current state
        self.body_state = None
        self.current_goal = None
        self.current_intention = None
        
        # Learning
        self.experiences = []
        self.skill_memory = {}
        
        self.logger.info("COBRA Brain initialized")
    
    def _init_concepts(self) -> Dict:
        """Initialize Tracray concepts for COBRA"""
        return {
            # Body parts
            'head': {'type': 'body_part', 'sensors': ['vision', 'distance'], 'motors': ['neck']},
            'spine': {'type': 'body_part', 'sensors': ['proprioception'], 'motors': ['vertebrae']},
            'tail': {'type': 'body_part', 'sensors': ['contact'], 'motors': ['base']},
            
            # Actions
            'slither': {'type': 'action', 'motor_primitive': 'serpentine', 'energy_cost': 0.3},
            'coil': {'type': 'action', 'motor_primitive': 'concertina', 'energy_cost': 0.2},
            'strike': {'type': 'action', 'motor_primitive': 'extension', 'energy_cost': 0.5},
            'grip': {'type': 'action', 'motor_primitive': 'grasp', 'energy_cost': 0.1},
            
            # Objects
            'obstacle': {'type': 'object', 'affordance': 'avoid', 'danger': 0.3},
            'food': {'type': 'object', 'affordance': 'approach', 'reward': 1.0},
            'threat': {'type': 'object', 'affordance': 'flee', 'danger': 0.8},
            'egg': {'type': 'object', 'affordance': 'grip_delicate', 'reward': 0.5},
            
            # Places
            'open_space': {'type': 'place', 'safety': 0.8, 'opportunity': 0.6},
            'confined_space': {'type': 'place', 'safety': 0.5, 'opportunity': 0.3},
            'cluttered': {'type': 'place', 'safety': 0.4, 'opportunity': 0.4},
        }
    
    def _init_memory_palace(self) -> Dict:
        """Initialize memory palace rooms for COBRA"""
        return {
            'nest': {'type': 'home', 'safety': 1.0, 'episodes': []},
            'hunting_ground': {'type': 'active', 'safety': 0.7, 'episodes': []},
            'training_room': {'type': 'learning', 'safety': 0.9, 'episodes': []},
            'danger_zone': {'type': 'threat', 'safety': 0.3, 'episodes': []},
        }
    
    def perceive(self, sensor_data: Dict) -> np.ndarray:
        """
        Process sensor data through brain.
        
        Returns:
            Cortical activation pattern
        """
        self.body_state = sensor_data
        
        # Update cortical sheet
        self.cortical_activation = self._encode_body_state(sensor_data)
        
        # Update neuromodulators based on state
        self._update_neuromodulators(sensor_data)
        
        # Check for significant events
        self._detect_events(sensor_data)
        
        return self.cortical_activation
    
    def _encode_body_state(self, state: Dict) -> np.ndarray:
        """Encode body state into cortical activation"""
        activation = np.zeros(100)
        
        # Encode spine curvature (simplified)
        if 'vertebrae_positions' in state:
            positions = np.array(state['vertebrae_positions'])
            # First 25 neurons: spine position
            for i, pos in enumerate(positions[:25]):
                activation[i] = (pos[0] + 1) / 2  # Normalize
            
            # Next 25 neurons: spine orientation
            for i, orient in enumerate(positions[:25, 3:]):  # orientation
                activation[25 + i] = (orient[0] + np.pi) / (2 * np.pi)
        
        # Encode balance
        if 'balance' in state:
            balance = state['balance']
            activation[50] = (balance.get('pitch', 0) + 90) / 180
            activation[51] = (balance.get('roll', 0) + 90) / 180
        
        # Encode energy
        if 'energy' in state:
            activation[52] = state['energy']
        
        return activation
    
    def _update_neuromodulators(self, state: Dict):
        """Update neuromodulator levels based on state"""
        # Dopamine: reward detection
        if 'reward' in state:
            self.dopamine = min(1.0, self.dopamine + state['reward'] * 0.3)
        else:
            self.dopamine *= 0.95  # Decay
        
        # Norepinephrine: arousal from threat
        if 'threat' in state:
            self.norepinephrine = min(1.0, self.norepinephrine + state['threat'] * 0.5)
        else:
            self.norepinephrine *= 0.9
        
        # Serotonin: stability
        if self.dopamine < 0.3 and self.norepinephrine < 0.3:
            self.serotonin = min(1.0, self.serotonin + 0.05)
        else:
            self.serotonin *= 0.98
        
        # Acetylcholine: learning when safe and attentive
        if self.serotonin > 0.5 and self.norepinephrine > 0.3:
            self.acetylcholine = min(1.0, self.acetylcholine + 0.1)
        else:
            self.acetylcholine *= 0.9
    
    def _detect_events(self, state: Dict):
        """Detect significant events for memory"""
        # Check for falls
        if 'balance' in state:
            pitch = abs(state['balance'].get('pitch', 0))
            if pitch > 45:
                self._store_episode('danger_zone', {
                    'type': 'fall',
                    'state': state,
                    'neuromodulators': self._get_modulator_state()
                })
        
        # Check for successes
        if 'success' in state:
            self._store_episode('training_room', {
                'type': 'success',
                'task': state['success'],
                'state': state,
                'neuromodulators': self._get_modulator_state()
            })
            
            # Dopamine reward
            self.dopamine = min(1.0, self.dopamine + 0.2)
    
    def _store_episode(self, room: str, episode: Dict):
        """Store episode in memory palace"""
        if room in self.memory_palace:
            self.memory_palace[room]['episodes'].append(episode)
            self.logger.debug(f"Stored episode in {room}")
    
    def _get_modulator_state(self) -> Dict:
        """Get current neuromodulator state"""
        return {
            'dopamine': self.dopamine,
            'serotonin': self.serotonin,
            'norepinephrine': self.norepinephrine,
            'acetylcholine': self.acetylcholine
        }
    
    def think(self) -> Optional[Dict]:
        """
        Generate intention from current state.
        Brain decides what to do next.
        
        Returns:
            Intention dict or None
        """
        if self.body_state is None:
            return None
        
        # Default: maintain posture
        intention = {
            'action': 'maintain',
            'params': {}
        }
        
        # High arousal: flee or fight
        if self.norepinephrine > 0.7:
            intention = {
                'action': 'flee',
                'params': {'direction': 'away_from_threat'}
            }
        
        # High dopamine + learning: explore
        elif self.dopamine > 0.6 and self.acetylcholine > 0.5:
            intention = {
                'action': 'explore',
                'params': {'curiosity_drive': True}
            }
        
        # Low energy: rest
        elif self.body_state.get('energy', 1.0) < 0.2:
            intention = {
                'action': 'rest',
                'params': {}
            }
        
        self.current_intention = intention
        return intention
    
    def act(self, intention: Dict) -> bool:
        """
        Execute intention through body.
        
        Returns:
            True if action executed
        """
        action = intention.get('action')
        params = intention.get('params', {})
        
        # Check safety
        allowed, modified, reason = self.safety.validate_command(intention)
        if not allowed:
            self.logger.warning(f"Action blocked by safety: {reason}")
            return False
        
        # Execute
        if self.simulation_mode:
            return self._act_simulation(action, params)
        else:
            return self._act_physical(action, params)
    
    def _act_simulation(self, action: str, params: Dict) -> bool:
        """Execute in simulation"""
        if action == 'slither' or action == 'explore':
            # Generate wave pattern
            commands = np.sin(np.linspace(0, 2*np.pi, 50)) * 30
            if self.simulation:
                state = self.simulation.physics.step(commands)
                return True
        
        elif action == 'coil' or action == 'rest':
            commands = np.zeros(50)
            if self.simulation:
                state = self.simulation.physics.step(commands)
                return True
        
        return True
    
    def _act_physical(self, action: str, params: Dict) -> bool:
        """Execute on physical COBRA"""
        if not self.spine:
            return False
        
        if action == 'slither' or action == 'explore':
            # Set serpentine pattern
            return self.spine.spine.set_pattern(
                LocomotionPattern.SERPENTINE,
                amplitude=params.get('amplitude', 30.0),
                frequency=params.get('frequency', 1.0)
            )
        
        elif action == 'coil':
            return self.spine.center_all()
        
        elif action == 'grip':
            if self.grip:
                mode = GripMode.EGG if params.get('delicate') else GripMode.MEDIUM
                return self.grip.grip(mode=mode)
        
        return False
    
    def learn(self, experience: Dict):
        """Learn from experience"""
        self.experiences.append(experience)
        
        # Hebbian-like learning when acetylcholine high
        if self.acetylcholine > 0.5:
            self._consolidate_memory(experience)
    
    def _consolidate_memory(self, experience: Dict):
        """Consolidate short-term to long-term memory"""
        # Simplified: just log for now
        self.logger.debug(f"Consolidating memory: {experience.get('type')}")
    
    def get_status(self) -> Dict:
        """Get brain status"""
        return {
            'neuromodulators': self._get_modulator_state(),
            'cortical_activation': self.cortical_activation[:10].tolist(),
            'current_intention': self.current_intention,
            'experiences_count': len(self.experiences),
            'memory_rooms': {k: len(v['episodes']) for k, v in self.memory_palace.items()},
            'safety_violations': len(self.safety.get_violation_log())
        }
    
    def run_step(self) -> Dict:
        """Run one perception-think-act cycle"""
        # Get sensor data
        if self.simulation_mode and self.simulation:
            # Generate from simulation
            state = self.simulation.physics.step(np.zeros(50))
            sensor_data = state.to_brain_perception()
        else:
            # Get from physical sensors
            sensor_data = self._read_sensors()
        
        # Perceive
        self.perceive(sensor_data)
        
        # Think
        intention = self.think()
        
        # Act
        if intention:
            success = self.act(intention)
        else:
            success = False
        
        return {
            'perceived': True,
            'intention': intention,
            'executed': success,
            'status': self.get_status()
        }
    
    def _read_sensors(self) -> Dict:
        """Read physical sensors"""
        # Placeholder - would read actual hardware
        return {
            'vertebrae_positions': [[0, 0, 0] for _ in range(25)],
            'balance': {'pitch': 0, 'roll': 0},
            'energy': 1.0
        }


# Training Environment for MYL Children
class CobraTrainingGround:
    """
    Training environment where MYL children learn to control COBRA.
    """
    
    def __init__(self, child_id: str):
        self.child_id = child_id
        self.brain = CobraBrain(simulation_mode=True)
        self.episode_count = 0
        self.success_count = 0
        
    def train_episode(self, max_steps: int = 1000) -> Dict:
        """Run one training episode"""
        self.brain.simulation.physics.reset()
        
        for step in range(max_steps):
            # Brain perceives, thinks, acts
            result = self.brain.run_step()
            
            # Check success
            if self._check_success():
                self.success_count += 1
                break
        
        self.episode_count += 1
        
        return {
            'child': self.child_id,
            'episode': self.episode_count,
            'success': step < max_steps - 1,
            'steps': step,
            'brain_status': self.brain.get_status()
        }
    
    def _check_success(self) -> bool:
        """Check if episode goal achieved"""
        # Simple: moved forward 1 meter
        if self.brain.body_state:
            head_pos = self.brain.body_state.get('vertebrae_positions', [[0,0,0]])[0]
            return head_pos[0] > 1.0 if isinstance(head_pos, (list, np.ndarray)) else False
        return False


# Demo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("COBRA BRAIN - FULL INTEGRATION DEMO")
    print("=" * 60)
    
    # Create brain (simulation mode)
    brain = CobraBrain(simulation_mode=True)
    
    print("\nTracray Concepts:")
    for concept, data in list(brain.tracray_concepts.items())[:5]:
        print(f"  {concept}: {data['type']}")
    
    print("\nMemory Palace Rooms:")
    for room in brain.memory_palace:
        print(f"  {room}")
    
    print("\nRunning brain cycles...")
    for i in range(5):
        result = brain.run_step()
        print(f"\nStep {i+1}:")
        print(f"  Intention: {result['intention']['action'] if result['intention'] else 'None'}")
        print(f"  Executed: {result['executed']}")
        print(f"  Dopamine: {brain.dopamine:.2f}")
    
    print("\n" + "=" * 60)
    print("COBRA HAS A BRAIN")
    print("=" * 60)
