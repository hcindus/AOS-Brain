import bpy, mathutils
from collections import Counter

SRC = "/root/.openclaw/workspace/orbital-shipyard/fleet/colony_starship_opt.glb"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

mesh = None
for o in bpy.data.objects:
    if o.type == 'MESH':
        mesh = o; break

bpy.context.view_layer.objects.active = mesh
mesh.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

parts = [o for o in bpy.data.objects if o.type == 'MESH']

# centroid of each part
centroids = []
for p in parts:
    bb = [p.matrix_world @ mathutils.Vector(c) for c in p.bound_box]
    cx = (min(v.x for v in bb) + max(v.x for v in bb))/2
    cy = (min(v.y for v in bb) + max(v.y for v in bb))/2
    cz = (min(v.z for v in bb) + max(v.z for v in bb))/2
    centroids.append((cx, cy, cz))

# cluster by X and Z sign (2x2 grid hypothesis)
def quad(cx, cz):
    xs = 'L' if cx < 0 else 'R'
    zs = 'F' if cz < 0 else 'B'
    return xs+zs

qcount = Counter(quad(cx, cz) for cx,cy,cz in centroids)
print("quadrant counts (X-sign + Z-sign):", dict(qcount))

# also show overall centroid ranges
xs = [c[0] for c in centroids]; zs = [c[2] for c in centroids]
print(f"centroid X range: {min(xs):.3f} .. {max(xs):.3f}")
print(f"centroid Z range: {min(zs):.3f} .. {max(zs):.3f}")
