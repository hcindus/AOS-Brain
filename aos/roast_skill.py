#!/usr/bin/env python3
"""
ROAST SKILL v1.0 - Adversarial Analysis for AOS
Based on Nate Herk's Council Pattern

Forces adversarial analysis before any significant action.
Spins up 6 personas to evaluate, then Judge gives final verdict.

Usage: Trigger before Patricia delegates complex tasks
"""

import json
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class RoastVerdict(Enum):
    GREEN_LIGHT = "GREEN_LIGHT"  # Proceed as planned
    RESHAPE = "RESHAPE"          # Modify but keep core idea
    KILL = "KILL"                # Abandon idea


@dataclass
class RoastPersona:
    """Individual persona in the roast council"""
    name: str
    role: str
    objective: str
    weight: float  # Influence on final score
    
    def evaluate(self, task: Dict) -> Dict:
        """Generate this persona's evaluation"""
        return {
            "persona": self.name,
            "role": self.role,
            "findings": self._generate_findings(task),
            "score": self._calculate_score(task),  # 0-10
            "confidence": 0.85,
            "timestamp": time.time()
        }
    
    def _generate_findings(self, task: Dict) -> List[str]:
        """Generate findings based on persona type"""
        # In production, this would call actual LLM
        # For now, return template based on persona
        templates = {
            "Contrarian": [
                "Critical flaw: [specific risk]",
                "Why this might fail: [failure mode]",
                "Hidden assumption: [untested assumption]"
            ],
            "Expansionist": [
                "Biggest upside: [max potential]",
                "Adjacent opportunity: [related market]",
                "Scale potential: [growth trajectory]"
            ],
            "FirstPrinciples": [
                "Core truth: [fundamental fact]",
                "Logical deduction: [if-then chain]",
                "Simpler path: [minimal version]"
            ],
            "Researcher": [
                f"Market size: [TAM/SAM/SOM data]",
                "Competitor intel: [pricing/features]",
                "Trend alignment: [market timing]"
            ],
            "Buyer": [
                "Purchase trigger: [why they'd buy]",
                "Objection: [why they wouldn't]",
                "Price sensitivity: [willingness to pay]"
            ],
            "Judge": [
                "Evidence summary: [key findings]",
                "Risk assessment: [probability of success]",
                "Recommended action: [verdict]"
            ]
        }
        return templates.get(self.name, ["Analysis complete"])
    
    def _calculate_score(self, task: Dict) -> float:
        """Calculate persona-specific score"""
        # In production, use actual evaluation
        # For demo, return realistic scores
        scores = {
            "Contrarian": 3.0,      # Harsh critic
            "Expansionist": 8.5,   # Optimist
            "FirstPrinciples": 6.0,  # Neutral logic
            "Researcher": 7.0,       # Data-driven
            "Buyer": 4.5,           # Skeptical customer
            "Judge": 0.0            # Calculated from others
        }
        return scores.get(self.name, 5.0)


