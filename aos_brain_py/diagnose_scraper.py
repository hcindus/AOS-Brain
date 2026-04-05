#!/usr/bin/env python3
"""
Scraper Diagnostic Tool
Uses Hermes state tracking + Mini-Agent (MiniMax-M2.7) for analysis
"""

import sys
import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from integration.hermes_brain_adapter import HermesBrainAdapter
from integration.mini_agent_minimax import MiniAgentMiniMax
from config.rationed_api_manager import get_ration_manager


class ScraperDiagnostic:
    """
    Diagnose scraper issues using Hermes + Mini-Agent.
    """
    
    def __init__(self):
        self.hermes = HermesBrainAdapter()
        self.mini_agent = MiniAgentMiniMax(daily_limit=100)
        self.ration = get_ration_manager(100)
        
        print("=" * 70)
        print("🔧 SCRAPER DIAGNOSTIC (Hermes + Mini-Agent)")
        print("=" * 70)
        print()
    
    def check_hermes_state(self):
        """Check previous scraper runs in Hermes."""
        print("📋 Checking Hermes state...")
        
        state = self.hermes.read_hermes_state("ca_sos_scraper")
        if state:
            print(f"   Last run: {state.get('last_run', 'unknown')}")
            print(f"   Status: {state.get('status', 'unknown')}")
            return state
        else:
            print("   No previous state found")
            return {}
    
    def diagnose_endpoint(self, endpoint: str) -> dict:
        """Diagnose why endpoint is failing."""
        print(f"\n🔍 Diagnosing endpoint: {endpoint}")
        
        if self.ration.can_make_call("Mini-Agent"):
            query = f"""The CA Secretary of State scraper is failing with error: 
"getaddrinfo ENOTFOUND businesssearch.sos.ca.gov"

The endpoint appears to be: https://businesssearch.sos.ca.gov/api/v1/business/search

Possible causes:
1. API endpoint has changed
2. Service requires authentication/API key
3. Rate limiting or blocking
4. Service moved to different domain
5. Network/DNS issues

What should I check first? Provide 3 diagnostic steps."""
            
            result = self.mini_agent.process(query, system="You are a network diagnostics expert.")
            
            print(f"\n🤖 Mini-Agent (MiniMax-M2.7) Analysis:")
            print(f"   {result['text'][:500]}")
            
            tokens = result.get('usage', {}).get('output_tokens', 100)
            self.ration.record_call("Mini-Agent", tokens)
            return result
        else:
            return {"text": "Check DNS resolution", "source": "local"}
    
    def propose_fix(self, diagnosis: dict):
        """Propose fix based on diagnosis."""
        print("\n🔧 Proposing Fix...")
        
        if self.ration.can_make_call("Mini-Agent"):
            query = f"""Based on diagnosis: {diagnosis.get('text', 'DNS failed')}

The CA SOS scraper needs to fetch business data from California Secretary of State.
Current endpoint: businesssearch.sos.ca.gov/api/v1/business/search (failing)

What are 3 alternative approaches to get CA business data?"""
            
            result = self.mini_agent.process(query, system="You are a data acquisition specialist.")
            
            print(f"\n🤖 Mini-Agent Proposal:")
            print(f"   {result['text'][:500]}")
            
            tokens = result.get('usage', {}).get('output_tokens', 100)
            self.ration.record_call("Mini-Agent", tokens)
            return result['text']
        return "local_proposal"
    
    def run(self):
        """Run full diagnostic."""
        state = self.check_hermes_state()
        diagnosis = self.diagnose_endpoint("businesssearch.sos.ca.gov")
        fix = self.propose_fix(diagnosis)
        
        # Update Hermes
        self.hermes.write_hermes_state("ca_sos_scraper", {
            "last_diagnostic": "2026-03-28",
            "status": "endpoint_failed",
            "error": "ENOTFOUND",
            "diagnosis": diagnosis.get('text', 'unknown')[:200],
            "proposed_fix": fix[:200]
        })
        
        print("\n✅ DIAGNOSTIC COMPLETE")
        print(f"Calls used: {self.ration.get_status()['daily_calls']}/100")


if __name__ == "__main__":
    diagnostic = ScraperDiagnostic()
    diagnostic.run()
