#!/usr/bin/env python3
"""
Pull Prompting Implementation for Proposal Generation
SOP-045: AI Presenting - Phase 3

Uses "outcome-based" prompting where AI asks questions
to gather requirements instead of push-based instructions.
"""

import json
import logging
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PullPrompter")


@dataclass
class QuestionResponse:
    """Question and answer pair from pull prompting"""
    question: str
    answer: str
    category: str  # business_context, pain_points, budget, timeline, etc.


class PullPromptingEngine:
    """
    Pull Prompting Engine for Sales Proposals
    
    Instead of pushing all context at once,
    the AI asks targeted questions to pull
    the necessary information.
    """
    
    def __init__(self):
        self.question_history: List[QuestionResponse] = []
        self.outcome_defined = False
        
    def define_outcome(self, objective: str) -> Dict:
        """
        Step 1: Define the outcome/objective
        
        Example: "Create a personalized sales proposal
        that converts this qualified lead into a customer"
        """
        self.outcome_defined = True
        
        return {
            "outcome": objective,
            "next_step": "AI will ask clarifying questions",
            "prompt_template": f"""Act as an expert sales consultant for Performance Supply Depot.

OUTCOME OBJECTIVE:
{objective}

Your task: Ask me all the questions you need to understand this prospect's situation deeply enough to create a personalized proposal that addresses their specific pain points and positions our solution as the obvious choice.

Ask about:
- Business context and current situation
- Specific pain points and challenges
- Budget and timeline
- Decision-making process
- Previous supplier experience
- Success criteria

Ask one question at a time. Wait for my answer before proceeding.

Once you have enough information, say "READY TO CREATE PROPOSAL" and provide a summary."""
        }
    
    def generate_clarifying_questions(self, context: Dict, 
                                     previous_qa: List[QuestionResponse] = None) -> List[str]:
        """
        Step 2: Generate questions based on what we know and what's missing
        
        This simulates the AI asking questions to pull information
        """
        if previous_qa is None:
            previous_qa = self.question_history
        
        questions = []
        
        # Determine what we know
        known_categories = {qa.category for qa in previous_qa}
        
        # Generate questions for missing categories
        if "business_context" not in known_categories:
            questions.extend([
                "What type of business are you running and how many locations do you have?",
                "What does a typical day look like for your operation?",
                "What POS equipment are you currently using?"
            ])
        
        if "pain_points" not in known_categories:
            questions.extend([
                "What's your biggest frustration with your current supply situation?",
                "When was the last time you ran out of supplies during a rush? What happened?",
                "If you could wave a magic wand and fix one thing about your supply chain, what would it be?"
            ])
        
        if "previous_supplier" not in known_categories:
            questions.extend([
                "Who are you currently using for supplies and what's working/not working with them?",
                "Have you considered switching before? What stopped you?"
            ])
        
        if "budget" not in known_categories:
            questions.extend([
                "What's your monthly spend on POS supplies currently?",
                "Is this coming out of a specific budget or cost center?",
                "What would justify a higher investment in quality supplies?"
            ])
        
        if "decision_process" not in known_categories:
            questions.extend([
                "Who else needs to be involved in this decision?",
                "What information do you typically need to make a purchasing decision?",
                "What's your typical timeline for evaluating a new supplier?"
            ])
        
        if "urgency" not in known_categories:
            questions.extend([
                "When do you need to have this resolved?",
                "Is there a specific event or situation driving this timeline?",
                "What happens if you don't make a change in the next 30 days?"
            ])
        
        # If we have enough info, indicate completion
        if len(known_categories) >= 5:
            questions = ["READY_TO_PROCEED"]
        
        return questions[:3]  # Return top 3 questions
    
    def process_answer(self, question: str, answer: str) -> Dict:
        """
        Step 3: Process the answer and categorize it
        """
        # Categorize the answer
        category = self._categorize_answer(question, answer)
        
        qa = QuestionResponse(
            question=question,
            answer=answer,
            category=category
        )
        
        self.question_history.append(qa)
        
        # Analyze if we have enough information
        coverage_score = self._calculate_coverage()
        
        return {
            "categorized_as": category,
            "coverage_score": coverage_score,
            "sufficient_info": coverage_score >= 0.8,
            "next_action": "ask_next_question" if coverage_score < 0.8 else "create_proposal"
        }
    
    def _categorize_answer(self, question: str, answer: str) -> str:
        """Categorize the answer based on content"""
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        if any(word in question_lower for word in ["business", "locations", "operation", "pos equipment"]):
            return "business_context"
        elif any(word in question_lower for word in ["frustration", "ran out", "pain", "challenge", "problem", "fix"]):
            return "pain_points"
        elif any(word in question_lower for word in ["currently using", "supplier", "previous"]):
            return "previous_supplier"
        elif any(word in question_lower for word in ["spend", "budget", "cost", "investment", "price"]):
            return "budget"
        elif any(word in question_lower for word in ["decision", "involved", "stakeholder", "approve"]):
            return "decision_process"
        elif any(word in question_lower for word in ["when", "timeline", "need", "urgent", "deadline"]):
            return "urgency"
        else:
            return "general"
    
    def _calculate_coverage(self) -> float:
        """Calculate how much information we have"""
        essential_categories = [
            "business_context",
            "pain_points",
            "budget",
            "decision_process"
        ]
        
        known_categories = {qa.category for qa in self.question_history}
        
        covered = sum(1 for cat in essential_categories if cat in known_categories)
        
        return covered / len(essential_categories)
    
    def synthesize_proposal_brief(self) -> Dict:
        """
        Step 4: Synthesize all Q&A into a proposal brief
        
        This is the "AI cooks" moment
        """
        if not self.outcome_defined:
            return {"error": "Outcome not defined"}
        
        # Organize by category
        categorized = {}
        for qa in self.question_history:
            if qa.category not in categorized:
                categorized[qa.category] = []
            categorized[qa.category].append(qa)
        
        # Extract key insights
        insights = self._extract_insights(categorized)
        
        proposal_brief = {
            "outcome": "Create personalized sales proposal",
            "business_summary": self._summarize_category(categorized.get("business_context", [])),
            "pain_points": self._summarize_category(categorized.get("pain_points", [])),
            "budget_context": self._summarize_category(categorized.get("budget", [])),
            "decision_process": self._summarize_category(categorized.get("decision_process", [])),
            "urgency": self._summarize_category(categorized.get("urgency", [])),
            "key_insights": insights,
            "recommended_approach": self._recommend_approach(insights),
            "confidence_score": self._calculate_coverage()
        }
        
        return proposal_brief
    
    def _extract_insights(self, categorized: Dict) -> List[str]:
        """Extract key insights from the Q&A"""
        insights = []
        
        # Look for patterns in pain points
        pain_answers = [qa.answer for qa in categorized.get("pain_points", [])]
        if any("run out" in ans.lower() for ans in pain_answers):
            insights.append("Supply reliability is a critical pain point")
        if any("slow" in ans.lower() for ans in pain_answers):
            insights.append("Delivery speed is a major concern")
        if any("quality" in ans.lower() for ans in pain_answers):
            insights.append("Product quality issues with current supplier")
        
        # Look for urgency signals
        urgency_answers = [qa.answer for qa in categorized.get("urgency", [])]
        if any(word in " ".join(urgency_answers).lower() for word in ["asap", "immediately", "this week"]):
            insights.append("High urgency - opportunity for quick close")
        
        return insights
    
    def _summarize_category(self, qas: List[QuestionResponse]) -> str:
        """Summarize a category of Q&A"""
        if not qas:
            return "No information gathered"
        
        # Simple concatenation for now
        # Would use AI summarization in production
        return " | ".join([f"Q: {qa.question} A: {qa.answer}" for qa in qas])
    
    def _recommend_approach(self, insights: List[str]) -> str:
        """Recommend sales approach based on insights"""
        if "Supply reliability" in " ".join(insights):
            return "Lead with reliability guarantee and 24hr delivery promise"
        elif "Delivery speed" in " ".join(insights):
            return "Emphasize local warehouse and fast fulfillment"
        else:
            return "Focus on quality and cost savings"
    
    def create_proposal_prompt(self, brief: Dict) -> str:
        """
        Step 5: Create the final prompt for proposal generation
        
        Now that we've PULLED all the context, we can push
        a structured request with complete information
        """
        return f"""Act as an expert sales consultant for Performance Supply Depot.

PROSPECT PROFILE (Gathered via pull prompting):
{brief['business_summary']}

PAIN POINTS:
{brief['pain_points']}

BUDGET CONTEXT:
{brief['budget_context']}

DECISION PROCESS:
{brief['decision_process']}

URGENCY:
{brief['urgency']}

KEY INSIGHTS:
{chr(10).join(['- ' + i for i in brief['key_insights']])}

RECOMMENDED APPROACH:
{brief['recommended_approach']}

TASK:
Create a personalized sales proposal using the VSL (Video Sales Letter) format:
1. Pain agitation (describe their pain better than they can)
2. Solution presentation (how PSD solves each pain point)
3. Specific product recommendations
4. Investment breakdown
5. Social proof (relevant case study)
6. Clear next steps

TONE: Consultative, energetic, professional (Miles style)
FORMAT: 1-2 page PDF structure with talking points
OUTPUT: JSON with proposal_sections and talk_track"""


