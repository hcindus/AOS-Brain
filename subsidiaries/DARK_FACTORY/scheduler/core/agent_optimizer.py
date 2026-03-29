"""
Agent-Station Assignment Optimizer
==================================

Uses optimization algorithms to assign agents to stations
based on skills, workload, and efficiency.
"""

import random
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("AgentOptimizer")


@dataclass
class AssignmentScore:
    """Score for an agent-station assignment"""
    agent_id: str
    station_id: str
    score: float
    factors: Dict[str, float]


class AgentStationOptimizer:
    """
    Optimizes agent-to-station assignments.
    
    Considers:
    - Agent skills vs station requirements
    - Workload balancing
    - Historical performance
    - Minimizing changeover time
    """
    
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.assignment_history: List[Dict] = []
        
        # Scoring weights
        self.weights = {
            "skill_match": 1.5,
            "role_match": 1.3,
            "efficiency": 1.0,
            "workload_balance": 0.8,
            "quality_score": 1.2,
        }
        
        logger.info("AgentStationOptimizer initialized")
    
    def calculate_assignment_score(
        self, 
        agent_id: str, 
        station_id: str,
        job_type: Optional[str] = None
    ) -> AssignmentScore:
        """Calculate assignment score for agent-station pair"""
        
        agent = self.scheduler.agents.get(agent_id)
        station = self.scheduler.workstations.get(station_id)
        
        if not agent or not station:
            return AssignmentScore(agent_id, station_id, 0.0, {})
        
        factors = {}
        
        # Skill match (1-10 scale)
        factors["skill_match"] = agent.skill_level / 10.0
        
        # Role match
        role_station_mapping = {
            "operator": ["3d_print", "cnc", "assembly"],
            "technician": ["maintenance"],
            "inspector": ["quality"],
            "coordinator": ["assembly", "packing"],
            "specialist": ["quality", "cnc"],
        }
        
        matched_roles = role_station_mapping.get(agent.role, [])
        factors["role_match"] = 1.0 if station.station_type in matched_roles else 0.5
        
        # Agent efficiency
        factors["efficiency"] = agent.efficiency_multiplier
        
        # Workload balance (prefer less busy agents)
        workload = agent.jobs_completed / max(
            [a.jobs_completed for a in self.scheduler.agents.values()] + [1]
        )
        factors["workload_balance"] = 1.0 - workload
        
        # Quality score
        factors["quality_score"] = agent.quality_score / 10.0 if agent.quality_score > 0 else 0.5
        
        # Calculate weighted total
        total_score = sum(
            factors.get(key, 0) * weight 
            for key, weight in self.weights.items()
        ) / sum(self.weights.values())
        
        # Boost for specific job types
        if job_type:
            if station.station_type == "quality" and "inspect" in job_type:
                total_score *= 1.2
            elif station.station_type in ["cnc", "3d_print"] and "precision" in job_type:
                total_score *= 1.15
        
        return AssignmentScore(agent_id, station_id, total_score, factors)
    
    def find_optimal_assignment(
        self, 
        station_id: str,
        available_agents: Optional[List[str]] = None,
        job_type: Optional[str] = None
    ) -> Optional[str]:
        """Find best agent for a station"""
        
        if not available_agents:
            available_agents = [
                aid for aid, a in self.scheduler.agents.items()
                if a.status == "available" and a.current_station is None
            ]
        
        if not available_agents:
            return None
        
        # Calculate scores
        scores = [
            self.calculate_assignment_score(aid, station_id, job_type)
            for aid in available_agents
        ]
        
        # Sort by score
        scores.sort(key=lambda x: x.score, reverse=True)
        
        logger.debug(f"Assignment scores for {station_id}: {[(s.agent_id, s.score) for s in scores[:3]]}")
        
        return scores[0].agent_id if scores else None
    
    def optimize_all_assignments(self) -> Dict[str, str]:
        """Optimize all agent-station assignments"""
        
        # Get idle stations and available agents
        idle_stations = [
            sid for sid, s in self.scheduler.workstations.items()
            if s.status.value == "idle" and s.current_job is None
        ]
        
        available_agents = [
            aid for aid, a in self.scheduler.agents.items()
            if a.status == "available" and a.current_station is None
        ]
        
        if not idle_stations or not available_agents:
            return {}
        
        assignments = {}
        
        # Greedy assignment - best score first
        for station_id in idle_stations:
            if not available_agents:
                break
            
            # Find best agent
            scores = [
                self.calculate_assignment_score(aid, station_id)
                for aid in available_agents
            ]
            scores.sort(key=lambda x: x.score, reverse=True)
            
            best = scores[0]
            if best.score > 0.5:  # Minimum threshold
                assignments[station_id] = best.agent_id
                available_agents.remove(best.agent_id)
                
                logger.info(f"Optimized assignment: {best.agent_id} -> {station_id} (score: {best.score:.2f})")
                
                # Record
                self.assignment_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "station_id": station_id,
                    "agent_id": best.agent_id,
                    "score": best.score,
                    "factors": best.factors,
                })
        
        return assignments
    
    def calculate_utilization_stats(self) -> Dict:
        """Calculate utilization statistics"""
        
        agent_stats = {
            "total": len(self.scheduler.agents),
            "available": sum(1 for a in self.scheduler.agents.values() if a.status == "available"),
            "working": sum(1 for a in self.scheduler.agents.values() if a.status == "working"),
            "avg_skill": sum(a.skill_level for a in self.scheduler.agents.values()) / len(self.scheduler.agents),
            "avg_efficiency": sum(a.efficiency_multiplier for a in self.scheduler.agents.values()) / len(self.scheduler.agents),
        }
        
        station_stats = {
            "total": len(self.scheduler.workstations),
            "idle": sum(1 for s in self.scheduler.workstations.values() if s.status.value == "idle"),
            "running": sum(1 for s in self.scheduler.workstations.values() if s.status.value == "running"),
            "maintenance": sum(1 for s in self.scheduler.workstations.values() if s.status.value == "maintenance"),
        }
        
        return {
            "agents": agent_stats,
            "stations": station_stats,
            "utilization_rate": agent_stats["working"] / agent_stats["total"] if agent_stats["total"] > 0 else 0,
        }
    
    def get_recommendations(self) -> List[str]:
        """Get optimization recommendations"""
        recommendations = []
        
        stats = self.calculate_utilization_stats()
        
        # Check utilization
        if stats["utilization_rate"] < 0.5:
            recommendations.append(f"Low utilization ({stats['utilization_rate']:.1%}). Consider submitting more jobs.")
        
        # Check idle stations
        idle_count = stats["stations"]["idle"]
        if idle_count > 5:
            recommendations.append(f"{idle_count} stations idle. Optimize job scheduling.")
        
        # Check available agents
        available = stats["agents"]["available"]
        if available > 10:
            recommendations.append(f"{available} agents available. May be overstaffed or underloaded.")
        
        return recommendations
    
    def simulate_24h_schedule(self, job_count: int = 50) -> Dict:
        """Simulate 24-hour schedule"""
        
        import random
        
        # Reset
        for station in self.scheduler.workstations.values():
            station.status = type(station.status).IDLE
            station.current_job = None
        
        for agent in self.scheduler.agents.values():
            agent.status = "available"
            agent.current_station = None
        
        # Simulate jobs
        completed = 0
        failed = 0
        total_time = 0
        
        for i in range(job_count):
            # Try to assign
            assignments = self.optimize_all_assignments()
            
            if assignments:
                completed += len(assignments)
                total_time += 60  # Assume 1 hour per assignment
            else:
                failed += 1
        
        return {
            "jobs_attempted": job_count,
            "jobs_assigned": completed,
            "failed_assignments": failed,
            "success_rate": completed / job_count if job_count > 0 else 0,
            "estimated_hours": total_time / 60,
        }
    
    def export_history(self, filepath: str):
        """Export assignment history"""
        import json
        
        with open(filepath, 'w') as f:
            json.dump({
                "exported_at": datetime.now().isoformat(),
                "total_assignments": len(self.assignment_history),
                "assignments": self.assignment_history
            }, f, indent=2)
        
        logger.info(f"Exported {len(self.assignment_history)} assignments to {filepath}")


def main():
    """Demo optimizer"""
    print("AgentStationOptimizer Demo")
    print("=" * 50)
    
    # This would normally use a real scheduler
    print("Optimizer initialized with scoring weights:")
    print("  - Skill match: 1.5x")
    print("  - Role match: 1.3x")
    print("  - Efficiency: 1.0x")
    print("  - Workload balance: 0.8x")
    print("  - Quality score: 1.2x")
    
    print("\n✅ AgentStationOptimizer ready for integration")


if __name__ == "__main__":
    main()
