# DaVerse Game Asset Pipeline Workflow

## Overview
This document describes the complete workflow for creating game-ready assets for DaVerse using Blender.

## Directory Structure
```
/workspace/aocros/games/assets/blender/
├── scripts/              # Python automation scripts
│   ├── export_game_assets.py       # Main export pipeline
│   ├── create_modular_character.py # Character generator
│   └── create_game_props.py        # Prop library generator
├── templates/            # Starter .blend files
├── exports/              # Output directory
│   ├── fbx/             # FBX exports (Unity/Unreal)
│   ├── gltf/            # glTF exports (WebGL/mobile)
│   └── obj/             # OBJ exports (compatibility)
├── characters/           # Character assets
├── props/               # Prop assets
├── environments/        # Environment assets
└── materials/           # Shared material libraries
```

## Quick Start

### 1. Generate Base Assets
```bash
# Run Blender with character generator
blender --python scripts/create_modular_character.py

# Run Blender with prop generator
blender --python scripts/create_game_props.py
```

### 2. Export Assets
```python
# In Blender Python console
import sys
sys.path.append('/root/.openclaw/workspace/aocros/games/assets/blender/scripts')
from export_game_assets import export_active_object
export_active_object("MyAsset", ['unity', 'unreal'])
```

## Asset Standards

### Naming Convention
```
CH_ = Character
PR_ = Prop
EN_ = Environment
MAT_ = Material
T_ = Texture
```

### File Naming Pattern
```
{TYPE}_{CATEGORY}_{NAME}_{VERSION}.{EXT}
Example: PR_Crate_Wood_01_v01.blend
```

### Export Checklist
- [ ] Scale applied (Ctrl+A → Scale)
- [ ] Origin at appropriate pivot point
- [ ] Modifiers applied if static mesh
- [ ] Materials assigned
- [ ] UV unwrapped (if textured)
- [ ] Triangulated for export (optional)
- [ ] Naming conventions followed

## Pipeline Steps

### Character Creation
1. Run `create_modular_character.py` to generate base mesh
2. Sculpt/retopo in sculpt mode if needed
3. UV unwrap with consistent texel density
4. Rig with generated armature
5. Paint vertex weights
6. Export using `export_game_assets.py`

### Prop Creation
1. Run `create_game_props.py` for base shapes
2. Customize in edit mode
3. Apply materials from library
4. Set pivot/origin
5. Export to appropriate format

### Environment Creation
1. Use modular tile system (1m, 2m, 4m grid)
2. Design for repetition and variation
3. Create trim sheets for texture efficiency
4. Export tile sets as separate FBX files

## Engine Integration

### Unity Import
1. Drag FBX into Assets folder
2. Set import settings:
   - Scale: 1
   - Mesh Compression: Medium
   - Optimize Mesh: On
   - Import Materials: Yes
   - Material Naming: From Model's Material

### Unreal Import
1. Import FBX to Content Browser
2. Set import settings:
   - Convert Scene Unit: True
   - Override Full Name: True
   - Import Uniform Scale: 1.0
   - Convert Scene: True

## Automation

### Batch Export
```python
from export_game_assets import batch_export_from_collection
batch_export_from_collection("Props", "PR_")
batch_export_from_collection("Characters", "CH_")
```

### Headless Export
```bash
blender -b file.blend --python scripts/export_game_assets.py
```

## Material Library

### Available Materials
- `MAT_Base_Skin` - Character skin
- `MAT_Wood_Crate` - Wood surfaces
- `MAT_Metal_Barrel` - Industrial metal
- `MAT_Rock_Gray` - Natural rock
- `MAT_Floor_Industrial` - Floor tiles
- `MAT_Wall_Metal` - Wall panels
- `MAT_Crate_SciFi` - Sci-fi containers

### Creating New Materials
1. Use Principled BSDF
2. Follow PBR workflow (Metallic/Roughness)
3. Keep texture sizes power of 2
4. Save to materials.blend library

## Performance Guidelines

### Polygon Budgets
- Hero Character: 5k-8k triangles
- NPC Character: 2k-4k triangles
- Small Prop: 100-300 triangles
- Large Prop: 500-1k triangles
- Environment Tile: 100-500 triangles

### LOD Strategy
- Create LOD0 (full detail)
- Decimate 50% for LOD1
- Decimate 75% for LOD2
- Export separate meshes or use engine LOD system

### Texture Optimization
- Use texture atlases for props
- Max 2048x2048 for hero assets
- 512x512 or 1024x1024 for props
- Compress to DXT1/BC1 (opaque) or DXT5/BC3 (alpha)

## Troubleshooting

### Common Issues

**Scale wrong in engine:**
- Check "Apply Transform" in export settings
- Ensure scale is applied in Blender (Ctrl+A)

**Missing textures:**
- Pack textures in Blender before export
- Or export to same directory as .blend

**Normals flipped:**
- Check "Recalculate Outside" in Edit mode
- Verify in Viewport Overlays > Face Orientation

**Armature not importing:**
- Add Armature modifier before export
- Enable "Add Leaf Bones" in FBX export

## Best Practices

1. **Work Modular** - Build from reusable pieces
2. **Name Everything** - Clear, consistent naming
3. **Test Early** - Import to engine frequently
4. **Version Control** - Save iterations as _v01, _v02
5. **Document** - Update this file with project-specific notes
