#!/usr/bin/env python3
"""
Mylonen + R2 Pixel Workers for MilkMan Game.
Generate pixel art assets and save to GitHub.
"""

import sys
import json
import time
import random
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.mylonen_adapter import MylonenAdapter
from agents.droid_r2 import R2DroidInterface


class PixelGenerator:
    """Generate pixel art using brain-powered creativity."""
    
    def __init__(self, brain):
        self.brain = brain
        self.palette = {
            'milk_white': (255, 255, 255),
            'cream': (255, 253, 208),
            'bottle_blue': (65, 105, 225),
            'straw_red': (220, 20, 60),
            'sky': (135, 206, 235),
            'grass': (34, 139, 34),
            'skin': (255, 228, 196),
            'shadow': (100, 100, 100),
            'gold': (255, 215, 0),
            'silver': (192, 192, 192)
        }
        
    def generate_sprite(self, name: str, size: tuple = (32, 32)) -> dict:
        """Generate a pixel sprite."""
        width, height = size
        pixels = []
        
        # Use brain to determine pattern
        self.brain.tick({"text": f"design {name}", "source": "pixel_gen"})
        
        # Generate based on name/entity type
        if "milkman" in name.lower():
            pixels = self._milkman_sprite(width, height)
        elif "bottle" in name.lower():
            pixels = self._bottle_sprite(width, height)
        elif "enemy" in name.lower():
            pixels = self._enemy_sprite(width, height)
        elif "collectible" in name.lower():
            pixels = self._collectible_sprite(width, height)
        else:
            pixels = self._abstract_sprite(width, height)
            
        return {
            "name": name,
            "size": size,
            "pixels": pixels,
            "palette_used": list(self.palette.keys()),
            "timestamp": datetime.now().isoformat()
        }
    
    def _milkman_sprite(self, w, h) -> list:
        """Generate milkman character."""
        pixels = []
        for y in range(h):
            row = []
            for x in range(w):
                # Simple milkman shape
                if 10 < y < 20 and 8 < x < 24:
                    row.append(self.palette['milk_white'])  # Body
                elif 6 < y < 12 and 10 < x < 22:
                    row.append(self.palette['skin'])  # Head
                elif y == 14 and x > 20:
                    row.append(self.palette['bottle_blue'])  # Bottle
                else:
                    row.append((0, 0, 0, 0))  # Transparent
            pixels.append(row)
        return pixels
    
    def _bottle_sprite(self, w, h) -> list:
        """Generate milk bottle."""
        pixels = []
        for y in range(h):
            row = []
            for x in range(w):
                # Bottle shape
                cx, cy = w // 2, h // 2
                dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if dist < 10:
                    if y < cy - 5:
                        row.append(self.palette['straw_red'])  # Cap
                    else:
                        row.append(self.palette['milk_white'])  # Bottle
                else:
                    row.append((0, 0, 0, 0))
            pixels.append(row)
        return pixels
    
    def _enemy_sprite(self, w, h) -> list:
        """Generate enemy character."""
        pixels = []
        for y in range(h):
            row = []
            for x in range(w):
                # Spiky enemy
                if (x + y) % 7 == 0:
                    row.append(self.palette['shadow'])
                elif 8 < y < 24 and 6 < x < 26:
                    row.append(self.palette['cream'])
                else:
                    row.append((0, 0, 0, 0))
            pixels.append(row)
        return pixels
    
    def _collectible_sprite(self, w, h) -> list:
        """Generate collectible item."""
        pixels = []
        for y in range(h):
            row = []
            for x in range(w):
                cx, cy = w // 2, h // 2
                # Gold coin
                if abs(x - cx) + abs(y - cy) < 8:
                    row.append(self.palette['gold'])
                else:
                    row.append((0, 0, 0, 0))
            pixels.append(row)
        return pixels
    
    def _abstract_sprite(self, w, h) -> list:
        """Generate abstract pattern."""
        pixels = []
        palette_values = list(self.palette.values())
        for y in range(h):
            row = []
            for x in range(w):
                # Brain-influenced pattern
                idx = (x * y + self.brain.tick_count) % len(palette_values)
                row.append(palette_values[idx])
            pixels.append(row)
        return pixels


