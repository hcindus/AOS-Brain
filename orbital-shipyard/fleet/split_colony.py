import bpy, mathutils

SRC = "/root/.openclaw/workspace/orbital-shipyard/fleet/colony_starship_opt.glb"
OUT = "/root/.openclaw/workspace/orbital-shipyard/fleet/"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

mesh = [o for o in bpy.data.objects if o.type == 'MESH'][0]
bpy.context.view_layer.objects.active = mesh
mesh.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

parts = [o for o in bpy.data.objects if o.type == 'MESH']

def centroid_x(p):
    bb = [p.matrix_world @ mathutils.Vector(c) for c in p.bound_box]
    return (min(v.x for v in bb) + max(v.x for v in bb)) / 2

# 4 X-strips (ships side by side along X)
bins = [(-0.48, -0.24), (-0.24, 0.0), (0.0, 0.24), (0.24, 0.48)]
groups = [[] for _ in bins]
for p in parts:
    cx = centroid_x(p)
    for i, (lo, hi) in enumerate(bins):
        if lo <= cx < hi:
            groups[i].append(p); break

for i, g in enumerate(groups):
    v = sum(len(p.data.vertices) for p in g)
    print(f"ship[{i}]: {len(g)} parts, {v} verts, X range {bins[i]}")

# join + export each group
for i, g in enumerate(groups):
    if not g: continue
    bpy.ops.object.select_all(action='DESELECT')
    for p in g:
        p.select_set(True)
    bpy.context.view_layer.objects.active = g[0]
    bpy.ops.object.join()
    joined = bpy.context.active_object
    joined.name = f"colony_ship_{i+1}"
    bpy.ops.object.select_all(action='DESELECT')
    joined.select_set(True)
    bpy.ops.export_scene.gltf(filepath=OUT + f"colony_ship_{i+1}.glb", export_format='GLB', use_selection=True)
    print(f"exported colony_ship_{i+1}.glb")
