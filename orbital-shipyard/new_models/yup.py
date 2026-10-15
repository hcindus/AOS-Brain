import bpy, math, sys

args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
SRC = args[0]; OUT = args[1]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

mesh = [o for o in bpy.data.objects if o.type == 'MESH'][0]

# rotate -90 around X to map height (Z) -> up (Y)
mesh.rotation_euler.x = -math.pi / 2
bpy.context.view_layer.objects.active = mesh
mesh.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# report new bounds
bbox = [mesh.matrix_world @ __import__('mathutils').Vector(c) for c in mesh.bound_box]
xs=[v.x for v in bbox]; ys=[v.y for v in bbox]; zs=[v.z for v in bbox]
print(f"new bounds X[{min(xs):.2f},{max(xs):.2f}] Y[{min(ys):.2f},{max(ys):.2f}] Z[{min(zs):.2f},{max(zs):.2f}]")

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True)
print("EXPORTED", OUT)
