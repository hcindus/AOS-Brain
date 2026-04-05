"""
Dark Factory Scheduler System
============================
AGI Connect Integrated Factory Management

36 Workstations | 36 Agents | Full Integration
"""

__version__ = "2.0.0"
__author__ = "Jordan (Project Manager)"

from .core.scheduler import DarkFactoryScheduler
from .core.job_queue import PersistentJobQueue
from .core.agent_optimizer import AgentStationOptimizer
from .connect.agi_connect import AGIConnectIntegration
from .metrics.dashboard import MetricsDashboard
from .maintenance.predictor import MaintenancePredictor

__all__ = [
    "DarkFactoryScheduler",
    "PersistentJobQueue",
    "AgentStationOptimizer",
    "AGIConnectIntegration",
    "MetricsDashboard",
    "MaintenancePredictor",
]