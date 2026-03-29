#!/usr/bin/env python3
"""
Humanoid Robot - Control Stack Hierarchy
Version: 1.0.0

Six-layer control system from hardware to cognition.
"""

import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable, Tuple
from enum import Enum
import time
import threading
import logging

__version__ = "1.0.0"


class ControlLayer(Enum):
    """Control hierarchy levels"""
    HARDWARE = 0      # kHz - Motor drivers
    JOINT = 1         # 500-1000 Hz - Impedance control
    BODY = 2          # 200-500 Hz - Balance, IK, gait
    SKILL = 3         # 50-100 Hz - Motor primitives
    TASK = 4          # 5-20 Hz - Planning, goals
    COGNITIVE = 5     # 1-10 Hz - Brain integration


@dataclass
class ControlCommand:
    """Command passing between layers"""
    layer: ControlLayer
    command_type: str
    data: Dict
    timestamp: float
    priority: int = 0


@dataclass
class SensorData:
    """Sensor data flowing up the stack"""
    layer: ControlLayer
    sensor_type: str
    data: Dict
    timestamp: float


class ControlLayerBase(ABC):
    """Base class for all control layers"""
    
    def __init__(self, layer: ControlLayer, rate_hz: float):
        self.layer = layer
        self.rate_hz = rate_hz
        self.period = 1.0 / rate_hz
        self.logger = logging.getLogger(f"Layer_{layer.name}")
        
        self._running = False
        self._thread: Optional[threading.Thread] = None
        
        # Up/down communication
        self._lower_layer: Optional['ControlLayerBase'] = None
        self._higher_layer: Optional['ControlLayerBase'] = None
        
        # Command queue
        self._commands: List[ControlCommand] = []
        self._lock = threading.Lock()
    
    def connect_layer_below(self, layer: 'ControlLayerBase'):
        """Connect to lower layer"""
        self._lower_layer = layer
        layer._higher_layer = self
    
    @abstractmethod
    def process(self):
        """Main processing loop - override in subclass"""
        pass
    
    def start(self):
        """Start control loop"""
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self.logger.info(f"Started at {self.rate_hz} Hz")
    
    def stop(self):
        """Stop control loop"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        self.logger.info("Stopped")
    
    def _run_loop(self):
        """Main timing loop"""
        while self._running:
            start = time.perf_counter()
            
            try:
                self.process()
            except Exception as e:
                self.logger.error(f"Processing error: {e}")
            
            # Maintain timing
            elapsed = time.perf_counter() - start
            if elapsed < self.period:
                time.sleep(self.period - elapsed)
    
    def send_down(self, command: ControlCommand):
        """Send command to lower layer"""
        if self._lower_layer:
            with self._lower_layer._lock:
                self._lower_layer._commands.append(command)
    
    def send_up(self, sensor_data: SensorData):
        """Send sensor data to higher layer"""
        if self._higher_layer:
            self._higher_layer.receive_data(sensor_data)
    
    def receive_data(self, sensor_data: SensorData):
        """Receive data from lower layer - override"""
        pass


class HardwareLayer(ControlLayerBase):
    """
    Layer 0: Hardware Control (kHz)
    Direct motor control, safety limits, encoder readout
    """
    
    def __init__(self):
        super().__init__(ControlLayer.HARDWARE, 1000.0)
        self.joint_targets: Dict[str, float] = {}
        self.joint_states: Dict[str, Dict] = {}
    
    def process(self):
        """Fast control loop"""
        # Update all joints
        for joint_name, target in self.joint_targets.items():
            # In real implementation: send to motor driver
            # Here: simulate
            current = self.joint_states.get(joint_name, {}).get('position', 0)
            error = target - current
            
            # Simple PD control
            kp, kd = 100.0, 10.0
            velocity = self.joint_states.get(joint_name, {}).get('velocity', 0)
            torque = kp * error - kd * velocity
            
            # Safety limits
            torque = max(-10, min(10, torque))
            
            self.joint_states[joint_name] = {
                'position': current + velocity * 0.001,
                'velocity': velocity + torque * 0.001,
                'torque': torque
            }
        
        # Send state up
        self.send_up(SensorData(
            layer=self.layer,
            sensor_type="joint_states",
            data=self.joint_states.copy(),
            timestamp=time.time()
        ))
    
    def receive_data(self, sensor_data: SensorData):
        """Receive commands from above"""
        if sensor_data.sensor_type == "joint_targets":
            self.joint_targets.update(sensor_data.data)


class JointLayer(ControlLayerBase):
    """
    Layer 1: Joint Control (500-1000 Hz)
    Impedance control, compliance, local reflexes
    """
    
    def __init__(self):
        super().__init__(ControlLayer.JOINT, 500.0)
        self.impedance_gains = {}
        self.reflex_enabled = True
    
    def process(self):
        """Joint-level control"""
        # Check commands from above
        with self._lock:
            commands = self._commands.copy()
            self._commands.clear()
        
        for cmd in commands:
            if cmd.command_type == "set_impedance":
                self.impedance_gains.update(cmd.data)
            elif cmd.command_type == "enable_reflex":
                self.reflex_enabled = cmd.data.get('enabled', True)
        
        # Process joint targets (would come from body layer)
        # For now: pass through
        
    def receive_data(self, sensor_data: SensorData):
        """Handle incoming sensor data"""
        if sensor_data.sensor_type == "joint_states":
            # Check for collisions (reflex)
            if self.reflex_enabled:
                for joint, state in sensor_data.data.items():
                    if abs(state.get('torque', 0)) > 8.0:  # Collision detected
                        self.logger.warning(f"Reflex: Collision on {joint}")
                        # Trigger compliance
                        self.send_down(ControlCommand(
                            layer=self.layer,
                            command_type="set_compliance",
                            data={joint: 0.5},
                            timestamp=time.time()
                        ))
            
            # Pass up
            self.send_up(sensor_data)


class BodyLayer(ControlLayerBase):
    """
    Layer 2: Whole-Body Control (200-500 Hz)
    Balance, inverse kinematics, gait generation
    """
    
    def __init__(self):
        super().__init__(ControlLayer.BODY, 200.0)
        self.balance_mode = "standing"
        self.com_position = np.array([0.0, 0.0, 1.0])  # Center of mass
        self.support_polygon = []
        self.ik_solver = None
    
    def process(self):
        """Whole-body control loop"""
        # Check for commands
        with self._lock:
            commands = self._commands.copy()
            self._commands.clear()
        
        for cmd in commands:
            if cmd.command_type == "set_balance_mode":
                self.balance_mode = cmd.data.get('mode', 'standing')
            elif cmd.command_type == "move_com":
                target_com = np.array(cmd.data.get('position', [0, 0, 1]))
                self._compute_balance_correction(target_com)
        
        # Balance control
        if self.balance_mode == "standing":
            self._standing_balance()
        elif self.balance_mode == "walking":
            self._walking_balance()
        
        # Send joint targets down
        joint_targets = self._compute_joint_targets()
        self.send_down(ControlCommand(
            layer=self.layer,
            command_type="joint_targets",
            data=joint_targets,
            timestamp=time.time()
        ))
    
    def _standing_balance(self):
        """Maintain standing balance"""
        # Simple CoM over feet
        error = self.com_position - np.array([0, 0, 1.0])
        # Would compute ankle torques, hip adjustments
        pass
    
    def _walking_balance(self):
        """Dynamic walking balance"""
        # Capture point, ZMP tracking
        pass
    
    def _compute_joint_targets(self) -> Dict[str, float]:
        """Compute target joint positions"""
        # Placeholder - would do full IK
        return {}
    
    def _compute_balance_correction(self, target_com: np.ndarray):
        """Compute corrections to achieve target CoM"""
        pass
    
    def receive_data(self, sensor_data: SensorData):
        """Handle sensor data"""
        if sensor_data.sensor_type == "joint_states":
            # Update CoM estimate
            self._update_com(sensor_data.data)
            self.send_up(sensor_data)
    
    def _update_com(self, joint_states: Dict):
        """Update center of mass estimate"""
        # Simplified
        pass


class SkillLayer(ControlLayerBase):
    """
    Layer 3: Motor Primitives (50-100 Hz)
    Learned skills: walk, reach, grasp, stand up
    """
    
    def __init__(self):
        super().__init__(ControlLayer.SKILL, 50.0)
        self.active_skills: Dict[str, 'Skill'] = {}
        self.skill_library = self._build_skill_library()
    
    def _build_skill_library(self) -> Dict[str, 'Skill']:
        """Build library of motor primitives"""
        return {
            "stand": StandSkill(),
            "walk": WalkSkill(),
            "reach": ReachSkill(),
            "grasp": GraspSkill(),
            "sit": SitSkill(),
        }
    
    def process(self):
        """Skill execution loop""""
        # Check commands
        with self._lock:
            commands = self._commands.copy()
            self._commands.clear()
        
        for cmd in commands:
            if cmd.command_type == "execute_skill":
                skill_name = cmd.data.get('skill')
                if skill_name in self.skill_library:
                    self._start_skill(skill_name, cmd.data)
            elif cmd.command_type == "stop_skill":
                skill_name = cmd.data.get('skill')
                self._stop_skill(skill_name)
        
        # Update active skills
        for name, skill in self.active_skills.items():
            result = skill.update(time.time())
            if result:
                # Send to body layer
                self.send_down(ControlCommand(
                    layer=self.layer,
                    command_type=result['type'],
                    data=result['data'],
                    timestamp=time.time()
                ))
    
    def _start_skill(self, name: str, params: Dict):
        """Start a skill"""
        if name in self.skill_library:
            self.active_skills[name] = self.skill_library[name]
            self.active_skills[name].start(params)
            self.logger.info(f"Started skill: {name}")
    
    def _stop_skill(self, name: str):
        """Stop a skill"""
        if name in self.active_skills:
            self.active_skills[name].stop()
            del self.active_skills[name]
            self.logger.info(f"Stopped skill: {name}")


class Skill(ABC):
    """Base class for motor skills"""
    
    @abstractmethod
    def start(self, params: Dict):
        pass
    
    @abstractmethod
    def update(self, timestamp: float) -> Optional[Dict]:
        pass
    
    @abstractmethod
    def stop(self):
        pass


class WalkSkill(Skill):
    """Walking skill"""
    
    def start(self, params: Dict):
        self.speed = params.get('speed', 0.5)
        self.direction = params.get('direction', 0.0)
        self.phase = 0.0
    
    def update(self, timestamp: float) -> Optional[Dict]:
        self.phase += 0.1
        # Generate step targets
        return {
            'type': 'set_balance_mode',
            'data': {'mode': 'walking'}
        }
    
    def stop(self):
        pass


class ReachSkill(Skill):
    """Reaching skill"""
    
    def start(self, params: Dict):
        self.target = params.get('target', [0, 0, 0])
        self.hand = params.get('hand', 'r_hand')
        self.phase = 0
    
    def update(self, timestamp: float) -> Optional[Dict]:
        self.phase += 0.05
        if self.phase >= 1.0:
            return {'type': 'reached', 'data': {'target': self.target}}
        return {
            'type': 'move_com',
            'data': {'position': self.target}
        }
    
    def stop(self):
        pass


class GraspSkill(Skill):
    """Grasping skill"""
    
    def start(self, params: Dict):
        self.object = params.get('object')
        self.hand = params.get('hand', 'r_hand')
        self.phase = 0
    
    def update(self, timestamp: float) -> Optional[Dict]:
        self.phase += 0.05
        # Would integrate with grip controller
        return None
    
    def stop(self):
        pass


class StandSkill(Skill):
    """Standing skill"""
    
    def start(self, params: Dict):
        pass
    
    def update(self, timestamp: float) -> Optional[Dict]:
        return {
            'type': 'set_balance_mode',
            'data': {'mode': 'standing'}
        }
    
    def stop(self):
        pass


class SitSkill(Skill):
    """Sitting skill"""
    
    def start(self, params: Dict):
        pass
    
    def update(self, timestamp: float) -> Optional[Dict]:
        return {
            'type': 'set_balance_mode',
            'data': {'mode': 'sitting'}
        }
    
    def stop(self):
        pass


class TaskLayer(ControlLayerBase):
    """
    Layer 4: Task Planning (5-20 Hz)
    Sub-goal decomposition, multi-step planning
    """
    
    def __init__(self):
        super().__init__(ControlLayer.TASK, 10.0)
        self.current_plan: Optional[List[Dict]] = None
        self.plan_step = 0
        self.goal_stack: List[Dict] = []
    
    def process(self):
        """Task planning loop"""
        # Check commands from cognitive layer
        with self._lock:
            commands = self._commands.copy()
            self._commands.clear()
        
        for cmd in commands:
            if cmd.command_type == "set_goal":
                self._plan_for_goal(cmd.data)
            elif cmd.command_type == "update_world":
                self._update_plan(cmd.data)
        
        # Execute current plan
        if self.current_plan and self.plan_step < len(self.current_plan):
            action = self.current_plan[self.plan_step]
            self._execute_action(action)
            self.plan_step += 1
    
    def _plan_for_goal(self, goal: Dict):
        """Generate plan to achieve goal"""
        goal_type = goal.get('type')
        
        if goal_type == "pick_up":
            obj = goal.get('object')
            self.current_plan = [
                {'skill': 'reach', 'params': {'target': obj['location']}},
                {'skill': 'grasp', 'params': {'object': obj['name']}},
                {'skill': 'lift', 'params': {'height': 0.1}},
            ]
        elif goal_type == "go_to":
            location = goal.get('location')
            self.current_plan = [
                {'skill': 'walk', 'params': {'direction': location['direction']}},
            ]
        
        self.plan_step = 0
        self.logger.info(f"Planned for goal: {goal_type}")
    
    def _execute_action(self, action: Dict):
        """Send action to skill layer"""
        self.send_down(ControlCommand(
            layer=self.layer,
            command_type="execute_skill",
            data=action,
            timestamp=time.time()
        ))
    
    def _update_plan(self, world_update: Dict):
        """Update plan based on world changes"""
        # Replan if needed
        pass
    
    def receive_data(self, sensor_data: SensorData):
        """Pass up to cognitive"""
        self.send_up(sensor_data)


class CognitiveLayer(ControlLayerBase):
    """
    Layer 5: Cognitive Integration (1-10 Hz)
    Integration with AOS Brain
    """
    
    def __init__(self, brain_interface=None):
        super().__init__(ControlLayer.COGNITIVE, 5.0)
        self.brain = brain_interface
        self.current_goals: List[Dict] = []
        self.world_model: Dict = {}
    
    def process(self):
        """Cognitive loop"""
        # Update from brain
        if self.brain:
            goals = self.brain.get_current_goals()
            if goals != self.current_goals:
                self.current_goals = goals
                self._push_goals(goals)
        
        # Update world model
        self._update_world_model()
        
        # Send to task layer
        if self.current_goals:
            self.send_down(ControlCommand(
                layer=self.layer,
                command_type="set_goal",
                data=self.current_goals[0],
                timestamp=time.time()
            ))
    
    def _push_goals(self, goals: List[Dict]):
        """Push goals to task layer"""
        for goal in goals:
            self.send_down(ControlCommand(
                layer=self.layer,
                command_type="set_goal",
                data=goal,
                timestamp=time.time()
            ))
    
    def _update_world_model(self):
        """Update internal world representation"""
        pass
    
    def receive_data(self, sensor_data: SensorData):
        """Integrate sensor data into world model"""
        if sensor_data.sensor_type == "joint_states":
            self.world_model['body'] = sensor_data.data
        
        # Pass to brain
        if self.brain:
            self.brain.perceive(sensor_data)


class ControlStack:
    """
    Complete 6-layer control stack
    """
    
    def __init__(self, brain_interface=None):
        self.logger = logging.getLogger("ControlStack")
        
        # Create layers
        self.hardware = HardwareLayer()
        self.joint = JointLayer()
        self.body = BodyLayer()
        self.skill = SkillLayer()
        self.task = TaskLayer()
        self.cognitive = CognitiveLayer(brain_interface)
        
        # Connect hierarchy
        self.cognitive.connect_layer_below(self.task)
        self.task.connect_layer_below(self.skill)
        self.skill.connect_layer_below(self.body)
        self.body.connect_layer_below(self.joint)
        self.joint.connect_layer_below(self.hardware)
        
        self.layers = [
            self.hardware,
            self.joint,
            self.body,
            self.skill,
            self.task,
            self.cognitive
        ]
    
    def start(self):
        """Start all layers (bottom-up)"""
        for layer in self.layers:
            layer.start()
        self.logger.info("Control stack started")
    
    def stop(self):
        """Stop all layers (top-down)"""
        for layer in reversed(self.layers):
            layer.stop()
        self.logger.info("Control stack stopped")
    
    def emergency_stop(self):
        """Emergency stop all motion"""
        self.logger.critical("EMERGENCY STOP")
        for layer in self.layers:
            layer._running = False


# Demo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("HUMANOID CONTROL STACK")
    print("=" * 60)
    
    stack = ControlStack()
    
    print("\nLayer Hierarchy:")
    for i, layer in enumerate(stack.layers):
        print(f"  Layer {i}: {layer.layer.name} @ {layer.rate_hz} Hz")
    
    print("\nStarting control stack...")
    stack.start()
    time.sleep(2)
    
    print("\nSimulating goal execution...")
    stack.cognitive.current_goals = [{
        'type': 'pick_up',
        'object': {'name': 'cup', 'location': [0.5, 0.2, 0.8]}
    }]
    
    time.sleep(3)
    
    print("\nStopping...")
    stack.stop()
    
    print("\nDone")
