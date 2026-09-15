import bpy, math

bpy.ops.wm.read_factory_settings(use_empty=True)

# Import shipyard
bpy.ops.wm.stl_import(filepath="/root/.openclaw/workspace/orbital-shipyard/osy7_v5.stl")
ship = bpy.context.active_object
ship.name = "Shipyard"
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')
ship_parts = [o for o in bpy.context.selected_objects]

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

# Export GLB (binary glTF) — shipyard only
bpy.ops.export_scene.gltf(
    filepath="/root/.openclaw/workspace/orbital-shipyard/osy7_shipyard.glb",
    export_format='GLB',
    use_selection=False,
    export_apply=False
)
print("GLB_EXPORTED")
