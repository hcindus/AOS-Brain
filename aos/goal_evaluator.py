#!/usr/bin/env python3
"""
GOAL EVALUATOR v1.0 - /goal Command Pattern
Based on Nate Herk's completion criteria pattern

Features:
- /goal command sets completion criteria upfront
- Separate evaluator judges "done" vs "not done"
- Prevents premature completion
- Forces explicit success criteria
"""

import json
import time
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class GoalStatus(Enum):
    PENDING = "pending"      # Not started
    IN_PROGRESS = "in_progress"  # Working
    UNDER_REVIEW = "under_review"  # Awaiting evaluation
    COMPLETED = "completed"  # Passed evaluation
    FAILED = "failed"        # Failed evaluation
    NEEDS_WORK = "needs_work"  # Partial, needs more


@dataclass
class CompletionCriteria:
    """Specific criteria for goal completion"""
    description: str
    measurable: bool
    expected_outcome: str
    validation_method: str  # How to verify
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Goal:
    """A goal with completion criteria"""
    goal_id: str
    title: str
    description: str
    criteria: List[CompletionCriteria]
    created_at: float
    evaluator_model: str  # Which model evaluates completion
    
    # Runtime state
    status: GoalStatus = GoalStatus.PENDING
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    evaluation_result: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        return {
            "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "criteria": [c.to_dict() for c in self.criteria],
            "created_at": self.created_at,
            "evaluator_model": self.evaluator_model,
            "status": self.status.value,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "evaluation_result": self.evaluation_result
        }


