#!/usr/bin/env python3
"""
SOP-007: AI-Powered Objection Handling Coach
Phase 4 of Dan Martell 5-Phase Sales Framework

Target: 90%+ objections handled confidently, 25%+ improvement via AI coaching
"""

import json
import re
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DepotCoach-1")


@dataclass
class ObjectionRecord:
    """Record of an objection encountered"""
    objection_text: str
    category: str  # price, timing, competition, authority, product, trust
    timestamp: str
    response_given: str
    outcome: str  # overcome, pending, lost
    score: int  # 1-10 effectiveness
    context: str = ""


class ObjectionCoachAgent:
    """
    AI Objection Handling Coach for PSD
    
    Responsibilities:
    - Analyze call transcripts for objections
    - Generate response scripts
    - Roleplay practice
    - Real-time whisper mode
    - Track improvement over time
    """
    
    def __init__(self):
        self.agent_name = "DepotCoach-1"
        self.model = "qwen2.5:14b"
        self.objection_library = self._load_objection_library()
        self.practice_history = []
        
    def _load_objection_library(self) -> Dict:
        """Load objection response library"""
        return {
            "price": {
                "patterns": [
                    "too expensive", "too high", "cheaper elsewhere", 
                    "can't afford", "budget", "discount"
                ],
                "feel_felt_found": """I understand how you feel. The price is higher than you expected.

Actually, a lot of our customers felt the same way at first.

But what they found was that the quality difference saved them money in the long run. Our thermal rolls don't jam printers, which means no downtime during rush.

Can I show you what I mean?""",
                "reframe": "What does it cost you when you run out of supplies during a busy shift?",
                "curiosity": "Help me understand - are you comparing this to a specific competitor, or is this about your allocated budget?"
            },
            "timing": {
                "patterns": [
                    "think about it", "call me back", "next quarter", 
                    "not ready", "later", "soon"
                ],
                "feel_felt_found": """Of course, I totally understand wanting to think it through.

Most of our partners felt that way too.

What they found was that delaying the decision actually cost them more in stockouts and rush shipping.

What specifically do you need to think through? Maybe I can help right now.""",
                "urgency": "What timeline are you thinking? And what's driving that timeline?",
                "commitment": "If we could solve [specific concern], would you be ready to move forward today?"
            },
            "competition": {
                "patterns": [
                    "happy with current", "already have", "using someone else",
                    "we've always used", "don't want to switch"
                ],
                "curiosity": """I'm glad you've got someone you trust. That's important.

Can I ask - what do you like most about working with them?

[pause]

That's great. What would you change if you could?

[pause - this is gold]

Interesting. What happens when [pain point they just mentioned]?

[pause]

Got it. So if there was a way to [solve that problem], would it be worth a conversation?""",
                "differentiation": "Most of our customers actually have a supplier they're happy with when we first talk. What they discover is..."
            },
            "authority": {
                "patterns": [
                    "need to ask", "talk to partner", "talk to boss",
                    "decision maker", "not my decision", "someone else decides"
                ],
                "collaboration": "Would it make sense to have them on this call now? Or should we schedule a time when we can all talk together?",
                "information": "No problem at all. What information do they typically need to make this kind of decision?"
            },
            "trust": {
                "patterns": [
                    "never heard of you", "how do I know", "what if",
                    "guarantee", "sure you'll deliver"
                ],
                "social_proof": "I totally understand. Can I share what happened with [similar customer]? They had the same concern...",
                "risk_reversal": "What would need to be true for you to feel confident moving forward?"
            }
        }
    
    def analyze_transcript(self, transcript: List[Dict], rep_name: str) -> Dict:
        """
        Analyze call transcript for objections
        """
        logger.info(f"Analyzing transcript for {rep_name}")
        
        objections_found = []
        
        for i, utterance in enumerate(transcript):
            if utterance.get("speaker") == "prospect":
                text = utterance.get("text", "").lower()
                
                # Check each objection category
                for category, data in self.objection_library.items():
                    for pattern in data["patterns"]:
                        if pattern in text:
                            # Find response (next rep utterance)
                            response = ""
                            for j in range(i+1, len(transcript)):
                                if transcript[j].get("speaker") == "rep":
                                    response = transcript[j].get("text", "")
                                    break
                            
                            objections_found.append(ObjectionRecord(
                                objection_text=utterance["text"],
                                category=category,
                                timestamp=utterance.get("timestamp", ""),
                                response_given=response,
                                outcome=self._determine_outcome(transcript, i),
                                score=0,  # Would be scored by AI
                                context=""
                            ))
                            break
        
        return {
            "rep_name": rep_name,
            "total_objections": len(objections_found),
            "objections_by_category": self._categorize_objections(objections_found),
            "objections": objections_found
        }
    
    def _determine_outcome(self, transcript: List[Dict], 
                          objection_index: int) -> str:
        """Determine if objection was overcome"""
        # Look ahead in transcript for outcome signals
        for utterance in transcript[objection_index:]:
            text = utterance.get("text", "").lower()
            if "book" in text or "schedule" in text or "move forward" in text:
                return "overcome"
            elif "not interested" in text or "no thanks" in text:
                return "lost"
        return "pending"
    
    def _categorize_objections(self, objections: List[ObjectionRecord]) -> Dict:
        """Group objections by category"""
        categories = {}
        for obj in objections:
            cat = obj.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(obj)
        return categories
    
    def generate_responses(self, objection_text: str, category: str = None) -> List[Dict]:
        """
        Generate multiple response options for an objection
        """
        if not category:
            category = self._classify_objection(objection_text)
        
        library = self.objection_library.get(category, {})
        
        responses = []
        
        # Feel-Felt-Found
        if "feel_felt_found" in library:
            responses.append({
                "technique": "Feel-Felt-Found",
                "script": library["feel_felt_found"],
                "when_to_use": "When prospect expresses emotion about objection",
                "effectiveness": 9
            })
        
        # Reframe/Curiosity
        if "curiosity" in library:
            responses.append({
                "technique": "Curiosity Pattern",
                "script": library["curiosity"],
                "when_to_use": "When you need more information",
                "effectiveness": 8
            })
        
        # Add more techniques
        if "urgency" in library:
            responses.append({
                "technique": "Urgency Close",
                "script": library["urgency"],
                "when_to_use": "When timeline is the real objection",
                "effectiveness": 7
            })
        
        return responses
    
    def _classify_objection(self, text: str) -> str:
        """Classify objection into category"""
        text_lower = text.lower()
        
        for category, data in self.objection_library.items():
            for pattern in data["patterns"]:
                if pattern in text_lower:
                    return category
        
        return "general"
    
    def roleplay_scenario(self, rep_name: str, objection_category: str = None,
                         difficulty: str = "medium") -> Dict:
        """
        Generate roleplay scenario for practice
        """
        scenarios = {
            "restaurant_owner": {
                "name": "Mike",
                "title": "Owner",
                "business": "Burger Joint",
                "situation": "Currently using cheap supplier, having quality issues",
                "personality": "skeptical but direct"
            },
            "bar_manager": {
                "name": "Sarah",
                "title": "Bar Manager",
                "business": "Downtown Bar",
                "situation": "Opening new location, tight timeline",
                "personality": "friendly but busy"
            },
            "retail_chain": {
                "name": "David",
                "title": "Operations Manager",
                "business": "Metro Retail (12 locations)",
                "situation": "Managing multiple suppliers, wants consolidation",
                "personality": "analytical, needs data"
            }
        }
        
        scenario = scenarios.get(difficulty, scenarios["restaurant_owner"])
        
        # Pick objection
        if not objection_category:
            objection_category = "price"  # Default
        
        objection_examples = {
            "price": "That seems expensive compared to what we're paying now.",
            "timing": "I need to think about it and talk to my partner.",
            "competition": "We're pretty happy with our current supplier.",
            "authority": "I'll need to run this by the owner."
        }
        
        return {
            "scenario": scenario,
            "objection": objection_examples.get(objection_category, "I'm not sure..."),
            "objection_category": objection_category,
            "instructions": f"""
ROLEPLAY SCENARIO

You are Miles, Sales Consultant at Performance Supply Depot.

PROSPECT:
- Name: {scenario['name']}
- Title: {scenario['title']}
- Business: {scenario['business']}
- Situation: {scenario['situation']}
- Personality: {scenario['personality']}

OBJECTION:
"{objection_examples.get(objection_category)}"

YOUR GOAL: Overcome the objection and move toward booking.

Type your response. I'll respond as {scenario['name']}.
            """
        }
    
    def score_roleplay(self, transcript: List[Dict], 
                      objection_category: str) -> Dict:
        """
        Score roleplay performance
        """
        scores = {
            "empathy": 0,  # Did they acknowledge feelings?
            "technique": 0,  # Did they use proper technique?
            "confidence": 0,  # Did they sound confident?
            "progression": 0,  # Did they move conversation forward?
            "closing": 0  # Did they attempt to close?
        }
        
        # Would be AI-scored based on transcript
        # For now, placeholder scoring logic
        
        total_score = sum(scores.values())
        
        feedback = []
        if scores["empathy"] < 7:
            feedback.append("Try using 'I understand how you feel' to show empathy")
        if scores["technique"] < 7:
            feedback.append(f"Practice the Feel-Felt-Found pattern for {objection_category} objections")
        
        return {
            "total_score": total_score,
            "max_score": 50,
            "percentage": (total_score / 50) * 100,
            "breakdown": scores,
            "feedback": feedback,
            "improvement_areas": [k for k, v in scores.items() if v < 7]
        }
    
    def whisper_mode(self, live_transcript: str) -> Optional[Dict]:
        """
        Real-time objection detection and suggestion
        """
        # Detect objection
        category = self._classify_objection(live_transcript)
        
        if category == "general":
            return None
        
        library = self.objection_library.get(category, {})
        
        return {
            "objection_detected": category.upper(),
            "suggested_response": library.get("feel_felt_found", "Acknowledge and ask questions"),
            "alternative": library.get("curiosity", "Use curiosity pattern"),
            "feel_felt_found_ready": "feel_felt_found" in library,
            "confidence": 0.92
        }
    
    def weekly_coaching_report(self, rep_name: str, 
                               week_start: datetime) -> Dict:
        """
        Generate weekly coaching report
        """
        # Aggregate data for the week
        return {
            "rep": rep_name,
            "week": week_start.isoformat(),
            "objections_encountered": 0,  # Would aggregate from database
            "objections_overcome": 0,
            "win_rate": 0.0,
            "top_objection_category": "price",  # Would calculate
            "practice_sessions": 0,
            "average_roleplay_score": 0,
            "recommended_focus": ["price", "timing"],  # Would calculate from data
            "improvement_trend": "up"  # Would compare to previous weeks
        }


def main():
    """CLI entry point"""
    agent = ObjectionCoachAgent()
    
    # Example: Analyze a transcript
    sample_transcript = [
        {"speaker": "rep", "text": "Hi, this is Miles from PSD..."},
        {"speaker": "prospect", "text": "Thanks for calling but your prices seem high."},
        {"speaker": "rep", "text": "I understand budget is important..."}
    ]
    
    analysis = agent.analyze_transcript(sample_transcript, "TestRep")
    print(f"Found {analysis['total_objections']} objections")
    
    # Generate responses
    responses = agent.generate_responses("Your price is too high", "price")
    print(f"Generated {len(responses)} response options")


if __name__ == "__main__":
    main()