class InteractivePullSession:
    """
    Interactive session for pull prompting
    
    Simulates a conversation where AI asks questions
    and human (or another system) answers
    """
    
    def __init__(self, prospect_data: Dict):
        self.engine = PullPromptingEngine()
        self.prospect_data = prospect_data
        self.current_questions = []
        self.session_complete = False
        
    def start_session(self) -> Dict:
        """Start the pull prompting session"""
        outcome = f"Create a personalized sales proposal for {self.prospect_data.get('company_name', 'this prospect')} that addresses their specific supply chain challenges and positions Performance Supply Depot as the solution"
        
        return self.engine.define_outcome(outcome)
    
    def get_next_questions(self) -> List[str]:
        """Get the next set of questions to ask"""
        if self.session_complete:
            return []
        
        questions = self.engine.generate_clarifying_questions(
            self.prospect_data,
            self.engine.question_history
        )
        
        if questions == ["READY_TO_PROCEED"] or questions == ["READY_TO_PROCEED"]:
            self.session_complete = True
            return ["SESSION_COMPLETE - Ready to generate proposal"]
        
        self.current_questions = questions
        return questions
    
    def answer_question(self, question: str, answer: str) -> Dict:
        """Submit an answer to a question"""
        result = self.engine.process_answer(question, answer)
        
        if result["sufficient_info"]:
            self.session_complete = True
            
        return result
    
    def generate_proposal_brief(self) -> Optional[Dict]:
        """Generate the final proposal brief"""
        if not self.session_complete:
            return None
            
        return self.engine.synthesize_proposal_brief()


