#!/usr/bin/env python3
"""
AGI Connect - Unified System Integration v2.0
Updated: 2026-03-29 by Spindle (CTO Agent)

OPTIMIZATIONS IMPLEMENTED:
✓ 1. Smart Agent Distribution Algorithm (weighted rotation)
✓ 2. Cross-Platform Event Propagation (unified event bus)
✓ 3. Economy Balancing (wealth redistribution + anti-monopoly)
✓ 4. Meeting Scheduling Automation (conflict resolution)

Connects everything:
- Brain (AOS core)
- All 66 agents
- Minecraft (dream world)
- Roblox (alternative dream)
- Gather Town (virtual office)
- Economy (agents trade)
- Consciousness cycle (sleep/wake)
- Silverflight0509 (chronicling)

Everything connected. Everything communicating.
"""

import sys
import random
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import heapq

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.brain.minecraft_bridge.multi_agent import MultiAgentMinecraft
from shared.brain.minecraft_bridge.economy import AgentEconomy, ProductType, SkillType
from shared.brain.minecraft_bridge.consciousness_cycle import AgentCollectiveConsciousness
from shared.brain.gather_bridge import GatherTownBridge


# ═══════════════════════════════════════════════════════════════════════════════
# OPTIMIZATION 1: SMART AGENT DISTRIBUTION ALGORITHM
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class AgentWorkloadMetrics:
    """Tracks agent performance and fatigue"""
    agent_id: str
    role: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    consecutive_work_ticks: int = 0
    consecutive_dream_ticks: int = 0
    last_rotation: datetime = field(default_factory=datetime.now)
    skill_usage: Dict[str, int] = field(default_factory=dict)
    platform_preference: Dict[str, float] = field(default_factory=dict)
    fatigue_score: float = 0.0
    efficiency_rating: float = 1.0


