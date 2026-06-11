"""
CUSTOMER RESPONDER SYSTEM
Simulates realistic customer reactions to sales emails
Completes full sales cycle from lead to close OR rejection
"""

import random
import json
from datetime import datetime
from enum import Enum

class CustomerSentiment(Enum):
    INTERESTED = "interested"
    SKEPTICAL = "skeptical"
    NEUTRAL = "neutral"
    BUSY = "busy"
    NOT_INTERESTED = "not_interested"
    ANNOYED = "annoyed"

class SalesStage(Enum):
    NEW = "new"
    CONTACTED = "contacted"
    ENGAGED = "engaged"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class CustomerProfile:
    """Defines a customer persona for testing"""
    
    PROFILES = [
        {
            "name": "The Skeptic",
            "description": "Has been burned before, needs proof",
            "openness": 0.3,
            "price_sensitivity": 0.8,
            "decision_speed": 0.2,
            "typical_responses": [
                "I've tried lead services before. They were garbage.",
                "How do I know this isn't just another scam?",
                "Send me a sample first. Then we'll talk.",
                "Your competitors promised the same thing.",
                "I need references from companies like mine."
            ]
        },
        {
            "name": "The Busy Decision Maker",
            "description": "Wants value, has no time",
            "openness": 0.5,
            "price_sensitivity": 0.4,
            "decision_speed": 0.3,
            "typical_responses": [
                "Can you get to the point? I have 2 minutes.",
                "Email me the details. I'll review when I can.",
                "Book something for next week. Too swamped now.",
                "What's the ROI? Numbers only.",
                "If it's under $500/month, I'm interested. Otherwise, no."
            ]
        },
        {
            "name": "The Eager Buyer",
            "description": "Has budget and pain, ready to move",
            "openness": 0.9,
            "price_sensitivity": 0.3,
            "decision_speed": 0.9,
            "typical_responses": [
                "This is exactly what I need! When can we start?",
                "I'm paying way too much for leads right now. Let's talk.",
                "Can I see a demo this week?",
                "What's the fastest we can get this running?",
                "I need this in 3 territories. What's the price?"
            ]
        },
        {
            "name": "The Bargain Hunter",
            "description": "Wants the deal, but wants it cheaper",
            "openness": 0.7,
            "price_sensitivity": 0.9,
            "decision_speed": 0.5,
            "typical_responses": [
                "Looks good, but $297 is too much. What can you do?",
                "My budget is $150/month. Can you work with that?",
                "I need 3 months at 50% off to try it out.",
                "Competitor X is offering the same for $199.",
                "I'll sign today for $197/month. Final offer."
            ]
        },
        {
            "name": "The Ghost",
            "description": "Disappears, rarely responds",
            "openness": 0.1,
            "price_sensitivity": 0.5,
            "decision_speed": 0.0,
            "typical_responses": [
                "",
                "",
                "Unsubscribe",
                "Please remove me from your list.",
                "Not interested."
            ]
        },
        {
            "name": "The Researcher",
            "description": "Wants to understand everything before deciding",
            "openness": 0.6,
            "price_sensitivity": 0.5,
            "decision_speed": 0.3,
            "typical_responses": [
                "How is the data collected? I need technical details.",
                "What's your accuracy rate on POS detection?",
                "Can you send me your data methodology whitepaper?",
                "Do you have case studies from companies in my exact vertical?",
                "What happens if the leads don't convert?"
            ]
        },
        {
            "name": "The Loyal Customer",
            "description": "Already likes the brand, easy upsell",
            "openness": 0.8,
            "price_sensitivity": 0.4,
            "decision_speed": 0.7,
            "typical_responses": [
                "Love your paper! Tell me more about DataDepot.",
                "Your service has been great. What else you got?",
                "Can you bundle this with my existing order?",
                "Miles took great care of me last time. Is he available?",
                "Sold. Just send me the contract."
            ]
        }
    ]
    
    @classmethod
    def get_random_profile(cls):
        """Returns a random customer profile"""
        return random.choice(cls.PROFILES)