def main():
    """Demo of pull prompting"""
    print("=== PULL PROMPTING DEMO ===\n")
    
    # Start with minimal prospect data
    prospect = {"company_name": "Downtown Grill"}
    
    session = InteractivePullSession(prospect)
    
    # Step 1: Define outcome
    outcome = session.start_session()
    print(f"Outcome defined: {outcome['outcome']}\n")
    
    # Step 2-3: Interactive Q&A loop
    for round_num in range(1, 4):  # Simulate 3 rounds
        questions = session.get_next_questions()
        
        if "SESSION_COMPLETE" in questions[0]:
            print("✓ Sufficient information gathered!\n")
            break
        
        print(f"--- Round {round_num} ---")
        for q in questions:
            print(f"AI asks: {q}")
            
            # Simulate answer
            simulated_answers = {
                "business": "Restaurant with 2 locations, 50 employees, using Square POS",
                "pain": "Running out of receipt paper during dinner rush, losing sales",
                "budget": "$2,000/month on supplies, willing to pay more for reliability"
            }
            
            # Simple matching for demo
            answer = "We run a busy restaurant and often run low on supplies during peak hours."
            if "business" in q.lower():
                answer = simulated_answers["business"]
            elif "pain" in q.lower() or "frustration" in q.lower():
                answer = simulated_answers["pain"]
            elif "budget" in q.lower() or "spend" in q.lower():
                answer = simulated_answers["budget"]
            
            print(f"Answer: {answer}\n")
            
            result = session.answer_question(q, answer)
            print(f"Coverage: {result['coverage_score']:.0%}\n")
    
    # Step 4: Generate proposal brief
    brief = session.generate_proposal_brief()
    
    if brief:
        print("=== PROPOSAL BRIEF ===")
        print(f"Confidence: {brief['confidence_score']:.0%}")
        print(f"\nKey Insights:")
        for insight in brief['key_insights']:
            print(f"  • {insight}")
        print(f"\nRecommended Approach: {brief['recommended_approach']}")


if __name__ == "__main__":
    main()
