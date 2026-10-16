#!/usr/bin/env python3
"""Render a hero thumbnail of the landing craft."""
import bpy, math, os

bpy.ops.wm.read_factory_settings(use_empty=True)

# Import the lander GLB (built Y-up already)
d = os.path.dirname(os.path.abspath(__file__))
bpy.ops.import_scene.gltf(filepath=os.path.join(d, "landing_craft.glb"))

# Camera
cam = bpy.data.cameras.new("Hero")
cam.lens = 50
camo = bpy.data.objects.new("Hero", cam)
bpy.context.collection.objects.link(camo)
camo.location = (6.0, -7.0, 4.5)
camo.rotation_euler = (math.radians(72), 0, math.radians(40))

bpy.context.scene.camera = camo

# Lighting
sun = bpy.data.lights.new("Sun", "SUN")
sun.energy = 4.0
suno = bpy.data.objects.new("Sun", sun)
bpy.context.collection.objects.link(suno)
suno.location = (8, -4, 10)

fill = bpy.data.lights.new("Fill", "AREA")
fill.energy = 60
fillo = bpy.data.objects.new("Fill", fill)
bpy.context.collection.objects.link(fillo)
fillo.location = (-5, 5, 2)

# World (dark blue space)
world = bpy.data.worlds.new("Space")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.02, 0.05, 1.0)
bpy.context.scene.world = world

# Render settings
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.render.resolution_x = 640
sc.render.resolution_y = 400
sc.render.film_transparent = False
sc.cycles.samples = 64

out = os.path.join(d, "..", "assets", "stations", "landing-craft.jpg")
sc.render.filepath = out
sc.render.image_settings.file_format = "JPEG"
sc.render.image_settings.quality = 88
bpy.ops.render.render(write_still=True)
print("RENDERED", out)
