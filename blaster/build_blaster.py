"""
Sidearm Blaster — block-out-first build (Blender 4.2, headless).
Primary silhouette -> secondary forms -> tertiary detail.
Design: compact sci-fi sidearm, circular muzzle vents, canted grip, top rail.
"""
import bpy
import math
import os
from mathutils import Vector, Matrix

# ---------------------------------------------------------------- cleanup
bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------------------------------------------------------------- helpers
def mat(name, base, rough, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = base
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    return m

matte_black = mat("MatteBlack", (0.045, 0.045, 0.05, 1.0), 0.55, 0.35)
steel       = mat("Steel",       (0.28, 0.28, 0.30, 1.0), 0.35, 1.0)
grip_mat    = mat("Grip",        (0.10, 0.10, 0.11, 1.0), 0.75, 0.0)
accent      = mat("Accent",      (0.62, 0.40, 0.10, 1.0), 0.45, 0.8)  # bronze

def assign(obj, m):
    if obj.data.materials:
        obj.data.materials[0] = m
    else:
        obj.data.materials.append(m)

def box(name, size, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = Vector(size)
    o.rotation_euler = Vector(rot)
    return o

def cyl(name, r, depth, loc=(0,0,0), rot=(0,0,0), verts=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth,
                                        location=loc, vertices=verts)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = Vector(rot)
    return o

def bevel(o, amount, segments=2):
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bevel(offset=amount, segments=segments, affect='EDGES')
    bpy.ops.object.mode_set(mode='OBJECT')

# ---------------------------------------------------------------- 1. PRIMARY SILHOUETTE
# Body / receiver — elongated box, nose slightly up, sits along +Y (barrel points +Y)
body = box("Receiver", (0.16, 0.44, 0.14), loc=(0, 0.0, 0.16))
assign(body, matte_black)

# Muzzle / barrel — cylinder pointing +Y, circular vents
barrel = cyl("Barrel", 0.052, 0.22, loc=(0, 0.26, 0.16), rot=(math.pi/2, 0, 0))
assign(barrel, steel)

# Grip — canted back ~18 deg
grip = box("Grip", (0.13, 0.14, 0.22), loc=(0, -0.24, 0.05), rot=(-0.31, 0, 0))
assign(grip, grip_mat)

# Top rail — thin strip over the receiver
rail = box("Rail", (0.06, 0.30, 0.025), loc=(0, 0.05, 0.245))
assign(rail, matte_black)

# Side power cell / mag — box on left side
cell = box("PowerCell", (0.05, 0.14, 0.10), loc=(0.11, -0.02, 0.16))
assign(cell, matte_black)

# ---------------------------------------------------------------- 2. SECONDARY FORMS
# Trigger guard — thin loop under the receiver, in front of grip
bpy.ops.mesh.primitive_torus_add(major_radius=0.055, minor_radius=0.008,
                                 location=(0, -0.11, 0.075), rotation=(0, math.pi/2, 0))
guard = bpy.context.object
guard.name = "TriggerGuard"
assign(guard, matte_black)

# Optic / red-dot on the rail
bpy.ops.mesh.primitive_cube_add(size=0.06, location=(0, 0.13, 0.27))
optic = bpy.context.object
optic.name = "Optic"
optic.dimensions = (0.05, 0.07, 0.04)
assign(optic, matte_black)
bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.06,
                                    location=(0, 0.13, 0.29), rotation=(math.pi/2,0,0))
lens = bpy.context.object
lens.name = "OpticLens"
assign(lens, accent)

# Muzzle circular vents — ring of round holes around the barrel tip (boolean)
# Build cutter cylinders arranged radially around +Y axis at the barrel tip
vent_y = 0.37
vent_r = 0.034  # radial distance of hole centers
hole_r = 0.011
cutters = []
for i in range(6):
    a = i * (2*math.pi/6)
    c = cyl(f"VentHole{i}", hole_r, 0.06,
            loc=(math.sin(a)*vent_r, vent_y, 0.16 + math.cos(a)*vent_r),
            rot=(0, math.pi/2, 0))
    cutters.append(c)

# apply booleans to barrel
for c in cutters:
    mod = barrel.modifiers.new("Vent", 'BOOLEAN')
    mod.object = c
    mod.operation = 'DIFFERENCE'
    bpy.context.view_layer.objects.active = barrel
    bpy.ops.object.modifier_apply(modifier="Vent")

# rail notches (secondary) — thin grooves via loop of small boxes as cutters (skip detail, keep simple)
# clean up cutter objects
for c in cutters:
    bpy.data.objects.remove(c, do_unlink=True)

# ---------------------------------------------------------------- 3. TERTIARY DETAIL (bevels)
# Apply scale before beveling
for o in (body, barrel, grip, rail, cell, guard, optic):
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    try:
        bevel(o, 0.006, 2)
    except Exception as e:
        print("bevel skip", o.name, e)

# ---------------------------------------------------------------- camera + light + render
bpy.ops.object.light_add(type='AREA', location=(2, -2, 3))
key = bpy.context.object
key.data.energy = 800
key.data.size = 2
key.rotation_euler = (math.radians(50), 0, math.radians(45))

bpy.ops.object.light_add(type='AREA', location=(-2, 2, 1))
fill = bpy.context.object
fill.data.energy = 300
fill.data.size = 3

cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
bpy.context.scene.collection.objects.link(cam)
cam.location = (1.4, -1.4, 1.1)
cam.rotation_euler = (math.radians(62), 0, math.radians(45))
bpy.context.scene.camera = cam

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 1600
scene.render.resolution_y = 1200
scene.cycles.samples = 128
scene.render.filepath = "/root/.openclaw/workspace/blaster/render.png"

out_blend = "/root/.openclaw/workspace/blaster/sidearm_blaster.blend"
bpy.ops.wm.save_as_mainfile(filepath=out_blend)
bpy.ops.render.render(write_still=True)
print("SAVED", out_blend)
print("RENDERED", scene.render.filepath)