class RoastSkill:
    """
    AOCROS Roast Skill - Council of adversarial personas
    
    Forces honest evaluation before significant actions.
    Prevents sycophancy and catches flaws early.
    """
    
    def __init__(self):
        self.personas = self._initialize_personas()
        self.complexity_threshold = 0.6  # Only roast if complexity > threshold
        print("[Roast Skill] 🔥 Adversarial analysis initialized")
        print("  Council: Contrarian, Expansionist, FirstPrinciples, Researcher, Buyer, Judge")
    
    def _initialize_personas(self) -> List[RoastPersona]:
        """Create the roast council"""
        return [
            RoastPersona(
                name="Contrarian",
                role="Fatal Flaw Finder",
                objective="Find every reason this will fail. Be brutal.",
                weight=0.25  # High weight - risks matter
            ),
            RoastPersona(
                name="Expansionist",
                role="Upside Maximizer",
                objective="Find the biggest possible win. Be optimistic.",
                weight=0.15  # Medium weight - upside validation
            ),
            RoastPersona(
                name="FirstPrinciples",
                role="Logic Purist",
                objective="Strip away assumptions. What's actually true?",
                weight=0.20  # High weight - truth matters
            ),
            RoastPersona(
                name="Researcher",
                role="Market Intelligence",
                objective="Pull real data. What do competitors charge? What's the TAM?",
                weight=0.20  # High weight - data matters
            ),
            RoastPersona(
                name="Buyer",
                role="Customer Proxy",
                objective="Would I pay for this? What's my objection?",
                weight=0.20  # High weight - customer truth
            ),
            RoastPersona(
                name="Judge",
                role="Final Arbiter",
                objective="Synthesize all findings. Deliver verdict.",
                weight=0.00  # Judge doesn't score - decides
            )
        ]
    
    def should_roast(self, task: Dict) -> bool:
        """
        Determine if task needs roasting based on complexity
        
        Criteria for roasting:
        - Budget > $1000
        - Time > 1 week
        - Revenue impact
        - New customer-facing feature
        - Security implications
        """
        complexity_score = self._assess_complexity(task)
        
        roast_triggers = [
            task.get("budget", 0) > 1000,
            task.get("time_estimate", 0) > 40,  # hours
            "revenue" in task.get("objective", "").lower(),
            "customer" in task.get("objective", "").lower(),
            "security" in task.get("objective", "").lower(),
            "launch" in task.get("objective", "").lower(),
            complexity_score > self.complexity_threshold
        ]
        
        return any(roast_triggers)
    
    def _assess_complexity(self, task: Dict) -> float:
        """Calculate complexity score 0-1"""
        score = 0.0
        
        # Factors that increase complexity
        if len(task.get("description", "")) > 200:
            score += 0.2
        if task.get("dependencies", []):
            score += 0.2
        if task.get("stakeholders", []):
            score += 0.2
        if "integrate" in task.get("description", "").lower():
            score += 0.15
        if "new" in task.get("description", "").lower():
            score += 0.15
        
        return min(1.0, score)
    
    def roast(self, task: Dict) -> Dict:
        """
        Execute full roast council evaluation
        
        Returns complete analysis with verdict and action items.
        """
        print(f"\n[Roast Skill] 🔥 Initiating roast for: {task.get('title', 'Untitled')}")
        print(f"  Objective: {task.get('objective', 'Unknown')[:60]}...")
        
        # Run all personas except Judge
        evaluations = []
        for persona in self.personas:
            if persona.name != "Judge":
                print(f"  🎭 {persona.name} evaluating...")
                eval_result = persona.evaluate(task)
                evaluations.append(eval_result)
        
        # Calculate weighted score
        weighted_score = self._calculate_weighted_score(evaluations)
        
        # Judge makes final verdict
        judge = next(p for p in self.personas if p.name == "Judge")
        verdict, reasoning = self._deliver_verdict(evaluations, weighted_score, task)
        
        # Compile full roast report
        roast_report = {
            "task": task,
            "evaluations": evaluations,
            "weighted_score": round(weighted_score, 2),
            "verdict": verdict.value,
            "judge_reasoning": reasoning,
            "action_items": self._generate_action_items(verdict, evaluations),
            "timestamp": time.time(),
            "cheap_test": self._recommend_cheap_test(task, verdict)
        }
        
        self._print_roast_summary(roast_report)
        
        return roast_report
    
    def _calculate_weighted_score(self, evaluations: List[Dict]) -> float:
        """Calculate weighted average of persona scores"""
        total_weight = 0.0
        weighted_sum = 0.0
        
        for eval in evaluations:
            persona = next(p for p in self.personas if p.name == eval["persona"])
            weighted_sum += eval["score"] * persona.weight
            total_weight += persona.weight
        
        return weighted_sum / total_weight if total_weight > 0 else 5.0
    
    def _deliver_verdict(self, evaluations: List[Dict], weighted_score: float, 
                        task: Dict) -> Tuple[RoastVerdict, str]:
        """Judge delivers final verdict based on weighted score"""
        
        if weighted_score >= 7.0:
            verdict = RoastVerdict.GREEN_LIGHT
            reasoning = (
                f"Strong consensus (score: {weighted_score:.1f}/10). "
                "Evidence supports viability. Market validation likely. "
                "Proceed with confidence."
            )
        elif weighted_score >= 5.0:
            verdict = RoastVerdict.RESHAPE
            reasoning = (
                f"Mixed signals (score: {weighted_score:.1f}/10). "
                "Core idea viable but needs modification. "
                "Address Contrarian concerns before proceeding. "
                "Run cheap test to validate."
            )
        else:
            verdict = RoastVerdict.KILL
            reasoning = (
                f"Low confidence (score: {weighted_score:.1f}/10). "
                "Fundamental flaws identified. "
                "Contrarian objections valid. "
                "Buyer unwillingness to pay. "
                "Abandon and pivot."
            )
        
        return verdict, reasoning
    
    def _generate_action_items(self, verdict: RoastVerdict, 
                               evaluations: List[Dict]) -> List[str]:
        """Generate specific action items based on verdict"""
        actions = []
        
        if verdict == RoastVerdict.GREEN_LIGHT:
            actions.append("✅ Proceed with implementation")
            actions.append("📊 Set success metrics")
            actions.append("⏰ Schedule checkpoint review")
        
        elif verdict == RoastVerdict.RESHAPE:
            actions.append("🔄 Modify approach based on feedback")
            actions.append("🧪 Run cheapest validation test")
            actions.append("📋 Address top 3 contrarian concerns")
            actions.append("⏰ Re-roast after modifications")
        
        else:  # KILL
            actions.append("🛑 Abandon current approach")
            actions.append("💡 Brainstorm alternatives")
            actions.append("📚 Document lessons learned")
            actions.append("🎯 Pivot to different opportunity")
        
        return actions
    
    def _recommend_cheap_test(self, task: Dict, verdict: RoastVerdict) -> Optional[str]:
        """Recommend cheapest test to validate within 48 hours"""
        if verdict == RoastVerdict.KILL:
            return None
        
        test_recommendations = {
            "sales": "DM 10-20 target customers, ask if they'd pay",
            "feature": "Build minimal prototype, test with 5 users",
            "content": "Post MVP version, measure engagement",
            "automation": "Manual process for 1 week, measure time saved",
            "default": "Survey 20 potential users, validate demand"
        }
        
        objective = task.get("objective", "").lower()
        for keyword, test in test_recommendations.items():
            if keyword in objective:
                return test
        
        return test_recommendations["default"]
    
    def _print_roast_summary(self, report: Dict):
        """Print formatted roast summary"""
        print("\n" + "=" * 70)
        print(f"  ROAST COMPLETE - Verdict: {report['verdict']}")
        print("=" * 70)
        
        print(f"\n  Weighted Score: {report['weighted_score']:.1f}/10")
        print(f"  Judge Reasoning: {report['judge_reasoning']}")
        
        print("\n  Persona Scores:")
        for eval in report['evaluations']:
            print(f"    {eval['persona']:20s}: {eval['score']:.1f}/10")
        
        print("\n  Action Items:")
        for action in report['action_items']:
            print(f"    {action}")
        
        if report['cheap_test']:
            print(f"\n  💡 Cheap Test (48h): {report['cheap_test']}")
        
        print("=" * 70)


