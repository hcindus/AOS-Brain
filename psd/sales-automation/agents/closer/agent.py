#!/usr/bin/env python3
"""
SOP-008: AI-Powered Closing & Delivery Agent
Phase 5 of Dan Martell 5-Phase Sales Framework

Target: 90%+ onboarding completion, first win within 48 hours
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DepotCloser-1")


@dataclass
class Customer:
    """Customer record for onboarding"""
    customer_id: str
    company_name: str
    contact_name: str
    email: str
    phone: str
    deal_value: float
    products_ordered: List[str] = field(default_factory=list)
    onboarding_status: str = "pending"  # pending, active, complete
    first_win_recorded: bool = False
    win_details: Dict = field(default_factory=dict)


class ClosingDeliveryAgent:
    """
    AI Closing & Delivery Agent for PSD
    
    Responsibilities:
    - Order processing automation
    - Welcome sequences
    - Onboarding flows
    - Win detection
    - Case study collection
    """
    
    def __init__(self):
        self.agent_name = "DepotCloser-1"
        self.model = "nous-hermes2:latest"  # Warm, personable
        self.onboarding_sequences = self._load_sequences()
        
    def _load_sequences(self) -> Dict:
        """Load onboarding email sequences"""
        return {
            "hour_0": {
                "subject": "Welcome to the team, {contact_name}! 🎉",
                "body": """Hi {contact_name},

Welcome to Performance Supply Depot! I'm thrilled to have {company_name} on board.

Here's what happens next:

✅ Your account is being set up (takes ~30 minutes)
✅ You'll get a call from our fulfillment team within 4 hours
✅ First delivery scheduled for {delivery_date}

Quick question: What's the #1 thing you want to make sure we get right?

Just reply and let me know.

Cheering you on,
Miles
Performance Supply Depot""",
                "delay_hours": 0
            },
            "hour_4": {
                "subject": "Your fulfillment team is on it",
                "body": """Hi {contact_name},

{fulfillment_rep} just reviewed your order. Everything looks good.

Quick heads up: Your first delivery is confirmed for {delivery_date}.

Questions? Just reply to this email.

Miles""",
                "delay_hours": 4
            },
            "day_1": {
                "subject": "Your first-win setup kit",
                "body": """Hi {contact_name},

To make sure you get off to a strong start, here are 3 resources:

1. Video: Setting up your supply closet for efficiency
2. PDF: Monthly reorder checklist  
3. Link: How to track usage so you never run out

These are from our most successful partners.

Remember: When you get that first win, tell me about it!

Miles""",
                "delay_hours": 24
            },
            "day_3": {
                "subject": "Quick check-in",
                "body": """Hi {contact_name},

Just checking in - how did your first delivery go?

Everything arrived as expected?

Let me know if you need anything!

Miles""",
                "delay_hours": 72
            },
            "day_7": {
                "subject": "Your first week - how's it going?",
                "body": """Hi {contact_name},

You've been with us for a week now. How are things going?

Any questions I can answer? Any feedback on the process?

I'm here if you need anything.

Miles""",
                "delay_hours": 168
            },
            "day_30": {
                "subject": "30-day partnership review",
                "body": """Hi {contact_name},

Can you believe it's been 30 days? Time flies!

Quick questions:
1. How has your experience been so far?
2. Any wins we should celebrate?
3. Anything we could do better?

I'd love to hear from you.

Miles""",
                "delay_hours": 720
            }
        }
    
    def process_close(self, deal: Dict) -> Customer:
        """
        Process closed deal and create customer record
        """
        logger.info(f"Processing close for {deal['company_name']}")
        
        customer = Customer(
            customer_id=f"CUST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            company_name=deal['company_name'],
            contact_name=deal['decision_maker_name'],
            email=deal['email'],
            phone=deal['phone'],
            deal_value=deal['deal_value'],
            products_ordered=deal.get('products', [])
        )
        
        # Trigger onboarding
        self.trigger_onboarding(customer)
        
        return customer
    
    def trigger_onboarding(self, customer: Customer):
        """
        Trigger onboarding sequence
        """
        logger.info(f"Triggering onboarding for {customer.company_name}")
        
        # Schedule all sequence emails
        for sequence_name, sequence in self.onboarding_sequences.items():
            send_time = datetime.now() + timedelta(hours=sequence["delay_hours"])
            
            # Queue email for sending
            self._queue_email(
                customer=customer,
                subject=sequence["subject"].format(**self._get_template_vars(customer)),
                body=sequence["body"].format(**self._get_template_vars(customer)),
                send_time=send_time
            )
        
        # Update status
        customer.onboarding_status = "active"
        
        # Notify fulfillment
        self._notify_fulfillment(customer)
    
    def _get_template_vars(self, customer: Customer) -> Dict:
        """Get variables for email templates"""
        return {
            "contact_name": customer.contact_name,
            "company_name": customer.company_name,
            "delivery_date": (datetime.now() + timedelta(days=2)).strftime("%A, %B %d"),
            "fulfillment_rep": "Alex"  # Would be dynamic
        }
    
    def _queue_email(self, customer: Customer, subject: str, 
                    body: str, send_time: datetime):
        """Queue email for sending"""
        # Would integrate with email service
        logger.info(f"Queued email to {customer.email} for {send_time}")
    
    def _notify_fulfillment(self, customer: Customer):
        """Notify fulfillment team"""
        # Would integrate with fulfillment system
        logger.info(f"Notified fulfillment for {customer.company_name}")
    
    def detect_win(self, customer: Customer, signal: Dict) -> Optional[Dict]:
        """
        Detect if customer has achieved a win
        """
        win_indicators = [
            "reorder placed",  # Reordering = satisfied
            "compliment",      # Positive feedback
            "referral",        # Referred someone
            "no issues",       # Support ticket resolved
            "on time",         # On-time delivery
        ]
        
        # Check for win signals
        detected_wins = []
        
        # Signal from email sentiment
        if signal.get("sentiment") == "positive":
            positive_keywords = ["thanks", "great", "love", "perfect", "awesome"]
            if any(kw in signal.get("text", "").lower() for kw in positive_keywords):
                detected_wins.append("Positive feedback")
        
        # Signal from reorder
        if signal.get("type") == "reorder":
            detected_wins.append("Satisfied customer - reordering")
        
        # Signal from on-time delivery
        if signal.get("delivery_status") == "on_time" and signal.get("delivery_count", 0) >= 3:
            detected_wins.append("3+ consecutive on-time deliveries")
        
        if detected_wins:
            win_record = {
                "customer_id": customer.customer_id,
                "company": customer.company_name,
                "wins_detected": detected_wins,
                "timestamp": datetime.now().isoformat(),
                "requires_celebration": True
            }
            
            customer.first_win_recorded = True
            customer.win_details = win_record
            
            logger.info(f"Win detected for {customer.company_name}: {detected_wins}")
            return win_record
        
        return None
    
    def generate_celebration_outreach(self, customer: Customer, 
                                     win: Dict) -> Dict:
        """
        Generate win celebration outreach
        """
        return {
            "subject": f"I heard the good news about {customer.company_name}!",
            "body": f"""Hi {customer.contact_name},

