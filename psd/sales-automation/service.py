#!/usr/bin/env python3
"""
Sales Automation Service
Runs as systemd service, exposes HTTP API for integration
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional
from pathlib import Path

from aiohttp import web

from orchestrator import SalesAutomationOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SalesAutomationService")


class SalesAutomationService:
    """
    HTTP service wrapping the sales automation orchestrator
    """
    
    def __init__(self, host="0.0.0.0", port=8090):
        self.host = host
        self.port = port
        self.orchestrator = SalesAutomationOrchestrator()
        self.app = web.Application()
        self._setup_routes()
        
    def _setup_routes(self):
        """Setup HTTP routes"""
        self.app.router.add_get('/health', self.health_check)
        self.app.router.add_post('/phase1/prospect', self.phase1_prospect)
        self.app.router.add_post('/phase2/qualify', self.phase2_qualify)
        self.app.router.add_post('/phase3/generate-proposal', self.phase3_proposal)
        self.app.router.add_post('/phase4/analyze-objection', self.phase4_objection)
        self.app.router.add_post('/phase5/close', self.phase5_close)
        self.app.router.add_post('/pipeline/full', self.full_pipeline)
        self.app.router.add_get('/status/{phase}', self.get_status)
        
    async def health_check(self, request):
        """Health check endpoint"""
        return web.json_response({
            "status": "healthy",
            "service": "sales-automation",
            "timestamp": datetime.now().isoformat()
        })
    
    async def phase1_prospect(self, request):
        """
        POST /phase1/prospect
        
        Body: {"companies": ["Company 1", "Company 2", ...]}
        """
        try:
            data = await request.json()
            companies = data.get("companies", [])
            
            if not companies:
                return web.json_response(
                    {"error": "No companies provided"}, status=400
                )
            
            leads = await self.orchestrator.run_phase_1_prospecting(companies)
            
            return web.json_response({
                "success": True,
                "leads_generated": len(leads),
                "leads": leads
            })
            
        except Exception as e:
            logger.error(f"Phase 1 error: {e}")
            return web.json_response(
                {"error": str(e)}, status=500
            )
    
    async def phase2_qualify(self, request):
        """
        POST /phase2/qualify
        
        Body: {"leads": [...]}
        """
        try:
            data = await request.json()
            leads = data.get("leads", [])
            
            if not leads:
                return web.json_response(
                    {"error": "No leads provided"}, status=400
                )
            
            appointments = await self.orchestrator.run_phase_2_qualifying(leads)
            
            return web.json_response({
                "success": True,
                "appointments_booked": len(appointments),
                "appointments": appointments
            })
            
        except Exception as e:
            logger.error(f"Phase 2 error: {e}")
            return web.json_response(
                {"error": str(e)}, status=500
            )
    
    async def phase3_proposal(self, request):
        """
        POST /phase3/generate-proposal
        
        Body: {"appointment": {...}}
        """
        try:
            data = await request.json()
            appointment = data.get("appointment")
            
            if not appointment:
                return web.json_response(
                    {"error": "No appointment provided"}, status=400
                )
            
            proposals = await self.orchestrator.run_phase_3_presenting([appointment])
            
            return web.json_response({
                "success": True,
                "proposals_generated": len(proposals),
                "proposals": proposals
            })
            
        except Exception as e:
            logger.error(f"Phase 3 error: {e}")
            return web.json_response(
                {"error": str(e)}, status=500
            )
    
    async def phase4_objection(self, request):
        """
        POST /phase4/analyze-objection
        
        Body: {"transcript": [...]}
        
        Real-time objection detection during calls
        """
        try:
            data = await request.json()
            transcript = data.get("transcript", [])
            
            if not transcript:
                return web.json_response(
                    {"error": "No transcript provided"}, status=400
                )
            
            result = await self.orchestrator.run_phase_4_objection_handling(transcript)
            
            return web.json_response({
                "success": True,
                "objection_detected": result is not None,
                "result": result
            })
            
        except Exception as e:
            logger.error(f"Phase 4 error: {e}")
            return web.json_response(
                {"error": str(e)}, status=500
            )
    
    async def phase5_close(self, request):
        """
        POST /phase5/close
        
        Body: {"deal": {...}}
        """
        try:
            data = await request.json()
            deal = data.get("deal")
            
            if not deal:
                return web.json_response(
                    {"error": "No deal provided"}, status=400
                )
            
            result = await self.orchestrator.run_phase_5_closing(deal)
            
            return web.json_response({
                "success": True,
                "customer_onboarded": True,
                "result": result
            })
            
        except Exception as e:
            logger.error(f"Phase 5 error: {e}")
            return web.json_response(
                {"error": str(e)}, status=500
            )
    
    async def full_pipeline(self, request):
        """
        POST /pipeline/full
        
        Run complete 5-phase pipeline
        
        Body: {"companies": [...]}
        """
        try:
            data = await request.json()
            companies = data.get("companies", [])
            
            if not companies:
                return web.json_response(
                    {"error": "No companies provided"}, status=400
                )
            
            results = await self.orchestrator.run_full_pipeline(companies)
            
            return web.json_response({
                "success": True,
                "results": results
            })
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            return web.json_response(
                {"error": str(e)}, status=500
            )
    
    async def get_status(self, request):
        """
        GET /status/{phase}
        
        Get status of a phase
        """
        phase = request.match_info.get('phase', 'all')
        
        state_file = Path(f"/root/.openclaw/workspace/psd/sales-automation/state/phase_{phase}_output.json")
        
        if state_file.exists():
            with open(state_file) as f:
                data = json.load(f)
            return web.json_response(data)
        
        return web.json_response(
            {"error": f"No status found for phase {phase}"}, status=404
        )
    
    def run(self):
        """Run the service"""
        logger.info(f"Starting Sales Automation Service on {self.host}:{self.port}")
        web.run_app(self.app, host=self.host, port=self.port)


if __name__ == "__main__":
    service = SalesAutomationService()
    service.run()
