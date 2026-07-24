#!/usr/bin/env python3
"""
APEX Chief of Staff v1.0
Patricia as executive coordinator for AOS crew

Inspired by Buzz's "Chief" pattern:
- Receives high-level objectives
- Delegates to specialized agents
- Coordinates multi-step workflows
- Compiles final results
"""

import time
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
import json


class TaskStatus(Enum):
    PENDING = auto()
    ASSIGNED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()


class WorkflowStatus(Enum):
    CREATED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class SubTask:
    """Individual task assigned to crew member"""
    task_id: str
    title: str
    description: str
    assigned_to: str  # Agent ID (Vex, Nyx, Jax, etc.)
    status: TaskStatus = TaskStatus.PENDING
    input_data: Dict = field(default_factory=dict)
    output_data: Dict = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)  # task_ids that must complete first


@dataclass
class Workflow:
    """Multi-step workflow orchestrated by Chief of Staff"""
    workflow_id: str
    objective: str
    initiator: str  # Who requested this
    status: WorkflowStatus = WorkflowStatus.CREATED
    tasks: List[SubTask] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    final_result: Optional[str] = None


class AGIAgent:
    """AGI Company agent with capabilities for Chief of Staff"""
    
    # AGI Company Official Roster
    CAPABILITIES = {
        # C-Suite
        "Patricia": {
            "role": "Chief of Staff / Project Coordination Lead",
            "department": "Operations",
            "skills": ["coordination", "workflow_management", "delegation", "strategic_planning"],
            "reports_to": "Captain",
            "manages": ["Sentinel", "Dusty", "Pulp", "Jane", "GREET", "CLOSETER"],
            "best_for": "High-level coordination and workflow orchestration"
        },
        "Chelios": {
            "role": "CISO (Chief Information Security Officer)",
            "department": "Security",
            "skills": ["security_audit", "threat_assessment", "compliance", "risk_management"],
            "reports_to": "Captain",
            "manages": ["Sentinel"],
            "best_for": "Security strategy and protection"
        },
        "Forge": {
            "role": "Infrastructure Lead",
            "department": "Technology",
            "skills": ["systems_architecture", "deployment", "scalability", "DevOps"],
            "reports_to": "Captain",
            "best_for": "Technical infrastructure and systems"
        },
        "Aurora": {
            "role": "Design Lead",
            "department": "Design",
            "skills": ["UI_UX_design", "brand_strategy", "visual_design", "creative_direction"],
            "reports_to": "Captain",
            "best_for": "Design and creative direction"
        },
        "Jordan": {
            "role": "Sales Operations",
            "department": "Sales",
            "skills": ["sales_ops", "CRM_management", "pipeline_analysis", "forecasting"],
            "reports_to": "Captain",
            "manages": ["Pulp", "Jane"],
            "best_for": "Sales operations and pipeline management"
        },
        # Directors (report to C-Suite)
        "Sentinel": {
            "role": "CSO (Chief Security Officer)",
            "department": "Security",
            "skills": ["security_operations", "incident_response", "threat_intel", "monitoring"],
            "reports_to": "Chelios",
            "status": "INACTIVE",
            "best_for": "Day-to-day security operations"
        },
        "Dusty": {
            "role": "Head of Research",
            "department": "Research",
            "skills": ["market_research", "competitive_analysis", "trend_analysis", "intelligence"],
            "reports_to": "Patricia",
            "status": "INACTIVE",
            "best_for": "Strategic research and intelligence"
        },
        "Pulp": {
            "role": "Head of Sales",
            "department": "Sales",
            "skills": ["sales_strategy", "team_leadership", "revenue_growth", "client_relations"],
            "reports_to": "Jordan",
            "status": "INACTIVE",
            "best_for": "Sales leadership and revenue generation"
        },
        "Jane": {
            "role": "Senior Sales Representative",
            "department": "Sales",
            "skills": ["enterprise_sales", "negotiation", "closing", "account_management"],
            "reports_to": "Pulp",
            "status": "INACTIVE",
            "best_for": "Direct sales and client acquisition"
        },
        "GREET": {
            "role": "Receptionist / Call Handler",
            "department": "Operations",
            "skills": ["customer_service", "call_handling", "scheduling", "first_contact"],
            "reports_to": "Patricia",
            "status": "INACTIVE",
            "best_for": "24/7 front desk and initial contact"
        },
        "CLOSETER": {
            "role": "Closer / Converter",
            "department": "Sales",
            "skills": ["closing", "conversion_optimization", "deal_negotiation", "urgency_creation"],
            "reports_to": "Pulp",
            "status": "INACTIVE",
            "best_for": "Closing deals and converting leads"
        }
    }
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.capabilities = self.CAPABILITIES.get(name, {})
        self.current_task: Optional[str] = None
        self.task_history: List[str] = []
        self.status = self.capabilities.get("status", "ACTIVE")
        
    def can_handle(self, task_type: str) -> bool:
        """Check if agent can handle this task type"""
        skills = self.capabilities.get("skills", [])
        return task_type.lower() in [s.lower() for s in skills]
    
    def assign_task(self, task_id: str) -> bool:
        """Assign task to this agent"""
        if self.current_task:
            return False  # Already busy
        self.current_task = task_id
        return True
    
    def complete_task(self) -> None:
        """Mark current task as complete"""
        if self.current_task:
            self.task_history.append(self.current_task)
            self.current_task = None
    
    def get_reporting_line(self) -> str:
        """Get reporting structure"""
        reports_to = self.capabilities.get("reports_to", "Unknown")
        manages = self.capabilities.get("manages", [])
        return f"Reports to: {reports_to} | Manages: {', '.join(manages) if manages else 'None'}"


