"""Configuration for V3 Cosmic Engine."""
from __future__ import annotations

# Random seed for reproducibility
SEED = 42

# Simulation limits
MAX_TICKS = 1000
TICK_DELAY = 0.1  # seconds between ticks

# Persistence
SAVE_HISTORY = True
HISTORY_FILE = "cosmic_history.json"

# Cosmic event probability (chance per tick)
COSMIC_EVENT_CHANCE = 0.012  # ~1.2% per tick

# Dream system
DREAM_COSMIC_CHANCE = 0.15  # 15% chance of cosmic omen in dreams
DREAM_INTENSITY_DECAY = 0.92  # Dream intensity decay per tick

# Initial agents
INITIAL_AGENTS = ["Aurora", "Sol", "Nyx"]

# Default archetypes distribution
DEFAULT_ARCHETYPES = ["warrior", "mystic", "builder", "wanderer"]

# Era configuration
ERA_MIN_LENGTH = 50  # ticks
ERA_MAX_LENGTH = 200  # ticks

# UI settings
DASHBOARD_REFRESH_RATE = 1  # ticks between dashboard updates
VISUALIZATION_ENABLED = True

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "cosmic_engine.log"