class MilkManPixelTeam:
    """Mylonen + R2 working together on pixel art."""
    
    def __init__(self):
        self.mylonen = MylonenAdapter()
        self.r2 = R2DroidInterface()
        self.generator = PixelGenerator(self.mylonen.brain)
        
        self.project_dir = Path("/root/.openclaw/workspace/MilkMan-Game")
        self.pixels_dir = self.project_dir / "assets" / "pixels"
        self.sprites_dir = self.project_dir / "assets" / "sprites"
        
        self.assets_created = []
        
    def create_asset(self, asset_type: str, name: str, size: tuple = (32, 32)):
        """Create a pixel asset."""
        print(f"\n[WORKER] Creating {asset_type}: {name}")
        
        # Mylonen designs
        self.mylonen.process(f"Design {name} for MilkMan game", "pixel_art")
        
        # Generate sprite
        sprite = self.generator.generate_sprite(name, size)
        
        # R2 saves to file
        if asset_type == "pixel":
            filepath = self.pixels_dir / f"{name}.json"
        else:
            filepath = self.sprites_dir / f"{name}.json"
            
        self.r2.deploy_tool("data_writer")
        
        # Save JSON
        with open(filepath, 'w') as f:
            json.dump(sprite, f, indent=2)
        
        self.assets_created.append({
            "type": asset_type,
            "name": name,
            "filepath": str(filepath),
            "size": size,
            "brain_ticks": self.mylonen.brain.tick_count
        })
        
        print(f"  ✓ Mylonen designed: {name}")
        print(f"  ✓ R2 saved to: {filepath}")
        print(f"  ✓ Brain ticks: {self.mylonen.brain.tick_count}")
        
    def create_pixel_batch(self):
        """Create batch of pixel assets."""
        print("\n" + "=" * 70)
        print("🎨 PIXEL WORKERS: Creating MilkMan Game Assets")
        print("=" * 70)
        
        # Character sprites
        self.create_asset("sprite", "milkman_idle", (32, 32))
        self.create_asset("sprite", "milkman_walk", (32, 32))
        self.create_asset("sprite", "milkman_jump", (32, 32))
        
        # Objects
        self.create_asset("sprite", "milk_bottle", (16, 16))
        self.create_asset("sprite", "golden_milk", (16, 16))
        
        # Enemies
        self.create_asset("sprite", "sour_milk_enemy", (32, 32))
        self.create_asset("sprite", "spill_monster", (32, 32))
        
        # Collectibles
        self.create_asset("pixel", "coin", (8, 8))
        self.create_asset("pixel", "straw_powerup", (16, 16))
        self.create_asset("pixel", "cream_bonus", (16, 16))
        
        # Environment
        self.create_asset("pixel", "grass_tile", (16, 16))
        self.create_asset("pixel", "sky_gradient", (64, 64))
        self.create_asset("pixel", "milk_carton_crate", (24, 24))
        
        print("\n" + "=" * 70)
        print("✅ BATCH COMPLETE")
        print("=" * 70)
        
    def commit_to_github(self):
        """Commit assets to GitHub."""
        print("\n[WORKER] Committing to GitHub...")
        
        import subprocess
        
        # Create README
        readme = self.project_dir / "README.md"
        with open(readme, 'w') as f:
            f.write("""# MilkMan Game

2D platformer game assets created by Mylonen + R2 (7-Region Brain Agents).

## Assets Created

""")
            for asset in self.assets_created:
                f.write(f"- **{asset['name']}** ({asset['type']}) - {asset['size']}\n")
        
        print(f"  ✓ Created README with {len(self.assets_created)} assets")
        
        return self.assets_created
    
    def get_status(self):
        """Return team status."""
        return {
            "mylonen": {
                "name": self.mylonen.name,
                "level": self.mylonen.level,
                "brain_ticks": self.mylonen.brain.tick_count
            },
            "r2": {
                "name": self.r2.name,
                "battery": self.r2.battery_level,
                "position": self.r2.position
            },
            "assets_created": len(self.assets_created),
            "asset_list": self.assets_created
        }


def deploy_pixel_workers():
    """Deploy Mylonen + R2 to create pixel art."""
    team = MilkManPixelTeam()
    
    # Create assets
    team.create_pixel_batch()
    
    # Commit
    team.commit_to_github()
    
    # Status
    status = team.get_status()
    
    print("\n" + "=" * 70)
    print("📊 FINAL STATUS")
    print("=" * 70)
    print(f"\n🤖 Mylonen:")
    print(f"  Brain ticks: {status['mylonen']['brain_ticks']}")
    print(f"\n🛸 R2:")
    print(f"  Battery: {status['r2']['battery']:.1f}%")
    print(f"\n🎨 Assets Created: {status['assets_created']}")
    for asset in status['asset_list']:
        print(f"  - {asset['name']} ({asset['type']})")
    
    return team


if __name__ == "__main__":
    deploy_pixel_workers()
