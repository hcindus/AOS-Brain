"""
Agent adapters for the ternary brain.

Provides Miles (sales), Mortimer (research), and Mini (minimal) agents
that connect to the brain server via HTTP or direct integration.
"""

from agents.agent_adapter import (
    BrainClient,
    AgentAdapter,
    MilesAdapter,
    MortimerAdapter,
    MiniAdapter,
    DirectBrainAdapter,
)

__all__ = [
    "BrainClient",
    "AgentAdapter", 
    "MilesAdapter",
    "MortimerAdapter",
    "MiniAdapter",
    "DirectBrainAdapter",
]
