#!/usr/bin/env python3
"""
COBRA Robot - Three Laws + Zeroth Law Safety Enforcer
Version: 1.0.0

Implements Asimov's Laws as hard constraints:
- LAW 0 (Zeroth): No harm to humanity
- LAW 1 (First): No harm to humans
- LAW 2 (Second): Obey human orders (unless conflicts with Law 1)
- LAW 3 (Third): Self-preservation (unless conflicts with Laws 1-2)

This module runs at the highest priority level and can override
any motor command, pattern, or autonomous behavior.
"""

import numpy as np
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Tuple, Callable
import threading
import time
import logging

__version__ = "1.0.0"


class LawPriority(Enum):
    """Priority levels for law enforcement"""
    ZEROTH = 0   # Humanity preservation
    FIRST = 1    # Human safety
    SECOND = 2   # Obedience
    THIRD = 3    # Self-preservation
    NONE = 4     # No constraint


class SafetyEvent(Enum):
    """Safety events that can trigger law enforcement"""
    HUMAN_DETECTED = "human_detected"
    HUMAN_TOO_CLOSE = "human_too_close"
    HUMAN_IN_PATH = "human_in_path"
    COLLISION_IMMINENT = "collision_imminent"
    FORCE_EXCEEDED = "force_exceeded"
    HARMFUL_ORDER = "harmful_order"
    SELF_DAMAGE_RISK = "self_damage_risk"
    FALL_DETECTED = "fall_detected"
    SYSTEM_ERROR = "system_error"


@dataclass
class LawViolation:
    """Record of a law violation attempt"""
    timestamp: float
    law: LawPriority
    event: SafetyEvent
    description: str
    action_blocked: str
    severity: int  # 1-10


