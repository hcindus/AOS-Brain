#!/usr/bin/env python3
"""
AOS KIDNEYS HOLD OUT v1.0 - Blind Validation Pattern
Strong DM-inspired: Validator has NO knowledge of implementation

Key Principle: Eliminate sycophantic bias by making validation blind.
The validator doesn't know what was built - it only evaluates output quality.
"""

import time
import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum, auto


class ValidationState(Enum):
    """States for blind validation"""
    PENDING = auto()      # Awaiting validation
    VALIDATING = auto()   # In blind validation
    PASSED = auto()       # Validation successful
    FAILED = auto()       # Validation failed
    NEEDS_FIX = auto()    # Failed but fixable


@dataclass
class ValidationTask:
    """A validation task with implementation masked"""
    task_id: str
    timestamp: float
    
    # The output to validate (ONLY this is exposed to validator)
    output_content: str
    output_type: str  # code/text/decision/etc
    
    # Metadata that IS available to validator
    requirements: str  # What was supposed to be built
    constraints: str   # Constraints and rules
    
    # Implementation details that are HIDDEN from validator
    _implementation_plan: str = ""  # Hidden
    _original_prompt: str = ""      # Hidden
    _developer_notes: str = ""      # Hidden
    
    # Validation results
    validation_state: str = "PENDING"
    validation_score: float = 0.0
    validation_feedback: str = ""
    
    def __post_init__(self):
        if not self.task_id:
            import uuid
            self.task_id = str(uuid.uuid4())[:8]
        if self.timestamp == 0.0:
            self.timestamp = time.time()


@dataclass
class BlindValidationResult:
    """Result of blind validation"""
    task_id: str
    passed: bool
    score: float  # 0.0-1.0
    feedback: str
    issues_found: List[str]
    
    # Comparison to requirements (without seeing implementation)
    requirements_met: Dict[str, bool]  # Which requirements were met
    constraint_violations: List[str]    # Which constraints were violated


