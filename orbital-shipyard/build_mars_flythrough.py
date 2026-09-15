import bpy, math

bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------------- Import Mars ----------------
bpy.ops.import_scene.gltf(filepath="/root/.openclaw/workspace/orbital-shipyard/mars/mars.glb")
mars = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
mars.name = "Mars"
mars.scale = (8, 8, 8)

# ---------------- Import Shipyard ----------------
bpy.ops.wm.stl_import(filepath="/root/.openclaw/workspace/orbital-shipyard/osy7_v5.stl")
ship = bpy.context.active_object
ship.name = "Shipyard"
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')
ship_parts = [o for o in bpy.context.selected_objects if o != mars]

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
    vol = d.x*d.y*d.z
    if d.x > 300 or d.y > 300 or d.z > 300: return "truss"
    if vol > 1.5e6: return "bay"
    if vol > 300000: return "ring"
    if max(d.x,d.y,d.z) < 4: return "light"
    if min(d.x,d.y,d.z) < 2.5 and max(d.x,d.y,d.z) > 50: return "radiator"
    if max(d.x,d.y) > 60 and min(d.x,d.y,d.z) < 4: return "solar"
    if min(d.x,d.y,d.z) < 3: return "arm"
    return "module"

for o in ship_parts:
    mat = bpy.data.materials.new(name="m_"+o.name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    key = classify(o)
    bsdf.inputs["Base Color"].default_value = palette[key]
    bsdf.inputs["Roughness"].default_value = 0.65
    bsdf.inputs["Metallic"].default_value = 0.35
    if key in ("light","red","cyan","win"):
        bsdf.inputs["Emission Color"].default_value = palette[key]
        bsdf.inputs["Emission Strength"].default_value = 4.0
    o.data.materials.clear()
    o.data.materials.append(mat)

pivot = bpy.data.objects.new("ShipyardPivot", None)
bpy.context.collection.objects.link(pivot)
for o in ship_parts:
    o.parent = pivot
pivot.location = (0, 4400, 0)

# ---------------- World ----------------
world = bpy.data.worlds.new("w")
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.008, 0.01, 0.02, 1.0)
bg.inputs[1].default_value = 0.7

sun = bpy.data.lights.new("SUN", type='SUN'); sun.energy = 3.5; sun.color = (1.0,0.95,0.85)
so = bpy.data.objects.new("Sun", sun); bpy.context.collection.objects.link(so)
so.rotation_euler = (math.radians(50), 0, math.radians(30))

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 240
scene.eevee.taa_render_samples = 16

cam_data = bpy.data.cameras.new("cam"); cam_data.lens = 35
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam); bpy.context.scene.camera = cam

import mathutils
def look_at(eye, target):
    d = mathutils.Vector(target) - mathutils.Vector(eye)
    return d.to_track_quat('-Z', 'Y').to_euler()

def set_cam(frame, loc, rot):
    cam.location = loc; cam.rotation_euler = rot
    cam.keyframe_insert(data_path="location", frame=frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=frame)

R = 2200
# Phase 1 (1-100): orbit approach
for i in range(100):
    t = i/99.0
    ang = math.radians(-70 + 140*t)
    loc = (4400 + R*math.sin(ang), 4700 - 300*t, R*math.cos(ang))
    rot = look_at(loc, (0, 4400, 0))
    set_cam(i+1, loc, rot)
# Phase 2 (101-160): fly through bay
for i in range(60):
    t = i/59.0
    z = -380 + 760*t
    loc = (0, 4400, z)
    rot = look_at(loc, (0, 4400, z+100))
    set_cam(i+101, loc, rot)
# Phase 3 (161-240): pull away
for i in range(80):
    t = i/79.0
    d = 800 + 2200*t
    loc = (0, 4600 + 200*t, 400 + d)
    rot = look_at(loc, (0, 4400, 0))
    set_cam(i+161, loc, rot)

scene.render.filepath = "/root/.openclaw/workspace/orbital-shipyard/mars_scene/frame_"
scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(animation=True)
print("FLYTHROUGH_DONE")
