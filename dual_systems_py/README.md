# ⚡ DUAL SYSTEMS ⚡
## Neural Warfare in the Twin Suns

A polished 3D space combat game featuring neural network AI enemies, dual solar systems with gravity physics, and retro-futuristic Flash Gordon aesthetics.

![Dual Systems](screenshot.png)

## Features

### Core Gameplay
- **3D Tetrahedron Ships**: Flash Gordon style wireframe fighters with glowing engine trails
- **Dual Solar Systems**: Navigate between two suns with realistic gravity wells
- **Neural AI Enemies**: OODA Loop (Observe-Orient-Decide-Act) decision making
- **Multiple View Modes**: First-person, third-person, and top-down perspectives
- **Weapon Systems**: Rapid-fire lasers with faction-colored projectiles
- **Shield Management**: Regenerating shields and power systems
- **Wave System**: Progressive difficulty with increasing enemy count

### Factions
- 🔵 **Blue (Player)** - Allied Forces
- 🔴 **Red Legion** - Hostile forces
- 🟢 **Green Horde** - Hostile forces  
- 🟣 **Purple Dynasty** - Hostile forces

### Physics
- **Gravity Physics**: Ships are affected by dual solar systems
- **Momentum-Based Movement**: Inertia-based flight model
- **Boost System**: Speed boost with cooldown

### Visual Effects
- Particle explosions
- Engine trail effects
- Glowing ship materials
- Procedural debris fields
- Starfield background
- Fog-based depth cues

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenGL 3.3 compatible graphics card

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install pygame moderngl PyGLM numpy
```

## Running the Game

```bash
python game.py
```

## Controls

| Key | Action |
|-----|--------|
| **W / Up** | Thrust Forward |
| **S / Down** | Thrust Backward |
| **A / Left** | Steer Left |
| **D / Right** | Steer Right |
| **Q** | Roll Down |
| **E** | Roll Up |
| **SHIFT** | Boost Speed |
| **SPACE** | Fire Weapons |
| **1** | Third-Person View |
| **2** | First-Person View |
| **3** | Top-Down View |
| **P** | Pause Game |
| **ESC** | Quit |
| **ENTER** | Start Game |
| **R** | Restart (Game Over) |

## How to Play

1. Launch the game
2. Press **ENTER** to start
3. Use WASD to thrust and steer your ship
4. The ship automatically turns into the movement direction (momentum-based)
5. Press **SPACE** to fire at enemies
6. Avoid getting hit - shields regenerate slowly
7. Watch out for solar system gravity wells
8. Survive waves of AI enemies
9. Press **1/2/3** to change camera views

## AI Behavior

Enemies use a neural network with OODA Loop decision making:

- **OBSERVE**: Detect player distance, angle, health, ally positions
- **ORIENT**: Calculate threat level and opportunity
- **DECIDE**: Neural network selects action (attack/evade/maneuver/retreat)
- **ACT**: Execute chosen behavior

The AI adapts based on health, distance, and tactical position.

## Technical Details

### Architecture
- **Renderer**: ModernGL for OpenGL 3.3+ rendering
- **Window**: Pygame for windowing and input
- **Math**: GLM (OpenGL Mathematics) for vectors and matrices
- **Audio**: Pygame mixer for procedural sound effects

### Graphics Pipeline
- Vertex/Fragment shaders with GLSL
- Phong-like lighting model
- Particle systems for effects
- Fog for depth perception
- Additive blending for glow effects

## File Structure

```
dual_systems_py/
├── game.py              # Main game (OpenGL/ModernGL version)
├── game_simple.py       # Simple version (Software rendering, no OpenGL required)
├── requirements.txt     # Python dependencies
└── README.md           # This file

## Two Python Versions

### 1. Full Version (game.py)
- **Requirements**: OpenGL 3.3+ compatible GPU
- **Graphics**: ModernGL for hardware-accelerated 3D
- **Features**: Full particle effects, shadows, advanced shaders
- **Best for**: Desktop PCs with dedicated graphics

### 2. Simple Version (game_simple.py)
- **Requirements**: None (pure pygame)
- **Graphics**: Software 3D rendering
- **Features**: Compatible with any system that runs Python
- **Best for**: Older hardware, VMs, systems without GPU
```

## Troubleshooting

### "No OpenGL context" error
- Ensure your graphics drivers are up to date
- Try running with software rendering: `LIBGL_ALWAYS_SOFTWARE=1 python game.py`

### Sound not working
- Check pygame mixer initialization
- Verify audio output is selected

### Low FPS
- Reduce resolution (edit SCREEN_WIDTH/HEIGHT in game.py)
- Disable particles (reduce particle count)
- Close other applications

## Future Enhancements

- [ ] Multiplayer support
- [ ] More ship types
- [ ] Mission system
- [ ] Upgrade system
- [ ] Save/load functionality
- [ ] Audio improvements
- [ ] Mobile touch controls

## License

MIT License - Feel free to use, modify, and distribute!

## Credits

Inspired by classic space shooters and Flash Gordon aesthetics.

---

**Fly safe, pilot! ⚡**