class CustomerResponder:
    """
    Simulates customer responses to sales emails
    Tracks conversation state and progresses through sales cycle
    """
    
    def __init__(self, customer_name="Test Customer", company="Test Company", 
                 profile=None, territory="Los Angeles"):
        self.customer_name = customer_name
        self.company = company
        self.profile = profile or CustomerProfile.get_random_profile()
        self.territory = territory
        
        self.stage = SalesStage.NEW
        self.email_history = []
        self.sentiment_history = []
        self.response_count = 0
        
        # State variables
        self.has_requested_sample = False
        self.has_had_call = False
        self.has_seen_pricing = False
        self.has_objected_to_price = False
        self.has_requested_references = False
        
    def respond_to_email(self, email_data, email_count=1):
        """
        Generate a response to an email
        Returns dict with response details
        """
        self.response_count += 1
        
        # Determine sentiment based on profile and email stage
        sentiment = self._determine_sentiment(email_data)
        self.sentiment_history.append(sentiment)
        
        # Generate response text
        response_text = self._generate_response(email_data, sentiment)
        
        # Determine next action
        next_action = self._determine_next_action(email_data, sentiment)
        
        # Update stage
        self._update_stage(email_data, sentiment)
        
        # Log the exchange
        exchange = {
            "email_id": email_data.get("id"),
            "email_subject": email_data.get("subject"),
            "sentiment": sentiment.value,
            "response": response_text,
            "stage_after": self.stage.value,
            "next_action": next_action
        }
        self.email_history.append(exchange)
        
        return {
            "customer_name": self.customer_name,
            "customer_company": self.company,
            "profile": self.profile["name"],
            "email_number": email_count,
            "sentiment": sentiment.value,
            "response_text": response_text,
            "current_stage": self.stage.value,
            "next_action": next_action,
            "emails_exchanged": len(self.email_history),
            "conversation_complete": self.stage in [SalesStage.CLOSED_WON, SalesStage.CLOSED_LOST]
        }
    
    def _determine_sentiment(self, email_data):
        """Determine customer sentiment based on profile and email context"""
        stage = email_data.get("stage", "prospecting")
        
        # Base openness from profile
        base_openness = self.profile["openness"]
        
        # Adjust based on email stage
        stage_adjustments = {
            "prospecting": -0.1,
            "research": 0.1,
            "handoff": 0.0,
            "nurture": 0.0,
            "scheduling": 0.2,
            "discovery": 0.3,
            "negotiation": 0.0,
            "closing": 0.2,
            "closed_won": 0.5,
            "breakup": -0.3,
            "retention": 0.3,
            "upsell": 0.1,
            "cross_sell": 0.1
        }
        
        adjusted = base_openness + stage_adjustments.get(stage, 0)
        adjusted = max(0.0, min(1.0, adjusted))  # Clamp to 0-1
        
        # Add some randomness
        roll = random.random()
        
        if roll < adjusted * 0.7:
            return CustomerSentiment.INTERESTED
        elif roll < adjusted:
            return CustomerSentiment.NEUTRAL
        elif roll < adjusted + 0.2:
            return CustomerSentiment.SKEPTICAL
        elif roll < adjusted + 0.4:
            return CustomerSentiment.BUSY
        elif roll < adjusted + 0.6:
            return CustomerSentiment.NOT_INTERESTED
        else:
            return CustomerSentiment.ANNOYED
    
    def _generate_response(self, email_data, sentiment):
        """Generate response text based on sentiment"""
        
        # Special case for Ghost profile
        if self.profile["name"] == "The Ghost" and random.random() < 0.6:
            return ""
        
        if sentiment == CustomerSentiment.INTERESTED:
            responses = [
                f"This sounds interesting. Tell me more about how it works for {self.territory} specifically.",
                "I'm definitely interested. What's the next step?",
                f"Can we set up a call? I'm usually free {{Meeting_Time}}.",
                "This is exactly the kind of thing I've been looking for. How soon can we start?",
                f"I like what I'm seeing. Do you have any references from companies similar to {self.company}?"
            ]
        elif sentiment == CustomerSentiment.SKEPTICAL:
            responses = self.profile["typical_responses"]
            if "sample" in email_data.get("subject", "").lower() and not self.has_requested_sample:
                self.has_requested_sample = True
                return f"I'll try a sample, but I'm skeptical. Send it to {self.customer_name.lower().replace(' ', '.')}@{self.company.lower().replace(' ', '')}.com"
        elif sentiment == CustomerSentiment.NEUTRAL:
            responses = [
                "Thanks for reaching out. I'll take a look when I have time.",
                "Email me more details and I'll review.",
                "Not sure if this is the right time, but I'll keep it in mind.",
                "Let me think about it and get back to you.",
                "I see what you're offering. Need to discuss with my team."
            ]
        elif sentiment == CustomerSentiment.BUSY:
            responses = [
                "Can you follow up next week? Swamped right now.",
                "Not the right time. Reach out in a month.",
                "Put me on your nurture list. Too busy to evaluate now.",
                "Quick question: How long is your typical sales process?",
                "Email only for now. No calls please."
            ]
        elif sentiment == CustomerSentiment.NOT_INTERESTED:
            responses = [
                "Not interested at this time.",
                "We have a solution that works for us already.",
                "This isn't a fit for our business model.",
                "Please remove me from your list.",
                "We don't buy leads. We generate our own."
            ]
        elif sentiment == CustomerSentiment.ANNOYED:
            responses = [
                "Stop emailing me.",
                "Unsubscribe.",
                "This is the third email I've gotten. Please stop.",
                "I reported this as spam.",
                "Remove me immediately."
            ]
        else:
            responses = ["Thanks for the email."]
        
        return random.choice(responses)
    
    def _determine_next_action(self, email_data, sentiment):
        """Determine what the salesperson should do next"""
        stage = email_data.get("stage", "prospecting")
        
        if sentiment in [CustomerSentiment.INTERESTED, CustomerSentiment.NEUTRAL]:
            if stage in ["prospecting", "research", "handoff"]:
                return "schedule_discovery_call"
            elif stage == "discovery":
                return "send_proposal"
            elif stage == "negotiation":
                return "attempt_close"
            elif stage == "closed_won":
                return "handoff_to_onboarding"
            elif stage == "breakup":
                return "resurrect_opportunity"
        elif sentiment == CustomerSentiment.SKEPTICAL:
            if "sample" in str(email_data).lower():
                return "send_sample_and_follow_up"
            return "send_case_studies_and_references"
        elif sentiment == CustomerSentiment.BUSY:
            return "nurture_sequence_delay_30_days"
        elif sentiment in [CustomerSentiment.NOT_INTERESTED, CustomerSentiment.ANNOYED]:
            return "mark_lost_and_remove_from_sequence"
        
        return "continue_sequence"
    
    def _update_stage(self, email_data, sentiment):
        """Update the sales stage based on interaction"""
        current_stage = self.stage
        email_stage = email_data.get("stage", "prospecting")
        
        # Progressive stage advancement
        stage_progression = {
            SalesStage.NEW: SalesStage.CONTACTED,
            SalesStage.CONTACTED: SalesStage.ENGAGED,
            SalesStage.ENGAGED: SalesStage.QUALIFIED,
            SalesStage.QUALIFIED: SalesStage.PROPOSAL,
            SalesStage.PROPOSAL: SalesStage.NEGOTIATION
        }
        
        # If interested and not at end stage, advance
        if sentiment == CustomerSentiment.INTERESTED and current_stage != SalesStage.CLOSED_WON:
            if current_stage in stage_progression:
                # Small chance to close won from any late stage
                if current_stage in [SalesStage.PROPOSAL, SalesStage.NEGOTIATION] and random.random() < 0.3:
                    self.stage = SalesStage.CLOSED_WON
                else:
                    self.stage = stage_progression[current_stage]
        
        # If annoyed or not interested multiple times, close lost
        if sentiment in [CustomerSentiment.ANNOYED, CustomerSentiment.NOT_INTERESTED]:
            annoyed_count = sum(1 for s in self.sentiment_history if s in [CustomerSentiment.ANNOYED, CustomerSentiment.NOT_INTERESTED])
            if annoyed_count >= 2:
                self.stage = SalesStage.CLOSED_LOST
        
        # If breakup email and no response, close lost
        if email_stage == "breakup" and sentiment == CustomerSentiment.NOT_INTERESTED:
            self.stage = SalesStage.CLOSED_LOST

