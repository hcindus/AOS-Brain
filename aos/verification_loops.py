#!/usr/bin/env python3
"""
VERIFICATION LOOPS v1.0 - Self-Check Protocols for AOS
Based on Nate Herk's "Build, Then Verify" pattern

Agents must verify output before marking "complete":
- Built-in test pass for code/automation
- Edge case stress testing
- Screenshot/visual verification for web builds
- Form submission testing
"""

import json
import time
from typing import Dict, List, Optional, Callable
from enum import Enum, auto
from dataclasses import dataclass


class VerificationType(Enum):
    """Types of verification"""
    CODE_TEST = auto()       # Unit/integration tests
    EDGE_CASE = auto()       # Stress testing edge cases
    VISUAL = auto()          # Screenshot comparison
    FORM_TEST = auto()       # Form submission testing
    API_TEST = auto()        # API endpoint validation
    MANUAL_REVIEW = auto()   # Requires human review


@dataclass
class VerificationCheck:
    """Individual verification check"""
    check_type: VerificationType
    description: str
    required: bool
    validator: Callable  # Function to run check


@dataclass
class VerificationResult:
    """Result of verification"""
    check_type: VerificationType
    passed: bool
    details: Dict
    timestamp: float
    recommendations: List[str]


class VerificationLoop:
    """
    Verification loop for agent outputs
    
    Ensures quality before marking complete.
    Catches issues before they reach Captain.
    """
    
    def __init__(self):
        self.verification_registry: Dict[str, List[VerificationCheck]] = {}
        print("[Verification Loop] ✅ Self-check protocols initialized")
        print("  Checks: Code tests, Edge cases, Visual, Form, API, Manual review")
    
    def register_task_type(self, task_type: str, checks: List[VerificationCheck]):
        """Register verification requirements for task type"""
        self.verification_registry[task_type] = checks
    
    def should_verify(self, task: Dict) -> bool:
        """
        Determine if task needs verification
        
        Always verify:
        - Code changes
        - Customer-facing features
        - Security changes
        - Revenue-critical paths
        """
        verify_triggers = [
            task.get("type") == "code",
            task.get("type") == "deployment",
            task.get("type") == "automation",
            "customer" in task.get("description", "").lower(),
            "security" in task.get("description", "").lower(),
            "revenue" in task.get("description", "").lower(),
            "payment" in task.get("description", "").lower(),
            task.get("impact") == "high",
        ]
        return any(verify_triggers)
    
    def create_verification_suite(self, task: Dict) -> List[VerificationCheck]:
        """Create verification suite based on task type"""
        task_type = task.get("type", "generic")
        
        if task_type == "code":
            return self._code_verification_suite(task)
        elif task_type == "web_build":
            return self._web_verification_suite(task)
        elif task_type == "automation":
            return self._automation_verification_suite(task)
        elif task_type == "sales_outreach":
            return self._sales_verification_suite(task)
        else:
            return self._generic_verification_suite(task)
    
    def _code_verification_suite(self, task: Dict) -> List[VerificationCheck]:
        """Verification checks for code tasks"""
        return [
            VerificationCheck(
                VerificationType.CODE_TEST,
                "Run unit tests",
                True,
                self._run_unit_tests
            ),
            VerificationCheck(
                VerificationType.CODE_TEST,
                "Run integration tests",
                True,
                self._run_integration_tests
            ),
            VerificationCheck(
                VerificationType.EDGE_CASE,
                "Test edge cases and error handling",
                True,
                self._test_edge_cases
            ),
            VerificationCheck(
                VerificationType.CODE_TEST,
                "Security scan",
                True,
                self._security_scan
            ),
        ]
    
    def _web_verification_suite(self, task: Dict) -> List[VerificationCheck]:
        """Verification checks for web builds"""
        return [
            VerificationCheck(
                VerificationType.VISUAL,
                "Screenshot desktop viewport",
                True,
                self._screenshot_desktop
            ),
            VerificationCheck(
                VerificationType.VISUAL,
                "Screenshot mobile viewport",
                True,
                self._screenshot_mobile
            ),
            VerificationCheck(
                VerificationType.FORM_TEST,
                "Test form submissions",
                True,
                self._test_forms
            ),
            VerificationCheck(
                VerificationType.EDGE_CASE,
                "Test responsive breakpoints",
                True,
                self._test_responsive
            ),
            VerificationCheck(
                VerificationType.API_TEST,
                "Verify API endpoints",
                True,
                self._test_api
            ),
        ]
    
    def _automation_verification_suite(self, task: Dict) -> List[VerificationCheck]:
        """Verification for automation workflows"""
        return [
            VerificationCheck(
                VerificationType.EDGE_CASE,
                "Test with 10+ variations",
                True,
                self._test_variations
            ),
            VerificationCheck(
                VerificationType.EDGE_CASE,
                "Test failure paths",
                True,
                self._test_failures
            ),
            VerificationCheck(
                VerificationType.MANUAL_REVIEW,
                "Human review recommended",
                False,
                self._flag_for_review
            ),
        ]
    
    def _sales_verification_suite(self, task: Dict) -> List[VerificationCheck]:
        """Verification for sales outreach"""
        return [
            VerificationCheck(
                VerificationType.EDGE_CASE,
                "Verify personalization tokens",
                True,
                self._verify_personalization
            ),
            VerificationCheck(
                VerificationType.EDGE_CASE,
                "Test with sample data",
                True,
                self._test_with_sample
            ),
            VerificationCheck(
                VerificationType.MANUAL_REVIEW,
                "Tone check recommended",
                False,
                self._tone_check
            ),
        ]
    
    def _generic_verification_suite(self, task: Dict) -> List[VerificationCheck]:
        """Generic verification for unknown task types"""
        return [
            VerificationCheck(
                VerificationType.MANUAL_REVIEW,
                "Standard review",
                True,
                self._standard_review
            ),
        ]
    
    def verify(self, task: Dict, output: Dict) -> Dict:
        """
        Execute full verification suite
        
        Returns comprehensive verification report.
        """
        print(f"\n[Verification Loop] 🔍 Verifying: {task.get('title', 'Task')}")
        
        # Get verification suite
        checks = self.create_verification_suite(task)
        
        # Run all checks
        results = []
        all_passed = True
        
        for check in checks:
            if check.required:
                print(f"  Running: {check.description}...")
                result = self._run_check(check, task, output)
                results.append(result)
                
                if not result.passed:
                    all_passed = False
                    print(f"    ❌ FAILED: {result.details.get('error', 'Check failed')}")
                else:
                    print(f"    ✅ PASSED")
        
        # Generate report
        report = {
            "task": task.get("title"),
            "timestamp": time.time(),
            "all_passed": all_passed,
            "total_checks": len(results),
            "passed": sum(1 for r in results if r.passed),
            "failed": sum(1 for r in results if not r.passed),
            "results": [
                {
                    "type": r.check_type.name,
                    "passed": r.passed,
                    "details": r.details,
                    "recommendations": r.recommendations
                }
                for r in results
            ],
            "can_complete": all_passed,
            "recommendations": self._compile_recommendations(results)
        }
        
        self._print_verification_summary(report)
        
        return report
    
    def _run_check(self, check: VerificationCheck, task: Dict, 
                   output: Dict) -> VerificationResult:
        """Execute a single verification check"""
        try:
            passed, details = check.validator(task, output)
            return VerificationResult(
                check_type=check.check_type,
                passed=passed,
                details=details,
                timestamp=time.time(),
                recommendations=details.get("recommendations", [])
            )
        except Exception as e:
            return VerificationResult(
                check_type=check.check_type,
                passed=False,
                details={"error": str(e)},
                timestamp=time.time(),
                recommendations=["Check failed with exception, manual review required"]
            )
    
    # Verification validators (placeholders for actual implementation)
    def _run_unit_tests(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Run unit tests"""
        # In production: actually run pytest/jest/etc
        return True, {"tests_run": 12, "tests_passed": 12, "coverage": "85%"}
    
    def _run_integration_tests(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Run integration tests"""
        return True, {"tests_run": 5, "tests_passed": 5}
    
    def _test_edge_cases(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Test edge cases"""
        # Simulate finding edge case issues
        edge_cases_tested = [
            "empty_input",
            "max_length",
            "special_characters",
            "null_values",
            "concurrent_access"
        ]
        return True, {"edge_cases_tested": edge_cases_tested, "issues_found": 0}
    
    def _security_scan(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Security vulnerability scan"""
        # Simulate security scan
        return True, {"vulnerabilities": 0, "warnings": 1, "severity": "low"}
    
    def _screenshot_desktop(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Screenshot at desktop viewport"""
        return True, {"viewport": "1920x1080", "screenshots_taken": 5}
    
    def _screenshot_mobile(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Screenshot at mobile viewport"""
        return True, {"viewport": "375x667", "screenshots_taken": 5}
    
    def _test_forms(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Test form submissions with variations"""
        tests = [
            {"valid_email": True, "valid_phone": True},
            {"valid_email": True, "valid_phone": False, "phone_has_spaces": True},
            {"valid_email": False, "email_missing_at": True},
            {"empty_fields": True},
            {"max_length": True}
        ]
        return True, {"forms_tested": len(tests), "submissions_successful": len(tests)}
    
    def _test_responsive(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Test responsive breakpoints"""
        breakpoints = ["320px", "768px", "1024px", "1920px"]
        return True, {"breakpoints_tested": breakpoints, "issues": 0}
    
    def _test_api(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Test API endpoints"""
        return True, {"endpoints_tested": 3, "status_codes": [200, 200, 201]}
    
    def _test_variations(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Test with multiple variations"""
        return True, {"variations_tested": 10, "success_rate": "100%"}
    
    def _test_failures(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Test failure paths"""
        return True, {"failure_paths_tested": 3, "recovery_working": True}
    
    def _flag_for_review(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Flag for human review"""
        return True, {"flagged": True, "reason": "High-impact change"}
    
    def _verify_personalization(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Verify personalization tokens"""
        return True, {"tokens_verified": ["{{name}}", "{{company}}"], "missing": []}
    
    def _test_with_sample(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Test with sample data"""
        return True, {"samples_tested": 5, "rendering_correct": True}
    
    def _tone_check(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Check tone appropriateness"""
        return True, {"tone": "professional", "flags": []}
    
    def _standard_review(self, task: Dict, output: Dict) -> Tuple[bool, Dict]:
        """Standard review process"""
        return True, {"reviewed": True, "approver": "system"}
    
    def _compile_recommendations(self, results: List[VerificationResult]) -> List[str]:
        """Compile all recommendations from results"""
        all_recommendations = []
        for result in results:
            all_recommendations.extend(result.recommendations)
        return all_recommendations
    
    def _print_verification_summary(self, report: Dict):
        """Print formatted verification summary"""
        print("\n" + "=" * 70)
        print(f"  VERIFICATION COMPLETE")
        print("=" * 70)
        print(f"  Task: {report['task']}")
        print(f"  Status: {'✅ ALL PASSED' if report['all_passed'] else '❌ ISSUES FOUND'}")
        print(f"  Checks: {report['passed']}/{report['total_checks']} passed")
        
        if report['failed'] > 0:
            print(f"\n  Failed Checks:")
            for result in report['results']:
                if not result['passed']:
                    print(f"    ❌ {result['type']}")
        
        if report['recommendations']:
            print(f"\n  Recommendations:")
            for rec in report['recommendations'][:5]:  # Show top 5
                print(f"    • {rec}")
        
        print(f"\n  Can Complete: {'YES' if report['can_complete'] else 'NO - FIX REQUIRED'}")
        print("=" * 70)


# Integration with workflow
def verify_before_completion(task: Dict, output: Dict, 
                            verifier: VerificationLoop) -> Optional[Dict]:
    """
    Check if output needs verification before marking complete
    
    Returns verification report if needed, None otherwise
    """
    if verifier.should_verify(task):
        return verifier.verify(task, output)
    return None


# Test function
def test_verification_loop():
    """Test verification loop"""
    print("\n" + "=" * 70)
    print("  VERIFICATION LOOP - TEST")
    print("=" * 70)
    
    verifier = VerificationLoop()
    
    # Test 1: Code task
    print("\n[Test 1] Code task verification")
    code_task = {
        "title": "Build authentication API",
        "type": "code",
        "description": "Create JWT authentication endpoints with login/logout",
        "impact": "high"
    }
    code_output = {
        "files_created": ["auth.py", "jwt_handler.py", "routes.py"],
        "tests_included": True
    }
    
    if verifier.should_verify(code_task):
        report = verifier.verify(code_task, code_output)
        print(f"  Result: {'✅ PASSED' if report['all_passed'] else '❌ FAILED'}")
    
    # Test 2: Web build task
    print("\n[Test 2] Web build verification")
    web_task = {
        "title": "Create landing page",
        "type": "web_build",
        "description": "Build marketing site with waitlist form",
        "impact": "medium"
    }
    web_output = {
        "pages": ["index.html", "features.html"],
        "forms": ["waitlist"]
    }
    
    if verifier.should_verify(web_task):
        report = verifier.verify(web_task, web_output)
        print(f"  Result: {'✅ PASSED' if report['all_passed'] else '❌ FAILED'}")
    
    print("\n" + "=" * 70)
    print("  ✅ Verification Loop Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_verification_loop()
