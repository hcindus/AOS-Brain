"""
Tracray Organizer Module
Self-organizing semantic map.
"""

from collections import defaultdict

# Global state
coactivation = defaultdict(lambda: defaultdict(int))
attract_lr = 0.05
repel_lr = 0.01

class TRACRAY_ORGANIZER:
    """Organizer state container"""
    pass


def register_activation(active_concepts, valence=0.0):
    """
    Register that concepts co-activated together.
    
    Args:
        active_concepts: List of concept names
        valence: Emotional valence (-1.0 to 1.0)
    """
    for i in range(len(active_concepts)):
        for j in range(i + 1, len(active_concepts)):
            a, b = active_concepts[i], active_concepts[j]
            boost = 1 + int(abs(valence) * 2)
            coactivation[a][b] += boost
            coactivation[b][a] += boost


def self_organize_tracray(TRACRAY, steps=1):
    """
    Move concepts based on co-activation patterns.
    
    Args:
        TRACRAY: Tracray lexicon dict
        steps: Number of optimization steps
    """
    global attract_lr, repel_lr
    
    for _ in range(steps):
        for name, spec in TRACRAY.get("concepts", {}).items():
            if "coord" not in spec:
                continue
                
            x, y, z = spec["coord"]
            fx = fy = fz = 0.0
            
            # Attraction
            for other, count in coactivation[name].items():
                if count <= 0 or other not in TRACRAY.get("concepts", {}):
                    continue
                ox, oy, oz = TRACRAY["concepts"][other]["coord"]
                dx, dy, dz = ox - x, oy - y, oz - z
                dist = max(0.1, (dx*dx + dy*dy + dz*dz) ** 0.5)
                strength = attract_lr * (count / (1.0 + dist))
                fx += strength * dx / dist
                fy += strength * dy / dist
                fz += strength * dz / dist
                
            # Repulsion
            for other, ospec in TRACRAY.get("concepts", {}).items():
                if other == name or "coord" not in ospec:
                    continue
                ox, oy, oz = ospec["coord"]
                dx, dy, dz = ox - x, oy - y, oz - z
                dist2 = dx*dx + dy*dy + dz*dz
                if dist2 < 1.0:
                    strength = repel_lr / max(0.1, dist2)
                    fx -= strength * dx
                    fy -= strength * dy
                    fz -= strength * dz
                    
            spec["coord"] = (x + fx, y + fy, z + fz)
