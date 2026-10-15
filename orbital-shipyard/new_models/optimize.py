import bpy, sys, os

args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
SRC = args[0]; OUT = args[1]; RATIO = float(args[2]) if len(args) > 2 else 0.15
MAX_TEX = 2048

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

for img in bpy.data.images:
    if img.size[0] > MAX_TEX or img.size[1] > MAX_TEX:
        try:
            img.scale(MAX_TEX, MAX_TEX)
            print(f"resized {img.name} -> {img.size[0]}x{img.size[1]}")
        except Exception as e:
            print(f"resize failed {img.name}: {e}")

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
before = sum(len(o.data.polygons) for o in meshes)
print(f"{os.path.basename(SRC)}: before {before} faces")

for o in meshes:
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    mod = o.modifiers.new(name='Dec', type='DECIMATE')
    mod.ratio = RATIO
    bpy.ops.object.modifier_apply(modifier='Dec')

after = sum(len(o.data.polygons) for o in meshes)
print(f"{os.path.basename(SRC)}: after {after} faces")

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True)
print("EXPORTED", OUT)
