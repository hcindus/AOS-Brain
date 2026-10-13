import bpy, os, glob
import mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)

d = "/root/.openclaw/workspace/orbital-shipyard/hi3d_parts/glb"
files = sorted(glob.glob(os.path.join(d, "*.glb")))
for f in files:
    bpy.ops.import_scene.gltf(filepath=f)

meshes = [o for o in bpy.data.objects if o.type == 'MESH']

# Combined world bounds
mn = mathutils.Vector((1e18,)*3); mx = mathutils.Vector((-1e18,)*3)
tot_verts = 0; tot_faces = 0
for o in meshes:
    for c in o.bound_box:
        v = o.matrix_world @ mathutils.Vector(c)
        for i in range(3):
            mn[i] = min(mn[i], v[i]); mx[i] = max(mx[i], v[i])
    tot_verts += len(o.data.vertices)
    tot_faces += len(o.data.polygons)

size = mx - mn
center = (mn + mx) / 2
print("=== COMBINED ===")
print(f"objects={len(meshes)}  verts={tot_verts}  faces={tot_faces}")
print(f"min=({mn.x:.4f},{mn.y:.4f},{mn.z:.4f})  max=({mx.x:.4f},{mx.y:.4f},{mx.z:.4f})")
print(f"size=({size.x:.4f},{size.y:.4f},{size.z:.4f})  center=({center.x:.4f},{center.y:.4f},{center.z:.4f})")

# material / texture info
print("=== MATERIALS ===")
for m in bpy.data.materials:
    has_img = any(n.type=='TEX_IMAGE' for n in m.node_tree.nodes if m.node_tree)
    print(f"{m.name:40s} images={has_img}")

print("=== IMAGES ===")
for im in bpy.data.images:
    print(f"{im.name:50s} {im.size[0]}x{im.size[1]}")
