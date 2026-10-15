import bpy, math

# ============================================================
# Thrust fire — BILLBOARD approach (image-texture emission).
# Follows the "jet engine thrust" tutorial: open cylinder +
# emission shader (image texture) + transparent (add shader) +
# layer-weight facing fade. Web-friendly (works as a sprite).
# ============================================================

FIGHTER = "/root/.openclaw/workspace/orbital-shipyard/fleet/x302_fighter_work.glb"
BLEND   = "/root/.openclaw/workspace/orbital-shipyard/fleet/x302_fighter_thrust_billboard.blend"
TEX     = "/root/.openclaw/workspace/orbital-shipyard/fleet/thrust_fire.png"

# thrusters (rear of fighter = -X): 2 small flanking + 1 large center
THRUSTERS = [
    dict(name="L", pos=(-0.55, -0.16, 0.0), radius=0.12, length=0.7),
    dict(name="R", pos=(-0.55,  0.16, 0.0), radius=0.12, length=0.7),
    dict(name="C", pos=(-0.55,  0.0, 0.0), radius=0.22, length=1.1),
]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=FIGHTER)

# world black
world = bpy.data.worlds.new("World"); bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

# load fire texture
img = bpy.data.images.load(TEX)

def make_billboard_material(name="ThrustBillboard"):
    mat = bpy.data.materials.new(name); mat.use_nodes = True
    nt = mat.node_tree; nodes = nt.nodes; links = nt.links; nodes.clear()

    out = nodes.new('ShaderNodeOutputMaterial'); out.location = (900, 0)

    em = nodes.new('ShaderNodeEmission'); em.location = (500, 200)
    em.inputs['Strength'].default_value = 10.0

    tex = nodes.new('ShaderNodeTexImage'); tex.location = (200, 200); tex.image = img
    uv = nodes.new('ShaderNodeUVMap'); uv.location = (-100, 200)
    links.new(uv.outputs['UV'], tex.inputs['Vector'])
    links.new(tex.outputs['Color'], em.inputs['Color'])

    # blue tint (multiply) on the fire
    mixc = nodes.new('ShaderNodeMixRGB'); mixc.blend_type = 'MULTIPLY'; mixc.location = (350, 400)
    mixc.inputs['Color2'].default_value = (0.6, 0.75, 1.0, 1.0)  # saturated blue
    links.new(tex.outputs['Color'], mixc.inputs['Color1'])
    links.new(mixc.outputs['Color'], em.inputs['Color'])

    trans = nodes.new('ShaderNodeBsdfTransparent'); trans.location = (500, -200)

    add = nodes.new('ShaderNodeAddShader'); add.location = (700, 0)
    links.new(em.outputs['Emission'], add.inputs[0])
    links.new(trans.outputs['BSDF'], add.inputs[1])
    links.new(add.outputs['Shader'], out.inputs['Surface'])

    # edge fade via layer-weight facing
    lw = nodes.new('ShaderNodeLayerWeight'); lw.location = (-100, -300)
    lw.inputs['Blend'].default_value = 0.7
    # alpha blend for transparency in Eevee
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    mat.use_backface_culling = False
    return mat, lw

fire_mat, lw_node = make_billboard_material()

# create cylinder plumes
bpy.context.scene.frame_start = 1; bpy.context.scene.frame_end = 120
for t in THRUSTERS:
    bpy.ops.mesh.primitive_cylinder_add(radius=t['radius'], depth=t['length'],
                                        end_fill_type='NOTHING', location=t['pos'])
    cyl = bpy.context.active_object
    cyl.name = f"Thrust_{t['name']}"
    # cylinder default axis = Z; rotate to point along X (thrust = -X)
    cyl.rotation_euler = (0, math.radians(90), 0)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.shade_smooth()
    cyl.data.materials.append(fire_mat)

    # engine-start scale animation
    cyl.scale = (0.001, 0.001, 0.001)
    cyl.keyframe_insert(data_path="scale", frame=1)
    cyl.scale = (1.0, 1.0, 1.0)
    cyl.keyframe_insert(data_path="scale", frame=20)

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print("SAVED", BLEND)
