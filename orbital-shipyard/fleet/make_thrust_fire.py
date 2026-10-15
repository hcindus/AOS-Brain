import bpy, math

# ============================================================
# Thrust fire — reusable effect for fleet ships.
# Follows the Hi3D/Blender volume-fire tutorial:
#   elongated cube + Principled Volume + spherical gradient +
#   color ramp (fire colors) + 4D noise (overlay) + animation.
# Works in Eevee and Cycles.
# ============================================================

FIGHTER = "/root/.openclaw/workspace/orbital-shipyard/fleet/x302_fighter_work.glb"
BLEND   = "/root/.openclaw/workspace/orbital-shipyard/fleet/x302_fighter_thrust.blend"

# thruster positions (rear of fighter). Adjust to match the model.
# 2 small flanking + 1 large center. Fighter long axis = X, rear = -X.
THRUSTERS = [
    dict(name="L", pos=(-0.52, -0.16, 0.0), size=0.14, length=0.55),
    dict(name="R", pos=(-0.52,  0.16, 0.0), size=0.14, length=0.55),
    dict(name="C", pos=(-0.52,  0.0, 0.0), size=0.26, length=0.9),
]

bpy.ops.wm.read_factory_settings(use_empty=True)

# --- import the fighter ---
bpy.ops.import_scene.gltf(filepath=FIGHTER)

# --- world background: pure black ---
world = bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

# --- thrust fire material (volume) ---
def make_fire_material(name="ThrustFire"):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes; links = nt.links
    nodes.clear()

    out = nodes.new('ShaderNodeOutputMaterial'); out.location = (800, 0)
    vol = nodes.new('ShaderNodeVolumePrincipled'); vol.location = (500, 0)
    vol.inputs['Density'].default_value = 0.0                 # no unwanted shadows
    vol.inputs['Emission Color'].default_value = (0.95, 0.45, 0.08, 1.0)  # orange
    links.new(vol.outputs['Volume'], out.inputs['Volume'])

    # spherical gradient -> emission strength (fire shape)
    grad = nodes.new('ShaderNodeTexGradient'); grad.gradient_type = 'SPHERICAL'; grad.location = (-400, 300)
    tc = nodes.new('ShaderNodeTexCoord'); tc.location = (-800, 300)
    mapn = nodes.new('ShaderNodeMapping'); mapn.location = (-600, 300)
    links.new(tc.outputs['Object'], mapn.inputs['Vector'])
    links.new(mapn.outputs['Vector'], grad.inputs['Vector'])
    links.new(grad.outputs['Fac'], vol.inputs['Emission Strength'])

    # color ramp -> fire color variation (into emission color)
    ramp = nodes.new('ShaderNodeValToRGB'); ramp.location = (-200, 100)
    ramp.color_ramp.elements[0].color = (1.0, 0.2, 0.02, 1.0)  # core white-hot
    ramp.color_ramp.elements[1].color = (0.05, 0.02, 0.01, 1.0) # outer fade
    links.new(grad.outputs['Fac'], ramp.inputs['Fac'])

    # 4D noise -> mix (overlay) for dynamic detail
    noise = nodes.new('ShaderNodeTexNoise'); noise.noise_dimensions = '4D'; noise.location = (-400, -100)
    links.new(tc.outputs['Object'], noise.inputs['Vector'])
    mix = nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'OVERLAY'; mix.location = (0, 100)
    mix.inputs['Fac'].default_value = 1.0
    links.new(ramp.outputs['Color'], mix.inputs['Color1'])
    links.new(noise.outputs['Fac'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], vol.inputs['Emission Color'])

    mat.node_tree.animation_data_create() if False else None
    return mat, noise

fire_mat, noise_node = make_fire_material()

# --- create the 3 thrust fire meshes (elongated cubes) ---
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 120
for t in THRUSTERS:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=t['pos'])
    fire = bpy.context.active_object
    fire.name = f"ThrustFire_{t['name']}"
    # elongate along X (pointing backward, -X)
    fire.scale = (t['length'], t['size'], t['size'])
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    fire.data.materials.append(fire_mat)

    # engine-start scale animation (ignition)
    fire.scale = (0.001, 0.001, 0.001)
    fire.keyframe_insert(data_path="scale", frame=1)
    fire.scale = (1.0, 1.0, 1.0)
    fire.keyframe_insert(data_path="scale", frame=20)

# --- animate the noise W value (4D) for motion ---
noise_node.inputs['W'].default_value = 0.0
noise_node.inputs['W'].keyframe_insert(data_path="default_value", frame=1)
noise_node.inputs['W'].default_value = 5.0
noise_node.inputs['W'].keyframe_insert(data_path="default_value", frame=120)

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print("SAVED", BLEND)