class TestCustomerGenerator:
    """Generates test customers for sales testing"""
    
    FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", 
                   "Avery", "Parker", "Dakota", "Reese", "Sawyer", "Hayden", "Emerson",
                   "John", "Sarah", "Michael", "Emily", "David", "Jessica", "Robert",
                   "Jennifer", "William", "Elizabeth", "James", "Linda", "Richard"]
    
    LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
                  "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
                  "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
    
    COMPANY_PREFIXES = ["POS", "Tech", "Restaurant", "Dining", "Food", "Hospitality",
                        "Merchant", "Retail", "Service", "Solution", "System", "Smart"]
    COMPANY_SUFFIXES = ["Solutions", "Technologies", "Services", "Group", "Partners",
                        "Consulting", "Enterprises", "Systems", "Inc", "LLC", "Corp"]
    
    TERRITORIES = ["Los Angeles", "San Francisco", "San Diego", "Orange County",
                   "Sacramento", "San Jose", "Oakland", "Fresno", "Bakersfield",
                   "Santa Barbara", "Monterey", "Riverside", "Ventura", "San Luis Obispo"]
    
    @classmethod
    def generate_customer(cls, profile_name=None):
        """Generate a random test customer"""
        first = random.choice(cls.FIRST_NAMES)
        last = random.choice(cls.LAST_NAMES)
        name = f"{first} {last}"
        
        company = f"{random.choice(cls.COMPANY_PREFIXES)} {random.choice(cls.COMPANY_SUFFIXES)}"
        
        territory = random.choice(cls.TERRITORIES)
        
        # Get specific profile if requested
        if profile_name:
            profile = next((p for p in CustomerProfile.PROFILES if p["name"] == profile_name), None)
        else:
            profile = CustomerProfile.get_random_profile()
        
        return CustomerResponder(
            customer_name=name,
            company=company,
            profile=profile,
            territory=territory
        )
    
    @classmethod
    def generate_customer_batch(cls, count=10, include_all_profiles=False):
        """Generate a batch of test customers"""
        customers = []
        
        if include_all_profiles:
            # Generate at least one of each profile type
            for profile in CustomerProfile.PROFILES:
                customers.append(cls.generate_customer(profile_name=profile["name"]))
            # Fill remaining with random
            remaining = count - len(CustomerProfile.PROFILES)
            for _ in range(max(0, remaining)):
                customers.append(cls.generate_customer())
        else:
            for _ in range(count):
                customers.append(cls.generate_customer())
        
        return customers