# Integration with Chief of Staff
def should_roast_before_delegation(task: Dict, roast_skill: RoastSkill) -> Optional[Dict]:
    """
    Check if task should be roasted before Patricia delegates
    
    Returns roast report if roasting needed, None otherwise
    """
    if roast_skill.should_roast(task):
        return roast_skill.roast(task)
    return None


# Test function
def test_roast_skill():
    """Test the roast skill"""
    print("\n" + "=" * 70)
    print("  ROAST SKILL - TEST")
    print("=" * 70)
    
    roast = RoastSkill()
    
    # Test 1: Simple task (should skip roast)
    print("\n[Test 1] Simple task (should skip)")
    simple_task = {
        "title": "Fix typo",
        "objective": "Fix typo in README",
        "description": "Change 'teh' to 'the'",
        "time_estimate": 5  # minutes
    }
    should_roast = roast.should_roast(simple_task)
    print(f"  Should roast: {should_roast} (expected: False)")
    
    # Test 2: Complex task (should trigger roast)
    print("\n[Test 2] Complex task (should roast)")
    complex_task = {
        "title": "Launch new product",
        "objective": "Create and launch $9/month YouTube to LinkedIn tool",
        "description": "Build web app that converts YouTube transcripts into LinkedIn posts. Target market: content creators. Revenue goal: $10K MRR within 6 months.",
        "budget": 5000,
        "time_estimate": 80,  # hours
        "dependencies": ["market_research", "mvp_build", "marketing_site"],
        "stakeholders": ["engineering", "design", "sales"]
    }
    should_roast = roast.should_roast(complex_task)
    print(f"  Should roast: {should_roast} (expected: True)")
    
    if should_roast:
        report = roast.roast(complex_task)
        print(f"\n  Final Verdict: {report['verdict']}")
        print(f"  Score: {report['weighted_score']:.1f}/10")
    
    print("\n" + "=" * 70)
    print("  ✅ Roast Skill Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_roast_skill()
