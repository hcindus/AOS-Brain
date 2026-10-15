import bpy, os

SRC = "/root/.openclaw/workspace/data/hi3d_torso/ingest/Myl2Ssa/Hi3D_Realistic Cyberpunk Female Biomechanical Cyborg 3D Asset_allparts_20261010_021653.zip"
OUT = "/root/.openclaw/workspace/orbital-shipyard/new_models/cyborg_biomech.glb"
MAX_TEX = 2048
RATIO = 0.15

bpy.ops.wm.read_factory_settings(use_empty=True)

# extract the obj + textures
import zipfile, tempfile
tmp = tempfile.mkdtemp()
with zipfile.ZipFile(SRC) as z:
    z.extractall(tmp)

obj_path = os.path.join(tmp, "model.obj")
print("importing OBJ:", obj_path, os.path.getsize(obj_path)/1e6, "MB")

bpy.ops.wm.obj_import(filepath=obj_path)

# downscale textures
for img in bpy.data.images:
    if img.size[0] > MAX_TEX or img.size[1] > MAX_TEX:
        try:
            img.scale(MAX_TEX, MAX_TEX)
            print(f"resized {img.name} -> {img.size[0]}x{img.size[1]}")
        except Exception as e:
            print(f"resize failed {img.name}: {e}")

# decimate
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
before = sum(len(o.data.polygons) for o in meshes)
print(f"before: {before} faces")
for o in meshes:
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    mod = o.modifiers.new(name='Dec', type='DECIMATE')
    mod.ratio = RATIO
    bpy.ops.object.modifier_apply(modifier='Dec')
after = sum(len(o.data.polygons) for o in meshes)
print(f"after: {after} faces")

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True)
print("EXPORTED", OUT)
