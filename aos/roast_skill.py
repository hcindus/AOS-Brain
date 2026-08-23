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
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

import requests

# --- Ollama LLM wiring for real adversarial analysis ---
# Point ROAST_OLLAMA_URL at a remote GPU host (e.g. Nebius/Lambda/Vast.ai
# running Ollama) to use big models; falls back to localhost otherwise.
OLLAMA_URL = os.environ.get(
    "ROAST_OLLAMA_URL", "http://localhost:11434"
).rstrip("/") + "/api/generate"
# NOTE: host has no GPU + ~1GB free RAM, so the 9GB qwen2.5:14b can't run here.
# Use small CPU-friendly models; the deep models need a GPU/VPS.
ROAST_MODEL = "gemma2:2b"            # fast, fits constrained CPU host
ROAST_MODEL_FALLBACKS = ["tinyllama:latest", "mistral:latest"]
ROAST_TIMEOUT = 60


def _query_ollama(prompt: str, model: str = ROAST_MODEL, timeout: int = ROAST_TIMEOUT) -> Optional[str]:
    """Call Ollama and return raw text, or None on any failure."""
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.4,   # enough for divergent personas, still coherent
                    "num_predict": 250,   # 3 findings + score, kept lean for CPU
                },
            },
            timeout=timeout,
        )
        if resp.status_code == 200:
            return resp.json().get("response", "").strip()
    except Exception:
        pass
    return None


def _llm_query_with_fallback(prompt: str) -> Optional[str]:
    """Try primary model, then fallbacks. Return None if all fail."""
    for model in [ROAST_MODEL] + ROAST_MODEL_FALLBACKS:
        out = _query_ollama(prompt, model=model)
        if out:
            return out
    return None


def _parse_llm_json(text: str) -> Optional[Dict]:
    """Extract a JSON object from an LLM response (tolerates prose + code fences)."""
    if not text:
        return None
    # Strip markdown code fences if present
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.split("\n", 1)[-1] if "\n" in stripped else stripped[3:]
        stripped = stripped.strip()
        if stripped.endswith("```"):
            stripped = stripped[:-3].strip()
    # Try the whole thing first, then the first { ... } block
    candidates = [stripped]
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end > start:
        candidates.append(stripped[start:end + 1])
    for c in candidates:
        try:
            return json.loads(c)
        except Exception:
            continue
    return None


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
        """Generate this persona's evaluation (LLM-backed, template fallback)."""
        findings, score, used_llm = self._llm_evaluate(task)
        if findings is None:
            findings = self._template_findings()
            score = self._template_score()
            used_llm = False
        return {
            "persona": self.name,
            "role": self.role,
            "findings": findings,
            "score": score,  # 0-10
            "confidence": 0.85 if used_llm else 0.4,
            "llm_backed": used_llm,
            "timestamp": time.time()
        }

    def _llm_evaluate(self, task: Dict) -> Tuple[Optional[List[str]], Optional[float], bool]:
        """Ask Ollama for real findings + score, with one retry. Returns (findings, score, used_llm)."""
        prompt = self._build_prompt(task)
        for _ in range(2):  # retry once — small models are flaky on strict JSON
            raw = _llm_query_with_fallback(prompt)
            if raw is None:
                continue
            parsed = _parse_llm_json(raw)
            if not parsed:
                continue
            findings = parsed.get("findings")
            score = parsed.get("score")
            if isinstance(findings, list) and findings and isinstance(score, (int, float)):
                score = max(0.0, min(10.0, float(score)))
                return findings, round(score, 1), True
        return None, None, False

    # Persona-specific output guidance — keeps each critic in its lane.
    _PERSONA_HINTS = {
        "Contrarian": "Find what will fail, why it fails, and the hidden assumption that breaks it. Be harsh — a score below 5 is expected if there are real risks.",
        "Expansionist": "Find the biggest upside, the adjacent market, and how it scales. Be optimistic — a score above 6 is expected if upside is real.",
        "FirstPrinciples": "Strip assumptions to the core truth, then reason from it. Give the simplest version that would work.",
        "Researcher": "Give market size, competitor intel, and timing. Cite the specific data you'd need to verify.",
        "Buyer": "Answer as the actual paying customer: would YOU buy this, what is YOUR objection, and what price feels right? Do NOT describe the offer — react to it.",
        "Judge": "Synthesize all findings into a clear verdict.",
    }

    def _build_prompt(self, task: Dict) -> str:
        """Persona-specific prompt instructing the model to roleplay the critic."""
        title = task.get("title", "Untitled")
        objective = task.get("objective", "")
        budget = task.get("budget", "n/a")
        time_estimate = task.get("time_estimate", "n/a")
        hint = self._PERSONA_HINTS.get(self.name, "")
        return (
            f'You are the "{self.name}" member of an adversarial review council. '
            f"Your role: {self.role}.\n"
            f"Your mandate: {self.objective}\n"
            f"Your angle: {hint}\n\n"
            f"TASK BEING EVALUATED:\n"
            f"Title: {title}\n"
            f"Objective: {objective}\n"
            f"Budget: {budget}\n"
            f"Time estimate (hours): {time_estimate}\n\n"
            f"IMPORTANT: Do NOT restate or summarize the task. Speak AS {self.name} and "
            f"deliver YOUR OWN judgment about THIS idea, using the angle above. "
            f"Be specific and concrete; do NOT be sycophantic — genuinely stress-test.\n\n"
            f'Respond with ONLY a JSON object in this exact shape (no markdown, no prose):\n'
            f'{{"findings": ["...", "...", "..."], "score": <0.0 to 10.0>}}\n\n'
            f'"findings" must be exactly 3 concise, specific findings relevant to your angle.\n'
            f'"score" is your 0-10 rating of the idea\'s viability from your perspective.'
        )

    def _template_findings(self) -> List[str]:
        """Offline fallback findings (only used if Ollama is unreachable)."""
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
                "Market size: [TAM/SAM/SOM data]",
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

    def _template_score(self) -> float:
        """Offline fallback scores (only used if Ollama is unreachable)."""
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
