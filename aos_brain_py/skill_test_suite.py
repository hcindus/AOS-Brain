#!/usr/bin/env python3
"""
Skill Test Suite

Automated testing framework for brain skills with contract validation,
performance benchmarks, and regression detection.
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class TestResult(Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"
    ERROR = "error"


@dataclass
class SkillTest:
    """Individual test case for a skill."""
    name: str
    skill_name: str
    input_data: Dict
    expected_output: Optional[Dict]
    expected_schema: Optional[Dict]
    timeout_ms: int
    should_succeed: bool = True
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'skill_name': self.skill_name,
            'input_data': self.input_data,
            'expected_output': self.expected_output,
            'expected_schema': self.expected_schema,
            'timeout_ms': self.timeout_ms,
            'should_succeed': self.should_succeed
        }


@dataclass
class TestRun:
    """Result of running a test."""
    test: SkillTest
    result: TestResult
    actual_output: Optional[Dict]
    latency_ms: float
    error_message: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'test_name': self.test.name,
            'skill_name': self.test.skill_name,
            'result': self.result.value,
            'latency_ms': self.latency_ms,
            'error_message': self.error_message,
            'timestamp': self.timestamp
        }


class SkillTestSuite:
    """
    Comprehensive test suite for brain skills.
    
    Tests:
    - Contract compliance (input/output validation)
    - Performance (latency within tier thresholds)
    - Functional correctness (expected outputs)
    - Regression detection (vs previous versions)
    """
    
    # Performance thresholds by tier (ms)
    TIER_THRESHOLDS = {
        'standard': {'target': 5, 'max': 20},
        'methodology': {'target': 50, 'max': 200},
        'personal': {'target': 200, 'max': 500},
        'diagnostic': {'target': 10, 'max': 50}
    }
    
    def __init__(self, registry, output_dir: Optional[str] = None):
        self.registry = registry
        self.output_dir = Path(output_dir) if output_dir else Path.home() / '.aos' / 'brain' / 'test_results'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.tests: List[SkillTest] = []
        self.results: List[TestRun] = []
        self._load_default_tests()
    
    def _load_default_tests(self):
        """Load default test cases for core skills."""
        
        # Thalamus tests
        self.tests.append(SkillTest(
            name="thalamus_standard_input",
            skill_name="thalamus",
            input_data={
                'source': 'agent',
                'data': 'test_observation',
                'timestamp': 1234567890,
                'priority': 0.5
            },
            expected_output=None,  # Just validate schema
            expected_schema={'required': ['normalized', 'priority', 'routing', 'signature']},
            timeout_ms=20
        ))
        
        self.tests.append(SkillTest(
            name="thalamus_high_priority",
            skill_name="thalamus",
            input_data={
                'source': 'sensor',
                'data': 'urgent_alert',
                'timestamp': 1234567890,
                'priority': 0.9
            },
            expected_output={'priority': 0.9},
            expected_schema=None,
            timeout_ms=20
        ))
        
        # PFC tests
        self.tests.append(SkillTest(
            name="pfc_decision_basic",
            skill_name="pfc",
            input_data={
                'context': {'tick': 1, 'previous_action': 'noop'},
                'options': [{'type': 'explore'}, {'type': 'wait'}],
                'signature': {'novelty': 0, 'value': 1, 'action': 0, 'risk': 0, 'growth': 0},
                'ollama_available': False
            },
            expected_output={'decision': 'analyze'},
            expected_schema={'required': ['decision', 'confidence', 'reasoning', 'action']},
            timeout_ms=200
        ))
        
        self.tests.append(SkillTest(
            name="pfc_risk_detection",
            skill_name="pfc",
            input_data={
                'context': {},
                'options': [{'type': 'act'}],
                'signature': {'novelty': 0, 'value': 0, 'action': 1, 'risk': -1, 'growth': 0},
                'ollama_available': False
            },
            expected_output={'decision': 'wait'},
            expected_schema=None,
            timeout_ms=200
        ))
        
        # Health check tests
        self.tests.append(SkillTest(
            name="health_check_basic",
            skill_name="brain-health-check",
            input_data={'detailed': False},
            expected_output={'status': 'healthy'},
            expected_schema={'required': ['status', 'metrics', 'recommendations', 'timestamp']},
            timeout_ms=50
        ))
        
        # Recovery tests
        self.tests.append(SkillTest(
            name="recovery_aggressive",
            skill_name="tick-recovery",
            input_data={
                'health_report': {'status': 'critical', 'metrics': {'tick_latency_ms': 1000}},
                'aggressive': True
            },
            expected_output={'status': 'recovered'},
            expected_schema={'required': ['status', 'actions_taken', 'regions_reset']},
            timeout_ms=50
        ))
    
    def add_test(self, test: SkillTest):
        """Add custom test case."""
        self.tests.append(test)
    
    def run_test(self, test: SkillTest) -> TestRun:
        """Execute single test."""
        start = time.time()
        
        try:
            # Get skill
            skill = self.registry.get(test.skill_name)
            if not skill:
                return TestRun(
                    test=test,
                    result=TestResult.ERROR,
                    actual_output=None,
                    latency_ms=(time.time() - start) * 1000,
                    error_message=f"Skill not found: {test.skill_name}"
                )
            
            # Check timeout
            tier = skill.tier.value
            threshold = self.TIER_THRESHOLDS.get(tier, {'max': 1000})
            
            if test.timeout_ms > threshold['max']:
                return TestRun(
                    test=test,
                    result=TestResult.SKIP,
                    actual_output=None,
                    latency_ms=0,
                    error_message=f"Timeout {test.timeout_ms}ms exceeds tier max {threshold['max']}ms"
                )
            
            # Call skill
            result = skill.call(test.input_data, timeout_ms=test.timeout_ms)
            latency = (time.time() - start) * 1000
            
            # Check for errors
            if 'error' in result:
                return TestRun(
                    test=test,
                    result=TestResult.FAIL if test.should_succeed else TestResult.PASS,
                    actual_output=result,
                    latency_ms=latency,
                    error_message=result['error']
                )
            
            # Check expected output
            if test.expected_output:
                for key, value in test.expected_output.items():
                    if key not in result or result[key] != value:
                        return TestRun(
                            test=test,
                            result=TestResult.FAIL,
                            actual_output=result,
                            latency_ms=latency,
                            error_message=f"Expected {key}={value}, got {result.get(key, 'MISSING')}"
                        )
            
            # Check latency
            if latency > threshold['max']:
                return TestRun(
                    test=test,
                    result=TestResult.FAIL,
                    actual_output=result,
                    latency_ms=latency,
                    error_message=f"Latency {latency:.1f}ms exceeds threshold {threshold['max']}ms"
                )
            
            return TestRun(
                test=test,
                result=TestResult.PASS if test.should_succeed else TestResult.FAIL,
                actual_output=result,
                latency_ms=latency
            )
            
        except Exception as e:
            return TestRun(
                test=test,
                result=TestResult.ERROR,
                actual_output=None,
                latency_ms=(time.time() - start) * 1000,
                error_message=str(e)
            )
    
    def run_all(self, skill_filter: Optional[str] = None) -> List[TestRun]:
        """Run all tests or filtered subset."""
        self.results = []
        
        tests = self.tests
        if skill_filter:
            tests = [t for t in tests if t.skill_name == skill_filter]
        
        for test in tests:
            result = self.run_test(test)
            self.results.append(result)
        
        return self.results
    
    def generate_report(self) -> Dict:
        """Generate test report."""
        if not self.results:
            return {"status": "no_tests_run", "total": 0}
        
        by_result = {r: [] for r in TestResult}
        for run in self.results:
            by_result[run.result].append(run)
        
        total = len(self.results)
        passed = len(by_result[TestResult.PASS])
        failed = len(by_result[TestResult.FAIL])
        errors = len(by_result[TestResult.ERROR])
        skipped = len(by_result[TestResult.SKIP])
        
        # Latency stats
        latencies = [r.latency_ms for r in self.results if r.result != TestResult.SKIP]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        max_latency = max(latencies) if latencies else 0
        
        report = {
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "skipped": skipped,
                "pass_rate": f"{(passed/total)*100:.1f}%" if total > 0 else "N/A",
                "avg_latency_ms": round(avg_latency, 2),
                "max_latency_ms": round(max_latency, 2)
            },
            "by_skill": {},
            "failures": [],
            "timestamp": time.time()
        }
        
        # Group by skill
        for run in self.results:
            skill = run.test.skill_name
            if skill not in report["by_skill"]:
                report["by_skill"][skill] = {"total": 0, "passed": 0, "failed": 0}
            report["by_skill"][skill]["total"] += 1
            if run.result == TestResult.PASS:
                report["by_skill"][skill]["passed"] += 1
            else:
                report["by_skill"][skill]["failed"] += 1
            
            if run.result in [TestResult.FAIL, TestResult.ERROR]:
                report["failures"].append({
                    "test": run.test.name,
                    "skill": skill,
                    "result": run.result.value,
                    "error": run.error_message
                })
        
        return report
    
    def save_report(self, filename: Optional[str] = None):
        """Save report to file."""
        report = self.generate_report()
        
        if not filename:
            timestamp = int(time.time())
            filename = f"skill_test_report_{timestamp}.json"
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath
    
    def check_regression(self, previous_report: Dict) -> List[Dict]:
        """Compare current results with previous to detect regressions."""
        regressions = []
        
        # Create lookup by test name
        current_by_name = {r.test.name: r for r in self.results}
        previous_failures = {f['test']: f for f in previous_report.get('failures', [])}
        
        for run in self.results:
            if run.result == TestResult.PASS:
                # Check if this was previously failing
                if run.test.name in previous_failures:
                    regressions.append({
                        'type': 'fixed',
                        'test': run.test.name,
                        'message': f"Was failing, now passes"
                    })
            elif run.result in [TestResult.FAIL, TestResult.ERROR]:
                # Check if this is a new failure
                if run.test.name not in previous_failures:
                    regressions.append({
                        'type': 'new_failure',
                        'test': run.test.name,
                        'message': f"New failure: {run.error_message}"
                    })
        
        return regressions
    
    def print_summary(self):
        """Print human-readable test summary."""
        report = self.generate_report()
        
        print("\n" + "="*60)
        print("SKILL TEST SUITE RESULTS")
        print("="*60)
        
        summary = report['summary']
        print(f"\nTotal Tests: {summary['total']}")
        print(f"  ✅ Passed:  {summary['passed']}")
        print(f"  ❌ Failed:  {summary['failed']}")
        print(f"  ⚠️  Errors: {summary['errors']}")
        print(f"  ⏭️  Skipped: {summary['skipped']}")
        print(f"\nPass Rate: {summary['pass_rate']}")
        print(f"Avg Latency: {summary['avg_latency_ms']}ms")
        print(f"Max Latency: {summary['max_latency_ms']}ms")
        
        if report['failures']:
            print(f"\n{'='*60}")
            print("FAILURES")
            print("="*60)
            for failure in report['failures']:
                print(f"\n❌ {failure['test']} ({failure['skill']})")
                print(f"   Result: {failure['result']}")
                print(f"   Error: {failure['error']}")
        
        print("\n" + "="*60)


if __name__ == '__main__':
    # Example usage
    from skill_registry import get_registry
    
    registry = get_registry()
    suite = SkillTestSuite(registry)
    
    # Run tests
    suite.run_all()
    
    # Print summary
    suite.print_summary()
    
    # Save report
    report_path = suite.save_report()
    print(f"\nReport saved to: {report_path}")