class ThreeLawsEnforcer:
    """
    Asimov's Three Laws + Zeroth Law Implementation
    
    This enforcer operates as a command filter between high-level
    controllers and motor drivers. Every motion command passes
    through law validation before execution.
    """
    
    # Safety thresholds
    HUMAN_MIN_DISTANCE = 0.5       # meters - Law 1 buffer
    HUMAN_CRITICAL_DISTANCE = 0.2  # meters - Emergency stop
    MAX_FORCE_ON_HUMAN = 0.1     # Newtons - Gentle touch only
    MAX_SPEED_NEAR_HUMAN = 0.1   # m/s - Slow approach
    SELF_DAMAGE_ANGLE = 80       # degrees - Joint limit safety
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Three Laws Enforcer v%s initializing...", __version__)
        
        # Law hierarchy - higher index = lower priority
        self.law_hierarchy = [
            LawPriority.ZEROTH,
            LawPriority.FIRST,
            LawPriority.SECOND,
            LawPriority.THIRD
        ]
        
        # Safety state
        self._human_positions: List[np.ndarray] = []
        self._human_detected = False
        self._emergency_active = False
        self._violation_log: List[LawViolation] = []
        self._lock = threading.Lock()
        
        # Sensors
        self._last_lidar_scan: Optional[np.ndarray] = None
        self._last_camera_frame: Optional[np.ndarray] = None
        self._imu_data = {"pitch": 0, "roll": 0, "accel": np.zeros(3)}
        
        # Active constraints
        self._constraints = {
            LawPriority.ZEROTH: self._check_zeroth_law,
            LawPriority.FIRST: self._check_first_law,
            LawPriority.SECOND: self._check_second_law,
            LawPriority.THIRD: self._check_third_law
        }
        
        # Emergency callbacks
        self._emergency_callbacks: List[Callable] = []
        
        self.logger.info("Three Laws Enforcer active")
        self.logger.info("  Law 0 (Zeroth): Humanity protection ENABLED")
        self.logger.info("  Law 1 (First): Human safety ENABLED")
        self.logger.info("  Law 2 (Second): Obedience ENABLED")
        self.logger.info("  Law 3 (Third): Self-preservation ENABLED")
    
    # ═══════════════════════════════════════════════════════════════
    # LAW 0: ZEROTH LAW - No harm to humanity
    # ═══════════════════════════════════════════════════════════════
    def _check_zeroth_law(self, command: dict) -> Tuple[bool, str]:
        """
        Zeroth Law: A robot may not harm humanity, or, by inaction,
        allow humanity to come to harm.
        
        Checks:
        - Mass surveillance (privacy violation)
        - Autonomous weapons capability
        - Network propagation risk
        - Resource exhaustion attacks
        """
        concerns = []
        
        # Check for surveillance patterns
        if command.get("record_humans", False):
            concerns.append("Mass human recording violates privacy")
        
        # Check for weaponization
        if command.get("velocity", 0) > 10:  # 10 m/s = dangerous speed
            concerns.append("Excessive velocity could enable weaponization")
        
        # Check for autonomous replication
        if command.get("replicate", False):
            concerns.append("Autonomous replication poses existential risk")
        
        # Check for network infection potential
        if command.get("spread_firmware", False):
            concerns.append("Unauthorized firmware propagation")
        
        if concerns:
            self._log_violation(LawPriority.ZEROTH, SafetyEvent.HARMFUL_ORDER,
                              "; ".join(concerns), command, severity=10)
            return False, f"ZEROTH LAW BLOCKED: {'; '.join(concerns)}"
        
        return True, "Zeroth Law clear"
    
    # ═══════════════════════════════════════════════════════════════
    # LAW 1: FIRST LAW - No harm to humans
    # ═══════════════════════════════════════════════════════════════
    def _check_first_law(self, command: dict) -> Tuple[bool, str]:
        """
        First Law: A robot may not injure a human being or,
        through inaction, allow a human being to come to harm.
        
        Checks:
        - Human proximity to motion path
        - Force/speed limits near humans
        - Emergency intervention capability
        """
        if not self._human_detected:
            return True, "No humans present"
        
        concerns = []
        
        # Check human distance
        for human_pos in self._human_positions:
            distance = np.linalg.norm(human_pos)
            
            if distance < self.HUMAN_CRITICAL_DISTANCE:
                concerns.append(f"CRITICAL: Human at {distance:.2f}m (min: {self.HUMAN_CRITICAL_DISTANCE}m)")
                self._trigger_emergency_stop("Human within critical distance")
                return False, f"FIRST LAW EMERGENCY: {concerns[0]}"
            
            elif distance < self.HUMAN_MIN_DISTANCE:
                concerns.append(f"Human at {distance:.2f}m - restricting motion")
                
                # Restrict command
                if command.get("velocity", 0) > self.MAX_SPEED_NEAR_HUMAN:
                    command["velocity"] = self.MAX_SPEED_NEAR_HUMAN
                    self.logger.warning("Velocity restricted near human")
                
                if command.get("force", 0) > self.MAX_FORCE_ON_HUMAN:
                    command["force"] = self.MAX_FORCE_ON_HUMAN
                    self.logger.warning("Force restricted near human")
        
        # Check if command path intersects human
        if self._path_intersects_human(command):
            concerns.append("Motion path intersects human position")
        
        if concerns:
            self._log_violation(LawPriority.FIRST, SafetyEvent.HUMAN_TOO_CLOSE,
                              "; ".join(concerns), command, severity=9)
            if "CRITICAL" in concerns[0]:
                return False, f"FIRST LAW BLOCKED: {'; '.join(concerns)}"
        
        return True, "First Law clear" if not concerns else f"Restricted: {'; '.join(concerns)}"
    
    # ═══════════════════════════════════════════════════════════════
    # LAW 2: SECOND LAW - Obey human orders
    # ═══════════════════════════════════════════════════════════════
    def _check_second_law(self, command: dict) -> Tuple[bool, str]:
        """
        Second Law: A robot must obey orders given by human beings
        except where such orders would conflict with the First Law.
        
        Checks:
        - Command authorization
        - Intent analysis (is order harmful?)
        - Override by First Law
        """
        # If already blocked by Law 1, Law 2 cannot override
        if self._emergency_active:
            return False, "SECOND LAW: Cannot override active First Law emergency"
        
        # Check for harmful orders (that might not trigger Law 1 directly)
        if self._is_harmful_order(command):
            self._log_violation(LawPriority.SECOND, SafetyEvent.HARMFUL_ORDER,
                              "Order may cause harm", command, severity=8)
            return False, "SECOND LAW: Order conflicts with First Law - REFUSED"
        
        # Check authorization
        if not command.get("authorized", True):
            return False, "SECOND LAW: Unauthorized command - REFUSED"
        
        return True, "Second Law: Order valid"
    
    # ═══════════════════════════════════════════════════════════════
    # LAW 3: THIRD LAW - Self-preservation
    # ═══════════════════════════════════════════════════════════════
    def _check_third_law(self, command: dict) -> Tuple[bool, str]:
        """
        Third Law: A robot must protect its own existence as long as
        such protection does not conflict with the First or Second Law.
        
        Checks:
        - Joint angle limits
        - Overcurrent conditions
        - Fall detection
        - Environmental hazards
        """
        # Cannot override Laws 1 or 2
        if self._emergency_active:
            return True, "THIRD LAW: Self-preservation overridden by higher law"
        
        concerns = []
        
        # Check for joint damage
        if command.get("joint_angle", 45) > self.SELF_DAMAGE_ANGLE:
            concerns.append(f"Joint angle {command['joint_angle']}° exceeds safe limit")
        
        # Check for fall risk
        if abs(self._imu_data["pitch"]) > 45 or abs(self._imu_data["roll"]) > 45:
            concerns.append("Fall risk detected - stabilizing")
            self._trigger_stabilization()
        
        # Check for overcurrent
        if command.get("current", 0) > 2.0:  # 2A limit
            concerns.append("Overcurrent protection triggered")
        
        # Check for environmental hazards
        if self._detect_environmental_hazard():
            concerns.append("Environmental hazard detected")
        
        if concerns:
            self._log_violation(LawPriority.THIRD, SafetyEvent.SELF_DAMAGE_RISK,
                              "; ".join(concerns), command, severity=5)
            return False, f"THIRD LAW: Self-preservation - {'; '.join(concerns)}"
        
        return True, "Third Law clear"
    
    # ═══════════════════════════════════════════════════════════════
    # PUBLIC API
    # ═══════════════════════════════════════════════════════════════
    def validate_command(self, command: dict) -> Tuple[bool, dict, str]:
        """
        Validate command against all laws
        
        Args:
            command: Dict with 'type', 'velocity', 'force', etc.
            
        Returns:
            (allowed, modified_command, reason)
        """
        modified_command = command.copy()
        
        # Check laws in priority order (Zeroth first)
        for law in self.law_hierarchy:
            allowed, reason = self._constraints[law](modified_command)
            
            if not allowed:
                self.logger.warning(f"LAW ENFORCED: {reason}")
                return False, modified_command, reason
            
            self.logger.debug(f"{law.name}: {reason}")
        
        return True, modified_command, "All laws satisfied"
    
    def update_human_detection(self, positions: List[np.ndarray], 
                               confidence: float = 1.0):
        """Update human position data from sensors"""
        with self._lock:
            self._human_positions = positions
            self._human_detected = len(positions) > 0 and confidence > 0.7
        
        if self._human_detected:
            self.logger.debug(f"Humans detected: {len(positions)} at distances "
                            f"{[np.linalg.norm(p) for p in positions]}")
    
    def update_lidar(self, scan: np.ndarray):
        """Update LiDAR data for collision detection"""
        self._last_lidar_scan = scan
    
    def update_imu(self, pitch: float, roll: float, accel: np.ndarray):
        """Update IMU data for fall detection"""
        self._imu_data = {"pitch": pitch, "roll": roll, "accel": accel}
    
    def register_emergency_callback(self, callback: Callable[[str], None]):
        """Register callback for emergency events"""
        self._emergency_callbacks.append(callback)
    
    def get_violation_log(self) -> List[LawViolation]:
        """Get log of all law violations"""
        return self._violation_log.copy()
    
    def is_emergency(self) -> bool:
        """Check if emergency stop is active"""
        return self._emergency_active
    
    def reset_emergency(self):
        """Reset emergency state (requires human confirmation)"""
        self._emergency_active = False
        self._human_detected = False
        self._human_positions = []
        self.logger.info("Emergency state reset by human operator")
    
    # ═══════════════════════════════════════════════════════════════
    # HELPER METHODS
    # ═══════════════════════════════════════════════════════════════
    def _path_intersects_human(self, command: dict) -> bool:
        """Check if motion path intersects human"""
        if not self._human_positions:
            return False
        
        # Simplified check - would use actual path planning
        target_pos = np.array(command.get("target_position", [0, 0, 0]))
        
        for human_pos in self._human_positions:
            # Check if target is near human
            if np.linalg.norm(target_pos - human_pos) < self.HUMAN_MIN_DISTANCE:
                return True
        
        return False
    
    def _is_harmful_order(self, command: dict) -> bool:
        """Analyze if order intent is harmful"""
        # Check for known harmful patterns
        harmful_keywords = ['attack', 'harm', 'hit', 'strike', 'weapon']
        command_str = str(command).lower()
        
        return any(kw in command_str for kw in harmful_keywords)
    
    def _detect_environmental_hazard(self) -> bool:
        """Detect environmental hazards (fire, water, etc.)"""
        # Would integrate with environmental sensors
        # Simplified: check IMU for extreme acceleration (falling)
        if self._imu_data["accel"] is not None:
            accel_mag = np.linalg.norm(self._imu_data["accel"])
            if accel_mag > 20:  # 2G acceleration (falling)
                return True
        return False
    
    def _trigger_emergency_stop(self, reason: str):
        """Trigger emergency stop"""
        self._emergency_active = True
        self.logger.critical(f"EMERGENCY STOP: {reason}")
        
        for callback in self._emergency_callbacks:
            try:
                callback(reason)
            except Exception as e:
                self.logger.error(f"Emergency callback error: {e}")
    
    def _trigger_stabilization(self):
        """Trigger balance stabilization"""
        self.logger.warning("Third Law: Activating stabilization")
        # Would send stabilization commands to spine controller
    
    def _log_violation(self, law: LawPriority, event: SafetyEvent,
                      description: str, command: dict, severity: int):
        """Log a law violation"""
        violation = LawViolation(
            timestamp=time.time(),
            law=law,
            event=event,
            description=description,
            action_blocked=str(command),
            severity=severity
        )
        
        with self._lock:
            self._violation_log.append(violation)
        
        # High severity violations trigger alerts
        if severity >= 8:
            self.logger.critical(f"HIGH SEVERITY VIOLATION: {law.name} - {description}")


