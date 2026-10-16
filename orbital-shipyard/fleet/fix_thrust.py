import bpy, math

# ============================================================
# FINAL thrust fix: attach ONE plume to the fighter's actual
# flat stealth nozzle (auto-detected at rear, Y~-0.16 Z~-0.11).
# The old script used hardcoded Y=0/Z=0 positions (wrong offset).
# ============================================================

FIGHTER = "/root/.openclaw/workspace/orbital-shipyard/fleet/x302_fighter_work.glb"
OUT_GLB = "/root/.openclaw/workspace/orbital-shipyard/fleet/x302_fighter_thrust.glb"
TEX     = "/root/.openclaw/workspace/orbital-shipyard/fleet/thrust_fire.png"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=FIGHTER)
o = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH'][0]

# --- detect rear exhaust via vertex cross-section ---
verts = [tuple(o.matrix_world @ v.co) for v in o.data.vertices]
xmin = min(p[0] for p in verts); xmax = max(p[0] for p in verts)
cut = xmin + (xmax-xmin)*0.05
rear = [p for p in verts if p[0] < cut]

ys = [p[1] for p in rear]; zs = [p[2] for p in rear]
cy = (min(ys)+max(ys))/2
cz = (min(zs)+max(zs))/2
half_w = (max(ys)-min(ys))/2   # flat slot half-width (Y)
half_h = (max(zs)-min(zs))/2   # flat slot half-height (Z)
print(f"nozzle center Y={cy:.3f} Z={cz:.3f}  halfW={half_w:.3f} halfH={half_h:.3f}")

# --- world + fire texture ---
world = bpy.data.worlds.new("W"); bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0,0,0,1)
img = bpy.data.images.load(TEX)

def make_billboard():
    mat = bpy.data.materials.new("Thrust"); mat.use_nodes = True
    nt = mat.node_tree; nodes = nt.nodes; links = nt.links; nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial'); out.location=(900,0)
    em = nodes.new('ShaderNodeEmission'); em.location=(500,200); em.inputs['Strength'].default_value=12.0
    tex = nodes.new('ShaderNodeTexImage'); tex.location=(200,200); tex.image=img
    uv = nodes.new('ShaderNodeUVMap'); uv.location=(-100,200)
    links.new(uv.outputs['UV'], tex.inputs['Vector'])
    links.new(tex.outputs['Color'], em.inputs['Color'])
    mixc = nodes.new('ShaderNodeMixRGB'); mixc.blend_type='MULTIPLY'; mixc.location=(350,400)
    mixc.inputs['Color2'].default_value=(0.55,0.72,1.0,1.0)
    links.new(tex.outputs['Color'], mixc.inputs['Color1'])
    links.new(mixc.outputs['Color'], em.inputs['Color'])
    trans = nodes.new('ShaderNodeBsdfTransparent'); trans.location=(500,-200)
    add = nodes.new('ShaderNodeAddShader'); add.location=(700,0)
    links.new(em.outputs['Emission'], add.inputs[0])
    links.new(trans.outputs['BSDF'], add.inputs[1])
    links.new(add.outputs['Shader'], out.inputs['Surface'])
    mat.blend_method='BLEND'; mat.shadow_method='NONE'; mat.use_backface_culling=False
    return mat

fire_mat = make_billboard()

# --- flat plume matching the flat nozzle (wide in Y, thin in Z) ---
radius_y = max(half_w, 0.06)
radius_z = max(half_h*2.2, 0.025)
length = radius_y * 5.0
cx = xmin - length/2 + 0.02  # attach at rear surface, extend rearward (-X)

bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=length,
                                    end_fill_type='NOTHING', location=(cx, cy, cz))
plume = bpy.context.active_object
plume.name = "Thrust"
# cylinder default axis Z -> point along X (plume extends -X)
plume.rotation_euler = (0, math.radians(90), 0)
# flatten: scale radius anisotropically (Y wide, Z thin) to match flat nozzle
plume.scale = (1.0, radius_y, radius_z)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.shade_smooth()
plume.data.materials.append(fire_mat)

print("attached 1 plume at", round(cx,3), round(cy,3), round(cz,3), "len", round(length,3))

bpy.ops.export_scene.gltf(filepath=OUT_GLB, export_format="GLB", export_yup=True, export_apply=True)
print("EXPORTED", OUT_GLB)
