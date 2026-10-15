import bpy, sys

SRC = "/root/.openclaw/workspace/orbital-shipyard/earth_assets/mercenary.glb"
OUT = "/root/.openclaw/workspace/orbital-shipyard/earth_assets/mercenary_opt.glb"
RATIO = 0.22

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
before = sum(len(o.data.polygons) for o in meshes)
print(f"before: {before} faces across {len(meshes)} meshes, verts={sum(len(o.data.vertices) for o in meshes)}")

for o in meshes:
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    mod = o.modifiers.new(name='Dec', type='DECIMATE')
    mod.ratio = RATIO
    bpy.ops.object.modifier_apply(modifier='Dec')

after = sum(len(o.data.polygons) for o in meshes)
print(f"after: {after} faces")

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath=OUT,
    export_format='GLB',
    use_selection=True,
)
print("EXPORTED", OUT)