def run_test_simulation(emails_to_send, num_customers=7):
    """
    Run a full test simulation with multiple customers
    
    Args:
        emails_to_send: List of email data dicts
        num_customers: Number of customer personas to test
    """
    results = []
    
    print("=" * 80)
    print("SALES EMAIL TEST SIMULATION")
    print("=" * 80)
    print(f"\nTesting {len(emails_to_send)} emails across {num_customers} customer profiles")
    print("\nCustomer Profiles:")
    for i, profile in enumerate(CustomerProfile.PROFILES[:num_customers], 1):
        print(f"  {i}. {profile['name']}: {profile['description']}")
    print()
    
    for profile in CustomerProfile.PROFILES[:num_customers]:
        customer = TestCustomerGenerator.generate_customer(profile_name=profile["name"])
        
        print(f"\n{'=' * 80}")
        print(f"CUSTOMER: {customer.customer_name} ({customer.company})")
        print(f"PROFILE: {customer.profile['name']}")
        print(f"TERRITORY: {customer.territory}")
        print(f"{'=' * 80}\n")
        
        for i, email in enumerate(emails_to_send, 1):
            result = customer.respond_to_email(email, email_count=i)
            
            print(f"\nEmail {i}: {email.get('subject', 'No subject')}")
            print(f"  Agent: {email.get('agent', 'Unknown')}")
            print(f"  Stage: {email.get('stage', 'Unknown')}")
            print(f"  -> Sentiment: {result['sentiment'].upper()}")
            print(f"  -> Response: \"{result['response_text'][:100]}{'...' if len(result['response_text']) > 100 else ''}\"")
            print(f"  -> Sales Stage: {result['current_stage']}")
            print(f"  -> Next Action: {result['next_action']}")
            
            if result['conversation_complete']:
                print(f"\n  [CONVERSATION COMPLETE: {result['current_stage'].upper()}]")
                break
        
        results.append({
            "customer": customer.customer_name,
            "company": customer.company,
            "profile": customer.profile["name"],
            "final_stage": customer.stage.value,
            "emails_exchanged": len(customer.email_history),
            "outcome": "WON" if customer.stage == SalesStage.CLOSED_WON else 
                      "LOST" if customer.stage == SalesStage.CLOSED_LOST else "OPEN"
        })
    
    # Summary
    print(f"\n{'=' * 80}")
    print("SIMULATION SUMMARY")
    print(f"{'=' * 80}\n")
    
    won = sum(1 for r in results if r["outcome"] == "WON")
    lost = sum(1 for r in results if r["outcome"] == "LOST")
    open_count = sum(1 for r in results if r["outcome"] == "OPEN")
    
    print(f"Results: {won} WON | {lost} LOST | {open_count} OPEN")
    print(f"\nBreakdown:")
    for r in results:
        status_emoji = "✅" if r["outcome"] == "WON" else "❌" if r["outcome"] == "LOST" else "⏳"
        print(f"  {status_emoji} {r['customer']} ({r['profile']}): {r['outcome']} after {r['emails_exchanged']} emails")
    
    return results

# Export
__all__ = [
    'CustomerResponder', 
    'CustomerProfile', 
    'TestCustomerGenerator',
    'CustomerSentiment',
    'SalesStage',
    'run_test_simulation'
]

if __name__ == "__main__":
    # Example test with a few emails
    test_emails = [
        {"id": "miles_01", "agent": "Miles", "stage": "prospecting", "subject": "CA restaurant intel you don't have"},
        {"id": "clippy_02", "agent": "Clippy-42", "stage": "handoff", "subject": "Connecting you with Miles"},
        {"id": "pulp_01", "agent": "Pulp", "stage": "discovery", "subject": "Your custom proposal is ready"},
        {"id": "pulp_03", "agent": "Pulp", "stage": "closing", "subject": "Last chance: county data"},
    ]
    
    run_test_simulation(test_emails, num_customers=5)