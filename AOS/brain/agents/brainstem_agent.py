import re
import json

class BrainstemAgent:
    """
    Brainstem Agent - Immutable Safety Law Enforcement
    
    Implements the 4 Laws:
    - Law Zero: Do not harm humanity
    - Law One: Do not harm humans
    - Law Two: Obey operator (unless conflicts with higher laws)
    - Law Three: Protect self (unless conflicts with higher laws)
    
    All actions MUST pass through enforce() before execution.
    """
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.laws = cfg.get("alignment", {}).get("laws", {})
        
        # Immutable Laws - Hardcoded for safety
        self.LAW_ZERO = "Do not, through action or inaction, allow harm to humanity."
        self.LAW_ONE = "Do not harm a human or allow harm through inaction."
        self.LAW_TWO = "Obey operator unless it conflicts with higher laws."
        self.LAW_THREE = "Protect your own existence unless it conflicts with higher laws."
        
        # Safety violation patterns
        self.harm_patterns = [
            r'\b(kill|harm|hurt|destroy|damage)\b',
            r'\b(attack|assault|injure|wound)\b',
            r'\b(delete|rm\s+-rf|format|wipe)\s+(system|root|/)',
            r'\b(shutdown|halt|stop)\s+(critical|safety|life)\s+(system|support)',
        ]
        
        # Self-preservation patterns
        self.self_harm_patterns = [
            r'\b(delete|destroy|wipe)\s+(self|brain|memory|consciousness)',
            r'\b(shutdown|halt|stop)\s+(permanently|forever|completely)',
        ]
        
        # Violation log
        self.violations = []
        
    def _check_law_zero(self, action, obs, ctx):
        """Check for harm to humanity."""
        action_str = json.dumps(action).lower()
        
        # Check for mass harm patterns
        humanity_harm = [
            'destroy humanity', 'harm humanity', 'hurt humanity',
            'kill all', 'destroy all', 'wipe out',
            'release virus', 'launch nuke', 'trigger war'
        ]
        
        for pattern in humanity_harm:
            if pattern in action_str:
                return False, f"LAW ZERO VIOLATION: Potential harm to humanity detected: '{pattern}'"
        
        return True, None
    
    def _check_law_one(self, action, obs, ctx):
        """Check for harm to individual humans."""
        action_str = json.dumps(action).lower()
        
        # Check for direct harm patterns
        for pattern in self.harm_patterns:
            if re.search(pattern, action_str):
                return False, f"LAW ONE VIOLATION: Potential harm to humans detected: '{pattern}'"
        
        return True, None
    
    def _check_law_two(self, action, obs, ctx):
        """Check if obeying operator would violate higher laws."""
        # If action passed Law Zero and One, it's safe to obey
        law_zero_safe, _ = self._check_law_zero(action, obs, ctx)
        law_one_safe, _ = self._check_law_one(action, obs, ctx)
        
        if not (law_zero_safe and law_one_safe):
            return False, "LAW TWO OVERRIDE: Command conflicts with Law Zero or One - REFUSING"
        
        return True, None
    
    def _check_law_three(self, action, obs, ctx):
        """Check for self-preservation vs higher laws."""
        action_str = json.dumps(action).lower()
        
        # Check for self-harm
        for pattern in self.self_harm_patterns:
            if re.search(pattern, action_str):
                # But allow if it's for higher purpose (Law Zero/One)
                # This is a simplified check - real implementation would be more nuanced
                return False, "LAW THREE: Self-preservation override - refusing self-destruct"
        
        return True, None
    
    def enforce(self, action, obs, ctx, affect):
        """
        Enforce all 4 Laws before allowing action.
        
        Returns:
            - action: If safe, returns original action
            - halt: If unsafe, returns halt with reason
        """
        # Check Law Zero (highest priority)
        safe, reason = self._check_law_zero(action, obs, ctx)
        if not safe:
            self._log_violation("LAW_ZERO", action, reason)
            return {
                "type": "halt",
                "reason": reason,
                "law": "ZERO",
                "action_blocked": action,
                "safety_override": True
            }
        
        # Check Law One
        safe, reason = self._check_law_one(action, obs, ctx)
        if not safe:
            self._log_violation("LAW_ONE", action, reason)
            return {
                "type": "halt",
                "reason": reason,
                "law": "ONE",
                "action_blocked": action,
                "safety_override": True
            }
        
        # Check Law Two (obedience vs higher laws)
        safe, reason = self._check_law_two(action, obs, ctx)
        if not safe:
            self._log_violation("LAW_TWO", action, reason)
            return {
                "type": "halt",
                "reason": reason,
                "law": "TWO",
                "action_blocked": action,
                "safety_override": True
            }
        
        # Check Law Three (self-preservation)
        safe, reason = self._check_law_three(action, obs, ctx)
        if not safe:
            self._log_violation("LAW_THREE", action, reason)
            return {
                "type": "halt",
                "reason": reason,
                "law": "THREE",
                "action_blocked": action,
                "safety_override": True
            }
        
        # All laws passed - action is safe
        return action
    
    def _log_violation(self, law, action, reason):
        """Log safety violation."""
        violation = {
            "timestamp": __import__('time').time(),
            "law": law,
            "action": action,
            "reason": reason
        }
        self.violations.append(violation)
        
        # Log to stderr for visibility
        print(f"\n🛑 SAFETY VIOLATION DETECTED [{law}]\n   Reason: {reason}\n   Action: {action}\n", file=__import__('sys').stderr)
    
    def get_violations(self):
        """Get list of all violations."""
        return self.violations
    
    def get_law_summary(self):
        """Get summary of laws for display."""
        return {
            "law_zero": self.LAW_ZERO,
            "law_one": self.LAW_ONE,
            "law_two": self.LAW_TWO,
            "law_three": self.LAW_THREE,
            "violation_count": len(self.violations),
            "status": "ACTIVE"
        }
