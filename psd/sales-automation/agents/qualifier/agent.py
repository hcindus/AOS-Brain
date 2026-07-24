#!/usr/bin/env python3
"""
SOP-005: AI-Powered Lead Qualifying Agent
Phase 2 of Dan Martell 5-Phase Sales Framework

Target: 95% reduction in unqualified calls, 80%+ qualified calendar
"""

import json
import logging
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DepotQual-1")


@dataclass
class BANTQualification:
    """BANT qualification data structure"""
    budget: Optional[int] = None
    budget_confirmed: bool = False
    authority: Optional[str] = None
    authority_confirmed: bool = False
    need: Optional[str] = None
    need_confirmed: bool = False
    timeline: Optional[str] = None
    timeline_confirmed: bool = False
    
    def calculate_score(self) -> int:
        """Calculate qualification score (0-100)"""
        score = 0
        if self.budget_confirmed and self.budget and self.budget >= 500:
            score += 25
        if self.authority_confirmed:
            score += 25
        if self.need_confirmed:
            score += 25
        if self.timeline_confirmed and self._is_urgent():
            score += 15
        if self._has_multiple_locations():
            score += 10
        return score
    
    def _is_urgent(self) -> bool:
        """Check if timeline is urgent"""
        if not self.timeline:
            return False
        urgent_keywords = ["asap", "urgent", "this week", "this month", "running low"]
        return any(kw in self.timeline.lower() for kw in urgent_keywords)
    
    def _has_multiple_locations(self) -> bool:
        """Check for multiple locations"""
        # Would parse from need/authority conversation
        return False  # Placeholder


