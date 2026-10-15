import bpy, mathutils

SRC = "/root/.openclaw/workspace/orbital-shipyard/fleet/colony_starship_opt.glb"
OUT = "/root/.openclaw/workspace/orbital-shipyard/fleet/"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

mesh = [o for o in bpy.data.objects if o.type == 'MESH'][0]
bpy.context.view_layer.objects.active = mesh
mesh.select_set(True)

# merge by distance (clean up duplicate vertices at seams)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.0001)
bpy.ops.object.mode_set(mode='OBJECT')
print(f"after merge-doubles: {len(mesh.data.vertices)} verts, {len(mesh.data.polygons)} faces")

# separate into loose parts
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

parts = [o for o in bpy.data.objects if o.type == 'MESH']
print(f"loose parts: {len(parts)}")

def centroid_x(p):
    bb = [p.matrix_world @ mathutils.Vector(c) for c in p.bound_box]
    return (min(v.x for v in bb) + max(v.x for v in bb)) / 2

# sort parts by centroid X, find the 3 largest gaps (boundaries between 4 ships)
cs = sorted((centroid_x(p) for p in parts))
gaps = []
for i in range(1, len(cs)):
    gaps.append((cs[i] - cs[i-1], cs[i-1], cs[i]))
gaps.sort(reverse=True)
top3 = sorted(gaps[:3], key=lambda g: g[1])  # sort by X position
print("top 3 gaps (X boundaries):", [(round(g[1],3), round(g[2],3)) for g in top3])

# boundaries = midpoints of the top 3 gaps
bounds = [ (g[1]+g[2])/2 for g in top3 ]
bounds = [-1e9] + bounds + [1e9]
print("split boundaries:", [round(b,3) for b in bounds])

groups = [[] for _ in range(4)]
for p in parts:
    cx = centroid_x(p)
    for i in range(4):
        if bounds[i] <= cx < bounds[i+1]:
            groups[i].append(p); break

for i, g in enumerate(groups):
    v = sum(len(p.data.vertices) for p in g)
    print(f"ship[{i}]: {len(g)} parts, {v} verts")

# join + export each group
for i, g in enumerate(groups):
    if not g: continue
    bpy.ops.object.select_all(action='DESELECT')
    for p in g: p.select_set(True)
    bpy.context.view_layer.objects.active = g[0]
    bpy.ops.object.join()
    joined = bpy.context.active_object
    joined.name = f"colony_ship_{i+1}"
    bpy.ops.object.select_all(action='DESELECT')
    joined.select_set(True)
    bpy.ops.export_scene.gltf(filepath=OUT + f"colony_ship_{i+1}.glb", export_format='GLB', use_selection=True)
    print(f"exported colony_ship_{i+1}.glb")