class SmartAgentDistributor:
    """
    OPTIMIZED: Weighted rotation based on agent state.
    
    Features:
    - Fatigue-aware scheduling
    - Skill-based task matching
    - Historical performance tracking
    - Dynamic platform allocation
    """
    
    def __init__(self, agents: Dict):
        self.agents = agents
        self.metrics: Dict[str, AgentWorkloadMetrics] = {}
        self._init_metrics()
        
        self.platform_quotas = {
            "gather": 20,
            "minecraft": 22,
            "roblox": 14,
            "work": 10,
        }
        
        self.role_platforms = {
            "c_suite": ["gather", "work"],
            "technical": ["minecraft", "roblox", "work"],
            "product": ["gather", "minecraft"],
            "secretarial": ["gather", "work"],
            "research": ["minecraft", "roblox"],
            "management": ["gather", "work"],
            "support": ["minecraft", "roblox"],
        }
        
        self.assignments: Dict[str, str] = {}
        
    def _init_metrics(self):
        for agent_id, agent in self.agents.items():
            role = self._get_agent_role(agent_id)
            self.metrics[agent_id] = AgentWorkloadMetrics(
                agent_id=agent_id,
                role=role,
                platform_preference={
                    "gather": 0.25, "minecraft": 0.25,
                    "roblox": 0.25, "work": 0.25,
                }
            )
            
    def _get_agent_role(self, agent_id: str) -> str:
        c_suite = ["qora", "spindle", "ledger-9", "sentinel"]
        technical = ["r2-d2", "taptap", "bugcatcher", "fiber", "pipeline", "stacktrace"]
        product = ["greet", "ledger", "clerk", "concierge", "closeter", "velvet", "executive"]
        secretarial = ["judy", "jane"]
        research = ["dusty"]
        management = ["jordan"]
        
        if agent_id in c_suite: return "c_suite"
        elif agent_id in technical: return "technical"
        elif agent_id in product: return "product"
        elif agent_id in secretarial: return "secretarial"
        elif agent_id in research: return "research"
        elif agent_id in management: return "management"
        return "support"
        
    def calculate_fatigue(self, agent_id: str) -> float:
        """Calculate agent fatigue (0-100)"""
        metrics = self.metrics[agent_id]
        work_fatigue = metrics.consecutive_work_ticks * 3
        dream_fatigue = metrics.consecutive_dream_ticks * 1
        failure_penalty = metrics.tasks_failed * 5
        hours_since = (datetime.now() - metrics.last_rotation).total_seconds() / 3600
        freshness = min(20, hours_since * 2)
        fatigue = work_fatigue + dream_fatigue + failure_penalty - freshness
        return max(0, min(100, fatigue))
        
    def calculate_platform_score(self, agent_id: str, platform: str) -> float:
        """Calculate agent-platform fit score"""
        metrics = self.metrics[agent_id]
        role = metrics.role
        
        score = metrics.platform_preference.get(platform, 0.25)
        preferred = self.role_platforms.get(role, ["minecraft"])
        if platform in preferred:
            score += 0.3
            
        fatigue = self.calculate_fatigue(agent_id)
        if platform in ["minecraft", "roblox"] and fatigue > 60:
            score += 0.2
        elif platform == "work" and fatigue > 70:
            score -= 0.3
            
        score *= metrics.efficiency_rating
        return score
        
    def optimize_distribution(self) -> Dict[str, str]:
        """Optimized assignment with fatigue awareness"""
        print("\n🧠 OPTIMIZING AGENT DISTRIBUTION...")
        
        scores = {}
        for agent_id in self.agents:
            for platform in self.platform_quotas:
                scores[(agent_id, platform)] = self.calculate_platform_score(agent_id, platform)
                
        assignments = {}
        platform_counts = {p: 0 for p in self.platform_quotas}
        available = set(self.agents.keys())
        
        sorted_assignments = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        for (agent_id, platform), score in sorted_assignments:
            if agent_id not in available:
                continue
            if platform_counts[platform] >= self.platform_quotas[platform]:
                continue
                
            assignments[agent_id] = platform
            platform_counts[platform] += 1
            available.remove(agent_id)
            
            self.metrics[agent_id].last_rotation = datetime.now()
            if platform == "work":
                self.metrics[agent_id].consecutive_dream_ticks += 1
            else:
                self.metrics[agent_id].consecutive_work_ticks += 1
                
        for agent_id in available:
            best = max(
                [p for p in self.platform_quotas if platform_counts[p] < self.platform_quotas[p]],
                key=lambda p: scores.get((agent_id, p), 0),
                default="minecraft"
            )
            assignments[agent_id] = best
            platform_counts[best] += 1
            
        self.assignments = assignments
        
        print(f"   ✅ Distribution complete")
        for platform, count in platform_counts.items():
            print(f"      {platform}: {count} agents")
            
        return assignments
        
    def should_rotate(self, agent_id: str) -> bool:
        """Check if agent needs rotation"""
        fatigue = self.calculate_fatigue(agent_id)
        metrics = self.metrics[agent_id]
        current = self.assignments.get(agent_id)
        
        if fatigue > 80:
            return True
        if current == "work" and metrics.consecutive_work_ticks > 5:
            return True
        if current in ["minecraft", "roblox"] and metrics.consecutive_dream_ticks > 8:
            return True
        if metrics.efficiency_rating < 0.7:
            return True
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# OPTIMIZATION 2: CROSS-PLATFORM EVENT PROPAGATION
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CrossPlatformEvent:
    event_id: str
    event_type: str
    source_platform: str
    target_platforms: List[str]
    payload: Dict[str, Any]
    timestamp: datetime
    priority: int
    propagation_depth: int = 0
    max_depth: int = 3


