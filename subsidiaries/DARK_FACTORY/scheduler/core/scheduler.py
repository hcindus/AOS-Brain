"""
Dark Factory Scheduler v2.0
AGI Connect Integrated Scheduler

Coordinates 36 agents across 36 workstations.
Integrated with procurement, quality control, and maintenance systems.
"""

import asyncio
import json
import heapq
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum, auto
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DarkFactoryScheduler")


class JobPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class JobStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StationStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    SETUP = "setup"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
    ERROR = "error"


@dataclass
class ManufacturingJob:
    """Enhanced manufacturing job with full tracking"""
    job_id: str
    product_type: str
    quantity: int
    priority: JobPriority
    materials_needed: Dict[str, int]
    estimated_duration: int  # minutes
    setup_time: int  # minutes
    
    # Quality control
    quality_requirements: Dict[str, Any] = field(default_factory=dict)
    inspection_points: List[str] = field(default_factory=list)
    
    # Tracking
    deadline: Optional[datetime] = None
    status: JobStatus = JobStatus.PENDING
    assigned_station: Optional[str] = None
    assigned_agent: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    actual_duration: Optional[int] = None
    
    # Quality metrics
    quality_score: Optional[float] = None
    defect_count: int = 0
    rework_required: bool = False
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    customer_id: Optional[str] = None
    order_id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert job to dictionary"""
        return {
            "job_id": self.job_id,
            "product_type": self.product_type,
            "quantity": self.quantity,
            "priority": self.priority.name,
            "materials_needed": self.materials_needed,
            "estimated_duration": self.estimated_duration,
            "setup_time": self.setup_time,
            "quality_requirements": self.quality_requirements,
            "inspection_points": self.inspection_points,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status.value,
            "assigned_station": self.assigned_station,
            "assigned_agent": self.assigned_agent,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "actual_duration": self.actual_duration,
            "quality_score": self.quality_score,
            "defect_count": self.defect_count,
            "rework_required": self.rework_required,
            "created_at": self.created_at.isoformat(),
            "customer_id": self.customer_id,
            "order_id": self.order_id,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "ManufacturingJob":
        """Create job from dictionary"""
        return cls(
            job_id=data["job_id"],
            product_type=data["product_type"],
            quantity=data["quantity"],
            priority=JobPriority[data["priority"]],
            materials_needed=data["materials_needed"],
            estimated_duration=data["estimated_duration"],
            setup_time=data["setup_time"],
            quality_requirements=data.get("quality_requirements", {}),
            inspection_points=data.get("inspection_points", []),
            deadline=datetime.fromisoformat(data["deadline"]) if data.get("deadline") else None,
            status=JobStatus(data.get("status", "pending")),
            assigned_station=data.get("assigned_station"),
            assigned_agent=data.get("assigned_agent"),
            start_time=datetime.fromisoformat(data["start_time"]) if data.get("start_time") else None,
            end_time=datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None,
            actual_duration=data.get("actual_duration"),
            quality_score=data.get("quality_score"),
            defect_count=data.get("defect_count", 0),
            rework_required=data.get("rework_required", False),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
            customer_id=data.get("customer_id"),
            order_id=data.get("order_id"),
        )


@dataclass
class WorkStation:
    """Enhanced factory workstation"""
    station_id: str
    station_type: str
    capabilities: List[str]
    
    # Status
    status: StationStatus = StationStatus.IDLE
    current_job: Optional[str] = None
    current_agent: Optional[str] = None
    
    # Performance
    efficiency_rating: float = 1.0
    utilization_rate: float = 0.0
    total_jobs_completed: int = 0
    total_uptime_minutes: int = 0
    total_downtime_minutes: int = 0
    
    # Tracking
    last_job_type: Optional[str] = None
    last_maintenance: datetime = field(default_factory=datetime.now)
    next_scheduled_maintenance: Optional[datetime] = None
    maintenance_count: int = 0
    
    # Quality
    quality_score_avg: float = 0.0
    defect_rate: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "station_id": self.station_id,
            "station_type": self.station_type,
            "capabilities": self.capabilities,
            "status": self.status.value,
            "current_job": self.current_job,
            "current_agent": self.current_agent,
            "efficiency_rating": self.efficiency_rating,
            "utilization_rate": self.utilization_rate,
            "total_jobs_completed": self.total_jobs_completed,
            "total_uptime_minutes": self.total_uptime_minutes,
            "total_downtime_minutes": self.total_downtime_minutes,
            "last_job_type": self.last_job_type,
            "last_maintenance": self.last_maintenance.isoformat(),
            "next_scheduled_maintenance": self.next_scheduled_maintenance.isoformat() if self.next_scheduled_maintenance else None,
            "maintenance_count": self.maintenance_count,
            "quality_score_avg": self.quality_score_avg,
            "defect_rate": self.defect_rate,
        }


@dataclass
class FactoryAgent:
    """Factory agent profile"""
    agent_id: str
    role: str  # operator, technician, inspector, coordinator, specialist
    skill_level: int  # 1-10
    certifications: List[str] = field(default_factory=list)
    
    # Assignment
    current_station: Optional[str] = None
    shift: str = "day"  # day, night, swing
    
    # Performance
    efficiency_multiplier: float = 1.0
    jobs_completed: int = 0
    quality_score: float = 0.0
    
    # Status
    status: str = "available"  # available, working, break, offline
    last_assignment: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "skill_level": self.skill_level,
            "certifications": self.certifications,
            "current_station": self.current_station,
            "shift": self.shift,
            "efficiency_multiplier": self.efficiency_multiplier,
            "jobs_completed": self.jobs_completed,
            "quality_score": self.quality_score,
            "status": self.status,
            "last_assignment": self.last_assignment.isoformat() if self.last_assignment else None,
        }


class DarkFactoryScheduler:
    """
    AGI Connect Integrated Factory Scheduler
    
    Features:
    - 36 workstations, 36 agents
    - Self-optimizing job scheduling
    - AGI Connect integration
    - Procurement system integration
    - Quality control integration
    - Predictive maintenance
    - Persistent job queue
    - Real-time metrics
    """
    
    # Factory configuration
    WORKSTATION_CONFIG = {
        "3d_print": {"count": 8, "capabilities": ["prototype", "custom_parts", "rapid_manufacturing"]},
        "cnc": {"count": 6, "capabilities": ["precision", "metal", "wood", "machining"]},
        "assembly": {"count": 12, "capabilities": ["assembly", "testing", "kitting"]},
        "quality": {"count": 6, "capabilities": ["inspection", "testing", "certification"]},
        "packing": {"count": 4, "capabilities": ["packaging", "shipping_prep", "labeling"]},
    }
    
    AGENT_ROLES = [
        ("operator", 16),
        ("technician", 8),
        ("inspector", 6),
        ("coordinator", 4),
        ("specialist", 2),
    ]
    
    def __init__(self, data_dir: str = "/root/.openclaw/workspace/subsidiaries/DARK_FACTORY/scheduler/data"):
        logger.info("🏭 INITIALIZING DARK FACTORY SCHEDULER v2.0")
        logger.info("=" * 70)
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Core components
        self.workstations: Dict[str, WorkStation] = {}
        self.agents: Dict[str, FactoryAgent] = {}
        self.jobs: Dict[str, ManufacturingJob] = {}
        self.job_queue: List[Tuple[int, str, datetime]] = []  # (priority, job_id, timestamp)
        
        # Integration connectors
        self.agi_connect = None
        self.procurement_connector = None
        self.quality_connector = None
        self.maintenance_predictor = None
        
        # Metrics
        self.metrics = {
            "jobs_completed": 0,
            "jobs_failed": 0,
            "total_changeover_time": 0,
            "total_setup_time": 0,
            "start_time": datetime.now(),
            "last_tick": datetime.now(),
        }
        
        # Load or initialize
        self._initialize_workstations()
        self._initialize_agents()
        self._load_state()
        
        logger.info(f"✅ Scheduler ready:")
        logger.info(f"   Workstations: {len(self.workstations)}")
        logger.info(f"   Agents: {len(self.agents)}")
        logger.info(f"   Data directory: {self.data_dir}")
    
    def _initialize_workstations(self):
        """Create all 36 factory workstations"""
        for station_type, config in self.WORKSTATION_CONFIG.items():
            for i in range(config["count"]):
                ws = WorkStation(
                    station_id=f"{station_type}_{i+1:02d}",
                    station_type=station_type,
                    capabilities=config["capabilities"],
                )
                self.workstations[ws.station_id] = ws
        
        logger.info(f"Initialized {len(self.workstations)} workstations")
    
    def _initialize_agents(self):
        """Initialize 36 factory agents"""
        import random
        
        agent_id = 0
        shifts = ["day", "night", "swing"]
        
        for role, count in self.AGENT_ROLES:
            for i in range(count):
                agent = FactoryAgent(
                    agent_id=f"agent_{agent_id:03d}",
                    role=role,
                    skill_level=random.randint(3, 10),
                    certifications=self._get_role_certifications(role),
                    shift=random.choice(shifts),
                    efficiency_multiplier=random.uniform(0.85, 1.25),
                )
                self.agents[agent.agent_id] = agent
                agent_id += 1
        
        logger.info(f"Initialized {len(self.agents)} agents")
    
    def _get_role_certifications(self, role: str) -> List[str]:
        """Get certifications for role"""
        certs = {
            "operator": ["OSHA-10", "Equipment Safety"],
            "technician": ["OSHA-30", "Machine Repair", "Electrical Safety"],
            "inspector": ["ISO 9001", "Six Sigma", "Quality Control"],
            "coordinator": ["Supply Chain", "Lean Manufacturing"],
            "specialist": ["OSHA-30", "Advanced Diagnostics", "Root Cause Analysis"],
        }
        return certs.get(role, [])
    
    def _load_state(self):
        """Load persisted state"""
        jobs_file = self.data_dir / "jobs.json"
        if jobs_file.exists():
            try:
                with open(jobs_file) as f:
                    jobs_data = json.load(f)
                    for job_dict in jobs_data:
                        job = ManufacturingJob.from_dict(job_dict)
                        self.jobs[job.job_id] = job
                        if job.status == JobStatus.PENDING:
                            heapq.heappush(self.job_queue, (job.priority.value, job.job_id, job.created_at))
                logger.info(f"Loaded {len(jobs_data)} jobs from persistence")
            except Exception as e:
                logger.error(f"Failed to load jobs: {e}")
    
    def connect_agi_connect(self, agi_connect):
        """Connect to AGI Connect"""
        self.agi_connect = agi_connect
        logger.info("Connected to AGI Connect")
    
    def connect_procurement(self, procurement_connector):
        """Connect to procurement system"""
        self.procurement_connector = procurement_connector
        logger.info("Connected to Procurement System")
    
    def connect_quality(self, quality_connector):
        """Connect to quality control system"""
        self.quality_connector = quality_connector
        logger.info("Connected to Quality Control System")
    
    def connect_maintenance(self, maintenance_predictor):
        """Connect to maintenance predictor"""
        self.maintenance_predictor = maintenance_predictor
        logger.info("Connected to Maintenance Predictor")
    
    def submit_job(self, job: ManufacturingJob) -> bool:
        """Submit a new manufacturing job"""
        self.jobs[job.job_id] = job
        
        # Check material availability via procurement
        if self.procurement_connector:
            materials_ok = self._check_materials(job)
            if not materials_ok:
                job.status = JobStatus.PENDING
                logger.warning(f"Job {job.job_id} waiting - materials not available")
        
        # Add to priority queue
        heapq.heappush(self.job_queue, (job.priority.value, job.job_id, job.created_at))
        job.status = JobStatus.QUEUED
        
        logger.info(f"📋 Job submitted: {job.job_id} | {job.product_type} x{job.quantity} | Priority: {job.priority.name}")
        
        # Persist
        self._persist_jobs()
        
        return True
    
    def _check_materials(self, job: ManufacturingJob) -> bool:
        """Check if materials are available"""
        # Integration with procurement system
        if not self.procurement_connector:
            return True
        
        # In real implementation, would check inventory
        # For now, assume available
        return True
    
    async def optimize_and_schedule(self):
        """
        Self-optimizing scheduler.
        Minimizes changeover, considers agent skills, respects deadlines.
        """
        logger.info("⚙️  Running optimization...")
        
        # Get pending jobs
        pending = [
            self.jobs[job_id]
            for _, job_id, _ in self.job_queue
            if self.jobs[job_id].status == JobStatus.QUEUED
        ]
        
        if not pending:
            logger.info("No pending jobs to optimize")
            return
        
        # Sort by priority and deadline
        pending.sort(key=lambda j: (
            j.priority.value,
            j.deadline or datetime.max,
            j.product_type
        ))
        
        # Rebuild queue
        self.job_queue = []
        for job in pending:
            heapq.heappush(self.job_queue, (job.priority.value, job.job_id, job.created_at))
        
        logger.info(f"Optimized {len(pending)} pending jobs")
        
        # Try to assign jobs
        await self._assign_pending_jobs()
    
    async def _assign_pending_jobs(self):
        """Assign pending jobs to available stations"""
        assigned_count = 0
        
        # Get pending jobs sorted by priority
        pending_jobs = [
            (priority, job_id, timestamp)
            for priority, job_id, timestamp in self.job_queue
            if self.jobs[job_id].status == JobStatus.QUEUED
        ]
        
        for _, job_id, _ in pending_jobs:
            job = self.jobs[job_id]
            
            # Find best station
            station_id = await self._find_best_station(job)
            if not station_id:
                continue
            
            # Find best agent
            agent_id = await self._find_best_agent(station_id, job)
            if not agent_id:
                continue
            
            # Assign
            await self._assign_job(job, station_id, agent_id)
            assigned_count += 1
        
        if assigned_count > 0:
            logger.info(f"Assigned {assigned_count} jobs")
    
    async def _find_best_station(self, job: ManufacturingJob) -> Optional[str]:
        """Find best workstation for job"""
        compatible = []
        
        for station_id, station in self.workstations.items():
            if station.status not in [StationStatus.IDLE, StationStatus.RUNNING]:
                continue
            
            if station.current_job:
                continue
            
            # Check compatibility
            if not self._station_compatible(station, job):
                continue
            
            # Calculate score
            score = 0
            
            # Prefer matching last job type (minimize changeover)
            if station.last_job_type == job.product_type:
                score += 100
            else:
                score -= job.setup_time
            
            # Factor in efficiency
            score += station.efficiency_rating * 10
            
            # Check maintenance schedule
            if self.maintenance_predictor:
                maint_needed = await self.maintenance_predictor.predict_maintenance_urgency(station_id)
                if maint_needed > 0.7:
                    continue  # Skip stations needing urgent maintenance
            
            compatible.append((station_id, score))
        
        if not compatible:
            return None
        
        # Return highest scored station
        compatible.sort(key=lambda x: x[1], reverse=True)
        return compatible[0][0]
    
    def _station_compatible(self, station: WorkStation, job: ManufacturingJob) -> bool:
        """Check if workstation can handle job"""
        product_caps = {
            "prototype": ["prototype", "custom_parts"],
            "custom": ["custom_parts", "rapid_manufacturing"],
            "precision": ["precision", "machining"],
            "metal": ["metal", "precision", "machining"],
            "wood": ["wood", "machining"],
            "assembly": ["assembly", "kitting"],
            "kit": ["assembly", "kitting"],
            "inspect": ["inspection", "testing"],
            "test": ["testing", "certification"],
            "package": ["packaging", "shipping_prep"],
        }
        
        required_caps = product_caps.get(job.product_type, [])
        return any(cap in station.capabilities for cap in required_caps)
    
    async def _find_best_agent(self, station_id: str, job: ManufacturingJob) -> Optional[str]:
        """Find best agent for a station"""
        station = self.workstations[station_id]
        
        available_agents = [
            (agent_id, agent)
            for agent_id, agent in self.agents.items()
            if agent.status == "available" and agent.current_station is None
        ]
        
        if not available_agents:
            return None
        
        scored_agents = []
        for agent_id, agent in available_agents:
            score = agent.skill_level * agent.efficiency_multiplier
            
            # Role matching bonuses
            if station.station_type == "quality" and agent.role == "inspector":
                score *= 1.5
            elif station.station_type in ["3d_print", "cnc"] and agent.role == "operator":
                score *= 1.3
            elif station.station_type == "assembly" and agent.role in ["operator", "coordinator"]:
                score *= 1.2
            
            # Quality score bonus
            score += agent.quality_score * 5
            
            scored_agents.append((agent_id, score))
        
        scored_agents.sort(key=lambda x: x[1], reverse=True)
        return scored_agents[0][0] if scored_agents else None
    
    async def _assign_job(self, job: ManufacturingJob, station_id: str, agent_id: str):
        """Assign job to station and agent"""
        station = self.workstations[station_id]
        agent = self.agents[agent_id]
        
        # Calculate setup time
        setup_time = 0
        if station.last_job_type and station.last_job_type != job.product_type:
            setup_time = job.setup_time
            self.metrics["total_setup_time"] += setup_time
        
        # Update job
        job.assigned_station = station_id
        job.assigned_agent = agent_id
        job.status = JobStatus.RUNNING
        job.start_time = datetime.now()
        
        # Calculate duration with efficiency
        duration = int(job.estimated_duration / (station.efficiency_rating * agent.efficiency_multiplier))
        job.end_time = job.start_time + timedelta(minutes=duration + setup_time)
        
        # Update station
        station.status = StationStatus.RUNNING
        station.current_job = job.job_id
        station.current_agent = agent_id
        
        # Update agent
        agent.current_station = station_id
        agent.status = "working"
        agent.last_assignment = datetime.now()
        
        logger.info(f"🚀 Job {job.job_id} assigned to {station_id} (agent: {agent_id})")
        
        # Notify quality system if inspection required
        if job.inspection_points and self.quality_connector:
            await self.quality_connector.schedule_inspection(job.job_id, job.inspection_points)
        
        # Persist
        self._persist_jobs()
    
    async def tick(self):
        """One tick of factory operation"""
        current_time = datetime.now()
        
        # 1. Check for completed jobs
        await self._check_completed_jobs()
        
        # 2. Check maintenance schedules
        await self._check_maintenance()
        
        # 3. Assign pending jobs
        await self._assign_pending_jobs()
        
        # 4. Update metrics
        self.metrics["last_tick"] = current_time
        
        # 5. Persist state
        self._persist_state()
    
    async def _check_completed_jobs(self):
        """Check for jobs that have finished"""
        current_time = datetime.now()
        completed = []
        
        for job_id, job in self.jobs.items():
            if job.status == JobStatus.RUNNING and job.end_time:
                if current_time >= job.end_time:
                    # Complete job
                    job.status = JobStatus.COMPLETED
                    job.actual_duration = int((current_time - job.start_time).total_seconds() / 60)
                    completed.append(job_id)
                    
                    # Update station
                    if job.assigned_station:
                        station = self.workstations[job.assigned_station]
                        station.current_job = None
                        station.status = StationStatus.IDLE
                        station.total_jobs_completed += 1
                        station.last_job_type = job.product_type
                        station.utilization_rate = self._calculate_utilization(station)
                    
                    # Update agent
                    if job.assigned_agent:
                        agent = self.agents[job.assigned_agent]
                        agent.current_station = None
                        agent.status = "available"
                        agent.jobs_completed += 1
                    
                    # Request quality inspection if needed
                    if job.quality_requirements and self.quality_connector:
                        quality_result = await self.quality_connector.inspect_completed_job(job)
                        job.quality_score = quality_result.get("score", 0)
                        job.defect_count = quality_result.get("defects", 0)
                    
                    logger.info(f"✅ Job completed: {job_id}")
        
        if completed:
            self.metrics["jobs_completed"] += len(completed)
    
    def _calculate_utilization(self, station: WorkStation) -> float:
        """Calculate station utilization rate"""
        total_time = station.total_uptime_minutes + station.total_downtime_minutes
        if total_time == 0:
            return 0.0
        return station.total_uptime_minutes / total_time
    
    async def _check_maintenance(self):
        """Check and schedule maintenance"""
        if not self.maintenance_predictor:
            return
        
        for station_id, station in self.workstations.items():
            if station.status == StationStatus.MAINTENANCE:
                continue
            
            # Predict maintenance need
            urgency = await self.maintenance_predictor.predict_maintenance_urgency(station_id)
            
            if urgency > 0.8 and station.status == StationStatus.IDLE:
                # Schedule maintenance
                station.status = StationStatus.MAINTENANCE
                station.next_scheduled_maintenance = datetime.now() + timedelta(hours=2)
                station.maintenance_count += 1
                
                # Request maintenance materials
                if self.procurement_connector:
                    await self.procurement_connector.request_maintenance_supplies(station_id)
                
                logger.info(f"🔧 Maintenance scheduled for {station_id} (urgency: {urgency:.2f})")
    
    def _persist_jobs(self):
        """Persist jobs to disk"""
        jobs_file = self.data_dir / "jobs.json"
        jobs_data = [job.to_dict() for job in self.jobs.values()]
        with open(jobs_file, 'w') as f:
            json.dump(jobs_data, f, indent=2)
    
    def _persist_state(self):
        """Persist full state"""
        # Persist jobs
        self._persist_jobs()
        
        # Persist stations
        stations_file = self.data_dir / "stations.json"
        stations_data = {sid: station.to_dict() for sid, station in self.workstations.items()}
        with open(stations_file, 'w') as f:
            json.dump(stations_data, f, indent=2)
        
        # Persist agents
        agents_file = self.data_dir / "agents.json"
        agents_data = {aid: agent.to_dict() for aid, agent in self.agents.items()}
        with open(agents_file, 'w') as f:
            json.dump(agents_data, f, indent=2)
        
        # Persist metrics
        metrics_file = self.data_dir / "metrics.json"
        with open(metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2, default=str)
    
    def get_factory_status(self) -> Dict:
        """Get complete factory status"""
        running = sum(1 for j in self.jobs.values() if j.status == JobStatus.RUNNING)
        completed = sum(1 for j in self.jobs.values() if j.status == JobStatus.COMPLETED)
        pending = sum(1 for j in self.jobs.values() if j.status == JobStatus.QUEUED)
        
        busy_stations = sum(1 for s in self.workstations.values() if s.status == StationStatus.RUNNING)
        idle_stations = sum(1 for s in self.workstations.values() if s.status == StationStatus.IDLE)
        maint_stations = sum(1 for s in self.workstations.values() if s.status == StationStatus.MAINTENANCE)
        
        busy_agents = sum(1 for a in self.agents.values() if a.status == "working")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "jobs": {
                "pending": pending,
                "running": running,
                "completed": completed,
                "total": len(self.jobs),
            },
            "stations": {
                "running": busy_stations,
                "idle": idle_stations,
                "maintenance": maint_stations,
                "total": len(self.workstations),
            },
            "agents": {
                "working": busy_agents,
                "available": len(self.agents) - busy_agents,
                "total": len(self.agents),
            },
            "efficiency": {
                "changeover_time_saved": self.metrics["total_changeover_time"],
                "total_setup_time": self.metrics["total_setup_time"],
            },
            "uptime": str(datetime.now() - self.metrics["start_time"]),
        }
    
    def get_job_report(self, job_id: str) -> Optional[Dict]:
        """Get detailed report for a job"""
        if job_id not in self.jobs:
            return None
        
        job = self.jobs[job_id]
        return {
            "job": job.to_dict(),
            "station": self.workstations.get(job.assigned_station, {}).to_dict() if job.assigned_station else None,
            "agent": self.agents.get(job.assigned_agent, {}).to_dict() if job.assigned_agent else None,
        }


async def main():
    """Demo factory scheduler"""
    scheduler = DarkFactoryScheduler()
    
    # Create sample jobs
    jobs = [
        ManufacturingJob(
            job_id="JOB-2024-001",
            product_type="prototype",
            quantity=10,
            priority=JobPriority.HIGH,
            materials_needed={"plastic": 5, "electronics": 2},
            estimated_duration=30,
            setup_time=10,
            deadline=datetime.now() + timedelta(hours=2),
        ),
        ManufacturingJob(
            job_id="JOB-2024-002",
            product_type="assembly",
            quantity=50,
            priority=JobPriority.MEDIUM,
            materials_needed={"parts": 50, "screws": 200},
            estimated_duration=60,
            setup_time=15,
        ),
        ManufacturingJob(
            job_id="JOB-2024-003",
            product_type="precision",
            quantity=5,
            priority=JobPriority.CRITICAL,
            materials_needed={"metal": 2},
            estimated_duration=45,
            setup_time=20,
            inspection_points=["dimensional", "surface_finish"],
        ),
    ]
    
    # Submit jobs
    for job in jobs:
        scheduler.submit_job(job)
    
    # Run optimization and scheduling
    await scheduler.optimize_and_schedule()
    
    # Simulate ticks
    print("\n🏭 Running factory simulation...")
    for tick in range(5):
        print(f"\n--- Tick {tick + 1} ---")
        await scheduler.tick()
        status = scheduler.get_factory_status()
        print(f"Running jobs: {status['jobs']['running']}")
        print(f"Completed jobs: {status['jobs']['completed']}")
    
    # Final status
    print("\n" + "=" * 70)
    print(scheduler.get_factory_status())
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
