"""
Learning Package for AOS Brain
Integrates growth laws into main brain loop.
"""

from .plasticity import step_sheet_with_plasticity
from .tracray_organizer import (
    register_activation, 
    self_organize_tracray,
    TRACRAY_ORGANIZER
)
from .reward import apply_reward_to_sheet, apply_reward_to_tracray, consolidate_memory
from .memory_palace_opt import optimize_memory_palace
from .development import BrainDevelopment
from .curiosity import CuriosityAgent, register_concept_use

__all__ = [
    'step_sheet_with_plasticity',
    'register_activation',
    'self_organize_tracray',
    'apply_reward_to_sheet',
    'apply_reward_to_tracray',
    'consolidate_memory',
    'optimize_memory_palace',
    'BrainDevelopment',
    'CuriosityAgent',
    'register_concept_use',
]
