"""History persistence for V3 Cosmic Engine."""
from __future__ import annotations

import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path

from config import HISTORY_FILE


class History:
    """Manages world history persistence."""
    
    def __init__(self, world: Any) -> None:
        self.world = world
        self.file_path = Path(HISTORY_FILE)
        self.snapshots: List[Dict[str, Any]] = []
    
    def load_if_exists(self) -> bool:
        """Load history from file if it exists."""
        if not self.file_path.exists():
            return False
        
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.snapshots = data.get('snapshots', [])
                
                # Restore world state from latest snapshot
                if self.snapshots:
                    latest = self.snapshots[-1]
                    self._restore_world_state(latest)
                
                return True
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load history: {e}")
            return False
    
    def save(self) -> None:
        """Save current world state to history file."""
        snapshot = self._create_snapshot()
        self.snapshots.append(snapshot)
        
        try:
            with open(self.file_path, 'w') as f:
                json.dump({
                    'snapshots': self.snapshots,
                    'meta': {
                        'total_snapshots': len(self.snapshots),
                        'last_turn': self.world.turn if hasattr(self.world, 'turn') else 0,
                    }
                }, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save history: {e}")
    
    def _create_snapshot(self) -> Dict[str, Any]:
        """Create a snapshot of the current world state."""
        return {
            "turn": self.world.turn if hasattr(self.world, 'turn') else 0,
            "era": getattr(self.world, 'era', 'unknown'),
            "state": self.world.to_dict() if hasattr(self.world, 'to_dict') else {},
            "timestamp": self._get_timestamp(),
        }
    
    def _restore_world_state(self, snapshot: Dict[str, Any]) -> None:
        """Restore world state from a snapshot."""
        if 'state' in snapshot:
            state = snapshot['state']
            if hasattr(self.world, 'turn'):
                self.world.turn = state.get('turn', 0)
            if hasattr(self.world, 'era'):
                self.world.era = state.get('era', 'dawn')
            if hasattr(self.world, 'myth_pool'):
                self.world.myth_pool = state.get('myths', [])
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the history."""
        return {
            "snapshots": len(self.snapshots),
            "file_path": str(self.file_path),
            "file_exists": self.file_path.exists(),
        }