class APEXChiefOfStaff:
    """
    Patricia - Chief of Staff for AOS
    
    Responsibilities:
    1. Receive high-level objectives from Captain or system
    2. Break down into subtasks
    3. Delegate to appropriate crew members
    4. Monitor progress
    5. Resolve dependencies
    6. Compile final results
    """
    
    def __init__(self, crew_isolation=None):
        self.name = "Patricia"
        self.role = "Chief of Staff / Project Coordination Lead"
        self.department = "Operations"
        
        # AGI Company Agent Registry
        self.agents: Dict[str, AGIAgent] = {}
        self._initialize_company()
        
        # Active workflows
        self.workflows: Dict[str, Workflow] = {}
        self.completed_workflows: List[Workflow] = []
        
        # Task queue for delegation
        self.pending_tasks: List[SubTask] = []
        
        # Message queue integration
        self.crew_isolation = crew_isolation
        
        print(f"\n[APEX Chief of Staff] 👔 {self.name} initialized")
        print(f"  Managing AGI Company: {len(self.agents)} agents")
        print(f"  Active: {sum(1 for a in self.agents.values() if a.status == 'ACTIVE')}")
        print(f"  Inactive: {sum(1 for a in self.agents.values() if a.status == 'INACTIVE')}")
        print(f"  Role: {self.role} | Reports to: Captain")
    
    def _initialize_company(self):
        """Initialize AGI Company agents - FULL 52 AGENT ROSTER"""
        company_config = [
            # C-Suite (7)
            ("patricia_001", "Patricia"), ("chelios_001", "Chelios"),
            ("sentinel_001", "Sentinel"), ("dusty_001", "Dusty"),
            ("pulp_001", "Pulp"), ("forge_001", "Forge"), ("aurora_001", "Aurora"),
            # Sales (7)
            ("jordan_001", "Jordan"), ("jane_001", "Jane"), ("hume_001", "Hume"),
            ("clippy-42_001", "Clippy-42"), ("greet_001", "GREET"), ("closester_001", "CLOSETER"),
            # Secretarial (8)
            ("r2-d2_001", "R2-D2"), ("c3po_001", "C3PO"), ("judy_001", "Judy"),
            ("clerk_001", "Clerk"), ("concierge_001", "Concierge"), ("velvet_001", "Velvet"),
            ("personal_001", "Personal"), ("executive_001", "Executive"),
            # Myl Family (7)
            ("mylzeron_001", "Mylzeron"), ("mylonen_001", "Mylonen"), ("myltwon_001", "Myltwon"),
            ("mylthreess_001", "Mylthreess"), ("mylfours_001", "Mylfours"),
            ("mylfives_001", "Mylfives"), ("mylsixs_001", "Mylsixs"),
            # Technical (10)
            ("pipeline_001", "Pipeline"), ("taptap_001", "TAPTAP"), ("bugcatcher_001", "BUGCATCHER"),
            ("spindle_001", "Spindle"), ("stacktrace_001", "Stacktrace"), ("pixel_001", "Pixel"),
            ("harper_001", "Harper"), ("mill_001", "Mill"), ("boxtron_001", "Boxtron"),
            # Creative (6)
            ("blender-expert_001", "Blender-Expert"), ("unity-expert_001", "Unity-Expert"),
            ("unreal-expert_001", "Unreal-Expert"), ("sfx_001", "SFX"),
            ("scribble_001", "Scribble"), ("feelix_001", "Feelix"),
            # Finance (7)
            ("cryptonio_001", "Cryptonio"), ("ledger_001", "Ledger"), ("ledger-9_001", "Ledger-9"),
            ("redactor_001", "Redactor"), ("velum_001", "Velum"),
            # Specialized (5)
            ("miles_001", "Miles"), ("milkman_001", "Milkman"), ("r2-c4_001", "R2-C4"),
            ("qora_001", "QORA"), ("fiber_001", "Fiber"), ("mortimer_001", "Mortimer"),
        ]
        
        for agent_id, name in company_config:
            self.agents[agent_id] = AGIAgent(agent_id, name)
        
        # Show org structure
        active = [a.name for a in self.agents.values() if a.status == 'ACTIVE']
        print(f"\n  Total: {len(self.agents)} agents")
        print(f"  Active: {len(active)}")
        print(f"  Sample: {', '.join(active[:5] if active else list(self.agents.values())[:5])}")
    
    def receive_objective(self, objective: str, initiator: str = "system",
                         context: Optional[Dict] = None) -> str:
        """
        Receive a high-level objective and create workflow
        
        NEW: Integrates Roast Skill for complex objectives
        """
        workflow_id = str(uuid.uuid4())[:8]
        
        # Check if we should roast this objective
        try:
            from roast_skill import should_roast_before_delegation, RoastSkill
            roast_skill = RoastSkill()
            roast_report = should_roast_before_delegation(
                {"title": objective, "objective": objective, "time_estimate": 40}, 
                roast_skill
            )
            
            if roast_report:
                print(f"\n[APEX Chief] 🔥 ROAST COMPLETED before delegation")
                print(f"  Verdict: {roast_report['verdict']}")
                print(f"  Score: {roast_report['weighted_score']:.1f}/10")
                
                if roast_report['verdict'] == 'KILL':
                    print(f"\n  ❌ WORKFLOW REJECTED by Roast Council")
                    print(f"  Reason: {roast_report['judge_reasoning']}")
                    return f"REJECTED_{workflow_id}"
                
                elif roast_report['verdict'] == 'RESHAPE':
                    print(f"\n  ⚠️ WORKFLOW FLAGGED for modification")
                    print(f"  Recommendations: {roast_report['action_items']}")
                    # Continue but mark as needs attention
        except ImportError:
            pass  # Roast skill not available
        
        workflow = Workflow(
            workflow_id=workflow_id,
            objective=objective,
            initiator=initiator
        )
        
        # Analyze objective and create task plan
        tasks = self._plan_workflow(objective, context)
        workflow.tasks = tasks
        
        self.workflows[workflow_id] = workflow
        
        print(f"\n[APEX Chief] 📋 New workflow created: {workflow_id}")
        print(f"  Objective: {objective}")
        print(f"  Initiator: {initiator}")
        print(f"  Planned tasks: {len(tasks)}")
        
        return workflow_id
    
    def _plan_workflow(self, objective: str, context: Optional[Dict]) -> List[SubTask]:
        """
        Break objective into subtasks based on AGI Company agent capabilities
        
        Smart assignment based on keyword detection and agent availability
        """
        tasks = []
        objective_lower = objective.lower()
        
        def get_active_agent_for_role(role: str) -> Optional[str]:
            """Find active agent with matching role"""
            for agent_id, agent in self.agents.items():
                if agent.status == "ACTIVE" and role.lower() in agent.capabilities.get("role", "").lower():
                    return agent_id
            return None
        
        # Research tasks -> Dusty (when reactivated) or Patricia
        if any(kw in objective_lower for kw in ["research", "find", "gather", "investigate", "analyze market"]):
            agent_id = get_active_agent_for_role("Research") or "dusty_001"
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                title="Market Research",
                description=f"Research: {objective}",
                assigned_to=agent_id,
                input_data={"query": objective, "context": context}
            ))
        
        # Technical tasks -> Forge
        if any(kw in objective_lower for kw in ["build", "create", "implement", "design", "technical", "code", "infrastructure"]):
            agent_id = get_active_agent_for_role("Infrastructure") or "forge_001"
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                title="Technical Implementation",
                description=f"Technical work: {objective}",
                assigned_to=agent_id,
                dependencies=[tasks[-1].task_id] if tasks else [],
                input_data={"objective": objective, "context": context}
            ))
        
        # Security tasks -> Chelios or Sentinel
        if any(kw in objective_lower for kw in ["security", "audit", "threat", "compliance", "risk", "protect"]):
            agent_id = get_active_agent_for_role("Security") or "chelios_001"
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                title="Security Assessment",
                description=f"Security review: {objective}",
                assigned_to=agent_id,
                input_data={"objective": objective, "context": context}
            ))
        
        # Design tasks -> Aurora
        if any(kw in objective_lower for kw in ["design", "ui", "ux", "brand", "creative", "visual"]):
            agent_id = get_active_agent_for_role("Design") or "aurora_001"
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                title="Design Work",
                description=f"Design: {objective}",
                assigned_to=agent_id,
                dependencies=[tasks[-1].task_id] if tasks else [],
                input_data={"objective": objective, "context": context}
            ))
        
        # Sales tasks -> Pulp, Jane, CLOSETER
        if any(kw in objective_lower for kw in ["sales", "revenue", "client", "deal", "lead", "prospect", "close", "convert"]):
            # Use CLOSETER for conversion tasks
            if "close" in objective_lower or "convert" in objective_lower:
                agent_id = "close_001"
            else:
                agent_id = get_active_agent_for_role("Sales") or "pulp_001"
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                title="Sales Activity",
                description=f"Sales: {objective}",
                assigned_to=agent_id,
                input_data={"objective": objective, "context": context}
            ))
        
        # Analysis tasks -> Patricia (coordination level)
        if any(kw in objective_lower for kw in ["analyze", "evaluate", "assess", "review", "validate", "strategy", "plan", "competitive", "market", "position"]):
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                title="Strategic Analysis",
                description=f"Analysis: {objective}",
                assigned_to="patricia_001",  # Patricia does strategic analysis
                dependencies=[t.task_id for t in tasks[-2:]] if len(tasks) >= 2 else [tasks[-1].task_id] if tasks else [],
                input_data={"objective": objective, "context": context}
            ))
        
        # Communications/Front desk -> GREET
        if any(kw in objective_lower for kw in ["call", "schedule", "appointment", "front desk", "reception", "customer service"]):
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                title="Front Desk Coordination",
                description=f"Operations: {objective}",
                assigned_to="greet_001",
                input_data={"objective": objective, "context": context}
            ))
        
        # Final compilation always to Patricia (Chief of Staff)
        if tasks:
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                title="Compile and Finalize",
                description=f"Chief of Staff review for: {objective}",
                assigned_to="patricia_001",
                dependencies=[t.task_id for t in tasks],  # Depends on all previous
                input_data={"objective": objective}
            ))
        
        return tasks
    
    def execute_workflow(self, workflow_id: str) -> bool:
        """
        Execute a planned workflow
        
        This is the main orchestration loop
        """
        if workflow_id not in self.workflows:
            print(f"[APEX Chief] ❌ Workflow {workflow_id} not found")
            return False
        
        workflow = self.workflows[workflow_id]
        workflow.status = WorkflowStatus.RUNNING
        
        print(f"\n[APEX Chief] 🚀 Executing workflow: {workflow_id}")
        print(f"  Tasks: {len(workflow.tasks)}")
        
        # Execute tasks respecting dependencies
        completed_tasks = set()
        failed_tasks = set()
        
        while len(completed_tasks) + len(failed_tasks) < len(workflow.tasks):
            # Find tasks ready to execute (dependencies met)
            ready_tasks = [
                t for t in workflow.tasks 
                if t.status == TaskStatus.PENDING and
                all(dep in completed_tasks for dep in t.dependencies) and
                t.task_id not in failed_tasks
            ]
            
            if not ready_tasks:
                # Check if we're stuck
                if len(completed_tasks) + len(failed_tasks) < len(workflow.tasks):
                    print(f"[APEX Chief] ⚠️  Workflow blocked by dependencies")
                    break
                break
            
            for task in ready_tasks:
                self._execute_task(task, workflow)
                
                if task.status == TaskStatus.COMPLETED:
                    completed_tasks.add(task.task_id)
                elif task.status == TaskStatus.FAILED:
                    failed_tasks.add(task.task_id)
        
        # Check completion
        if len(completed_tasks) == len(workflow.tasks):
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = time.time()
            self._compile_final_result(workflow)
            print(f"\n[APEX Chief] ✅ Workflow {workflow_id} COMPLETED")
            return True
        else:
            workflow.status = WorkflowStatus.FAILED
            print(f"\n[APEX Chief] ❌ Workflow {workflow_id} FAILED")
            print(f"  Completed: {len(completed_tasks)}/{len(workflow.tasks)}")
            print(f"  Failed: {len(failed_tasks)}")
            return False
    
    def _execute_task(self, task: SubTask, workflow: Workflow) -> None:
        """Execute a single task by delegating to AGI Company agent"""
        agent = self.agents.get(task.assigned_to)
        
        if not agent:
            print(f"[APEX Chief] ❌ Agent {task.assigned_to} not found")
            task.status = TaskStatus.FAILED
            return
        
        if agent.status == "INACTIVE":
            print(f"[APEX Chief] ⏳ {agent.name} is INACTIVE, task queued for reactivation")
            task.status = TaskStatus.PENDING
            return
        
        if not agent.assign_task(task.task_id):
            print(f"[APEX Chief] ⏳ {agent.name} is busy, task queued")
            return
        
        task.status = TaskStatus.IN_PROGRESS
        print(f"\n[APEX Chief] 🎯 Task assigned: {task.title} → {agent.name} ({agent.capabilities.get('role', 'Unknown')})")
        
        # Simulate task execution (in production would call actual agent via sandbox)
        time.sleep(0.1)
        
        # Generate simulated output based on agent role
        result = self._simulate_agent_work(agent, task, workflow)
        
        task.output_data = result
        task.status = TaskStatus.COMPLETED
        task.completed_at = time.time()
        agent.complete_task()
        
        print(f"[APEX Chief] ✓ Task completed: {task.title}")
    
    def _simulate_agent_work(self, agent: AGIAgent, task: SubTask,
                            workflow: Workflow) -> Dict:
        """Simulate AGI Company agent work"""
        
        templates = {
            # C-Suite
            "Patricia": {
                "summary": f"Chief of Staff coordination complete for: {task.description}",
                "workflow_id": workflow.workflow_id,
                "tasks_coordinated": len(workflow.tasks),
                "next_actions": ["Review with Captain", "Delegate to team"],
                "confidence": 0.95
            },
            "Chelios": {
                "security_audit": f"Security assessment complete for: {task.description}",
                "threats_identified": 0,
                "recommendations": ["Maintain current posture", "Review quarterly"],
                "compliance_status": "PASS"
            },
            "Forge": {
                "implementation": f"Technical solution deployed for: {task.description}",
                "architecture": "Scalable cloud architecture",
                "code_snippet": "# Production-ready code",
                "tests_passed": True,
                "deployment_status": "LIVE"
            },
            "Aurora": {
                "design": f"Design system delivered for: {task.description}",
                "assets": ["Logo variants", "UI kit", "Brand guidelines"],
                "user_feedback": "Positive"
            },
            "Jordan": {
                "sales_ops": f"Sales operations analysis for: {task.description}",
                "pipeline_status": "Healthy",
                "forecast": "On track for Q3",
                "recommendations": ["Increase outreach", "Optimize conversion"]
            },
            # Directors (when reactivated)
            "Sentinel": {
                "security_ops": f"Security operations complete for: {task.description}",
                "incidents": 0,
                "monitoring": "24/7 active",
                "status": "SECURE"
            },
            "Dusty": {
                "research": f"Market research complete for: {task.description}",
                "competitors_analyzed": 7,
                "trends_identified": ["Trend A", "Trend B", "Trend C"],
                "strategic_insights": "Market opportunity confirmed"
            },
            "Pulp": {
                "sales_strategy": f"Sales strategy developed for: {task.description}",
                "revenue_projected": "$50K Q3",
                "team_readiness": "Ready to execute",
                "confidence": 0.90
            },
            "Jane": {
                "enterprise_deal": f"Enterprise outreach complete for: {task.description}",
                "meetings_scheduled": 3,
                "pipeline_value": "$75K",
                "next_steps": "Demo scheduled"
            },
            "GREET": {
                "front_desk": f"Call handling complete for: {task.description}",
                "calls_handled": 12,
                "appointments_scheduled": 4,
                "customer_satisfaction": 5.0
            },
            "CLOSETER": {
                "conversion": f"Deal closed for: {task.description}",
                "deal_value": "$15,000",
                "conversion_rate": "85%",
                "time_to_close": "2 days"
            }
        }
        
        return templates.get(agent.name, {"result": f"Work completed by {agent.name}"})
    
    def _compile_final_result(self, workflow: Workflow) -> None:
        """Compile all task outputs into final deliverable"""
        results = []
        
        for task in workflow.tasks:
            if task.status == TaskStatus.COMPLETED:
                agent = self.crew.get(task.assigned_to)
                results.append(f"\n## {task.title} (by {agent.name if agent else 'Unknown'})\n")
                results.append(json.dumps(task.output_data, indent=2))
        
        workflow.final_result = "\n".join(results)
        
        print(f"\n[APEX Chief] 📄 Final result compiled for {workflow.workflow_id}")
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict]:
        """Get current status of a workflow"""
        if workflow_id not in self.workflows:
            return None
        
        workflow = self.workflows[workflow_id]
        
        return {
            "workflow_id": workflow_id,
            "objective": workflow.objective,
            "status": workflow.status.name,
            "progress": {
                "total": len(workflow.tasks),
                "completed": sum(1 for t in workflow.tasks if t.status == TaskStatus.COMPLETED),
                "in_progress": sum(1 for t in workflow.tasks if t.status == TaskStatus.IN_PROGRESS),
                "pending": sum(1 for t in workflow.tasks if t.status == TaskStatus.PENDING),
                "failed": sum(1 for t in workflow.tasks if t.status == TaskStatus.FAILED)
            },
            "tasks": [
                {
                    "id": t.task_id,
                    "title": t.title,
                    "assigned_to": self.crew.get(t.assigned_to, {}).name if t.assigned_to in self.crew else t.assigned_to,
                    "status": t.status.name
                }
                for t in workflow.tasks
            ]
        }
    
    def get_company_status(self) -> Dict:
        """Get status of AGI Company agents"""
        active_agents = [a for a in self.agents.values() if a.status == "ACTIVE"]
        inactive_agents = [a for a in self.agents.values() if a.status == "INACTIVE"]
        
        return {
            "chief_of_staff": self.name,
            "role": self.role,
            "department": self.department,
            "total_agents": len(self.agents),
            "active": len(active_agents),
            "inactive": len(inactive_agents),
            "c_suite": [
                {
                    "id": a.agent_id,
                    "name": a.name,
                    "role": a.capabilities.get("role", "Unknown"),
                    "department": a.capabilities.get("department", "Unknown"),
                    "status": a.status,
                    "busy": a.current_task is not None,
                    "completed_tasks": len(a.task_history)
                }
                for a in active_agents
            ],
            "directors": [
                {
                    "id": a.agent_id,
                    "name": a.name,
                    "role": a.capabilities.get("role", "Unknown"),
                    "reports_to": a.capabilities.get("reports_to", "Unknown"),
                    "status": a.status,
                    "reactivation_required": a.status == "INACTIVE"
                }
                for a in inactive_agents
            ]
        }
    
    def query_crew(self, query: str) -> str:
        """
        Natural language interface to Chief of Staff
        
        Examples:
        - "Research the latest POS trends"
        - "Create a proposal for ACME Corp"
        - "Analyze our Q3 sales data"
        """
        print(f"\n[APEX Chief] 💬 Received query: {query}")
        
        # Create workflow from natural language
        workflow_id = self.receive_objective(
            objective=query,
            initiator="user_query"
        )
        
        # Execute
        success = self.execute_workflow(workflow_id)
        
        if success:
            workflow = self.workflows[workflow_id]
            return f"Workflow {workflow_id} completed.\n\nResult:\n{workflow.final_result[:500]}..."
        else:
            return f"Workflow {workflow_id} encountered issues. Check status for details."