class HoldOutKidneysV1:
    """
    Blind Validation System
    
    Like Strong DM's "hold out" pattern:
    - Implementation team delivers output
    - Validation team evaluates ONLY the output
    - No communication of implementation details
    - Pure assessment of "does this solve the problem?"
    """
    
    def __init__(self, state_dir: str = "/var/lib/aos/brain_state"):
        self.state_dir = state_dir
        
        # Validation queues
        self.pending_validation: Dict[str, ValidationTask] = {}
        self.validation_results: Dict[str, BlindValidationResult] = {}
        
        # Statistics
        self.stats = {
            "total_validated": 0,
            "passed": 0,
            "failed": 0,
            "avg_score": 0.0
        }
        
        print(f"[Hold Out Kidneys v1.0] Initialized")
        print(f"  🎭 Blind validation active")
        print(f"  🚫 Implementation bias eliminated")
    
    def submit_for_validation(self, 
                             output_content: str,
                             output_type: str,
                             requirements: str,
                             constraints: str,
                             implementation_plan: str = "",  # Hidden from validator
                             original_prompt: str = "") -> ValidationTask:
        """
        Submit output for blind validation
        
        The implementation details are stored but NOT passed to validator.
        """
        import uuid
        task = ValidationTask(
            task_id=str(uuid.uuid4())[:8],
            timestamp=time.time(),
            output_content=output_content,
            output_type=output_type,
            requirements=requirements,
            constraints=constraints,
            _implementation_plan=implementation_plan,  # Hidden
            _original_prompt=original_prompt,          # Hidden
            validation_state="PENDING"
        )
        
        self.pending_validation[task.task_id] = task
        
        print(f"\n[Hold Out Kidneys] 🎭 Task {task.task_id} queued for blind validation")
        print(f"  Type: {output_type}")
        print(f"  Requirements: {requirements[:60]}...")
        print(f"  🚫 Implementation plan HIDDEN from validator")
        
        return task
    
    def get_validation_package(self, task_id: str) -> Optional[Dict]:
        """
        Get the validation package (ONLY what validator should see)
        
        This strips out all implementation details - only output,
        requirements, and constraints are visible.
        """
        if task_id not in self.pending_validation:
            return None
        
        task = self.pending_validation[task_id]
        
        # ONLY return what validator needs - NO implementation details
        return {
            "task_id": task.task_id,
            "output_content": task.output_content,
            "output_type": task.output_type,
            "requirements": task.requirements,
            "constraints": task.constraints,
            "timestamp": task.timestamp
            # NOTE: _implementation_plan and _original_prompt are INTENTIONALLY omitted
        }
    
    def perform_blind_validation(self, task_id: str) -> BlindValidationResult:
        """
        Perform blind validation on a task
        
        Simulates the "hold out" pattern:
        1. Get validation package (without implementation details)
        2. Evaluate output against requirements ONLY
        3. Return assessment without bias
        """
        if task_id not in self.pending_validation:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.pending_validation[task_id]
        task.validation_state = "VALIDATING"
        
        print(f"\n[Hold Out Kidneys] 🔍 Performing blind validation on {task_id}")
        print(f"  ❌ Validator CANNOT see implementation plan")
        print(f"  ❌ Validator CANNOT see original prompt")
        print(f"  ✅ Validator ONLY sees output + requirements")
        
        # Get blind package (no implementation details)
        package = self.get_validation_package(task_id)
        
        # Simulate blind validation (in production, this would call actual validator)
        result = self._validate_blind(package)
        
        # Update task
        task.validation_state = "PASSED" if result.passed else "FAILED"
        task.validation_score = result.score
        task.validation_feedback = result.feedback
        
        # Store result
        self.validation_results[task_id] = result
        
        # Update stats
        self.stats["total_validated"] += 1
        if result.passed:
            self.stats["passed"] += 1
        else:
            self.stats["failed"] += 1
        
        # Calculate running average
        total_score = sum(r.score for r in self.validation_results.values())
        self.stats["avg_score"] = total_score / len(self.validation_results)
        
        print(f"\n[Hold Out Kidneys] ✅ Validation complete for {task_id}")
        print(f"  Score: {result.score:.2f}")
        print(f"  Passed: {result.passed}")
        print(f"  Issues: {len(result.issues_found)}")
        
        return result
    
    def _validate_blind(self, package: Dict) -> BlindValidationResult:
        """
        Simulate blind validation
        
        In production, this would:
        1. Send output to separate validation agent
        2. Agent has NO context of implementation
        3. Agent evaluates purely on "does this meet requirements?"
        4. Return assessment
        """
        task_id = package["task_id"]
        output = package["output_content"]
        requirements = package["requirements"]
        constraints = package["constraints"]
        
        # Simulate validation scoring
        # In production, this would be actual AI validation
        score = 0.0
        issues = []
        requirements_met = {}
        constraint_violations = []
        
        # Check if output exists
        if len(output) > 50:
            score += 0.3
        else:
            issues.append("Output too short")
        
        # Check against requirements (simplified)
        if "error" in output.lower():
            score += 0.2
            requirements_met["handles_errors"] = True
        else:
            requirements_met["handles_errors"] = False
        
        if "function" in output.lower() or "def " in output:
            score += 0.3
            requirements_met["has_structure"] = True
        else:
            requirements_met["has_structure"] = False
        
        # Check constraints
        if len(output) > 1000 and "concise" in constraints.lower():
            constraint_violations.append("Too verbose for 'concise' constraint")
            score -= 0.1
        
        # Ensure score in bounds
        score = max(0.0, min(1.0, score))
        
        # Determine pass/fail
        passed = score >= 0.6
        
        feedback = f"Score: {score:.2f}. "
        if passed:
            feedback += "Output meets requirements."
        else:
            feedback += f"Issues found: {', '.join(issues)}"
        
        return BlindValidationResult(
            task_id=task_id,
            passed=passed,
            score=score,
            feedback=feedback,
            issues_found=issues,
            requirements_met=requirements_met,
            constraint_violations=constraint_violations
        )
    
    def compare_to_non_blind(self, task_id: str) -> Dict:
        """
        Compare blind validation vs what non-blind validation would say
        
        Demonstrates the bias elimination.
        """
        if task_id not in self.pending_validation:
            return {"error": "Task not found"}
        
        task = self.pending_validation[task_id]
        blind_result = self.validation_results.get(task_id)
        
        if not blind_result:
            return {"error": "Validation not performed yet"}
        
        # Simulate what non-blind validation would say
        # (knowing implementation details introduces bias)
        non_blind_score = blind_result.score + 0.15  # Bias: +15% for knowing context
        non_blind_score = min(1.0, non_blind_score)
        
        return {
            "task_id": task_id,
            "blind_score": blind_result.score,
            "non_blind_score": non_blind_score,
            "bias": non_blind_score - blind_result.score,
            "bias_percentage": f"{(non_blind_score - blind_result.score) * 100:.1f}%",
            "conclusion": "Blind validation removes grade inflation from context awareness"
        }
    
    def get_validation_summary(self) -> Dict:
        """Get summary of all validations"""
        return {
            "stats": self.stats,
            "pending_count": len(self.pending_validation),
            "completed_count": len(self.validation_results),
            "pass_rate": self.stats["passed"] / max(self.stats["total_validated"], 1),
            "recent_validations": [
                {
                    "task_id": tid,
                    "score": r.score,
                    "passed": r.passed
                }
                for tid, r in list(self.validation_results.items())[-5:]
            ]
        }


