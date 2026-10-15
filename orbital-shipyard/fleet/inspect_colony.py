import bpy, mathutils

SRC = "/root/.openclaw/workspace/orbital-shipyard/fleet/colony_starship_opt.glb"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

mesh = None
for o in bpy.data.objects:
    if o.type == 'MESH':
        mesh = o
        break

print(f"verts={len(mesh.data.vertices)} faces={len(mesh.data.polygons)}")

# separate by loose parts
bpy.context.view_layer.objects.active = mesh
mesh.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

parts = [o for o in bpy.data.objects if o.type == 'MESH']
print(f"loose parts: {len(parts)}")

for i, p in enumerate(parts):
    bb = [p.matrix_world @ mathutils.Vector(c) for c in p.bound_box]
    xs=[v.x for v in bb]; ys=[v.y for v in bb]; zs=[v.z for v in bb]
    print(f"  part[{i}] verts={len(p.data.vertices)} bounds X[{min(xs):.2f},{max(xs):.2f}] Y[{min(ys):.2f},{max(ys):.2f}] Z[{min(zs):.2f},{max(zs):.2f}]")
