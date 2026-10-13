import bpy, os, glob
import mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)

d = "/root/.openclaw/workspace/orbital-shipyard/hi3d_parts/glb"
files = sorted(glob.glob(os.path.join(d, "*.glb")))
for f in files:
    bpy.ops.import_scene.gltf(filepath=f)

# check a few material base colors
print("=== SAMPLE MATERIAL COLORS ===")
for m in list(bpy.data.materials)[:6]:
    if m.node_tree:
        bsdf = m.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            c = bsdf.inputs["Base Color"].default_value
            print(f"{m.name:20s} base=({c[0]:.3f},{c[1]:.3f},{c[2]:.3f})")

# Select all meshes, export merged GLB with Draco
bpy.ops.object.select_all(action='SELECT')
out = "/root/.openclaw/workspace/orbital-shipyard/hi3d_parts/seg_station_hi3d.glb"
bpy.ops.export_scene.gltf(
    filepath=out,
    export_format='GLB',
    use_selection=True,
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=10,
)
print("EXPORTED", out)
