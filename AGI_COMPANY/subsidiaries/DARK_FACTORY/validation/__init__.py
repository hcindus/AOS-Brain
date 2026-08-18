"""Dark Factory validation package — blind hold-out validation."""
from .hold_out_scenarios import HoldOutValidator, validate_hold_out

__all__ = ["HoldOutValidator", "validate_hold_out"]
