import bpy, mathutils

SRC = "/root/.openclaw/workspace/orbital-shipyard/fleet/mech_opt.glb"
OUT = "/root/.openclaw/workspace/orbital-shipyard/fleet/mech_rigged.glb"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

mesh = None
for o in bpy.data.objects:
    if o.type == 'MESH':
        mesh = o; break

bpy.context.view_layer.objects.active = mesh
mesh.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

bbox = [mesh.matrix_world @ mathutils.Vector(c) for c in mesh.bound_box]
xs=[v.x for v in bbox]; ys=[v.y for v in bbox]; zs=[v.z for v in bbox]
minx,maxx=min(xs),max(xs); miny,maxy=min(ys),max(ys); minz,maxz=min(zs),max(zs)
height = maxy - miny
halfw = (maxx - minx) / 2.0
cz = (minz + maxz) / 2
print(f"mech bounds X[±{halfw:.2f}] Y[{miny:.2f},{maxy:.2f}] (height {height:.2f}) Z[{minz:.2f},{maxz:.2f}]")

def fy(t):
    return miny + height * t

# --- Y-up armature ---
arm_data = bpy.data.armatures.new("Rig")
arm_obj = bpy.data.objects.new("Rig", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
arm_obj.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bones = arm_data.edit_bones

def bone(name, head, tail, parent=None):
    b = bones.new(name); b.head = head; b.tail = tail
    if parent: b.parent = parent
    return b

V = mathutils.Vector
hips  = bone("Hips",  V((0, fy(0.48), cz)), V((0, fy(0.58), cz)))
spine = bone("Spine", V((0, fy(0.58), cz)), V((0, fy(0.78), cz)), hips)
neck  = bone("Neck",  V((0, fy(0.78), cz)), V((0, fy(0.88), cz)), spine)
head  = bone("Head",  V((0, fy(0.88), cz)), V((0, fy(0.98), cz)), neck)

shx = halfw * 0.45; elx = halfw * 0.72; hx = halfw * 0.92
for side, sx in [("L", -1), ("R", 1)]:
    sh = bone(side+".Shoulder", V((0, fy(0.78), cz)), V((sx*shx, fy(0.78), cz)), spine)
    ua = bone(side+".UpperArm", V((sx*shx, fy(0.78), cz)), V((sx*elx, fy(0.62), cz)), sh)
    fa = bone(side+".Forearm", V((sx*elx, fy(0.62), cz)), V((sx*hx, fy(0.46), cz)), ua)
    hd = bone(side+".Hand",    V((sx*hx, fy(0.46), cz)), V((sx*hx, fy(0.40), cz)), fa)

lgx = halfw * 0.25
for side, sx in [("L", -1), ("R", 1)]:
    ul = bone(side+".UpperLeg", V((0, fy(0.48), cz)), V((sx*lgx, fy(0.24), cz)), hips)
    ll = bone(side+".LowerLeg", V((sx*lgx, fy(0.24), cz)), V((sx*lgx, fy(0.06), cz)), ul)
    ft = bone(side+".Foot",     V((sx*lgx, fy(0.06), cz)), V((sx*lgx, fy(0.00), cz)), ll)

bpy.ops.object.mode_set(mode='OBJECT')

# --- skin (envelope weights) ---
mesh.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')
for m in mesh.modifiers:
    if m.type == 'ARMATURE':
        m.object = arm_obj

vg_empty = []
for vg in mesh.vertex_groups:
    cnt = sum(1 for v in mesh.data.vertices if any(g.group == vg.index for g in v.groups))
    if cnt == 0: vg_empty.append(vg.name)
print("empty vertex groups:", vg_empty)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=False, export_skins=True)
print("EXPORTED", OUT)