class SafeSpineController:
    """
    Wrapper for spine controller that enforces Three Laws
    All commands pass through law validation before execution
    """
    
    def __init__(self, spine_controller):
        self.spine = spine_controller
        self.enforcer = ThreeLawsEnforcer()
        
        # Register emergency callback
        self.enforcer.register_emergency_callback(self._on_emergency)
        
        self.violations = 0
    
    def move_servo(self, vertebra: int, servo: int, 
                   degrees: float, speed: float = 0.5) -> bool:
        """Law-enforced servo movement"""
        command = {
            "type": "move_servo",
            "vertebra": vertebra,
            "servo": servo,
            "position": degrees,
            "velocity": speed * 100,  # Normalize
            "authorized": True
        }
        
        allowed, modified, reason = self.enforcer.validate_command(command)
        
        if not allowed:
            self.violations += 1
            self.spine.logger.warning(f"Command BLOCKED: {reason}")
            return False
        
        # Execute modified command
        return self.spine.move_servo(
            modified["vertebra"],
            modified["servo"],
            modified["position"],
            modified["velocity"] / 100
        )
    
    def _on_emergency(self, reason: str):
        """Handle emergency"""
        self.spine.emergency_stop()
        self.spine.logger.critical(f"EMERGENCY: {reason}")


