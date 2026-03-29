"""
Minecraft Bridge Module
Connects AOS Brain to Minecraft for embodied learning.

The brain plays Minecraft, learns from experience, and watches itself grow.
"""

from .observer import MinecraftObserver
from .actor import MinecraftActor
from .translator import ConceptTranslator
# from .integration import MinecraftBrainIntegration  # Deferred to avoid circular import

__all__ = [
    'MinecraftObserver',
    'MinecraftActor', 
    'ConceptTranslator',
    # 'MinecraftBrainIntegration',
]