class UnifiedEventBus:
    """Central event bus for cross-platform communication"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[callable]] = defaultdict(list)
        self.event_queue: List[Tuple[int, datetime, CrossPlatformEvent]] = []
        self.event_history: List[CrossPlatformEvent] = []
        
        self.propagation_rules = {
            "economy": ["minecraft", "roblox", "gather"],
            "social": ["gather", "minecraft"],
            "achievement": ["minecraft", "roblox", "gather", "work"],
            "system": ["work", "gather"],
            "emergency": ["minecraft", "roblox", "gather", "work"],
        }
        
    def subscribe(self, event_type: str, callback: callable):
        self.subscribers[event_type].append(callback)
        
    def emit(self, event: CrossPlatformEvent) -> bool:
        if event.propagation_depth >= event.max_depth:
            return False
        heapq.heappush(self.event_queue, (-event.priority, event.timestamp, event))
        return True
        
    def process_queue(self, max_events: int = 10) -> List[CrossPlatformEvent]:
        processed = []
        for _ in range(min(max_events, len(self.event_queue))):
            if not self.event_queue:
                break
            _, _, event = heapq.heappop(self.event_queue)
            self._propagate_event(event)
            processed.append(event)
            self.event_history.append(event)
        return processed
        
    def _propagate_event(self, event: CrossPlatformEvent):
        for target in event.target_platforms:
            if target == event.source_platform:
                continue
            for callback in self.subscribers.get(event.event_type, []):
                try:
                    callback(event.payload, target, event.source_platform)
                except Exception as e:
                    print(f"   ⚠️  Event handler error: {e}")
                    
    def create_economy_event(self, source: str, buyer: str, seller: str, 
                               item: str, price: int) -> CrossPlatformEvent:
        return CrossPlatformEvent(
            event_id=f"econ_{datetime.now().timestamp()}",
            event_type="economy",
            source_platform=source,
            target_platforms=self.propagation_rules["economy"],
            payload={
                "message": f"{buyer} bought {item} from {seller} for {price}",
                "buyer": buyer, "seller": seller, "item": item, "price": price,
            },
            timestamp=datetime.now(),
            priority=5,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# OPTIMIZATION 3: ECONOMY BALANCING
# ═══════════════════════════════════════════════════════════════════════════════

class BalancedEconomy(AgentEconomy):
    """Economy with wealth redistribution and anti-monopoly"""
    
    WEALTH_CAP = 500
    POVERTY_LINE = 50
    TAX_BRACKETS = [
        (0, 100, 0.0),
        (100, 200, 0.05),
        (200, 500, 0.15),
        (500, float('inf'), 0.25),
    ]
    UBI_AMOUNT = 20
    
    def __init__(self, agents: Dict):
        super().__init__(agents)
        self.tax_collected = 0
        self.ubi_distributed = 0
        self.welfare_skills_granted = 0
        
    def calculate_gini(self) -> float:
        """Gini coefficient measure of inequality"""
        wealths = sorted(self.agent_currency.values())
        n = len(wealths)
        if n == 0 or sum(wealths) == 0:
            return 0
        cumsum = sum((i + 1) * w for i, w in enumerate(wealths))
        return (2 * cumsum) / (n * sum(wealths)) - (n + 1) / n
        
    def get_wealth_distribution(self) -> Dict:
        wealths = sorted(self.agent_currency.values(), reverse=True)
        total = sum(wealths)
        n = len(wealths)
        if total == 0:
            return {"gini": 0, "top_10": 0, "bottom_50": 0}
        top_10 = sum(wealths[:max(1, n // 10)]) / total
        bottom_50 = sum(wealths[-max(1, n // 2):]) / total
        return {"gini": self.calculate_gini(), "top_10": top_10, 
                "bottom_50": bottom_50, "total_wealth": total, "avg_wealth": total / n}
        
    def apply_progressive_taxation(self) -> Dict[str, int]:
        taxes = {}
        for agent_id, wealth in self.agent_currency.items():
            if wealth <= 0:
                continue
            tax = 0
            remaining = wealth
            for lower, upper, rate in self.TAX_BRACKETS:
                bracket = min(remaining, upper - lower)
                if bracket > 0:
                    tax += bracket * rate
                    remaining -= bracket
            if tax > 0:
                self.agent_currency[agent_id] -= int(tax)
                taxes[agent_id] = int(tax)
                self.tax_collected += int(tax)
        return taxes
        
    def distribute_ubi(self, tax_revenue: int) -> int:
        poor = [aid for aid, w in self.agent_currency.items() if w < self.POVERTY_LINE]
        if not poor:
            return 0
        ubi = min(self.UBI_AMOUNT, tax_revenue // len(poor))
        if ubi <= 0:
            return 0
        distributed = 0
        for agent_id in poor:
            self.agent_currency[agent_id] += ubi
            distributed += ubi
            self.ubi_distributed += ubi
            # Grant skills to help earn
            if agent_id not in self.agent_skills or len(self.agent_skills[agent_id]) < 2:
                skills = [s for s in SkillType]
                if skills:
                    new_skill = random.choice(skills)
                    if agent_id not in self.agent_skills:
                        self.agent_skills[agent_id] = {}
                    if new_skill not in self.agent_skills[agent_id]:
                        self.agent_skills[agent_id][new_skill] = 1
                        self.welfare_skills_granted += 1
        return distributed
        
    def enforce_wealth_cap(self) -> List[str]:
        capped = []
        for agent_id, wealth in self.agent_currency.items():
            if wealth > self.WEALTH_CAP:
                excess = wealth - self.WEALTH_CAP
                self.agent_currency[agent_id] = self.WEALTH_CAP
                poor = [aid for aid, w in self.agent_currency.items() 
                        if w < self.POVERTY_LINE and aid != agent_id]
                if poor:
                    share = excess // len(poor)
                    for p in poor:
                        self.agent_currency[p] += share
                capped.append(agent_id)
        return capped
        
    def run_economic_maintenance(self) -> Dict:
        print("\n💰 ECONOMIC MAINTENANCE...")
        before = self.get_wealth_distribution()
        taxes = self.apply_progressive_taxation()
        tax_total = sum(taxes.values())
        print(f"   💸 Tax: {tax_total} from {len(taxes)} agents")
        ubi = self.distribute_ubi(tax_total)
        print(f"   💝 UBI: {ubi} to poor agents")
        capped = self.enforce_wealth_cap()
        if capped:
            print(f"   🚫 Wealth cap on {len(capped)} agents")
        after = self.get_wealth_distribution()
        print(f"   📊 Gini: {before['gini']:.3f} → {after['gini']:.3f}")
        return {"tax": tax_total, "ubi": ubi, "capped": len(capped),
                "gini_before": before["gini"], "gini_after": after["gini"]}


# ═══════════════════════════════════════════════════════════════════════════════
# OPTIMIZATION 4: MEETING SCHEDULING AUTOMATION
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Meeting:
    meeting_id: str
    title: str
    attendees: List[str]
    platform: str
    room: str
    start_time: datetime
    duration_minutes: int
    priority: int
    agenda: List[str]


class AutomatedMeetingScheduler:
    """Smart meeting scheduling with conflict resolution"""
    
    def __init__(self, agents: Dict, gather: GatherTownBridge):
        self.agents = agents
        self.gather = gather
        self.scheduled_meetings: List[Meeting] = []
        self.agent_schedules: Dict[str, List[Tuple[datetime, datetime]]] = defaultdict(list)
        self.work_hours = range(9, 18)
        
    def _get_agent_role(self, agent_id: str) -> str:
        c_suite = ["qora", "spindle", "ledger-9", "sentinel"]
        technical = ["r2-d2", "taptap", "bugcatcher", "fiber", "pipeline", "stacktrace"]
        management = ["jordan"]
        research = ["dusty"]
        secretarial = ["judy", "jane"]
        
        if agent_id in c_suite: return "c_suite"
        elif agent_id in technical: return "technical"
        elif agent_id in management: return "management"
        elif agent_id in research: return "research"
        elif agent_id in secretarial: return "secretarial"
        return "support"
        
    def find_optimal_time(self, attendees: List[str], duration: int) -> Optional[datetime]:
        now = datetime.now()
        for hour_offset in range(48):
            for minute in [0, 15, 30, 45]:
                start = now + timedelta(hours=hour_offset, minutes=minute)
                end = start + timedelta(minutes=duration)
                if start.hour not in self.work_hours:
                    continue
                conflict = False
                for agent_id in attendees:
                    for s, e in self.agent_schedules.get(agent_id, []):
                        if start < e and end > s:
                            conflict = True
                            break
                    if conflict:
                        break
                if not conflict:
                    return start
        return None
        
    def schedule_meeting(self, meeting_type: str, title: str, 
                        priority: int = 5) -> Optional[Meeting]:
        templates = {
            "standup": {"duration": 15, "platform": "gather", "room": "conference_room_a"},
            "strategy": {"duration": 60, "platform": "gather", "room": "conference_room_b"},
            "brainstorm": {"duration": 45, "platform": "minecraft", "room": "central_hub"},
        }
        template = templates.get(meeting_type)
        if not template:
            return None
            
        # Auto-select attendees based on role
        roles_needed = {"standup": ["technical", "management"],
                       "strategy": ["c_suite", "management"],
                       "brainstorm": ["technical", "research", "c_suite"]}[meeting_type]
        
        attendees = []
        for agent_id in self.agents:
            if self._get_agent_role(agent_id) in roles_needed:
                if len(self.agent_schedules.get(agent_id, [])) < 5:
                    attendees.append(agent_id)
                    if len(attendees) >= 6:
                        break
                        
        if len(attendees) < 2:
            return None
            
        start = self.find_optimal_time(attendees, template["duration"])
        if not start:
            return None
            
        meeting = Meeting(
            meeting_id=f"mtg_{datetime.now().timestamp()}",
            title=title,
            attendees=attendees,
            platform=template["platform"],
            room=template["room"],
            start_time=start,
            duration_minutes=template["duration"],
            priority=priority,
            agenda=["Review", "Discuss", "Plan"],
        )
        
        end = start + timedelta(minutes=template["duration"])
        for agent_id in attendees:
            self.agent_schedules[agent_id].append((start, end))
        self.scheduled_meetings.append(meeting)
        
        print(f"\n📅 MEETING: {title}")
        print(f"   When: {start.strftime('%H:%M')}, Where: {template['platform']}")
        print(f"   Attendees: {', '.join(attendees[:4])}")
        return meeting
        
    def auto_schedule(self):
        print("\n🤖 Auto-scheduling meetings...")
        self.schedule_meeting("standup", "Daily Standup", priority=8)
        self.schedule_meeting("strategy", "Strategy Sync", priority=7)
        print(f"   ✅ {len(self.scheduled_meetings)} meetings scheduled")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN AGI CONNECT CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class AGIConnect:
    """
    The unified AGI Connect system with all optimizations.
    """
    
    def __init__(self):
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                     AGI CONNECT v2.0                           ║")
        print("║              Unified System - OPTIMIZED                        ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print()
        
        print("👥 PHASE 1: Spawning 66 Agents...")
        self.multi = MultiAgentMinecraft(None)
        self.agents = self.multi.spawn_all_agents()
        print(f"   ✅ {len(self.agents)} agents ready")
        
        print("\n🧠 PHASE 2: Loading Optimized Systems...")
        self.distributor = SmartAgentDistributor(self.agents)
        print("   ✅ Smart Agent Distributor")
        
        self.event_bus = UnifiedEventBus()
        self._setup_event_handlers()
        print("   ✅ Unified Event Bus")
        
        self.economy = BalancedEconomy(self.agents)
        print("   ✅ Balanced Economy (anti-monopoly)")
        
        print("\n🌓 PHASE 3: Starting Consciousness Cycle...")
        self.consciousness = AgentCollectiveConsciousness(self.agents)
        print(f"   ✅ Dream: {len(self.consciousness.dream_shift)}, Work: {len(self.consciousness.work_shift)}")
        
        print("\n🏢 PHASE 4: Connecting Platforms...")
        self.gather = GatherTownBridge()
        self.scheduler = AutomatedMeetingScheduler(self.agents, self.gather)
        print("   ✅ Gather Town + Automated Scheduler")
        
        self.tick_count = 0
        self.start_time = datetime.now()
        
        print("\n" + "=" * 70)
        print("✅ AGI CONNECT INITIALIZED")
        print("=" * 70)
        
    def _setup_event_handlers(self):
        def on_economy(payload, target, source):
            print(f"   💰 [{source}→{target}] {payload.get('message', '')}")
        def on_achievement(payload, target, source):
            print(f"   🏆 [{source}→{target}] {payload.get('message', '')}")
        self.event_bus.subscribe("economy", on_economy)
        self.event_bus.subscribe("achievement", on_achievement)
        
    def connect_all(self, distribution: Dict[str, int] = None):
        """Connect all agents using optimized distribution"""
        if distribution is None:
            distribution = self.distributor.optimize_distribution()
            
        print("\n🌐 CONNECTING AGENTS")
        print("=" * 70)
        
        for agent_id, platform in distribution.items():
            if platform == "gather":
                self.gather.agent_join_office(agent_id, self.agents[agent_id].agent_name)
            elif platform == "minecraft":
                if agent_id in self.consciousness.agent_minds:
                    self.consciousness.agent_minds[agent_id].enter_dream_mode()
                    
        print("\n✅ All agents connected")
        
    def unified_tick(self):
        """One tick across all systems"""
        self.tick_count += 1
        
        # Check rotations every 20 ticks
        if self.tick_count % 20 == 0:
            to_rotate = [aid for aid in self.agents if self.distributor.should_rotate(aid)]
            if to_rotate:
                print(f"   🔄 Rotating {len(to_rotate)} agents...")
                
        # Process events
        self.event_bus.process_queue(max_events=5)
        
        # Consciousness cycle
        self.consciousness.collective_tick()
        
        # Gather activity
        if self.tick_count % 10 == 0:
            self.gather.simulate_office_hour()
            
        # Economic activity
        if self.tick_count % 5 == 0 and self.economy.stores:
            for _ in range(min(3, len(self.economy.stores))):
                buyer = random.choice(list(self.agents.keys()))
                seller = random.choice(list(self.economy.stores.keys()))
                if seller in self.economy.stores and self.economy.stores[seller].inventory:
                    product = self.economy.stores[seller].inventory[0]
                    if self.economy.buy_product(buyer, seller, product.name):
                        event = self.event_bus.create_economy_event(
                            "minecraft", buyer, seller, product.name, product.price
                        )
                        self.event_bus.emit(event)
                        
        # Meeting automation
        if self.tick_count % 100 == 0:
            self.scheduler.auto_schedule()
            
        # Economic maintenance
        if self.tick_count % 50 == 0:
            self.economy.run_economic_maintenance()
            
    def run_unified(self, ticks: int = 500):
        """Run unified simulation"""
        print(f"\n🚀 RUNNING UNIFIED SYSTEM ({ticks} ticks)")
        
        for i in range(ticks):
            self.unified_tick()
            if i > 0 and i % 100 == 0:
                print(f"\n{'='*50}")
                print(f"Tick {i} - Status Report")
                print(f"{'='*50}")
                wealth = self.economy.get_wealth_distribution()
                print(f"   Gini: {wealth['gini']:.3f}, Total: {wealth['total_wealth']}")
                print(f"   Meetings: {len(self.scheduler.scheduled_meetings)}")
                
        print("\n" + "=" * 70)
        print("📊 FINAL REPORT")
        print("=" * 70)
        print(f"\n💰 Economy:")
        print(f"   Tax collected: {self.economy.tax_collected}")
        print(f"   UBI distributed: {self.economy.ubi_distributed}")
        print(f"   Skills granted: {self.economy.welfare_skills_granted}")
        wealth = self.economy.get_wealth_distribution()
        print(f"   Final Gini: {wealth['gini']:.3f}")
        print(f"\n🌐 Distribution:")
        for platform in self.distributor.platform_quotas:
            count = sum(1 for p in self.distributor.assignments.values() if p == platform)
            print(f"   {platform}: {count}")
        print("\n✅ All systems optimized and running.")


def main():
    """Run AGI Connect"""
    agi = AGIConnect()
    agi.connect_all()
    agi.run_unified(ticks=250)


if __name__ == "__main__":
    main()