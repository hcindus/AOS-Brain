import bpy, glob, os

SRC = "/root/.openclaw/workspace/orbital-shipyard/new_models/android_parts/*.glb"
OUT = "/root/.openclaw/workspace/orbital-shipyard/new_models/android_merged.glb"
RATIO = 0.15

bpy.ops.wm.read_factory_settings(use_empty=True)

files = sorted(glob.glob(SRC))
print(f"importing {len(files)} parts")
for f in files:
    bpy.ops.import_scene.gltf(filepath=f)

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
print(f"{len(meshes)} mesh objects")

# join all into one
bpy.ops.object.select_all(action='DESELECT')
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.join()
joined = bpy.context.active_object
print(f"joined: {len(joined.data.vertices)} verts, {len(joined.data.polygons)} faces")

# apply transform
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# decimate
mod = joined.modifiers.new(name='Dec', type='DECIMATE')
mod.ratio = RATIO
bpy.ops.object.modifier_apply(modifier='Dec')
print(f"after decimate: {len(joined.data.polygons)} faces")

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True)
print("EXPORTED", OUT)