class VoiceQualifierAgent:
    """
    AI Voice Qualification Agent for PSD
    
    Responsibilities:
    - Make qualification calls
    - Ask BANT questions
    - Score leads
    - Book calendar
    - Handle ghosted leads
    """
    
    def __init__(self):
        self.agent_name = "DepotQual-1"
        self.voice = "Adam"
        self.model = "Mort_II:latest"
        self.max_call_duration = 600  # 10 minutes
        
        # Qualification scripts
        self.scripts = self._load_scripts()
        
    def _load_scripts(self) -> Dict:
        """Load conversation scripts"""
        return {
            "opening": """Hi, this is Miles from Performance Supply Depot. 
I hope I'm not catching you at a bad time?""",
            
            "permission": """Great! You just popped up on my calendar. 
Do you have 2 minutes for a quick conversation about your supply needs?""",
            
            "discovery": [
                "What type of business are you running?",
                "How many locations do you have?",
                "What POS supplies are you currently using?",
                "Are you happy with your current supplier?",
                "When do you typically need to restock?",
                "What's your monthly spend on supplies?",
                "Who makes the purchasing decisions?"
            ],
            
            "booking": """Perfect! Based on what you told me, I think we can definitely help. 
Let me get you scheduled with our team. When's a good time this week?""",
            
            "disqualify": """I totally understand. Sounds like now might not be the right time, 
and that's okay. I'll send you our catalog via email - no pressure, just so you have it 
when you need it. And if things change, just reply to that email or give us a call. 
Sound fair?"""
        }
    
    def initiate_call(self, lead: Dict) -> Dict:
        """
        Initiate qualification call to lead
        """
        logger.info(f"Initiating call to {lead['company_name']}")
        
        # This would integrate with:
        # - Twilio/similar for voice
        # - Real-time TTS with Mort_II
        # - Speech-to-text for responses
        # - Conversation state management
        
        return {
            "call_id": f"CALL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "lead_id": lead["lead_id"],
            "status": "initiated",
            "timestamp": datetime.now().isoformat()
        }
    
    def conduct_qualification(self, call_id: str) -> BANTQualification:
        """
        Conduct qualification conversation
        """
        bant = BANTQualification()
        
        # This would be the actual voice conversation
        # For now, structure the flow
        
        conversation_log = []
        
        # Opening
        conversation_log.append({
            "speaker": "ai",
            "text": self.scripts["opening"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Permission
        conversation_log.append({
            "speaker": "ai",
            "text": self.scripts["permission"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Discovery questions
        for question in self.scripts["discovery"]:
            conversation_log.append({
                "speaker": "ai",
                "text": question,
                "timestamp": datetime.now().isoformat()
            })
            
            # Prospect response would be captured here
            # AI would parse and update BANT
            
        return bant, conversation_log
    
    def score_lead(self, bant: BANTQualification) -> Dict:
        """
        Score lead based on BANT qualification
        """
        score = bant.calculate_score()
        
        routing = {
            "score": score,
            "routing": "unknown"
        }
        
        if score >= 80:
            routing["routing"] = "senior_closer"
            routing["priority"] = "immediate"
        elif score >= 60:
            routing["routing"] = "sdr"
            routing["priority"] = "high"
        elif score >= 40:
            routing["routing"] = "nurture"
            routing["priority"] = "medium"
        else:
            routing["routing"] = "archive"
            routing["priority"] = "low"
        
        return routing
    
    def book_calendar(self, lead: Dict, bant: BANTQualification, 
                      availability: List[str]) -> Optional[Dict]:
        """
        Book calendar with qualified lead
        """
        score = bant.calculate_score()
        
        if score < 60:
            logger.info(f"Lead {lead['lead_id']} not qualified for booking (score: {score})")
            return None
        
        # Calendar integration
        booking = {
            "booking_id": f"BK-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "lead_id": lead["lead_id"],
            "score": score,
            "calendar": "sales@psdepot.com",
            "scheduled_time": availability[0] if availability else None,
            "buffer_minutes": 15,
            "assigned_to": "senior_closer" if score >= 80 else "sdr"
        }
        
        logger.info(f"Booked calendar for {lead['company_name']}")
        return booking
    
    def ghost_recovery_sequence(self, lead: Dict, days_since_noshow: int) -> Optional[str]:
        """
        Ghosted lead recovery email sequence
        """
        sequences = {
            1: {  # 24 hours
                "subject": "Did I catch you at a bad time?",
                "body": f"""Hi {lead.get('contact_name', 'there')},

I hope I'm not catching you at a bad time. We were scheduled to talk about your POS supply needs yesterday.

If now isn't a good time, no worries - just reply with "LATER" and I'll circle back in a few weeks.

If you're still interested, here's my calendar: [LINK]

Best,
Miles
Performance Supply Depot"""
            },
            3: {  # 3 days
                "subject": f"Quick question about {lead['company_name']}",
                "body": f"""Hi {lead.get('contact_name', 'there')},

Quick question - are you still looking for a POS supplies partner, or should I close out your file?

Just reply "YES" if you're still interested, or "NO" if you've got it handled.

Thanks,
Miles"""
            },
            7: {  # 7 days - final
                "subject": "Last follow-up",
                "body": f"""Hi {lead.get('contact_name', 'there')},

This is my last follow-up. If you're still interested in supplies for {lead['company_name']}, book a time here: [LINK]

If not, no hard feelings - good luck with your business!

Miles"""
            }
        }
        
        if days_since_noshow in sequences:
            return sequences[days_since_noshow]
        
        return None
    
    def generate_qualification_report(self, call_id: str, bant: BANTQualification,
                                     conversation_log: List[Dict]) -> Dict:
        """
        Generate qualification report for CRM
        """
        score = bant.calculate_score()
        routing = self.score_lead(bant)
        
        return {
            "call_id": call_id,
            "qualification_score": score,
            "bant": {
                "budget": bant.budget,
                "budget_confirmed": bant.budget_confirmed,
                "authority": bant.authority,
                "authority_confirmed": bant.authority_confirmed,
                "need": bant.need,
                "need_confirmed": bant.need_confirmed,
                "timeline": bant.timeline,
                "timeline_confirmed": bant.timeline_confirmed
            },
            "routing": routing,
            "transcript": conversation_log,
            "ai_confidence": 0.92,  # Would calculate from conversation
            "timestamp": datetime.now().isoformat()
        }


def main():
    """CLI entry point"""
    import sys
    
    agent = VoiceQualifierAgent()
    
    # Example: Process a lead
    test_lead = {
        "lead_id": "LEAD-001",
        "company_name": "Test Restaurant",
        "contact_name": "John Smith",
        "phone": "555-0100",
        "email": "john@testrestaurant.com"
    }
    
    # Simulate qualification
    call = agent.initiate_call(test_lead)
    bant, log = agent.conduct_qualification(call["call_id"])
    
    # Score and route
    routing = agent.score_lead(bant)
    print(f"Qualification score: {bant.calculate_score()}")
    print(f"Routing: {routing}")


if __name__ == "__main__":
    main()
