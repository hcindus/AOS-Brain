import bpy, mathutils, sys

args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
SRC = args[0]; OUT = args[1]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

mesh = None
for o in bpy.data.objects:
    if o.type == 'MESH':
        mesh = o
        break

# normalize transform so local == world (fixes auto-weight scale mismatch)
bpy.context.view_layer.objects.active = mesh
mesh.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
print("mesh scale after apply:", list(mesh.scale))

bbox = [mesh.matrix_world @ mathutils.Vector(c) for c in mesh.bound_box]
xs = [v.x for v in bbox]; ys = [v.y for v in bbox]; zs = [v.z for v in bbox]
minx, maxx = min(xs), max(xs)
miny, maxy = min(ys), max(ys)
minz, maxz = min(zs), max(zs)
height = maxz - minz
halfw = (maxx - minx) / 2.0
cy = (miny + maxy) / 2
print(f"bounds X[±{halfw:.3f}] Y[{miny:.3f},{maxy:.3f}] Z[{minz:.3f},{maxz:.3f}] height={height:.3f}")

def fz(t):
    return minz + height * t

# --- Armature (bones kept INSIDE mesh bounds) ---
arm_data = bpy.data.armatures.new("Rig")
arm_obj = bpy.data.objects.new("Rig", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
arm_obj.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bones = arm_data.edit_bones

def bone(name, head, tail, parent=None):
    b = bones.new(name)
    b.head = head; b.tail = tail
    if parent: b.parent = parent
    return b

V = mathutils.Vector
hips   = bone("Hips",  V((0, cy, fz(0.48))), V((0, cy, fz(0.58))))
spine  = bone("Spine", V((0, cy, fz(0.58))), V((0, cy, fz(0.78))), hips)
neck   = bone("Neck",  V((0, cy, fz(0.78))), V((0, cy, fz(0.88))), spine)
head   = bone("Head",  V((0, cy, fz(0.88))), V((0, cy, fz(0.98))), neck)

# arms — keep within halfw
shx = halfw * 0.45; elx = halfw * 0.72; hx = halfw * 0.92
for side, sx in [("L", -1), ("R", 1)]:
    sh = bone(side+".Shoulder", V((0, cy, fz(0.78))), V((sx*shx, cy, fz(0.78))), spine)
    ua = bone(side+".UpperArm", V((sx*shx, cy, fz(0.78))), V((sx*elx, cy, fz(0.62))), sh)
    fa = bone(side+".Forearm", V((sx*elx, cy, fz(0.62))), V((sx*hx, cy, fz(0.46))), ua)
    hd = bone(side+".Hand",    V((sx*hx, cy, fz(0.46))), V((sx*hx, cy, fz(0.40))), fa)

# legs — feet extend DOWN not forward
lgx = halfw * 0.25
for side, sx in [("L", -1), ("R", 1)]:
    ul = bone(side+".UpperLeg", V((0, cy, fz(0.48))), V((sx*lgx, cy, fz(0.24))), hips)
    ll = bone(side+".LowerLeg", V((sx*lgx, cy, fz(0.24))), V((sx*lgx, cy, fz(0.06))), ul)
    ft = bone(side+".Foot",     V((sx*lgx, cy, fz(0.06))), V((sx*lgx, cy, fz(0.00))), ll)

bpy.ops.object.mode_set(mode='OBJECT')

# --- Skin ---
mesh.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')
for m in mesh.modifiers:
    if m.type == 'ARMATURE':
        m.object = arm_obj

# report empty vertex groups
empty = [vg.name for vg in mesh.vertex_groups if vg.index not in [i for i in range(len(mesh.vertex_groups))] or sum(1 for v in mesh.data.vertices if vg.index in [g.group for g in v.groups]) == 0]
vg_empty = []
for vg in mesh.vertex_groups:
    cnt = sum(1 for v in mesh.data.vertices if any(g.group == vg.index for g in v.groups))
    if cnt == 0:
        vg_empty.append(vg.name)
print("empty vertex groups:", vg_empty)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=False, export_skins=True)
print("EXPORTED", OUT)
