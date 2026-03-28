# Blender Python Script: Create Modular Game-Ready Character
# Creates a base low-poly character with proper topology for DaVerse
# Usage: Run in Blender Script Editor

import bpy
import bmesh
import math

class ModularCharacterBuilder:
    """Creates a modular, game-ready character base mesh"""
    
    def __init__(self):
        self.collection = None
        self.parts = {}
        
    def setup_scene(self):
        """Prepare scene for character creation"""
        # Clear existing mesh objects
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()
        
        # Create new collection
        if "Character_Base" in bpy.data.collections:
            bpy.data.collections.remove(bpy.data.collections["Character_Base"])
        
        self.collection = bpy.data.collections.new("Character_Base")
        bpy.context.scene.collection.children.link(self.collection)
        
        # Set units to metric
        bpy.context.scene.unit_settings.system = 'METRIC'
        bpy.context.scene.unit_settings.scale_length = 1.0
        
    def create_torso(self):
        """Create torso base mesh"""
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.25,
            depth=0.5,
            location=(0, 0, 1.0)
        )
        torso = bpy.context.active_object
        torso.name = "CH_Base_Torso"
        
        # Shape the torso slightly by scaling in object mode
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        # Use proportional editing for taper effect
        bpy.ops.transform.resize(value=(1.1, 1.05, 1.0), orient_type='GLOBAL')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        self.parts['torso'] = torso
        return torso
    
    def create_head(self):
        """Create head base mesh"""
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.12,
            location=(0, 0, 1.45)
        )
        head = bpy.context.active_object
        head.name = "CH_Base_Head"
        
        # Scale to make it more head-like
        head.scale = (0.85, 1.0, 1.1)
        bpy.ops.object.transform_apply(scale=True)
        
        self.parts['head'] = head
        return head
    
    def create_limbs(self):
        """Create arms and legs"""
        # Arms
        for side, x_pos in [('L', -0.35), ('R', 0.35)]:
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8,
                radius=0.06,
                depth=0.55,
                location=(x_pos, 0, 1.15)
            )
            arm = bpy.context.active_object
            arm.name = f"CH_Base_Arm_{side}"
            self.parts[f'arm_{side.lower()}'] = arm
        
        # Legs
        for side, x_pos in [('L', -0.12), ('R', 0.12)]:
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8,
                radius=0.08,
                depth=0.75,
                location=(x_pos, 0, 0.45)
            )
            leg = bpy.context.active_object
            leg.name = f"CH_Base_Leg_{side}"
            self.parts[f'leg_{side.lower()}'] = leg
    
    def create_hand(self, side):
        """Create a simple low-poly hand"""
        x_pos = -0.38 if side == 'L' else 0.38
        
        # Palm
        bpy.ops.mesh.primitive_cube_add(
            size=0.08,
            location=(x_pos, 0, 0.82)
        )
        palm = bpy.context.active_object
        palm.name = f"CH_Base_Hand_{side}"
        palm.scale = (0.3, 0.8, 1.0)
        bpy.ops.object.transform_apply(scale=True)
        
        # Fingers (simplified)
        for i in range(4):
            bpy.ops.mesh.primitive_cube_add(
                size=0.02,
                location=(x_pos, (i - 1.5) * 0.025, 0.77)
            )
            finger = bpy.context.active_object
            finger.name = f"CH_Base_Finger_{side}_{i}"
            finger.scale = (0.5, 1.0, 2.0)
            bpy.ops.object.transform_apply(scale=True)
        
        self.parts[f'hand_{side.lower()}'] = palm
    
    def create_feet(self):
        """Create simple feet"""
        for side, x_pos in [('L', -0.12), ('R', 0.12)]:
            bpy.ops.mesh.primitive_cube_add(
                size=0.08,
                location=(x_pos, 0.08, 0.04)
            )
            foot = bpy.context.active_object
            foot.name = f"CH_Base_Foot_{side}"
            foot.scale = (1.2, 2.0, 0.6)
            bpy.ops.object.transform_apply(scale=True)
            self.parts[f'foot_{side.lower()}'] = foot
    
    def setup_materials(self):
        """Create basic PBR materials"""
        # Skin material
        skin_mat = bpy.data.materials.new(name="MAT_Base_Skin")
        skin_mat.use_nodes = True
        nodes = skin_mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (0.8, 0.6, 0.5, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.6
        
        # Apply to head and hands
        if 'head' in self.parts:
            self.parts['head'].data.materials.append(skin_mat)
    
    def setup_modularity(self):
        """Setup for modular character system"""
        # Create empty parent for rigging
        bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0.9))
        root = bpy.context.active_object
        root.name = "CH_Base_Root"
        root.empty_display_size = 0.3
        
        # Parent all parts to root
        for part_name, part in self.parts.items():
            if part and part != root:
                part.parent = root
                part.matrix_parent_inverse = root.matrix_world.inverted()
    
    def create_base_rig(self):
        """Create basic armature for character"""
        bpy.ops.object.armature_add(location=(0, 0, 0.9))
        armature = bpy.context.active_object
        armature.name = "CH_Base_Armature"
        armature.show_in_front = True
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Get the single bone and rename
        bone = armature.data.edit_bones[0]
        bone.name = "root"
        bone.head = (0, 0, 0)
        bone.tail = (0, 0, 0.3)
        
        # Spine
        spine = armature.data.edit_bones.new("spine")
        spine.head = (0, 0, 0.75)
        spine.tail = (0, 0, 1.0)
        spine.parent = bone
        
        # Chest
        chest = armature.data.edit_bones.new("chest")
        chest.head = (0, 0, 1.0)
        chest.tail = (0, 0, 1.25)
        chest.parent = spine
        
        # Head
        head = armature.data.edit_bones.new("head")
        head.head = (0, 0, 1.35)
        head.tail = (0, 0, 1.6)
        head.parent = chest
        
        # Arms
        for side, x in [('L', -0.3), ('R', 0.3)]:
            upper_arm = armature.data.edit_bones.new(f"upper_arm_{side}")
            upper_arm.head = (x, 0, 1.3)
            upper_arm.tail = (x, 0, 1.0)
            upper_arm.parent = chest
            
            lower_arm = armature.data.edit_bones.new(f"lower_arm_{side}")
            lower_arm.head = (x, 0, 1.0)
            lower_arm.tail = (x, 0, 0.7)
            lower_arm.parent = upper_arm
            
            hand = armature.data.edit_bones.new(f"hand_{side}")
            hand.head = (x, 0, 0.7)
            hand.tail = (x, 0, 0.6)
            hand.parent = lower_arm
        
        # Legs
        for side, x in [('L', -0.12), ('R', 0.12)]:
            upper_leg = armature.data.edit_bones.new(f"upper_leg_{side}")
            upper_leg.head = (x, 0, 0.75)
            upper_leg.tail = (x, 0, 0.45)
            upper_leg.parent = spine
            
            lower_leg = armature.data.edit_bones.new(f"lower_leg_{side}")
            lower_leg.head = (x, 0, 0.45)
            lower_leg.tail = (x, 0, 0.1)
            lower_leg.parent = upper_leg
            
            foot = armature.data.edit_bones.new(f"foot_{side}")
            foot.head = (x, 0, 0.1)
            foot.tail = (x, 0.1, 0.0)
            foot.parent = lower_leg
        
        bpy.ops.object.mode_set(mode='OBJECT')
        self.parts['armature'] = armature
        
        return armature
    
    def add_to_collection(self):
        """Move all parts to the character collection"""
        for obj in bpy.context.scene.objects:
            if obj.name.startswith("CH_Base"):
                # Unlink from all collections
                for coll in obj.users_collection:
                    coll.objects.unlink(obj)
                # Link to our collection
                self.collection.objects.link(obj)
    
    def build_character(self):
        """Execute full character build"""
        print("Building modular character base...")
        
        self.setup_scene()
        self.create_torso()
        self.create_head()
        self.create_limbs()
        self.create_hand('L')
        self.create_hand('R')
        self.create_feet()
        self.setup_materials()
        self.create_base_rig()
        self.setup_modularity()
        self.add_to_collection()
        
        print("Character build complete!")
        print(f"Parts created: {list(self.parts.keys())}")
        
        return self.parts


def main():
    """Main entry point"""
    builder = ModularCharacterBuilder()
    return builder.build_character()


if __name__ == "__main__":
    main()
