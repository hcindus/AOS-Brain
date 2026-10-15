import bpy, mathutils

SRC = "/root/.openclaw/workspace/orbital-shipyard/new_models/android_merged.glb"
OUT = "/root/.openclaw/workspace/orbital-shipyard/new_models/android_scaled.glb"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

mesh = [o for o in bpy.data.objects if o.type == 'MESH'][0]

# world bounds
bbox = [mesh.matrix_world @ mathutils.Vector(c) for c in mesh.bound_box]
xs = [v.x for v in bbox]; ys = [v.y for v in bbox]; zs = [v.z for v in bbox]
minx, maxx = min(xs), max(xs); miny, maxy = min(ys), max(ys); minz, maxz = min(zs), max(zs)
cx = (minx+maxx)/2; cy = (miny+maxy)/2; cz = (minz+maxz)/2
print(f"orig bounds X[{minx:.3f},{maxx:.3f}] Y[{miny:.3f},{maxy:.3f}] Z[{minz:.3f},{maxz:.3f}] center=({cx:.3f},{cy:.3f},{cz:.3f})")

# scale up so height ~2 units, and center at origin
scale = 2.0 / (maxy - miny)
print(f"scale factor: {scale:.2f}")

mesh.scale = (scale, scale, scale)
# re-center: translate so center maps to origin
mesh.location = (-cx*scale, -cy*scale, -cz*scale)

bpy.context.view_layer.objects.active = mesh
mesh.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

bbox2 = [mesh.matrix_world @ mathutils.Vector(c) for c in mesh.bound_box]
xs2=[v.x for v in bbox2]; ys2=[v.y for v in bbox2]; zs2=[v.z for v in bbox2]
print(f"new bounds X[{min(xs2):.2f},{max(xs2):.2f}] Y[{min(ys2):.2f},{max(ys2):.2f}] Z[{min(zs2):.2f},{max(zs2):.2f}]")

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True)
print("EXPORTED", OUT)
