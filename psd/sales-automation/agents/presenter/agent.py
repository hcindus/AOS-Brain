#!/usr/bin/env python3
"""
SOP-006: AI-Powered Proposal Generation & Presenting Agent
Phase 3 of Dan Martell 5-Phase Sales Framework

Target: Custom proposal <10 min, 35%+ close rate
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DepotProposal-1")


class ProposalAgent:
    """
    AI Proposal Generation Agent for PSD
    
    Responsibilities:
    - Research prospect intelligence
    - Generate custom proposals
    - Create talk tracks
    - Generate VSL scripts
    """
    
    def __init__(self):
        self.agent_name = "DepotProposal-1"
        self.model = "qwen2.5:14b"  # Deep reasoning
        self.voice_model = "Mort_II:latest"
        
        # Template library
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict:
        """Load proposal templates"""
        return {
            "restaurant_bar": {
                "name": "Restaurant/Bar Package",
                "pain_points": [
                    "Running out of receipt paper during rush",
                    "Slow supplier delivery",
                    "Inconsistent quality"
                ],
                "products": [
                    "Thermal receipt rolls (3-1/8\" x 230')",
                    "Liquor pourers (1oz, 1.5oz, 2oz)",
                    "Cleaning supplies",
                    "Bar mats and accessories"
                ],
                "value_prop": "Never run out, 24-hour delivery guarantee",
                "case_study": "The Corner Bar - reduced stockouts by 95%"
            },
            "retail_chain": {
                "name": "Retail Chain Package",
                "pain_points": [
                    "Inconsistent quality across locations",
                    "Complex ordering process",
                    "Multiple supplier management"
                ],
                "products": [
                    "Custom labels and tags",
                    "Branded shopping bags",
                    "Inventory management system",
                    "Multi-location delivery"
                ],
                "value_prop": "Centralized ordering, location-specific delivery",
                "case_study": "Metro Retail - unified 12 locations"
            },
            "new_business": {
                "name": "New Business Setup",
                "pain_points": [
                    "Don't know what they need",
                    "Tight timeline for opening",
                    "Overwhelmed by options"
                ],
                "products": [
                    "Complete starter kit consultation",
                    "Setup checklist",
                    "30-day supply package",
                    "Ongoing support"
                ],
                "value_prop": "Complete setup in 48 hours, ongoing support",
                "case_study": "Brew & Bean - opened on time with full stock"
            }
        }
    
    def gather_intelligence(self, qualified_lead: Dict) -> Dict:
        """
        Gather pre-call intelligence
        """
        logger.info(f"Gathering intelligence for {qualified_lead['company_name']}")
        
        intelligence = {
            "company": qualified_lead["company_name"],
            "industry": qualified_lead.get("industry", "Unknown"),
            "locations": qualified_lead.get("num_locations", 1),
            "decision_maker": qualified_lead.get("decision_maker_name"),
            "pain_points": qualified_lead.get("pain_points", []),
            "budget": qualified_lead.get("budget_confirmed"),
            "timeline": qualified_lead.get("timeline"),
            "discovered_needs": [],
            "research_notes": {}
        }
        
        # Would integrate with:
        # - LinkedIn research
        # - Company website scraping
        # - News/search signals
        # - Similar customer analysis
        
        return intelligence
    
    def generate_proposal(self, intelligence: Dict, template_key: str = None) -> Dict:
        """
        Generate custom proposal using AI
        """
        logger.info(f"Generating proposal for {intelligence['company']}")
        
        # Select template based on intelligence
        if not template_key:
            template_key = self._select_template(intelligence)
        
        template = self.templates.get(template_key, self.templates["restaurant_bar"])
        
        # Build prompt for AI
        prompt = self._build_proposal_prompt(intelligence, template)
        
        # Would call qwen2.5:14b here
        # For now, structure the expected output
        
        proposal = {
            "proposal_id": f"PROP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "company": intelligence["company"],
            "generated_at": datetime.now().isoformat(),
            "template_used": template_key,
            
            "sections": {
                "pain_agitation": self._generate_pain_section(intelligence, template),
                "solution": self._generate_solution_section(intelligence, template),
                "products": self._select_products(intelligence, template),
                "pricing": self._generate_pricing(intelligence),
                "social_proof": template["case_study"],
                "cta": "Schedule your first delivery today"
            },
            
            "metadata": {
                "estimated_value": intelligence.get("budget", 2500),
                "confidence": 0.88
            }
        }
        
        return proposal
    
    def _select_template(self, intelligence: Dict) -> str:
        """Select best template based on intelligence"""
        industry = intelligence.get("industry", "").lower()
        
        if "restaurant" in industry or "bar" in industry or "cafe" in industry:
            return "restaurant_bar"
        elif "retail" in industry or "store" in industry:
            return "retail_chain"
        elif intelligence.get("is_new_business"):
            return "new_business"
        
        return "restaurant_bar"  # Default
    
    def _build_proposal_prompt(self, intelligence: Dict, template: Dict) -> str:
        """Build AI prompt for proposal generation"""
        return f"""
You are an expert sales consultant for Performance Supply Depot.

