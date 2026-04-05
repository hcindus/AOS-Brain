#!/usr/bin/env python3
"""
R2-D2 + MiniMax-M2.5 Integration
Astromech Technical Specialist with Coding LLM
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.minimax_brain_adapter import MiniMaxBrainAdapter
from agents.r2_brain_adapter import R2BrainAdapter


class R2MiniMaxIntegration:
    """
    R2-D2 using MiniMax-M2.5 for technical operations.
    
    Combines R2's astromech capabilities with MiniMax coding expertise.
    """
    
    def __init__(self):
        print("🤖 R2-D2 + MiniMax-M2.5 Integration Initializing...")
        
        # R2's brain (shared)
        self.r2 = R2BrainAdapter("R2-D2")
        
        # MiniMax adapter
        self.minimax = MiniMaxBrainAdapter(
            brain=self.r2.brain,
            heart=self.r2.heart,
            stomach=self.r2.stomach
        )
        
        print("✅ R2-D2 ready for technical operations")
        
    def technical_diagnostic(self, system: str, issue: str) -> dict:
        """Run technical diagnostic via MiniMax."""
        print(f"🔧 R2 Diagnostic: {system} - {issue}")
        
        query = f"Diagnose {system} issue: {issue}. Provide technical analysis."
        result = self.minimax.process_query(query, context="system_diagnostic")
        
        return {
            "agent": "R2-D2",
            "model": "MiniMax-M2.5",
            "system": system,
            "issue": issue,
            "diagnosis": result,
            "brain_ticks": self.r2.brain.tick_count,
            "r2_position": self.r2.sensors.position,
            "battery": self.r2.sensors.battery
        }
    
    def repair_protocol(self, component: str, damage: str) -> dict:
        """Generate repair protocol via MiniMax."""
        print(f"🔧 R2 Repair Protocol: {component}")
        
        query = f"Create repair protocol for {component} with {damage}. Step-by-step technical instructions."
        result = self.minimax.process_query(query, context="repair_protocol")
        
        return {
            "agent": "R2-D2",
            "model": "MiniMax-M2.5",
            "component": component,
            "damage": damage,
            "protocol": result,
            "tool_arm": self.r2.sensors.tool_arm
        }
    
    def system_analysis(self, data: dict) -> dict:
        """Analyze system data via MiniMax."""
        print(f"📊 R2 System Analysis")
        
        query = f"Analyze system data: {str(data)[:200]}. Identify anomalies and recommendations."
        result = self.minimax.process_query(query, context="data_analysis")
        
        return {
            "agent": "R2-D2",
            "model": "MiniMax-M2.5",
            "data_points": len(data),
            "analysis": result
        }
    
    def test_integration(self):
        """Test R2 + MiniMax integration."""
        print("\n" + "="*70)
        print("🧪 R2-D2 + MiniMax Integration Test")
        print("="*70)
        
        tests = [
            ("diagnostic", "Reactor", "coolant leak"),
            ("repair", "Hyperdrive motivator", "complete failure"),
            ("analysis", {"temp": 450, "pressure": 1200, "status": "critical"})
        ]
        
        for test_type, *args in tests:
            print(f"\n[{test_type.upper()}]")
            if test_type == "diagnostic":
                result = self.technical_diagnostic(*args)
            elif test_type == "repair":
                result = self.repair_protocol(*args)
            else:
                result = self.system_analysis(args[0])
            
            print(f"  ✓ Completed via MiniMax-M2.5")
            print(f"  Brain ticks: {result.get('brain_ticks', self.r2.brain.tick_count)}")
        
        print("\n" + "="*70)
        print("✅ R2-D2 + MiniMax Test Complete")
        print("="*70)


def main():
    r2_minimax = R2MiniMaxIntegration()
    r2_minimax.test_integration()


if __name__ == "__main__":
    main()
