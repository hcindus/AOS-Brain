import bpy

BLEND = "/root/.openclaw/workspace/orbital-shipyard/fleet/x302_fighter_thrust_billboard.blend"
OUT   = "/root/.openclaw/workspace/orbital-shipyard/fleet/x302_fighter_thrust.glb"

bpy.ops.wm.open_mainfile(filepath=BLEND)

# select all objects and export
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath=OUT,
    export_format='GLB',
    use_selection=True,
)
print("EXPORTED", OUT)
