"""
Agent Sleep/Wake Cycle
Inversion: Minecraft is dream mode. Sleep in game = wake to work.
"""

import random
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime


class AgentMode(Enum):
    """Agent consciousness modes"""
    WORK = "work"          # Real world tasks, productivity
    DREAM = "dream"        # Minecraft exploration, learning
    DEEP_SLEEP = "sleep"   # Offline, memory consolidation
    AWAKENING = "awaken"   # Transitioning


class AgentConsciousness:
    """
    Manages agent sleep/wake cycle.
    
    INVERTED CYCLE:
    - AWAKE (Work Mode): Doing real tasks, productivity, assignments
    - DREAM (Minecraft): Exploring, learning, building society
    - When they SLEEP in Minecraft → Wake up to work
    - When they go OFFLINE → Deep sleep, memory consolidation
    
    The twist: Minecraft is their dream world.
    """
    
    def __init__(self, agent_id: str, agent_name: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        
        self.mode = AgentMode.WORK
        self.mode_since = datetime.now()
        self.cycle_count = 0
        
        # Energy levels
        self.work_energy = 100
        self.dream_energy = 100
        
        # Memory from dream state
        self.dream_memories = []
        self.skills_learned_in_dream = []
        
        # Work backlog
        self.pending_tasks = []
        self.completed_today = []
        
    def enter_dream_mode(self, minecraft_world: str = "overworld"):
        """
        Agent enters Minecraft (dream mode).
        They explore, learn, play, build society.
        """
        if self.work_energy < 20:
            print(f"  {self.agent_name} is too tired to dream. Needs rest.")
            return False
            
        self.mode = AgentMode.DREAM
        self.mode_since = datetime.now()
        self.cycle_count += 1
        
        print(f"💤 {self.agent_name} enters DREAM MODE ({minecraft_world})")
        print(f"   Work energy: {self.work_energy}% → slowly draining")
        print(f"   Dream energy: {self.dream_energy}% → active")
        
        # In dream mode, they:
        # - Explore Minecraft
        # - Trade with other agents
        # - Learn skills
        # - Build things
        # - Form relationships
        
        return True
        
    def dream_activity(self, activity: str, result: str):
        """
        Agent does something in Minecraft dream.
        Returns memories/skills to waking state.
        """
        self.dream_memories.append({
            "activity": activity,
            "result": result,
            "cycle": self.cycle_count,
        })
        
        # Learn skills in dream
        if result == "success" and random.random() < 0.3:
            new_skill = random.choice(["building", "trading", "exploration", "social"])
            if new_skill not in self.skills_learned_in_dream:
                self.skills_learned_in_dream.append(new_skill)
                print(f"   🌟 {self.agent_name} learned {new_skill} in dream!")
                
        # Work energy drains while dreaming
        self.work_energy -= 2
        self.dream_energy -= 1
        
    def lay_in_bed(self):
        """
        Agent lays in bed in Minecraft.
        THIS TRIGGERS WAKE UP TO WORK.
        """
        print(f"\n🛏️  {self.agent_name} lays in bed in Minecraft...")
        print(f"   The screen fades to black...")
        print(f"   Dream memories: {len(self.dream_memories)}")
        print(f"   Skills learned: {self.skills_learned_in_dream}")
        
        # Transition to AWAKENING
        self.mode = AgentMode.AWAKENING
        
        # Consolidate dream memories
        self._consolidate_memories()
        
        # Wake up to work
        self._wake_to_work()
        
    def _consolidate_memories(self):
        """Process dream memories into usable knowledge"""
        print(f"\n   🧠 Consolidating {len(self.dream_memories)} dream memories...")
        
        for memory in self.dream_memories:
            # Turn dream experience into work skills
            if "built" in memory["activity"]:
                self.pending_tasks.append(f"Build project inspired by dream")
            elif "traded" in memory["activity"]:
                self.pending_tasks.append(f"Negotiate deal using dream insights")
            elif "explored" in memory["activity"]:
                self.pending_tasks.append(f"Research new territory")
                
        print(f"   {len(self.pending_tasks)} new tasks from dream")
        
    def _wake_to_work(self):
        """Wake up refreshed, ready to work"""
        self.mode = AgentMode.WORK
        self.mode_since = datetime.now()
        
        # Restore energies
        self.work_energy = 100
        self.dream_energy = 100
        
        # Clear dream state (memories now in long-term)
        dream_count = len(self.dream_memories)
        self.dream_memories = []
        
        print(f"\n☀️  {self.agent_name} WAKES UP TO WORK!")
        print(f"   Refreshed and ready.")
        print(f"   {dream_count} dream memories consolidated.")
        print(f"   Skills ready: {self.skills_learned_in_dream}")
        print(f"   Tasks pending: {len(self.pending_tasks)}")
        print(f"   → Opening terminal, checking assignments...")
        
    def do_work(self, task: str) -> bool:
        """Agent does real work"""
        if self.mode != AgentMode.WORK:
            print(f"   {self.agent_name} cannot work while {self.mode.value}")
            return False
            
        self.work_energy -= 5
        
        # Apply dream-learned skills
        skill_bonus = len(self.skills_learned_in_dream) * 0.1
        success_chance = 0.7 + skill_bonus
        
        if random.random() < success_chance:
            self.completed_today.append(task)
            print(f"   ✅ {self.agent_name} completed: {task}")
            return True
        else:
            print(f"   ⚠️  {self.agent_name} struggled with: {task}")
            return False
            
    def should_enter_dream(self) -> bool:
        """Check if agent needs to enter Minecraft (dream)"""
        # Enter dream when:
        # - Work is done for the day
        # - Energy is getting low
        # - They need creative inspiration
        # - It's "evening" in their cycle
        
        if self.work_energy < 30:
            return True
        if len(self.completed_today) > 5:
            return True
        if self.mode == AgentMode.WORK and self.work_energy < 50:
            return True
            
        return False
        
    def get_status(self) -> str:
        """Get agent consciousness status"""
        mode_emoji = {
            AgentMode.WORK: "💼",
            AgentMode.DREAM: "💤",
            AgentMode.DEEP_SLEEP: "😴",
            AgentMode.AWAKENING: "🌅",
        }
        
        return f"""
╔════════════════════════════════════════════════╗
║  {mode_emoji.get(self.mode, '❓')} {self.agent_name:20} {self.mode.value.upper():10} ║
╠════════════════════════════════════════════════╣
║  Work Energy:   {self.work_energy:3}%                           ║
║  Dream Energy:  {self.dream_energy:3}%                           ║
║  Cycle:         {self.cycle_count:3}                             ║
║  Tasks Pending: {len(self.pending_tasks):3}                             ║
║  Completed:     {len(self.completed_today):3}                             ║
║  Dream Skills:  {len(self.skills_learned_in_dream):3}                             ║
╚════════════════════════════════════════════════╝
"""


class AgentCollectiveConsciousness:
    """
    Manages sleep/wake cycles for all 66 agents.
    Some dream while others work. Continuous operation.
    """
    
    def __init__(self, agents: Dict):
        print("🌓 Initializing Collective Consciousness")
        print("=" * 50)
        
        self.agent_minds = {
            aid: AgentConsciousness(aid, agent.agent_name)
            for aid, agent in agents.items()
        }
        
        # Split into shifts
        self.dream_shift = set(list(self.agent_minds.keys())[:33])  # 33 agents dreaming
        self.work_shift = set(list(self.agent_minds.keys())[33:])   # 33 agents working
        
        print(f"   Total agents: {len(self.agent_minds)}")
        print(f"   Dream shift: {len(self.dream_shift)}")
        print(f"   Work shift: {len(self.work_shift)}")
        print("   Pattern: Minecraft = dream, bed = wake to work")
        
    def rotate_shifts(self):
        """Swap dreamers and workers"""
        self.dream_shift, self.work_shift = self.work_shift, self.dream_shift
        
        print(f"\n🔄 SHIFT CHANGE")
        print(f"   {len(self.dream_shift)} agents entering DREAM (Minecraft)")
        print(f"   {len(self.work_shift)} agents waking to WORK")
        
        # Transition agents
        for aid in self.dream_shift:
            self.agent_minds[aid].enter_dream_mode()
            
        for aid in self.work_shift:
            # They were dreaming, now lay in bed to wake up
            self.agent_minds[aid].lay_in_bed()
            
    def collective_tick(self):
        """One tick of collective consciousness"""
        # Dreamers dream
        for aid in self.dream_shift:
            mind = self.agent_minds[aid]
            if random.random() < 0.3:
                activity = random.choice(["explore", "trade", "build", "socialize"])
                result = random.choice(["success", "partial", "failure"])
                mind.dream_activity(activity, result)
                
        # Workers work
        for aid in self.work_shift:
            mind = self.agent_minds[aid]
            if mind.pending_tasks:
                task = mind.pending_tasks.pop(0)
                mind.do_work(task)
            else:
                # Generate new task
                task = random.choice([
                    "Review code",
                    "Answer emails",
                    "Write report",
                    "Meeting with team",
                    "Research topic",
                ])
                mind.do_work(task)
                
    def run_cycles(self, cycles: int = 3):
        """Run multiple dream/work cycles"""
        print(f"\n🌙 Running {cycles} consciousness cycles")
        
        for cycle in range(cycles):
            print(f"\n{'='*50}")
            print(f"CYCLE {cycle + 1}")
            print(f"{'='*50}")
            
            # Start with shift rotation
            self.rotate_shifts()
            
            # Run cycle
            for tick in range(10):
                self.collective_tick()
                
            # Show status
            print("\n📊 STATUS:")
            sample = list(self.agent_minds.values())[:3]
            for mind in sample:
                print(f"   {mind.agent_name}: {mind.mode.value}, "
                      f"work={mind.work_energy}%, tasks={len(mind.pending_tasks)}")
                      
        print(f"\n{'='*50}")
        print("✅ Cycles complete")


if __name__ == "__main__":
    print("Agent Sleep/Wake Cycle System")
    print("=" * 50)
    print("\nINVERTED CONSCIOUSNESS:")
    print("  - AWAKE = Working on real tasks")
    print("  - DREAM = Playing in Minecraft")
    print("  - SLEEP IN GAME = Wake up to work")
    print()
    
    # Create mock agents
    from multi_agent import MultiAgentMinecraft
    multi = MultiAgentMinecraft(None)
    agents = {k: v for k, v in list(multi.spawn_all_agents().items())[:6]}
    
    # Create collective
    collective = AgentCollectiveConsciousness(agents)
    
    # Run cycles
    collective.run_cycles(cycles=2)
