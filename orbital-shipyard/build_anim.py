import bpy, math

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath="/root/.openclaw/workspace/orbital-shipyard/osy7_v5.stl")
obj = bpy.context.active_object

# Separate by loose parts
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')
parts = [o for o in bpy.context.selected_objects]

# Palette (locked orbital-shipyard)
palette = {
    "truss":    (0.55, 0.57, 0.60, 1.0),
    "bay":      (0.25, 0.35, 0.50, 0.35),
    "ring":     (0.36, 0.42, 0.32, 1.0),
    "module":   (0.42, 0.44, 0.46, 1.0),
    "arm":      (0.85, 0.45, 0.12, 1.0),
    "solar":    (0.10, 0.16, 0.32, 1.0),
    "radiator": (0.75, 0.77, 0.80, 1.0),
    "port":     (0.65, 0.72, 0.82, 1.0),
    "light":    (1.0, 0.95, 0.6, 1.0),
    "red":      (0.85, 0.15, 0.12, 1.0),
    "cyan":     (0.2, 0.8, 0.9, 1.0),
    "hab":      (0.5, 0.5, 0.35, 1.0),
    "floor":    (0.45, 0.3, 0.2, 1.0),
    "win":      (0.55, 0.75, 0.9, 1.0),
}

def classify(o):
    d = o.dimensions
    vol = d.x * d.y * d.z
    if d.x > 300 or d.y > 300 or d.z > 300:
        return "truss"
    if vol > 1.5e6:
        return "bay"
    if vol > 300000:
        return "ring"
    if max(d.x, d.y, d.z) < 4:
        return "light"
    if d.x < 2 and d.y < 2 and d.z < 2:
        return "light"
    if min(d.x,d.y,d.z) < 2.5 and max(d.x,d.y,d.z) > 50:
        return "radiator"
    if max(d.x, d.y) > 60 and min(d.x,d.y,d.z) < 4:
        return "solar"
    if min(d.x,d.y,d.z) < 3:
        return "arm"
    return "module"

for o in parts:
    mat = bpy.data.materials.new(name="m_"+o.name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    key = classify(o)
    bsdf.inputs["Base Color"].default_value = palette[key]
    bsdf.inputs["Roughness"].default_value = 0.65
    bsdf.inputs["Metallic"].default_value = 0.35
    if key in ("light","red","cyan","win"):
        bsdf.inputs["Emission Color"].default_value = palette[key]
        bsdf.inputs["Emission Strength"].default_value = 3.0
    if o.data.materials:
        o.data.materials[0] = mat
    else:
        o.data.materials.append(mat)

# World
world = bpy.data.worlds.new("w")
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.02, 0.03, 0.05, 1.0)
bg.inputs[1].default_value = 0.5

# Lights
key = bpy.data.lights.new("KEY", type='AREA'); key.energy = 8000
k = bpy.data.objects.new("Key", key); bpy.context.collection.objects.link(k)
k.location = (250, 200, 400); k.rotation_euler = (math.radians(-40),0,math.radians(30)); k.data.size = 200
fill = bpy.data.lights.new("FILL", type='AREA'); fill.energy = 2500
f = bpy.data.objects.new("Fill", fill); bpy.context.collection.objects.link(f)
f.location = (-300,-200,100); f.rotation_euler = (math.radians(30),0,math.radians(-45)); f.data.size = 250

# Camera
cam_data = bpy.data.cameras.new("cam"); cam_data.lens = 50
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam); bpy.context.scene.camera = cam

# Frame model
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.select_all(action='SELECT')
bpy.ops.view3d.camera_to_view_selected()

# Empty pivot for turntable
pivot = bpy.data.objects.new("Pivot", None)
bpy.context.collection.objects.link(pivot)
pivot.location = (0,0,0)

# Parent all parts to pivot so they rotate together
for o in parts:
    o.parent = pivot

# Animate rotation of pivot over 240 frames (10s @ 24fps)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.cycles.samples = 48
scene.frame_start = 1
scene.frame_end = 240
scene.render.fps = 24

pivot.rotation_euler = (0, 0, 0)
pivot.keyframe_insert(data_path="rotation_euler", frame=1)
pivot.rotation_euler = (0, 0, math.radians(360))
pivot.keyframe_insert(data_path="rotation_euler", frame=240)

# Linear interpolation (constant angular velocity)
for fc in pivot.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'LINEAR'

scene.render.filepath = "/root/.openclaw/workspace/orbital-shipyard/anim/frame_"
scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(animation=True)
print("ANIM_DONE")
