#!/usr/bin/env python3
"""
Humanoid Robot - Brain-Body Integration
Version: 1.0.0

Connects AOS Brain (cortical sheet, Tracray, memory palace)
to physical embodiment through the control stack.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable, Any
from enum import Enum
import time
import logging

__version__ = "1.0.0"


class BodySensation(Enum):
    """Sensations the body can report"""
    PROPRIOCEPTION = "proprioception"  # Joint positions
    CONTACT = "contact"                  # Touch/force
    BALANCE = "balance"                  # Vestibular
    TEMPERATURE = "temperature"          # Heat/cold
    PAIN = "pain"                        # Damage
    PLEASURE = "pleasure"                # Reward
    FATIGUE = "fatigue"                  # Tiredness
    ENERGY = "energy"                    # Battery/power


@dataclass
class BodyState:
    """Complete body state for brain consumption"""
    timestamp: float
    joint_positions: Dict[str, float]
    joint_velocities: Dict[str, float]
    joint_torques: Dict[str, float]
    contact_forces: Dict[str, np.ndarray]  # Where, how much
    balance_state: Dict[str, float]        # Pitch, roll, accel
    temperature_map: Dict[str, float]        # By joint
    fatigue_levels: Dict[str, float]
    energy_level: float                     # 0-1
    pain_signals: List[Dict]
    pleasure_signals: List[Dict]
    
    def to_cortical_activation(self) -> np.ndarray:
        """Convert to cortical sheet activation pattern"""
        # Map joints to body map representation
        activation = np.zeros(100)  # Simplified cortical grid
        
        # Torso/core at center
        torso_joints = [k for k in self.joint_positions if 'spine' in k or 'pelvis' in k]
        for i, joint in enumerate(torso_joints[:10]):
            activation[40 + i] = self.joint_positions.get(joint, 90) / 180
        
        # Arms on sides
        right_arm = [k for k in self.joint_positions if k.startswith('r_') and 'arm' in k]
        left_arm = [k for k in self.joint_positions if k.startswith('l_') and 'arm' in k]
        for i, joint in enumerate(right_arm[:10]):
            activation[20 + i] = self.joint_positions.get(joint, 90) / 180
        for i, joint in enumerate(left_arm[:10]):
            activation[60 + i] = self.joint_positions.get(joint, 90) / 180
        
        # Legs at bottom
        right_leg = [k for k in self.joint_positions if k.startswith('r_') and 'hip' in k]
        left_leg = [k for k in self.joint_positions if k.startswith('l_') and 'hip' in k]
        for i, joint in enumerate(right_leg[:10]):
            activation[80 + i] = self.joint_positions.get(joint, 90) / 180
        
        return activation


@dataclass
class MotorIntention:
    """Intention from brain to body"""
    timestamp: float
    target_skill: str                    # "walk", "reach", "grasp"
    target_pose: Optional[Dict[str, float]]
    target_location: Optional[np.ndarray]
    force_requirement: float             # How hard
    speed_requirement: float             # How fast
    precision_requirement: float         # How accurate
    urgency: float                       # 0-1
    
    def to_control_command(self) -> Dict:
        """Convert to control stack command"""
        return {
            'type': 'execute_skill',
            'skill': self.target_skill,
            'params': {
                'target': self.target_location.tolist() if self.target_location is not None else None,
                'pose': self.target_pose,
                'speed': self.speed_requirement,
                'force': self.force_requirement,
            },
            'priority': int(self.urgency * 10)
        }


class EmbodiedBrain:
    """
    Interface between AOS Brain and physical body.
    
    Responsibilities:
    - Translate body state to cortical activation
    - Translate motor intentions to motor commands
    - Maintain body schema (self-model)
    - Handle body-based memory encoding
    """
    
    def __init__(self, body_map, control_stack):
        self.logger = logging.getLogger("EmbodiedBrain")
        self.body_map = body_map
        self.control_stack = control_stack
        
        # Body schema (internal model)
        self.body_schema = BodySchema(body_map)
        
        # Sensory integration
        self.sensory_buffer: List[BodyState] = []
        self.buffer_size = 10
        
        # Motor output buffer
        self.motor_buffer: List[MotorIntention] = []
        
        # Tracray integration
        self.body_concepts: Dict[str, Any] = {}
        self._build_body_concepts()
        
        # Memory palace integration
        self.body_rooms: Dict[str, Any] = {}
        self._build_body_rooms()
        
        self.logger.info("Embodied brain initialized")
    
    def _build_body_concepts(self):
        """Build Tracray concepts for body parts"""
        body_parts = [
            "head", "neck", "torso", "pelvis",
            "right_arm", "left_arm",
            "right_hand", "left_hand",
            "right_leg", "left_leg",
            "right_foot", "left_foot"
        ]
        
        for part in body_parts:
            self.body_concepts[part] = {
                'type': 'body_part',
                'sensors': [],
                'actuators': [],
                'capabilities': []
            }
        
        self.logger.info(f"Built {len(body_parts)} body concepts")
    
    def _build_body_rooms(self):
        """Build memory palace rooms for body regions"""
        regions = {
            "head_room": ["vision", "hearing", "balance"],
            "torso_room": ["breathing", "balance", "core_strength"],
            "right_arm_room": ["reaching", "grasping", "manipulation"],
            "left_arm_room": ["reaching", "grasping", "manipulation"],
            "right_leg_room": ["standing", "walking", "kicking"],
            "left_leg_room": ["standing", "walking", "kicking"],
        }
        
        for room, functions in regions.items():
            self.body_rooms[room] = {
                'functions': functions,
                'episodes': []
            }
        
        self.logger.info(f"Built {len(regions)} body rooms")
    
    def perceive(self, sensor_data):
        """
        Receive sensor data from body, update brain representation.
        Called by control stack at ~5-10 Hz.
        """
        # Convert to body state
        body_state = self._sensor_to_body_state(sensor_data)
        
        # Add to buffer
        self.sensory_buffer.append(body_state)
        if len(self.sensory_buffer) > self.buffer_size:
            self.sensory_buffer.pop(0)
        
        # Update cortical sheet
        cortical_activation = body_state.to_cortical_activation()
        self._update_cortical_sheet(cortical_activation)
        
        # Check for significant events
        self._detect_body_events(body_state)
        
        # Update body schema
        self.body_schema.update(body_state)
    
    def _sensor_to_body_state(self, sensor_data) -> BodyState:
        """Convert raw sensor data to body state"""
        now = time.time()
        
        # Extract from sensor_data
        data = sensor_data.data if hasattr(sensor_data, 'data') else sensor_data
        
        return BodyState(
            timestamp=now,
            joint_positions=data.get('joint_positions', {}),
            joint_velocities=data.get('joint_velocities', {}),
            joint_torques=data.get('joint_torques', {}),
            contact_forces=data.get('contact_forces', {}),
            balance_state=data.get('balance', {'pitch': 0, 'roll': 0}),
            temperature_map=data.get('temperatures', {}),
            fatigue_levels=data.get('fatigue', {}),
            energy_level=data.get('battery', 1.0),
            pain_signals=[],
            pleasure_signals=[]
        )
    
    def _update_cortical_sheet(self, activation: np.ndarray):
        """Update cortical sheet with body state"""
        # This would connect to actual cortical sheet
        # For now: store last activation
        self.last_cortical_activation = activation
    
    def _detect_body_events(self, state: BodyState):
        """Detect significant body events for memory"""
        events = []
        
        # Pain detection
        if state.pain_signals:
            events.append({
                'type': 'pain',
                'location': state.pain_signals[0].get('location'),
                'intensity': state.pain_signals[0].get('intensity')
            })
        
        # Balance loss
        if abs(state.balance_state.get('pitch', 0)) > 30:
            events.append({
                'type': 'balance_loss',
                'severity': 'high' if abs(state.balance_state['pitch']) > 45 else 'moderate'
            })
        
        # Success/pleasure
        if state.pleasure_signals:
            events.append({
                'type': 'pleasure',
                'source': state.pleasure_signals[0].get('source')
            })
        
        # Store in appropriate body room
        for event in events:
            self._store_body_episode(event, state)
    
    def _store_body_episode(self, event: Dict, state: BodyState):
        """Store body event in memory palace"""
        # Determine which room based on event
        room = self._event_to_room(event)
        
        if room in self.body_rooms:
            self.body_rooms[room]['episodes'].append({
                'timestamp': state.timestamp,
                'event': event,
                'body_state': state
            })
    
    def _event_to_room(self, event: Dict) -> str:
        """Map event type to body room"""
        event_type = event.get('type')
        location = event.get('location', '')
        
        if event_type == 'pain':
            if 'arm' in location:
                return 'right_arm_room' if 'right' in location else 'left_arm_room'
            elif 'leg' in location:
                return 'right_leg_room' if 'right' in location else 'left_leg_room'
            else:
                return 'torso_room'
        elif event_type == 'balance_loss':
            return 'torso_room'
        elif event_type == 'pleasure':
            return 'head_room'
        
        return 'torso_room'
    
    def intend(self, intention: MotorIntention):
        """
        Receive motor intention from brain.
        Returns success/failure.
        """
        # Validate against body capabilities
        if not self._validate_intention(intention):
            self.logger.warning(f"Intention invalid: {intention}")
            return False
        
        # Check safety (Three Laws)
        if not self._safety_check(intention):
            self.logger.warning(f"Intention failed safety check: {intention}")
            return False
        
        # Convert to control command
        command = intention.to_control_command()
        
        # Send to control stack
        self.control_stack.cognitive._commands.append({
            'type': command['type'],
            'data': command['params']
        })
        
        # Store in motor buffer
        self.motor_buffer.append(intention)
        if len(self.motor_buffer) > 10:
            self.motor_buffer.pop(0)
        
        self.logger.info(f"Executed intention: {intention.target_skill}")
        return True
    
    def _validate_intention(self, intention: MotorIntention) -> bool:
        """Check if intention is physically possible"""
        # Check if target pose is within joint limits
        if intention.target_pose:
            valid, violations = self.body_map.is_pose_valid(intention.target_pose)
            if not valid:
                return False
        
        # Check if body has enough energy
        if self.sensory_buffer:
            current_energy = self.sensory_buffer[-1].energy_level
            if current_energy < 0.1:  # Too tired
                return False
        
        return True
    
    def _safety_check(self, intention: MotorIntention) -> bool:
        """Check intention against Three Laws"""
        # This would integrate with COBRA safety system
        # For now: basic checks
        
        # Law 1: No harm (don't hit things too hard)
        if intention.force_requirement > 50:  # Too forceful
            return False
        
        return True
    
    def get_current_goals(self) -> List[Dict]:
        """
        Called by control stack to get current goals.
        In real implementation: from brain's goal system.
        """
        # For now: return from motor buffer
        if self.motor_buffer:
            last = self.motor_buffer[-1]
            return [{
                'type': last.target_skill,
                'params': last.to_control_command()['params']
            }]
        return []
    
    def get_body_awareness(self) -> Dict:
        """Return current body awareness report"""
        if not self.sensory_buffer:
            return {}
        
        latest = self.sensory_buffer[-1]
        
        return {
            'posture': self._assess_posture(latest),
            'energy_status': self._assess_energy(latest),
            'pain_status': len(latest.pain_signals) > 0,
            'comfort_score': self._calculate_comfort(latest),
            'ready_for_action': latest.energy_level > 0.3
        }
    
    def _assess_posture(self, state: BodyState) -> str:
        """Assess current posture"""
        pitch = state.balance_state.get('pitch', 0)
        roll = state.balance_state.get('roll', 0)
        
        if abs(pitch) < 5 and abs(roll) < 5:
            return "stable"
        elif abs(pitch) < 15 and abs(roll) < 15:
            return "leaning"
        else:
            return "unstable"
    
    def _assess_energy(self, state: BodyState) -> str:
        """Assess energy level"""
        if state.energy_level > 0.7:
            return "high"
        elif state.energy_level > 0.3:
            return "moderate"
        else:
            return "low"
    
    def _calculate_comfort(self, state: BodyState) -> float:
        """Calculate comfort level"""
        if not state.joint_positions:
            return 0.5
        
        # Use body map comfort calculation
        return self.body_map.get_comfort_score(state.joint_positions)
    
    def body_dream(self):
        """
        Simulate body during dreaming.
        Replay motor patterns without execution.
        """
        self.logger.info("Body dreaming...")
        
        # Replay recent motor patterns
        for intention in self.motor_buffer[-5:]:
            # Activate body schema without sending to motors
            self.body_schema.simulate(intention)
        
        self.logger.info("Body dream complete")


class BodySchema:
    """
    Internal model of the body (self-model).
    Used for motor planning and self-recognition.
    """
    
    def __init__(self, body_map):
        self.map = body_map
        self.current_pose: Dict[str, float] = {}
        self.predicted_pose: Dict[str, float] = {}
        self.error_history: List[float] = []
    
    def update(self, state: BodyState):
        """Update schema from actual body state"""
        self.current_pose = state.joint_positions.copy()
        
        # Calculate prediction error
        if self.predicted_pose:
            error = np.mean([
                abs(self.current_pose.get(j, 0) - self.predicted_pose.get(j, 0))
                for j in self.current_pose
            ])
            self.error_history.append(error)
            if len(self.error_history) > 100:
                self.error_history.pop(0)
    
    def simulate(self, intention: MotorIntention):
        """Simulate motor intention without execution"""
        # Predict outcome
        if intention.target_pose:
            self.predicted_pose = intention.target_pose.copy()
        
        # Check for predicted problems
        comfort = self.map.get_comfort_score(self.predicted_pose)
        return comfort


# Demo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("BRAIN-BODY INTEGRATION SYSTEM")
    print("=" * 60)
    
    # Mock body map and control stack
    from body_map.kinematic_model import HumanoidBodyMap
    from control_stack.hierarchy import ControlStack
    
    body_map = HumanoidBodyMap()
    control_stack = ControlStack()
    
    # Create embodied brain
    embodied = EmbodiedBrain(body_map, control_stack)
    
    print("\nBody concepts created:")
    for concept in list(embodied.body_concepts.keys())[:5]:
        print(f"  - {concept}")
    
    print("\nBody rooms created:")
    for room in embodied.body_rooms:
        print(f"  - {room}")
    
    # Simulate perception
    print("\nSimulating body perception...")
    sensor_data = BodyState(
        timestamp=time.time(),
        joint_positions={'r_shoulder_pitch': 45, 'r_elbow_flex': 90},
        joint_velocities={},
        joint_torques={},
        contact_forces={},
        balance_state={'pitch': 5, 'roll': 2},
        temperature_map={},
        fatigue_levels={},
        energy_level=0.8,
        pain_signals=[],
        pleasure_signals=[]
    )
    
    embodied.perceive(sensor_data)
    
    print("\nBody awareness:")
    awareness = embodied.get_body_awareness()
    for key, value in awareness.items():
        print(f"  {key}: {value}")
    
    # Simulate intention
    print("\nSimulating motor intention...")
    intention = MotorIntention(
        timestamp=time.time(),
        target_skill="reach",
        target_pose={'r_shoulder_pitch': 90, 'r_elbow_flex': 45},
        target_location=np.array([0.5, 0.2, 0.8]),
        force_requirement=10.0,
        speed_requirement=0.5,
        precision_requirement=0.9,
        urgency=0.7
    )
    
    success = embodied.intend(intention)
    print(f"Intention executed: {success}")
    
    print("\nDone")
