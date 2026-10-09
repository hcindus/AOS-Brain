import bpy
import os
import math

# ---- clear the default scene ----
bpy.ops.wm.read_factory_settings(use_empty=True)

STL = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/production/stl_leg_modules/cylon_full_anatomy.stl"
HEAD = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/production/stl/cylon_head.stl"
OUT = "/root/.openclaw/workspace/renders"

os.makedirs(OUT, exist_ok=True)

# ---- import the STL meshes ----
bpy.ops.wm.stl_import(filepath=STL)
body = bpy.context.active_object
body.name = "CylonBody"

# ---- apply a brushed-metal material ----
mat = bpy.data.materials.new("Chrome")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Metallic"].default_value = 0.95
    bsdf.inputs["Roughness"].default_value = 0.25
    bsdf.inputs["Base Color"].default_value = (0.35, 0.38, 0.42, 1.0)

if body.data.materials:
    body.data.materials[0] = mat
else:
    body.data.materials.append(mat)

# ---- normalize scale + position ----
# compute bounding box, center at origin, scale to a reasonable size
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

# scale to ~1.8 units tall (human scale)
dims = body.dimensions
max_dim = max(dims)
scale = 1.8 / max_dim if max_dim > 0 else 1.0
body.scale = (scale, scale, scale)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# center on Z
body.location = (0, 0, 0.9)

# ---- lighting ----
def add_light(loc, energy, name):
    bpy.ops.object.light_add(type='AREA', location=loc)
    l = bpy.context.active_object
    l.data.energy = energy
    l.name = name
    return l

add_light((0, -4, 3), 400, "Key")
add_light((-3, 2, 2), 150, "Rim")
add_light((3, 1, 1), 100, "Fill")

# world background
world = bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.03, 0.04, 0.06, 1.0)

# ---- camera + render helper ----
def render_view(name, rot_z):
    bpy.ops.object.camera_add(location=(0, -3.2, 1.0))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(90), 0, 0)  # point at -Y (the body)
    cam.name = "Cam_" + name
    # rotate around Z to orbit the body
    cam.location = (3.2 * math.sin(rot_z), -3.2 * math.cos(rot_z), 1.0)
    cam.rotation_euler = (math.radians(90), 0, rot_z)
    bpy.context.scene.camera = cam

    bpy.context.scene.render.filepath = os.path.join(OUT, f"cylon_{name}.png")
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.resolution_x = 1200
    bpy.context.scene.render.resolution_y = 1600
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    bpy.ops.render.render(write_still=True)
    print(f"rendered {name}")

render_view("front", 0)
render_view("threequarter", math.radians(40))
render_view("back", math.radians(180))

print("DONE")
