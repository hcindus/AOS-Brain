import bpy, os, glob

bpy.ops.wm.read_factory_settings(use_empty=True)

d = "/root/.openclaw/workspace/orbital-shipyard/hi3d_parts/glb"
files = sorted(glob.glob(os.path.join(d, "*.glb")))

for f in files:
    bpy.ops.import_scene.gltf(filepath=f)

# Report all mesh objects with world-space bounds
print("=== IMPORTED OBJECTS ===")
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    # world-space bounding box via bound_box + matrix_world
    bb = [o.matrix_world @ bpy.utils.units.to_compat if False else (o.matrix_world @ __import__('mathutils').Vector(c)) for c in o.bound_box]
    xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
    cx = (min(xs)+max(xs))/2; cy = (min(ys)+max(ys))/2; cz = (min(zs)+max(zs))/2
    sx = max(xs)-min(xs); sy = max(ys)-min(ys); sz = max(zs)-min(zs)
    print(f"{o.name:60s} loc=({o.location.x:8.1f},{o.location.y:8.1f},{o.location.z:8.1f}) center=({cx:8.1f},{cy:8.1f},{cz:8.1f}) size=({sx:7.1f},{sy:7.1f},{sz:7.1f})")