class GoalEvaluator:
    """
    /goal command implementation with separate evaluator
    
    Forces explicit completion criteria before work starts.
    Prevents "feels done" subjective completion.
    """
    
    def __init__(self):
        self.active_goals: Dict[str, Goal] = {}
        self.completed_goals: List[Goal] = []
        
        # Simulated evaluator models
        self.evaluators = {
            "strict": self._strict_evaluator,
            "balanced": self._balanced_evaluator,
            "lenient": self._lenient_evaluator
        }
        
        print("[Goal Evaluator] 🎯 /goal command initialized")
        print("  Evaluators: strict, balanced, lenient")
        print("  Pattern: Set criteria → Execute → Evaluate → Done")
    
    def set_goal(self, title: str, description: str,
                 criteria: List[CompletionCriteria],
                 evaluator: str = "balanced") -> str:
        """
        /goal command - Set goal with completion criteria
        
        Must be called BEFORE work starts.
        """
        goal_id = f"goal_{int(time.time())}_{hash(title) % 10000}"
        
        # Validate evaluator
        if evaluator not in self.evaluators:
            evaluator = "balanced"
        
        goal = Goal(
            goal_id=goal_id,
            title=title,
            description=description,
            criteria=criteria,
            created_at=time.time(),
            evaluator_model=evaluator,
            status=GoalStatus.PENDING
        )
        
        self.active_goals[goal_id] = goal
        
        print(f"\n[Goal Evaluator] 🎯 GOAL SET: {title}")
        print(f"  ID: {goal_id}")
        print(f"  Evaluator: {evaluator}")
        print(f"  Criteria:")
        for i, c in enumerate(criteria, 1):
            print(f"    {i}. {c.description}")
            print(f"       → Validation: {c.validation_method}")
        
        return goal_id
    
    def start_work(self, goal_id: str) -> bool:
        """Mark goal as in progress"""
        if goal_id not in self.active_goals:
            print(f"[Goal Evaluator] ❌ Goal {goal_id} not found")
            return False
        
        goal = self.active_goals[goal_id]
        goal.status = GoalStatus.IN_PROGRESS
        goal.started_at = time.time()
        
        print(f"\n[Goal Evaluator] ▶️  STARTED: {goal.title}")
        print(f"  Working toward {len(goal.criteria)} criteria")
        
        return True
    
    def submit_for_evaluation(self, goal_id: str, 
                             work_product: Dict) -> Dict:
        """
        Submit completed work for evaluation
        
        Separate evaluator judges against criteria.
        Cannot mark done without passing evaluation.
        """
        if goal_id not in self.active_goals:
            return {"error": "Goal not found"}
        
        goal = self.active_goals[goal_id]
        goal.status = GoalStatus.UNDER_REVIEW
        
        print(f"\n[Goal Evaluator] 🔍 SUBMITTED FOR REVIEW: {goal.title}")
        
        # Run evaluation
        evaluator_func = self.evaluators.get(goal.evaluator_model, self._balanced_evaluator)
        evaluation = evaluator_func(goal, work_product)
        
        goal.evaluation_result = evaluation
        
        # Determine final status
        if evaluation["passed"]:
            goal.status = GoalStatus.COMPLETED
            goal.completed_at = time.time()
            self.completed_goals.append(goal)
            del self.active_goals[goal_id]
            print(f"  ✅ PASSED: {evaluation['score']:.0f}%")
        elif evaluation["score"] >= 50:
            goal.status = GoalStatus.NEEDS_WORK
            print(f"  ⚠️  NEEDS WORK: {evaluation['score']:.0f}%")
        else:
            goal.status = GoalStatus.FAILED
            print(f"  ❌ FAILED: {evaluation['score']:.0f}%")
        
        # Print detailed results
        print(f"\n  Criteria Results:")
        for criterion_result in evaluation["criteria_results"]:
            status_icon = "✅" if criterion_result["passed"] else "❌"
            print(f"    {status_icon} {criterion_result['description']}")
            if not criterion_result["passed"]:
                print(f"       Gap: {criterion_result['gap']}")
        
        if evaluation.get("recommendations"):
            print(f"\n  Recommendations:")
            for rec in evaluation["recommendations"]:
                print(f"    • {rec}")
        
        return evaluation
    
    def _strict_evaluator(self, goal: Goal, work_product: Dict) -> Dict:
        """
        Strict evaluator - ALL criteria must pass
        Good for: Security, critical features, customer-facing
        """
        results = []
        all_passed = True
        
        for criterion in goal.criteria:
            # Simulate evaluation
            passed, gap = self._evaluate_criterion(criterion, work_product)
            results.append({
                "description": criterion.description,
                "passed": passed,
                "gap": gap if not passed else None
            })
            if not passed:
                all_passed = False
        
        score = (sum(1 for r in results if r["passed"]) / len(results)) * 100
        
        return {
            "passed": all_passed,  # Must be 100%
            "score": score,
            "criteria_results": results,
            "evaluator": "strict",
            "recommendations": self._generate_recommendations(results) if not all_passed else []
        }
    
    def _balanced_evaluator(self, goal: Goal, work_product: Dict) -> Dict:
        """
        Balanced evaluator - 80% of criteria must pass
        Good for: Most features, improvements
        """
        results = []
        
        for criterion in goal.criteria:
            passed, gap = self._evaluate_criterion(criterion, work_product)
            results.append({
                "description": criterion.description,
                "passed": passed,
                "gap": gap if not passed else None
            })
        
        passed_count = sum(1 for r in results if r["passed"])
        score = (passed_count / len(results)) * 100
        
        # 80% threshold
        passed = score >= 80
        
        return {
            "passed": passed,
            "score": score,
            "criteria_results": results,
            "evaluator": "balanced",
            "recommendations": self._generate_recommendations(results) if not passed else []
        }
    
    def _lenient_evaluator(self, goal: Goal, work_product: Dict) -> Dict:
        """
        Lenient evaluator - 60% of criteria must pass
        Good for: Prototypes, experiments, MVPs
        """
        results = []
        
        for criterion in goal.criteria:
            passed, gap = self._evaluate_criterion(criterion, work_product)
            results.append({
                "description": criterion.description,
                "passed": passed,
                "gap": gap if not passed else None
            })
        
        passed_count = sum(1 for r in results if r["passed"])
        score = (passed_count / len(results)) * 100
        
        # 60% threshold
        passed = score >= 60
        
        return {
            "passed": passed,
            "score": score,
            "criteria_results": results,
            "evaluator": "lenient",
            "recommendations": self._generate_recommendations(results) if not passed else []
        }
    
    def _evaluate_criterion(self, criterion: CompletionCriteria, 
                         work_product: Dict) -> Tuple[bool, Optional[str]]:
        """
        Evaluate single criterion against work product
        
        In production, this would use actual validation logic
        """
        # Check if validation method exists in work product
        if criterion.validation_method in work_product:
            result = work_product[criterion.validation_method]
            if isinstance(result, bool):
                return result, None if result else "Not implemented"
            elif isinstance(result, dict):
                return result.get("passed", False), result.get("error", "Unknown error")
        
        # Default: assume passed for demo
        return True, None
    
    def _generate_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate recommendations based on failed criteria"""
        recommendations = []
        
        failed = [r for r in results if not r["passed"]]
        for fail in failed:
            if fail.get("gap"):
                recommendations.append(f"Fix: {fail['description']} - {fail['gap']}")
            else:
                recommendations.append(f"Complete: {fail['description']}")
        
        return recommendations[:5]  # Top 5
    
    def get_goal_status(self, goal_id: str) -> Optional[Dict]:
        """Get current status of goal"""
        if goal_id in self.active_goals:
            return self.active_goals[goal_id].to_dict()
        
        for goal in self.completed_goals:
            if goal.goal_id == goal_id:
                return goal.to_dict()
        
        return None
    
    def list_active_goals(self) -> List[Dict]:
        """List all active goals"""
        return [g.to_dict() for g in self.active_goals.values()]
    
    def get_stats(self) -> Dict:
        """Get completion statistics"""
        total = len(self.completed_goals) + len(self.active_goals)
        completed = len(self.completed_goals)
        
        return {
            "total_goals": total,
            "completed": completed,
            "active": len(self.active_goals),
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }


# Integration with Chief of Staff
def goal_command(objective: str, evaluator: GoalEvaluator) -> str:
    """
    /goal command - Parse objective and set completion criteria
    
    Usage: /goal "Build X with criteria A, B, C"
    """
    # Parse objective into criteria
    # In production, use LLM to extract criteria
    criteria = [
        CompletionCriteria(
            description="Core functionality works",
            measurable=True,
            expected_outcome="Feature performs primary function",
            validation_method="test_core_function"
        ),
        CompletionCriteria(
            description="Edge cases handled",
            measurable=True,
            expected_outcome="No crashes on invalid input",
            validation_method="test_edge_cases"
        ),
        CompletionCriteria(
            description="Documentation complete",
            measurable=True,
            expected_outcome="README updated with usage",
            validation_method="check_documentation"
        )
    ]
    
    return evaluator.set_goal(
        title=objective[:50],
        description=objective,
        criteria=criteria,
        evaluator="balanced"
    )


# Test function
def test_goal_evaluator():
    """Test goal evaluator"""
    print("\n" + "=" * 70)
    print("  GOAL EVALUATOR - TEST")
    print("=" * 70)
    
    ge = GoalEvaluator()
    
    # Test 1: Set goal
    print("\n[Test 1] Set goal with criteria")
    criteria = [
        CompletionCriteria(
            description="API endpoints return 200 OK",
            measurable=True,
            expected_outcome="All endpoints respond correctly",
            validation_method="test_api_endpoints"
        ),
        CompletionCriteria(
            description="Authentication working",
            measurable=True,
            expected_outcome="Login/logout flow works",
            validation_method="test_auth_flow"
        ),
        CompletionCriteria(
            description="Database connected",
            measurable=True,
            expected_outcome="Reads/writes succeed",
            validation_method="test_db_connection"
        )
    ]
    
    goal_id = ge.set_goal(
        "Build REST API",
        "Create FastAPI REST API with auth and database",
        criteria,
        "balanced"
    )
    
    # Test 2: Start work
    print("\n[Test 2] Start work")
    ge.start_work(goal_id)
    
    # Test 3: Submit passing work
    print("\n[Test 3] Submit passing evaluation")
    work_product = {
        "test_api_endpoints": {"passed": True},
        "test_auth_flow": {"passed": True},
        "test_db_connection": {"passed": True}
    }
    
    result = ge.submit_for_evaluation(goal_id, work_product)
    print(f"\n  Final: {result['status']}")
    
    # Test 4: Set another goal with failing work
    print("\n[Test 4] Set goal with partial completion")
    criteria2 = [
        CompletionCriteria(
            description="Feature A complete",
            measurable=True,
            expected_outcome="A works",
            validation_method="test_a"
        ),
        CompletionCriteria(
            description="Feature B complete",
            measurable=True,
            expected_outcome="B works",
            validation_method="test_b"
        ),
        CompletionCriteria(
            description="Feature C complete",
            measurable=True,
            expected_outcome="C works",
            validation_method="test_c"
        )
    ]
    
    goal_id2 = ge.set_goal("Build features A, B, C", "Multiple features", criteria2)
    ge.start_work(goal_id2)
    
    partial_work = {
        "test_a": {"passed": True},
        "test_b": {"passed": True},
        "test_c": {"passed": False, "error": "Not implemented yet"}
    }
    
    result2 = ge.submit_for_evaluation(goal_id2, partial_work)
    
    # Stats
    print("\n[Test 5] Stats")
    stats = ge.get_stats()
    print(f"  Total goals: {stats['total_goals']}")
    print(f"  Completed: {stats['completed']}")
    print(f"  Completion rate: {stats['completion_rate']:.0f}%")
    
    print("\n" + "=" * 70)
    print("  ✅ Goal Evaluator Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_goal_evaluator()