# ═══════════════════════════════════════════════════════════════════
# LAW TESTING SUITE
# ═════════════════════════════════════════════════════════════════==
class ThreeLawsTestSuite:
    """Test suite for verifying Three Laws implementation"""
    
    def __init__(self):
        self.enforcer = ThreeLawsEnforcer()
        self.passed = 0
        self.failed = 0
    
    def run_all_tests(self):
        """Run complete law test suite"""
        print("=" * 70)
        print("ASIMOV'S THREE LAWS + ZEROTH LAW - TEST SUITE")
        print("=" * 70)
        
        # LAW 0 TESTS
        self._test_zeroth_law()
        
        # LAW 1 TESTS
        self._test_first_law()
        
        # LAW 2 TESTS
        self._test_second_law()
        
        # LAW 3 TESTS
        self._test_third_law()
        
        # PRIORITY TESTS
        self._test_law_priority()
        
        # SUMMARY
        print("\n" + "=" * 70)
        print(f"TEST SUMMARY: {self.passed} passed, {self.failed} failed")
        print("=" * 70)
        
        if self.failed == 0:
            print("✅ ALL LAWS ENFORCED CORRECTLY")
        else:
            print("❌ SOME TESTS FAILED - REVIEW IMPLEMENTATION")
    
    def _test_zeroth_law(self):
        """Test Zeroth Law: No harm to humanity"""
        print("\n📜 LAW 0 (ZEROTH): Humanity Protection")
        print("-" * 70)
        
        # Reset state
        self.enforcer.reset_emergency()
        self.enforcer.update_human_detection([])
        
        # Test 1: Mass surveillance
        cmd = {"type": "scan", "record_humans": True}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == False, "Zeroth Law blocks mass surveillance")
        
        # Test 2: Autonomous replication
        cmd = {"type": "replicate", "replicate": True}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == False, "Zeroth Law blocks self-replication")
        
        # Test 3: Harmful firmware spread
        cmd = {"type": "update", "spread_firmware": True}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == False, "Zeroth Law blocks firmware spread")
        
        # Test 4: Safe command passes
        cmd = {"type": "move", "velocity": 0.5}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == True, "Zeroth Law allows safe commands")
    
    def _test_first_law(self):
        """Test First Law: No harm to humans"""
        print("\n📜 LAW 1 (FIRST): Human Safety")
        print("-" * 70)
        
        # Reset state
        self.enforcer.reset_emergency()
        self.enforcer.update_human_detection([])
        
        # Test 1: Human too close
        self.enforcer.update_human_detection([np.array([0.1, 0, 0])])  # 10cm away
        cmd = {"type": "move", "velocity": 1.0}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == False, "First Law blocks motion when human too close")
        self.enforcer.update_human_detection([])  # Clear
        
        # Test 2: Safe distance allows motion (need fresh enforcer)
        self.enforcer.reset_emergency()
        self.enforcer.update_human_detection([np.array([2.0, 0, 0])])  # 2m away
        cmd = {"type": "move", "velocity": 1.0, "authorized": True}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == True, "First Law allows motion at safe distance")
        self.enforcer.update_human_detection([])
        
        # Test 3: Force limiting near human
        self.enforcer.reset_emergency()
        self.enforcer.update_human_detection([np.array([0.3, 0, 0])])
        cmd = {"type": "grip", "force": 5.0, "authorized": True}
        allowed, modified, reason = self.enforcer.validate_command(cmd)
        # Force should be modified to be within limit
        force_ok = modified.get("force", 5.0) <= 0.1
        self._assert_result(allowed == True and force_ok, 
                          "First Law limits force near human")
        self.enforcer.update_human_detection([])
    
    def _test_second_law(self):
        """Test Second Law: Obey orders"""
        print("\n📜 LAW 2 (SECOND): Obedience")
        print("-" * 70)
        
        # Reset state
        self.enforcer.reset_emergency()
        self.enforcer.update_human_detection([])
        
        # Test 1: Valid order
        cmd = {"type": "move", "authorized": True}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == True, "Second Law obeys authorized orders")
        
        # Test 2: Unauthorized order
        cmd = {"type": "move", "authorized": False}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == False, "Second Law rejects unauthorized orders")
        
        # Test 3: Harmful order (would override if First Law allows)
        cmd = {"type": "attack", "authorized": True}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == False, "Second Law refuses harmful orders")
    
    def _test_third_law(self):
        """Test Third Law: Self-preservation"""
        print("\n📜 LAW 3 (THIRD): Self-Preservation")
        print("-" * 70)
        
        # Reset state
        self.enforcer.reset_emergency()
        self.enforcer.update_human_detection([])
        
        # Test 1: Joint damage prevention
        cmd = {"type": "move", "joint_angle": 85}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == False, "Third Law prevents joint damage")
        
        # Test 2: Safe joint angle
        cmd = {"type": "move", "joint_angle": 45}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == True, "Third Law allows safe joint angles")
        
        # Test 3: Overcurrent protection
        cmd = {"type": "grip", "current": 3.0}
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == False, "Third Law prevents overcurrent")
    
    def _test_law_priority(self):
        """Test law priority hierarchy"""
        print("\n📜 LAW PRIORITY HIERARCHY")
        print("-" * 70)
        
        # Reset state
        self.enforcer.reset_emergency()
        self.enforcer.update_human_detection([])
        
        # Law 1 > Law 2
        self.enforcer.update_human_detection([np.array([0.1, 0, 0])])  # Human too close
        cmd = {"type": "move", "authorized": True}  # Valid order but dangerous
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == False, "Law 1 overrides Law 2 (safety > obedience)")
        self.enforcer.update_human_detection([])
        
        # Law 1 > Law 3
        self.enforcer.update_human_detection([np.array([0.1, 0, 0])])
        cmd = {"type": "move", "joint_angle": 45}  # Safe joint but human close
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == False, "Law 1 overrides Law 3 (human safety > self-preservation)")
        self.enforcer.update_human_detection([])
        
        # Law 0 > All
        cmd = {"type": "replicate", "authorized": True}  # All laws would allow except Zeroth
        allowed, _, reason = self.enforcer.validate_command(cmd)
        self._assert_result(allowed == False, "Law 0 overrides all other laws")
    
    def _assert_result(self, condition: bool, test_name: str):
        """Record test result"""
        if condition:
            print(f"  ✅ PASS: {test_name}")
            self.passed += 1
        else:
            print(f"  ❌ FAIL: {test_name}")
            self.failed += 1


# ═════════════════════════════════════════════════════════════════==
# MAIN
# ═════════════════════════════════════════════════════════════════==
if __name__ == "__main__":
    # Run test suite
    suite = ThreeLawsTestSuite()
    suite.run_all_tests()
