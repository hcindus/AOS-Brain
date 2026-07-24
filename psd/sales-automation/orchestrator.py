#!/usr/bin/env python3
"""
Sales Automation Orchestrator
Coordinates all 5 phases of Dan Martell AI Sales Framework

SOPs: 004, 005, 006, 007, 008
"""

import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

from agents.prospector.agent import ProspectorAgent
from agents.qualifier.agent import VoiceQualifierAgent
from agents.presenter.agent import ProposalAgent
from agents.coach.agent import ObjectionCoachAgent
from agents.closer.agent import ClosingDeliveryAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SalesOrchestrator")


class SalesAutomationOrchestrator:
    """
    Orchestrates the complete 5-phase AI sales pipeline:
    
    1. Prospecting (SOP-004) → AI Prospector Agent
    2. Qualifying (SOP-005) → Voice Qualifier Agent
    3. Presenting (SOP-006) → Proposal Agent
    4. Objection Handling (SOP-007) → Coach Agent (whisper mode)
    5. Closing/Delivery (SOP-008) → Closer Agent
    """
    
    def __init__(self):
        self.agents = {
            "prospector": ProspectorAgent(),
            "qualifier": VoiceQualifierAgent(),
            "presenter": ProposalAgent(),
            "coach": ObjectionCoachAgent(),
            "closer": ClosingDeliveryAgent()
        }
        
        self.state_dir = Path("/root/.openclaw/workspace/psd/sales-automation/state")
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
    async def run_phase_1_prospecting(self, company_list: List[str]) -> List[Dict]:
        """
        Phase 1: AI-Powered Prospecting
        SOP-004
        """
        logger.info("=== PHASE 1: PROSPECTING ===")
        
        agent = self.agents["prospector"]
        
        # Process batch
        leads = agent.run_batch(company_list)
        
        # Export to hot lead queue
        hot_leads = [l for l in leads if l["icp_score"] >= 7]
        
        # Save state
        self._save_state("phase_1_output", {
            "timestamp": datetime.now().isoformat(),
            "total_processed": len(company_list),
            "qualified_leads": len(leads),
            "hot_leads": len(hot_leads),
            "leads": hot_leads
        })
        
        logger.info(f"Phase 1 complete: {len(hot_leads)} hot leads ready for qualification")
        return hot_leads
    
    async def run_phase_2_qualifying(self, leads: List[Dict]) -> List[Dict]:
        """
        Phase 2: AI-Powered Qualifying
        SOP-005
        """
        logger.info("=== PHASE 2: QUALIFYING ===")
        
        agent = self.agents["qualifier"]
        qualified_appointments = []
        
        for lead in leads[:20]:  # Limit for testing
            # Initiate call
            call = agent.initiate_call(lead)
            
            # Conduct qualification
            bant, conversation_log = agent.conduct_qualification(call["call_id"])
            
            # Score
            routing = agent.score_lead(bant)
            
            if routing["score"] >= 60:
                # Book calendar
                availability = ["2026-07-28 14:00", "2026-07-28 15:00"]
                booking = agent.book_calendar(lead, bant, availability)
                
                if booking:
                    qualified_appointments.append({
                        "lead": lead,
                        "qualification": bant.__dict__,
                        "booking": booking,
                        "score": routing["score"]
                    })
                    
                    logger.info(f"Booked appointment: {lead['company_name']} (score: {routing['score']})")
        
        # Save state
        self._save_state("phase_2_output", {
            "timestamp": datetime.now().isoformat(),
            "leads_processed": len(leads),
            "qualified_appointments": len(qualified_appointments),
            "appointments": qualified_appointments
        })
        
        logger.info(f"Phase 2 complete: {len(qualified_appointments)} qualified appointments")
        return qualified_appointments
    
    async def run_phase_3_presenting(self, appointments: List[Dict]) -> List[Dict]:
        """
        Phase 3: AI-Powered Presenting
        SOP-006
        """
        logger.info("=== PHASE 3: PRESENTING ===")
        
        agent = self.agents["presenter"]
        proposals = []
        
        for appt in appointments:
            lead = appt["lead"]
            
            # Gather intelligence
            intel = agent.gather_intelligence({
                **lead,
                **appt["qualification"]
            })
            
            # Generate proposal
            proposal = agent.generate_proposal(intel)
            
            # Generate talk track
            talk_track = agent.generate_talk_track(proposal)
            
            # Export PDF
            output_path = f"/root/.openclaw/workspace/psd/sales-automation/output/proposal_{lead['lead_id']}.md"
            agent.export_proposal_pdf(proposal, output_path)
            
            proposals.append({
                "appointment": appt,
                "proposal": proposal,
                "talk_track": talk_track,
                "pdf_path": output_path
            })
            
            logger.info(f"Generated proposal: {lead['company_name']}")
        
        # Save state
        self._save_state("phase_3_output", {
            "timestamp": datetime.now().isoformat(),
            "proposals_generated": len(proposals),
            "proposals": proposals
        })
        
        logger.info(f"Phase 3 complete: {len(proposals)} proposals ready")
        return proposals
    
    async def run_phase_4_objection_handling(self, call_transcript: List[Dict]) -> Optional[Dict]:
        """
        Phase 4: AI-Powered Objection Handling
        SOP-007
        
        Runs in parallel during sales calls (whisper mode)
        """
        agent = self.agents["coach"]
        
        # Analyze transcript for objections
        analysis = agent.analyze_transcript(call_transcript, "CurrentRep")
        
        if analysis["total_objections"] > 0:
            # Get first objection
            objection = analysis["objections"][0]
            
            # Generate responses
            responses = agent.generate_responses(
                objection.objection_text,
                objection.category
            )
            
            # Whisper mode suggestion
            whisper = agent.whisper_mode(objection.objection_text)
            
            return {
                "objection_detected": True,
                "category": objection.category,
                "suggested_responses": responses,
                "whisper": whisper
            }
        
        return None
    
    async def run_phase_5_closing(self, deal: Dict) -> Dict:
        """
        Phase 5: AI-Powered Closing & Delivery
        SOP-008
        """
        logger.info("=== PHASE 5: CLOSING & DELIVERY ===")
        
        agent = self.agents["closer"]
        
        # Process close
        customer = agent.process_close(deal)
        
        # Generate order confirmation
        confirmation = agent.generate_order_confirmation(customer, deal)
        
        # Generate "How do you feel?" script for human to use
        feel_script = agent.how_do_you_feel_script(customer.contact_name)
        
        # Generate win agreement script
        win_agreement = agent.win_agreement_script()
        
        result = {
            "customer": customer.__dict__,
            "confirmation_email": confirmation,
            "scripts": {
                "how_do_you_feel": feel_script,
                "win_agreement": win_agreement
            },
            "onboarding_triggered": True
        }
        
        # Save state
        self._save_state("phase_5_output", result)
        
        logger.info(f"Phase 5 complete: Customer {customer.customer_id} onboarded")
        return result
    
    async def run_full_pipeline(self, company_list: List[str]):
        """
        Run complete 5-phase pipeline
        """
        logger.info("=== STARTING FULL SALES PIPELINE ===")
        
        # Phase 1: Prospecting
        hot_leads = await self.run_phase_1_prospecting(company_list)
        
        if not hot_leads:
            logger.warning("No hot leads generated. Stopping pipeline.")
            return
        
        # Phase 2: Qualifying
        appointments = await self.run_phase_2_qualifying(hot_leads)
        
        if not appointments:
            logger.warning("No qualified appointments. Stopping pipeline.")
            return
        
        # Phase 3: Presenting
        proposals = await self.run_phase_3_presenting(appointments)
        
        # Phase 4: Objection handling (runs during calls)
        # This would be triggered by real-time call monitoring
        
        # Phase 5: Closing (would trigger on deal close)
        # This would be triggered by CRM webhook
        
        logger.info("=== FULL PIPELINE COMPLETE ===")
        
        return {
            "hot_leads": len(hot_leads),
            "qualified_appointments": len(appointments),
            "proposals_generated": len(proposals)
        }
    
    def _save_state(self, name: str, data: Dict):
        """Save pipeline state to disk"""
        state_file = self.state_dir / f"{name}.json"
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)


async def main():
    """CLI entry point"""
    orchestrator = SalesAutomationOrchestrator()
    
    # Test with sample companies
    test_companies = [
        "Downtown Grill",
        "Metro Cafe",
        "Corner Bar",
        "Retail Plus",
        "Bistro 42"
    ]
    
    results = await orchestrator.run_full_pipeline(test_companies)
    
    print("\n=== RESULTS ===")
    print(f"Hot leads: {results['hot_leads']}")
    print(f"Qualified appointments: {results['qualified_appointments']}")
    print(f"Proposals generated: {results['proposals_generated']}")


if __name__ == "__main__":
    asyncio.run(main())
