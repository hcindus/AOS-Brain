# COBRA Robot Version Index

## Version History

### v1.0.0 - 2026-03-29 (Current)
**Codename:** SNAKE_EYE
**Status:** Production Ready

#### Deliverables
- `bom_generator.py` v1.0.0 - Complete BOM with 46 parts, $1,089.18 unit cost
- `assembly_animator.py` v1.0.0 - 20-step interactive build guide
- `configurator.html` v1.0.0 - Interactive 3D web configurator
- `grip_control/` v1.0.0 - Force-sensing grip control system

#### Hardware Specs
- 25 vertebrae (7 cervical, 12 thoracic, 6 lumbar)
- 52 MG90S servos (50 + 2 base)
- Raspberry Pi 5 + AI HAT (13 TOPS)
- 3S2P 18650 battery (21Ah)
- 6-axis IMU balance system
- Force-sensitive grip (egg-capable)

#### Software
- Python 3.11+ control system
- Arduino Nano real-time controller
- ROS 2 Humble compatible
- WebRTC video streaming

---

## Semantic Versioning

- **MAJOR:** Breaking hardware changes (new spine design)
- **MINOR:** Feature additions (new sensors, software features)
- **PATCH:** Bug fixes, documentation updates

## Tags
- `stable` - Current production version
- `dev` - Development branch
- `v1.0.0` - This release

## Checksums
```
bom_generator.py:        sha256:pending
assembly_animator.py:    sha256:pending
configurator.html:       sha256:pending
grip_control/:           sha256:pending
```
