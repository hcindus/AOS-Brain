# Game-Ready Asset Creation Guide

## DaVerse Asset Standards

### Polycount Targets
| Asset Type | Low Poly | Mid Poly | High Poly |
|------------|----------|----------|-----------|
| Hero Character | 5,000-8,000 | 15,000-25,000 | 50,000+ |
| NPC Character | 2,000-4,000 | 8,000-12,000 | 20,000+ |
| Props (Large) | 500-1,000 | 2,000-4,000 | 8,000+ |
| Props (Small) | 100-300 | 500-1,000 | 2,000+ |
| Environment Tiles | 100-500 | 500-1,500 | 3,000+ |

### Topology Rules
1. **Quads First**: Model with quads, triangles only where necessary
2. **Even Distribution**: Avoid dense areas next to sparse areas
3. **Edge Flow**: Follow natural deformation lines for characters
4. **Poles**: Minimize 5+ edge poles; hide them in non-visible areas
5. **Non-Manifold**: Never export with non-manifold geometry

### UV Mapping Standards
- **Texel Density**: Consistent 512px per meter for stylized, 1024px for realistic
- **Padding**: 2-4px between UV islands
- **Orientation**: Align UVs to world axes when possible
- **Channel 2**: Lightmap UVs (unique, no overlaps) for Unity/Unreal

### Scale Standards
- **Unit Scale**: 1 Blender unit = 1 meter
- **Character Height**: 1.8m average (Blender units)
- **Prop Scale**: Real-world proportions
- **Grid Snapping**: Work on 0.1m or 0.5m grid for modularity

### Material Guidelines
- **PBR Workflow**: Metallic/Roughness
- **Texture Sizes**: Power of 2 (512, 1024, 2048)
- **Channels**: BaseColor, Normal, Metallic, Roughness, AO, Emission
- **Atlas Strategy**: Props share materials when possible

### Naming Conventions
```
Characters: CH_Hero_01_v01.blend
Props:      PR_Crate_Wood_01_v01.blend
Environments: EN_Floor_Industrial_01_v01.blend
Materials:  MAT_Metal_Rusted_01
Textures:   T_CH_Hero_Albedo_01.png
```

### Modularity Principles
- **Grid-Based**: Design for 1m, 2m, or 4m grid systems
- **Snap-Friendly**: Pivot points at corners/centers
- **Tileable**: Textures should tile seamlessly
- **Combinations**: Few pieces = many configurations

### LOD (Level of Detail)
| LOD | % of Original | Distance |
|-----|---------------|----------|
| LOD0 | 100% | 0-10m |
| LOD1 | 60% | 10-25m |
| LOD2 | 30% | 25-50m |
| LOD3 | 15% | 50m+ |