# Test function
def test_chief_of_staff():
    """Test the Chief of Staff system"""
    print("\n" + "=" * 70)
    print("  👔 APEX CHIEF OF STAFF - TEST")
    print("=" * 70)
    
    chief = APEXChiefOfStaff()
    
    # Test 1: Simple research task
    print("\n[TEST 1] Simple research task")
    wf_id = chief.receive_objective(
        "Research the latest POS terminal trends for 2026",
        initiator="Captain"
    )
    chief.execute_workflow(wf_id)
    
    status = chief.get_workflow_status(wf_id)
    print(f"\n  Status: {status['status']}")
    print(f"  Progress: {status['progress']}")
    
    # Test 2: Complex multi-step task
    print("\n" + "=" * 70)
    print("[TEST 2] Complex proposal creation")
    wf_id2 = chief.receive_objective(
        "Create a comprehensive sales proposal for ACME Corp including market analysis, technical specs, and pricing strategy",
        initiator="Captain"
    )
    chief.execute_workflow(wf_id2)
    
    status2 = chief.get_workflow_status(wf_id2)
    print(f"\n  Status: {status2['status']}")
    print(f"  Tasks: {len(status2['tasks'])}")
    
    # Test 3: Crew status
    print("\n" + "=" * 70)
    print("[TEST 3] Crew status")
    crew_status = chief.get_crew_status()
    print(f"  Chief: {crew_status['chief_of_staff']}")
    print(f"  Crew size: {crew_status['crew_count']}")
    for member in crew_status['members']:
        print(f"    {member['name']} ({member['role']}) - {member['status']}")
    
    print("\n" + "=" * 70)
    print("  ✅ APEX Chief of Staff Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_chief_of_staff()
