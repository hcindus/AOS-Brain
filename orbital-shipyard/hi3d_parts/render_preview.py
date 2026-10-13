import bpy, math

bpy.ops.wm.read_factory_settings(use_empty=True)

bpy.ops.import_scene.gltf(filepath="/root/.openclaw/workspace/orbital-shipyard/hi3d_parts/seg_station_hi3d.glb")

# check vertex color attribute
print("=== VERTEX COLORS ===")
for o in bpy.data.objects:
    if o.type=='MESH':
        has_vcol = any(a.data_type=='FLOAT_COLOR' or a.data_type=='BYTE_COLOR' for a in o.data.color_attributes)
        if has_vcol:
            print("HAS VERTEX COLOR:", o.name)
            break

# camera + light
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1200
scene.render.resolution_y = 1200
scene.render.film_transparent = False

cam_data = bpy.data.cameras.new("cam")
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
cam.location = (1.4, 1.6, 1.2)
cam.rotation_euler = (math.radians(60), 0, math.radians(40))
scene.camera = cam

# lights
for name, loc, energy in [("key",(3,3,4),500), ("fill",(-2,0,1),200)]:
    l = bpy.data.lights.new(name, type='SUN')
    lo = bpy.data.objects.new(name, l)
    lo.location = loc
    l.energy = energy
    scene.collection.objects.link(lo)

# add a subtle background
scene.world = bpy.data.worlds.new("w")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.01,0.02,0.04,1)

out = "/root/.openclaw/workspace/orbital-shipyard/hi3d_parts/preview.png"
scene.render.filepath = out
bpy.ops.render.render(write_still=True)
print("RENDERED", out)
