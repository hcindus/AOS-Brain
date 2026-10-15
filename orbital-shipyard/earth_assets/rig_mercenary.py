import bpy, mathutils

SRC = "/root/.openclaw/workspace/orbital-shipyard/earth_assets/mercenary_opt.glb"
OUT = "/root/.openclaw/workspace/orbital-shipyard/earth_assets/mercenary_rigged.glb"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

mesh = None
for o in bpy.data.objects:
    if o.type == 'MESH':
        mesh = o
        break

# world bounds
bbox = [mesh.matrix_world @ mathutils.Vector(c) for c in mesh.bound_box]
xs = [v.x for v in bbox]; ys = [v.y for v in bbox]; zs = [v.z for v in bbox]
minx, maxx = min(xs), max(xs)
miny, maxy = min(ys), max(ys)
minz, maxz = min(zs), max(zs)
print(f"mesh bounds: X[{minx:.3f},{maxx:.3f}] Y[{miny:.3f},{maxy:.3f}] Z[{minz:.3f},{maxz:.3f}]")

# Character height along Z (Blender Z-up after glTF Y-up import)
height = maxz - minz
cy = (miny + maxy) / 2  # center in Y (front/back)
foot_z = minz
head_z = maxz
print(f"height={height:.3f}  foot_z={foot_z:.3f}  head_z={head_z:.3f}  centerY={cy:.3f}")

def frac(f):
    return foot_z + height * f

# --- Create armature ---
arm_data = bpy.data.armatures.new("Rig")
arm_obj = bpy.data.objects.new("Rig", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
arm_obj.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')

bones = arm_data.edit_bones

def bone(name, head, tail, parent=None):
    b = bones.new(name)
    b.head = head
    b.tail = tail
    if parent:
        b.parent = parent
    return b

# Root / hips
hips = bone("Hips", mathutils.Vector((0, cy, frac(0.48))), mathutils.Vector((0, cy, frac(0.58))))
spine = bone("Spine", mathutils.Vector((0, cy, frac(0.58))), mathutils.Vector((0, cy, frac(0.76))), hips)
neck = bone("Neck", mathutils.Vector((0, cy, frac(0.76))), mathutils.Vector((0, cy, frac(0.86))), spine)
head = bone("Head", mathutils.Vector((0, cy, frac(0.86))), mathutils.Vector((0, cy, frac(0.97))), neck)

# Arms
half_w = (maxx - minx) * 0.42
l_shoulder = bone("L.Shoulder", mathutils.Vector((0, cy, frac(0.76))), mathutils.Vector((-half_w, cy, frac(0.76))), spine)
l_uparm = bone("L.UpperArm", mathutils.Vector((-half_w, cy, frac(0.76))), mathutils.Vector((-half_w*1.6, cy, frac(0.60))), l_shoulder)
l_forearm = bone("L.Forearm", mathutils.Vector((-half_w*1.6, cy, frac(0.60))), mathutils.Vector((-half_w*1.6, cy, frac(0.46))), l_uparm)
l_hand = bone("L.Hand", mathutils.Vector((-half_w*1.6, cy, frac(0.46))), mathutils.Vector((-half_w*1.6, cy, frac(0.40))), l_forearm)

r_shoulder = bone("R.Shoulder", mathutils.Vector((0, cy, frac(0.76))), mathutils.Vector((half_w, cy, frac(0.76))), spine)
r_uparm = bone("R.UpperArm", mathutils.Vector((half_w, cy, frac(0.76))), mathutils.Vector((half_w*1.6, cy, frac(0.60))), r_shoulder)
r_forearm = bone("R.Forearm", mathutils.Vector((half_w*1.6, cy, frac(0.60))), mathutils.Vector((half_w*1.6, cy, frac(0.46))), r_uparm)
r_hand = bone("R.Hand", mathutils.Vector((half_w*1.6, cy, frac(0.46))), mathutils.Vector((half_w*1.6, cy, frac(0.40))), r_forearm)

# Legs
leg_x = (maxx - minx) * 0.15
l_upleg = bone("L.UpperLeg", mathutils.Vector((0, cy, frac(0.48))), mathutils.Vector((-leg_x, cy, frac(0.24))), hips)
l_lowleg = bone("L.LowerLeg", mathutils.Vector((-leg_x, cy, frac(0.24))), mathutils.Vector((-leg_x, cy, frac(0.05))), l_upleg)
l_foot = bone("L.Foot", mathutils.Vector((-leg_x, cy, frac(0.05))), mathutils.Vector((-leg_x, cy+height*0.12, frac(0.00))), l_lowleg)

r_upleg = bone("R.UpperLeg", mathutils.Vector((0, cy, frac(0.48))), mathutils.Vector((leg_x, cy, frac(0.24))), hips)
r_lowleg = bone("R.LowerLeg", mathutils.Vector((leg_x, cy, frac(0.24))), mathutils.Vector((leg_x, cy, frac(0.05))), r_upleg)
r_foot = bone("R.Foot", mathutils.Vector((leg_x, cy, frac(0.05))), mathutils.Vector((leg_x, cy+height*0.12, frac(0.00))), r_lowleg)

bpy.ops.object.mode_set(mode='OBJECT')

# --- Skin (parent with automatic weights) ---
mesh.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# verify armature modifier + vertex groups
print("modifiers:", [(m.type, getattr(m, 'object', None).name if getattr(m,'object',None) else None) for m in mesh.modifiers])
print("vertex groups:", len(mesh.vertex_groups))

# ensure armature modifier references the rig
for m in mesh.modifiers:
    if m.type == 'ARMATURE':
        m.object = arm_obj

print("AUTO-WEIGHTS applied")

# --- Export with skin ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath=OUT,
    export_format='GLB',
    use_selection=False,
    export_skins=True,
    export_animations=True,
)
print("EXPORTED", OUT)