# Test
def test_hold_out_kidneys():
    """Test blind validation pattern"""
    print("\n" + "=" * 70)
    print("  🎭 HOLD OUT KIDNEYS v1.0 - Blind Validation Test")
    print("=" * 70)
    
    hok = HoldOutKidneysV1()
    
    # Simulate an implementation
    print("\n[1] Submitting implementation for validation...")
    
    implementation_code = """
    def process_data(data):
        try:
            result = data["key"] * 2
            return {"success": True, "result": result}
        except KeyError as e:
            return {"success": False, "error": str(e)}
    """
    
    task = hok.submit_for_validation(
        output_content=implementation_code,
        output_type="code",
        requirements="Create a function that doubles data values with error handling",
        constraints="Keep it concise, handle KeyError specifically",
        implementation_plan="Step 1: Extract data, Step 2: Multiply by 2, Step 3: Return",  # HIDDEN
        original_prompt="Build a data processor"  # HIDDEN
    )
    
    print(f"\n  Task ID: {task.task_id}")
    print(f"  Implementation plan: {task._implementation_plan}")
    print(f"  (This is HIDDEN from validator)")
    
    # Get validation package (what validator sees)
    print("\n[2] Getting validation package (validator's view)...")
    package = hok.get_validation_package(task.task_id)
    print(f"  Package keys: {list(package.keys())}")
    print(f"  ❌ 'implementation_plan' NOT in package: {'_implementation_plan' not in package}")
    print(f"  ❌ 'original_prompt' NOT in package: {'_original_prompt' not in package}")
    print(f"  ✅ 'output_content' in package: {'output_content' in package}")
    
    # Perform blind validation
    print("\n[3] Performing blind validation...")
    result = hok.perform_blind_validation(task.task_id)
    
    print(f"\n  Score: {result.score:.2f}")
    print(f"  Passed: {result.passed}")
    print(f"  Requirements met: {result.requirements_met}")
    print(f"  Constraint violations: {result.constraint_violations}")
    
    # Compare to non-blind
    print("\n[4] Comparing blind vs non-blind validation...")
    comparison = hok.compare_to_non_blind(task.task_id)
    print(f"  Blind score: {comparison['blind_score']:.2f}")
    print(f"  Non-blind score: {comparison['non_blind_score']:.2f}")
    print(f"  Bias: {comparison['bias_percentage']}")
    
    # Summary
    print("\n[5] Validation summary...")
    summary = hok.get_validation_summary()
    print(f"  Total validated: {summary['stats']['total_validated']}")
    print(f"  Pass rate: {summary['pass_rate']:.1%}")
    print(f"  Avg score: {summary['stats']['avg_score']:.2f}")
    
    print("\n" + "=" * 70)
    print("  ✅ Hold Out Kidneys v1.0 Test Complete")
    print("=" * 70)
    print("\n  Key Achievement:")
    print("    🎭 Validator has ZERO knowledge of implementation")
    print("    🚫 No sycophantic bias (can't be swayed by intent)")
    print("    ✅ Pure assessment of output quality vs requirements")
    
    return True


if __name__ == "__main__":
    test_hold_out_kidneys()
