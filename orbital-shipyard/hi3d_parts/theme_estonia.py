import bpy, mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)

bpy.ops.import_scene.gltf(filepath="/root/.openclaw/workspace/orbital-shipyard/hi3d_parts/seg_station_hi3d.glb")

# Estonian flag colors
BLUE  = (0.00, 0.45, 0.81)   # #0072CE-ish
BLACK = (0.04, 0.04, 0.05)
WHITE = (1.00, 1.00, 1.00)

meshes = [o for o in bpy.data.objects if o.type == 'MESH']

# global Y range (long axis)
ys = []
for o in meshes:
    for c in o.bound_box:
        v = o.matrix_world @ mathutils.Vector(c)
        ys.append(v.y)
ymin, ymax = min(ys), max(ys)
third = (ymax - ymin) / 3.0
print(f"Y range {ymin:.3f}..{ymax:.3f}  third={third:.3f}")

def pick(cy):
    if cy > ymin + 2*third: return BLUE
    if cy > ymin + third:   return BLACK
    return WHITE

seen_meshes = set()
for o in meshes:
    cs = [(o.matrix_world @ mathutils.Vector(c)).y for c in o.bound_box]
    cy = (min(cs)+max(cs))/2
    col = pick(cy)
    # material base color
    if o.material_slots:
        mat = o.material_slots[0].material
        if mat and mat.node_tree:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bc = bsdf.inputs["Base Color"]
                for link in list(bc.links):
                    mat.node_tree.links.remove(link)
                bc.default_value = (col[0], col[1], col[2], 1.0)
    # remove vertex colors so material color shows pure
    md = o.data
    if md.name not in seen_meshes:
        seen_meshes.add(md.name)
        for a in list(md.color_attributes):
            md.color_attributes.remove(a)

bpy.ops.object.select_all(action='SELECT')
out = "/root/.openclaw/workspace/orbital-shipyard/hi3d_parts/seg_station_estonia.glb"
bpy.ops.export_scene.gltf(
    filepath=out,
    export_format='GLB',
    use_selection=True,
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=10,
)
print("EXPORTED", out)
