#!/usr/bin/env python3
"""
Seed One Lander — surface<->space landing craft.
Built from primitives (Blender alpha-map technique spirit), no hard-surface booleans.
Vertical lander: tapered hull, docking ring, 4 landing legs, 3 retro engines,
emissive window band, panel ring greebles. Exports GLB for the fleet viewer.
"""
import bpy, math, os

# ---------------------------------------------------------------------------
# Clean scene
# ---------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)

def mat(name, color, metallic=0.6, rough=0.5, emit=None, emit_strength=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    if emit is not None:
        bsdf.inputs["Emission Color"].default_value = (*emit, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emit_strength
    return m

hull_m   = mat("Hull",    (0.62, 0.64, 0.68), metallic=0.85, rough=0.35)
dark_m   = mat("Dark",    (0.20, 0.21, 0.23), metallic=0.7, rough=0.45)
accent_m = mat("Accent",  (0.85, 0.30, 0.18), metallic=0.5, rough=0.4)
window_m = mat("Window",  (0.0, 0.0, 0.0),    metallic=0.2, rough=0.3,
               emit=(0.30, 0.85, 1.0), emit_strength=8.0)
engine_m = mat("Engine",  (0.15, 0.15, 0.16), metallic=0.9, rough=0.25,
               emit=(1.0, 0.45, 0.05), emit_strength=4.0)
shield_m = mat("Shield",  (0.10, 0.11, 0.12), metallic=0.4, rough=0.7)

def assign(obj, m):
    if obj.data.materials:
        obj.data.materials[0] = m
    else:
        obj.data.materials.append(m)

def cyl(name, radius, depth, loc=(0,0,0), rot=None, verts=64, m=hull_m):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts, radius=radius, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    if rot: o.rotation_euler = rot
    assign(o, m)
    return o

def cone(name, r1, r2, depth, loc=(0,0,0), verts=64, m=hull_m):
    bpy.ops.mesh.primitive_cone_add(
        vertices=verts, radius1=r1, radius2=r2, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    assign(o, m)
    return o

def box(name, size, loc, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = size
    assign(o, m)
    return o

# ---------------------------------------------------------------------------
# Build the lander (Z = vertical)
# ---------------------------------------------------------------------------
R = 2.0        # hull radius
H = 8.0        # hull height

# Hull body (tapered slightly at top via a separate nose cone)
cyl("HullBody", R, H, loc=(0,0,0))

# Nose cone (command section) -> docks with Seed One
cone("Nose", R, 0.55, 2.6, loc=(0,0,H/2 + 2.6/2))

# Docking ring on the nose tip
cyl("DockingRing", 0.6, 0.5, loc=(0,0,H/2 + 2.6 + 0.25), m=accent_m)

# Heat-shield base plate
cyl("BaseShield", R*1.08, 0.35, loc=(0,0,-H/2 - 0.17), m=shield_m)

# Engine section (wider skirt at the base)
cyl("EngineSkirt", R*1.06, 1.2, loc=(0,0,-H/2 - 0.6), m=dark_m)

# 3 retro-engine nozzles (cones pointing down)
for i in range(3):
    a = math.radians(i*120 + 30)
    x = R*0.55 * math.cos(a)
    y = R*0.55 * math.sin(a)
    cone(f"Engine{i+1}", 0.55, 0.30, 1.1, loc=(x,y,-H/2 - 0.6 - 0.55), m=engine_m)

# 4 landing legs (angled struts from the skirt)
for i in range(4):
    a = math.radians(i*90 + 45)
    # leg cylinder, angled outward + down
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.16, depth=3.4,
        location=(0,0,0))
    leg = bpy.context.object
    leg.name = f"Leg{i+1}"
    assign(leg, dark_m)
    # rotate to point outward/down
    leg.rotation_euler = (math.radians(35), 0, a)
    leg.location = (R*0.85*math.cos(a), R*0.85*math.sin(a), -H/2 - 0.3)

# Panel ring greebles (3 horizontal rings of small emissive + panel blocks)
ring_z = [-H/4, 0, H/4]
for rz in ring_z:
    for i in range(16):
        a = math.radians(i*22.5)
        x = R*1.02 * math.cos(a)
        y = R*1.02 * math.sin(a)
        box(f"Panel_{rz:.0f}_{i}", (0.32, 0.06, 0.22), (x,y,rz), accent_m)

# Emissive window band (port-hole windows around upper hull)
wz = H/2 - 0.6
for i in range(20):
    a = math.radians(i*18)
    x = R*1.01 * math.cos(a)
    y = R*1.01 * math.sin(a)
    cyl(f"Window_{i}", 0.16, 0.10, loc=(x,y,wz), rot=(math.radians(90),0,a), verts=16, m=window_m)

# ---------------------------------------------------------------------------
# Export GLB
# ---------------------------------------------------------------------------
outdir = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(outdir, "landing_craft.glb")
bpy.ops.export_scene.gltf(filepath=out, export_format="GLB",
                          export_yup=True, export_apply=True)
print("EXPORTED", out)
