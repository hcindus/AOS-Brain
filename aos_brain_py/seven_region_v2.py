#!/usr/bin/env python3
"""
SevenRegionBrain v2 - Skills-First Architecture
Phase 3: Region Migration

The brain becomes a skill orchestrator.
Regions become thin wrappers that call skills.
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import deque

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from skill_registry import SkillRegistry, SkillTier, Skill, Contract, get_registry

# Skill handlers loaded dynamically in _register_core_skills
brain_health_check = None
thalamus_handler = None
pfc_handler = None
tick_recovery_handler = None


class Region:
    """Base class for brain regions using skills."""
    
    def __init__(self, registry: SkillRegistry, skill_name: str):
        self.registry = registry
        self.skill_name = skill_name
    
    def call(self, input_data: Dict, timeout_ms: int = 100) -> Dict:
        """Call region skill."""
        return self.registry.call(self.skill_name, input_data, timeout_ms=timeout_ms)


class ThalamusRegion(Region):
    """Sensory relay - now calls skill."""
    
    def __init__(self, registry: SkillRegistry):
        super().__init__(registry, 'thalamus')
    
    def process(self, sensory_input: Dict) -> Dict:
        """Process sensory input via thalamus skill."""
        return self.call({
            'source': sensory_input.get('source', 'system'),
            'data': sensory_input.get('data'),
            'timestamp': sensory_input.get('timestamp', time.time()),
            'priority': sensory_input.get('priority', 0.5)
        }, timeout_ms=10)  # Standard tier = fast


class PFCRegion(Region):
    """Prefrontal cortex - now calls skill."""
    
    def __init__(self, registry: SkillRegistry):
        super().__init__(registry, 'pfc')
    
    def decide(self, context: Dict, options: List[Dict], signature: Dict, ollama_available: bool = False) -> Dict:
        """Make decision via PFC skill."""
        return self.call({
            'context': context,
            'options': options,
            'signature': signature,
            'ollama_available': ollama_available
        }, timeout_ms=100)  # Methodology tier


class BrainDiagnostics:
    """Self-diagnostic system using skills."""
    
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
    
    def check(self, detailed: bool = False) -> Dict:
        """Run full health check via skill."""
        return self.registry.call('brain-health-check', {
            'detailed': detailed
        }, timeout_ms=50)
    
    def recover(self, health_report: Dict, aggressive: bool = False) -> Dict:
        """Recover from failure via skill."""
        return self.registry.call('tick-recovery', {
            'health_report': health_report,
            'aggressive': aggressive
        }, timeout_ms=50)


class SevenRegionBrainV2:
    """
    Skills-first brain architecture.
    
    Regions call skills instead of hardcoded logic.
    Self-diagnostic capabilities via diagnostic skills.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        # Initialize skill registry
        self.registry = get_registry()
        self._register_core_skills()
        
        # Initialize regions as skill consumers
        self.thalamus = ThalamusRegion(self.registry)
        self.pfc = PFCRegion(self.registry)
        # Other regions would follow same pattern...
        
        # Self-diagnostics
        self.diagnostics = BrainDiagnostics(self.registry)
        
        # State
        self.tick_count = 0
        self.running = True
        self.tick_interval = 0.2  # 200ms
        
        # Performance tracking
        self.latency_history = deque(maxlen=100)
        self.last_tick_time = time.time()
    
    def _register_core_skills(self):
        """Register built-in brain skills."""
        skills_base = Path(__file__).parent / 'skills'
        
        # Load thalamus handler
        thalamus_path = skills_base / 'thalamus-v1' / 'handler.py'
        thalamus_locals = {}
        exec(open(thalamus_path).read(), thalamus_locals)
        thalamus_handler = thalamus_locals['thalamus_handler']
        
        # Load pfc handler
        pfc_path = skills_base / 'pfc-v2' / 'handler.py'
        pfc_locals = {}
        exec(open(pfc_path).read(), pfc_locals)
        pfc_handler = pfc_locals['pfc_handler']
        
        # Load brain health check handler
        health_check_path = skills_base / 'brain-health-check' / 'handler.py'
        health_locals = {}
        exec(open(health_check_path).read(), health_locals)
        brain_health_check = health_locals['brain_health_check']
        
        # Load tick recovery handler
        recovery_path = skills_base / 'tick-recovery' / 'handler.py'
        recovery_locals = {}
        exec(open(recovery_path).read(), recovery_locals)
        tick_recovery_handler = recovery_locals['tick_recovery_handler']
        
        # Thalamus skill
        thalamus_skill = Skill(
            name='thalamus',
            version='1.0.0',
            tier=SkillTier.STANDARD,
            description='Normalize and route sensory input',
            contract=Contract(
                input_schema={'required': ['source', 'data', 'timestamp']},
                output_schema={'required': ['normalized', 'priority', 'routing', 'signature']}
            ),
            handler=thalamus_handler
        )
        self.registry.register(thalamus_skill)
        
        # PFC skill
        pfc_skill = Skill(
            name='pfc',
            version='2.0.0',
            tier=SkillTier.METHODOLOGY,
            description='Prefrontal cortex decision-making',
            contract=Contract(
                input_schema={'required': ['context', 'options', 'signature']},
                output_schema={'required': ['decision', 'confidence', 'reasoning', 'action']}
            ),
            handler=pfc_handler
        )
        self.registry.register(pfc_skill)
        
        # Brain health check skill
        health_skill = Skill(
            name='brain-health-check',
            version='1.0.0',
            tier=SkillTier.DIAGNOSTIC,
            description='Check brain health metrics',
            contract=Contract(
                input_schema={'properties': {'detailed': {'type': 'boolean'}}},
                output_schema={'required': ['status', 'metrics', 'recommendations', 'timestamp']}
            ),
            handler=brain_health_check
        )
        self.registry.register(health_skill)
        
        # Tick recovery skill
        recovery_skill = Skill(
            name='tick-recovery',
            version='1.0.0',
            tier=SkillTier.DIAGNOSTIC,
            description='Recover from stalled tick states',
            contract=Contract(
                input_schema={'required': ['health_report']},
                output_schema={'required': ['status', 'actions_taken', 'regions_reset']}
            ),
            handler=tick_recovery_handler
        )
        self.registry.register(recovery_skill)
    
    def tick(self, observation: Dict) -> Dict:
        """
        One OODA cycle using skills.
        
        Observe → Orient → Decide → Act
        """
        tick_start = time.time()
        self.tick_count += 1
        
        try:
            # 1. OBSERVE - Thalamus skill
            sensory = self.thalamus.process(observation)
            if 'error' in sensory:
                return self._handle_error('thalamus', sensory)
            
            # 2. ORIENT - Would call hippocampus/limbic skills here
            context = {
                'signature': sensory.get('signature', {}),
                'routing': sensory.get('routing', []),
                'tick': self.tick_count
            }
            
            # 3. DECIDE - PFC skill
            decision = self.pfc.decide(
                context=context,
                options=[{'type': 'explore'}, {'type': 'wait'}, {'type': 'act'}],
                signature=sensory.get('signature', {}),
                ollama_available=False  # Could check Ollama here
            )
            if 'error' in decision:
                return self._handle_error('pfc', decision)
            
            # 4. ACT - Would call basal/cerebellum skills here
            action = decision.get('action', {'type': 'noop'})
            
            # 5. DIAGNOSE - Every 100 ticks
            if self.tick_count % 100 == 0:
                health = self.diagnostics.check()
                if health.get('status') != 'healthy':
                    recovery = self.diagnostics.recover(health)
                    action['_recovery'] = recovery
            
            # Track latency
            latency = (time.time() - tick_start) * 1000
            self.latency_history.append(latency)
            self.last_tick_time = time.time()
            
            return {
                'tick': self.tick_count,
                'status': 'success',
                'sensory': sensory,
                'decision': decision,
                'action': action,
                'latency_ms': latency
            }
            
        except Exception as e:
            return self._handle_error('tick', {'error': str(e)})
    
    def _handle_error(self, source: str, error_data: Dict) -> Dict:
        """Handle errors with recovery attempt."""
        health = self.diagnostics.check()
        recovery = self.diagnostics.recover(health, aggressive=True)
        
        return {
            'tick': self.tick_count,
            'status': 'error',
            'source': source,
            'error': error_data.get('error', 'unknown'),
            'recovery': recovery
        }
    
    def run_forever(self):
        """Run tick loop continuously."""
        print(f"🧠 SevenRegionBrainV2 starting (skills-first)")
        print(f"   Skills registered: {len(self.registry.skills)}")
        print(f"   Tick interval: {self.tick_interval}s")
        
        while self.running:
            # Create synthetic observation
            obs = {
                'source': 'system',
                'data': f'tick_{self.tick_count}',
                'timestamp': time.time(),
                'priority': 0.5
            }
            
            result = self.tick(obs)
            
            # Log every 10 ticks
            if self.tick_count % 10 == 0:
                status = result.get('status')
                latency = result.get('latency_ms', 0)
                decision = result.get('decision', {}).get('decision', 'none')
                print(f"[tick {self.tick_count}] {status} | {decision} | {latency:.1f}ms")
            
            time.sleep(self.tick_interval)
    
    def get_health(self) -> Dict:
        """Get brain health report."""
        return {
            'tick_count': self.tick_count,
            'avg_latency': sum(self.latency_history) / len(self.latency_history) if self.latency_history else 0,
            'skills_registered': len(self.registry.skills),
            'registry_health': self.registry.health_check(),
            'diagnostics': self.diagnostics.check()
        }


# Backward compatibility alias
SevenRegionBrain = SevenRegionBrainV2

if __name__ == '__main__':
    brain = SevenRegionBrainV2()
    brain.run_forever()