I heard {win['wins_detected'][0]} - that's fantastic!

Remember our agreement? You got a win, and now I'm asking permission to share it.

Here's why: I want to celebrate YOU. Not for marketing (though I'd love that), but because when you share wins publicly, it builds momentum.

Would you be open to a quick 5-minute call? I'd love to:
- Hear the full story
- Get your permission to share
- See how else we can support you

Just reply with a time that works.

Proud of you,
Miles""",
            "follow_up_call": True,
            "case_study_eligible": True
        }
    
    def generate_case_study_questions(self, customer: Customer) -> List[str]:
        """
        Generate case study interview questions
        """
        return [
            f"What was the situation at {customer.company_name} before working with Performance Supply Depot?",
            "What specific problem were you trying to solve?",
            "Why did you choose us over other suppliers?",
            "What results have you seen since working with us?",
            "What would you tell someone who's considering Performance Supply Depot?",
            "Can we share your story with other potential customers?"
        ]
    
    def how_do_you_feel_script(self, customer_name: str) -> str:
        """
        The "How do you feel?" script - addresses buyer's remorse immediately
        """
        return f""""Before we get into the details, I have to ask - how do you feel right now?

[pause - let them respond]

[nervous/excited/etc.]

That's completely normal. And I want you to know - this was absolutely the right decision. You're going to look back on this as a turning point for your business.

I'm genuinely excited to be working with you."""
    
    def win_agreement_script(self) -> str:
        """
        The Win Agreement script - sets up case study pipeline
        """
        return """"One thing I ask of all my partners - when you get your first win using our supplies, I want you to tell me about it.

I'm not asking for a testimonial or anything for marketing. This is for YOU.

Here's why: when you share that win, it holds you accountable to keep building momentum.

Can I count on you for that?

[Get confirmation]

Great. Initial here: _____"

[Make it part of the agreement - they initial]"""
    
    def generate_order_confirmation(self, customer: Customer, deal: Dict) -> Dict:
        """
        Generate order confirmation
        """
        return {
            "subject": f"Order Confirmation - {customer.company_name}",
            "body": f"""Hi {customer.contact_name},

Thank you for your order! Here are the details:

ORDER #{customer.customer_id}
─────────────────────
Company: {customer.company_name}
Total: ${deal['deal_value']:,.2f}
Payment Terms: Net 30

ITEMS ORDERED:
""" + "\n".join([f"• {product}" for product in customer.products_ordered]) + """

DELIVERY:
Expected: {(datetime.now() + timedelta(days=2)).strftime('%A, %B %d')}

What's Next:
✓ Your order is being prepared
✓ You'll receive tracking within 24 hours
✓ I'll check in after delivery

Questions? Reply to this email or call me at (555) 123-4567.

Welcome to the team!

Miles
Performance Supply Depot"""
        }
    
    def onboarding_status_report(self) -> Dict:
        """
        Generate onboarding status report
        """
        # Would query database
        return {
            "total_customers_onboarding": 0,
            "avg_time_to_first_delivery": "0 hours",
            "first_win_rate": "0%",
            "onboarding_completion_rate": "0%",
            "at_risk_customers": [],
            "wins_to_celebrate": []
        }


def main():
    """CLI entry point"""
    agent = ClosingDeliveryAgent()
    
    # Example: Process a close
    test_deal = {
        "company_name": "Test Restaurant",
        "decision_maker_name": "John Smith",
        "email": "john@test.com",
        "phone": "555-0100",
        "deal_value": 2500.00,
        "products": ["Thermal rolls (case)", "1oz pourers (dozen)", "Cleaning supplies"]
    }
    
    customer = agent.process_close(test_deal)
    print(f"Created customer: {customer.customer_id}")
    print(f"Onboarding status: {customer.onboarding_status}")
    
    # Simulate win detection
    win_signal = {
        "type": "reorder",
        "sentiment": "positive",
        "text": "Thanks for the great service!"
    }
    
    win = agent.detect_win(customer, win_signal)
    if win:
        print(f"Win detected: {win['wins_detected']}")
        celebration = agent.generate_celebration_outreach(customer, win)
        print(f"Celebration email subject: {celebration['subject']}")


if __name__ == "__main__":
    main()
