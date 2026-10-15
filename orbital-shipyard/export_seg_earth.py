import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)

bpy.ops.wm.stl_import(filepath="/root/.openclaw/workspace/orbital-shipyard/seg_earth_station.stl")
obj = bpy.context.active_object
obj.name = "SEG-EARTH"
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')
parts = [o for o in bpy.context.selected_objects]

palette = {
    "hull":      (0.30, 0.42, 0.55, 1.0),  # steel blue
    "deck":      (0.48, 0.48, 0.50, 1.0),  # grey grating
    "room":      (0.52, 0.56, 0.32, 1.0),  # olive habitat
    "shaft":     (0.38, 0.38, 0.40, 1.0),  # dim grey
    "solar":     (0.06, 0.11, 0.26, 1.0),  # midnight blue
    "radiator":  (0.74, 0.76, 0.80, 1.0),  # silver
    "port":      (0.62, 0.70, 0.80, 1.0),  # light steel blue
    "arm":       (0.82, 0.45, 0.10, 1.0),  # dark orange
    "light":     (1.0, 0.95, 0.6, 1.0),    # emissive yellow
    "window":    (0.55, 0.75, 0.9, 1.0),   # light blue
}

def classify(o):
    d = o.dimensions
    sx, sy, sz = sorted([d.x, d.y, d.z])  # ascending
    L, M, S = sz, sy, sx  # long, mid, short
    # small spheres -> lights
    if L < 6:
        return "light"
    # thin flat panels
    if S < 3.5:
        if L > 60:
            return "solar"
        if L > 40:
            return "radiator"
        return "window"  # window strips are thin small
    # deck discs: short height, large diameter
    if S < 6 and M > 80:
        return "deck"
    # hollow cylinders: large diameter
    if M > 100:
        return "hull"
    # central shaft: long, medium
    if L > 300 and M < 60:
        return "shaft"
    # docking ports / end caps
    if 20 < M < 80 and L < 40:
        return "port"
    # habitat rooms: boxes ~16x20x22
    if M > 14 and M < 30:
        return "room"
    # robotic arm bits
    return "arm"

for o in parts:
    mat = bpy.data.materials.new(name="m_"+o.name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    key = classify(o)
    bsdf.inputs["Base Color"].default_value = palette[key]
    bsdf.inputs["Roughness"].default_value = 0.6
    bsdf.inputs["Metallic"].default_value = 0.35
    if key in ("light", "window"):
        bsdf.inputs["Emission Color"].default_value = palette[key]
        bsdf.inputs["Emission Strength"].default_value = 4.0
    o.data.materials.clear()
    o.data.materials.append(mat)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath="/root/.openclaw/workspace/orbital-shipyard/seg_earth_station.glb",
    export_format='GLB',
    use_selection=True,
)
print("GLB_EXPORTED")
