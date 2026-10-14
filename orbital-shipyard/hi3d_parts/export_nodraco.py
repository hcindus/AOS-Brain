import bpy, os, mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)

# Import the merged (Draco) GLB — Blender decodes its own Draco fine
bpy.ops.import_scene.gltf(filepath="/root/.openclaw/workspace/orbital-shipyard/hi3d_parts/seg_station_hi3d.glb")

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
tot_before = sum(len(o.data.polygons) for o in meshes)
print(f"before decimate: {tot_before} faces across {len(meshes)} meshes")

RATIO = 0.15
for o in meshes:
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    mod = o.modifiers.new(name='Dec', type='DECIMATE')
    mod.ratio = RATIO
    bpy.ops.object.modifier_apply(modifier='Dec')

tot_after = sum(len(o.data.polygons) for o in meshes)
print(f"after decimate: {tot_after} faces")

bpy.ops.object.select_all(action='SELECT')
out = "/root/.openclaw/workspace/orbital-shipyard/hi3d_parts/seg_station_nodraco.glb"
bpy.ops.export_scene.gltf(
    filepath=out,
    export_format='GLB',
    use_selection=True,
)
print("EXPORTED", out)