PROSPECT:
- Company: {intelligence['company']}
- Industry: {intelligence['industry']}
- Locations: {intelligence['locations']}
- Pain Points: {', '.join(intelligence['pain_points'])}
- Budget: ${intelligence.get('budget', 'Unknown')}

Create a personalized proposal with:
1. Pain agitation (describe their pain better than they can)
2. Solution presentation (how PSD solves it)
3. Product recommendations
4. Pricing (within budget)
5. Social proof
6. Clear CTA

Tone: Consultative, energetic, professional
"""
    
    def _generate_pain_section(self, intelligence: Dict, template: Dict) -> str:
        """Generate pain agitation section"""
        pain_points = intelligence.get("pain_points", template["pain_points"])
        
        # Would be AI-generated
        return f"""Running a {intelligence['industry']} means constantly juggling priorities.

When you're dealing with {pain_points[0].lower()}, it's not just inconvenient—it's 
costing you money. Every minute spent dealing with supply issues is a minute not spent 
growing your business.

Sound familiar?"""
    
    def _generate_solution_section(self, intelligence: Dict, template: Dict) -> str:
        """Generate solution section"""
        return f"""Here's how Performance Supply Depot solves this:

✓ {template['value_prop']}
✓ Consistent quality across all orders
✓ Dedicated account manager
✓ Automatic reorder reminders

We become your supply partner, not just another vendor."""
    
    def _select_products(self, intelligence: Dict, template: Dict) -> List[Dict]:
        """Select products based on intelligence"""
        products = []
        
        for product in template["products"]:
            products.append({
                "name": product,
                "quantity": "TBD",  # Would calculate from intelligence
                "unit_price": 0,    # Would lookup from catalog
                "total": 0
            })
        
        return products
    
    def _generate_pricing(self, intelligence: Dict) -> Dict:
        """Generate pricing within budget"""
        budget = intelligence.get("budget", 2500)
        
        return {
            "subtotal": budget * 0.9,
            "shipping": 0,  # Free shipping over $500
            "tax": budget * 0.07,
            "total": budget * 0.97,  # Under budget
            "payment_terms": "Net 30",
            "delivery": "24-48 hours"
        }
    
    def generate_talk_track(self, proposal: Dict) -> Dict:
        """
        Generate talk track for sales call
        """
        logger.info(f"Generating talk track for {proposal['company']}")
        
        return {
            "opening": f"""Thanks for taking the time today, [Name]. 
I spent some time looking into {proposal['company']} and I've got to say, 
I'm excited about what you're building.

Before I show you what I put together, I want to make sure I understand 
your situation correctly...""",
            
            "pain_questions": [
                f"You mentioned dealing with {proposal['sections']['pain_agitation'][:50]}...",
                "How is that impacting your day-to-day operations?",
                "What does it cost you when that happens?",
                "What have you tried to solve it so far?"
            ],
            
            "solution_walkthrough": [
                "Here's what I put together for you...",
                "[Screen share proposal]",
                f"I looked at your situation, and I thought about what {proposal['sections']['social_proof']} went through..."
            ],
            
            "likely_objections": [
                {
                    "objection": "Price too high",
                    "response": "I understand budget is a concern. What specifically about the investment concerns you?"
                },
                {
                    "objection": "Need to think about it",
                    "response": "Of course. What timeline are you thinking?"
                },
                {
                    "objection": "Happy with current supplier",
                    "response": "What do you like most about them? What would you change if you could?"
                }
            ],
            
            "closing": [
                "Does this feel like the right solution for your business?",
                "Are you ready to join the team?",
                "Let's get you set up with your first delivery."
            ],
            
            "next_steps": [
                "Confirm delivery date",
                "Set up account",
                "Schedule onboarding call"
            ]
        }
    
    def export_proposal_pdf(self, proposal: Dict, output_path: str):
        """
        Export proposal to PDF
        """
        # Would use PDF generation library
        logger.info(f"Exporting proposal to {output_path}")
        
        # Placeholder - would generate actual PDF
        with open(output_path.replace('.pdf', '.md'), 'w') as f:
            f.write(f"# Proposal for {proposal['company']}\n\n")
            f.write(f"Generated: {proposal['generated_at']}\n\n")
            f.write(f"## Pain Points\n\n{proposal['sections']['pain_agitation']}\n\n")
            f.write(f"## Solution\n\n{proposal['sections']['solution']}\n\n")
            f.write(f"## Pricing\n\nTotal: ${proposal['sections']['pricing']['total']:.2f}\n\n")


def main():
    """CLI entry point"""
    agent = ProposalAgent()
    
    # Example usage
    test_lead = {
        "company_name": "Test Restaurant",
        "industry": "Restaurant",
        "num_locations": 2,
        "decision_maker_name": "John Smith",
        "pain_points": ["Running low on supplies", "Slow delivery"],
        "budget_confirmed": 2500
    }
    
    # Generate intelligence and proposal
    intel = agent.gather_intelligence(test_lead)
    proposal = agent.generate_proposal(intel)
    talk_track = agent.generate_talk_track(proposal)
    
    print(f"Generated proposal for {proposal['company']}")
    print(f"Template: {proposal['template_used']}")
    print(f"Talk track keys: {list(talk_track.keys())}")


if __name__ == "__main__":
    main()
