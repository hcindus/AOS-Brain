import bpy, math

bpy.ops.wm.read_factory_settings(use_empty=True)

bpy.ops.wm.stl_import(filepath="/root/.openclaw/workspace/orbital-shipyard/seg_station.stl")
obj = bpy.context.active_object
obj.name = "SEG-1"
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')
parts = [o for o in bpy.context.selected_objects]

palette = {
    "segment":   (0.82, 0.84, 0.88, 1.0),  # pressure hulls (white/grey)
    "hub":       (0.55, 0.58, 0.62, 1.0),  # central core
    "spoke":     (0.45, 0.47, 0.50, 1.0),  # truss spokes
    "solar":     (0.10, 0.16, 0.32, 1.0),  # dark blue panels
    "radiator":  (0.75, 0.77, 0.80, 1.0),  # light fins
    "port":      (0.60, 0.66, 0.72, 1.0),  # docking
    "light":     (1.0, 0.95, 0.6, 1.0),    # nav lights (emissive)
    "red":       (0.85, 0.15, 0.12, 1.0),
    "cyan":      (0.2, 0.8, 0.9, 1.0),
}

def classify(o):
    d = o.dimensions
    vol = d.x * d.y * d.z
    # flat thin large -> solar panel or radiator
    if min(d.x, d.y, d.z) < 3.0:
        # very thin + large -> panel
        if max(d.x, d.y) > 40:
            return "solar"
        if max(d.x, d.y) > 25:
            return "radiator"
        return "spoke"
    # small spheres -> nav lights
    if vol < 300:
        return "light"
    # long thin -> spoke
    if max(d.x, d.y, d.z) > 90 and min(d.x, d.y, d.z) < 6:
        return "spoke"
    # segment modules: elongated capsule
    if max(d.x, d.y, d.z) > 55:
        return "segment"
    # hub / core cylinder
    if vol > 80000:
        return "hub"
    return "port"

for o in parts:
    mat = bpy.data.materials.new(name="m_" + o.name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    key = classify(o)
    bsdf.inputs["Base Color"].default_value = palette[key]
    bsdf.inputs["Roughness"].default_value = 0.55
    bsdf.inputs["Metallic"].default_value = 0.4
    if key in ("light", "red", "cyan"):
        bsdf.inputs["Emission Color"].default_value = palette[key]
        bsdf.inputs["Emission Strength"].default_value = 5.0
    if key == "solar":
        bsdf.inputs["Metallic"].default_value = 0.6
        bsdf.inputs["Roughness"].default_value = 0.35
    o.data.materials.clear()
    o.data.materials.append(mat)

bpy.ops.export_scene.gltf(
    filepath="/root/.openclaw/workspace/orbital-shipyard/seg_station.glb",
    export_format='GLB',
    use_selection=False,
    export_apply=False
)
print("GLB_EXPORTED")
