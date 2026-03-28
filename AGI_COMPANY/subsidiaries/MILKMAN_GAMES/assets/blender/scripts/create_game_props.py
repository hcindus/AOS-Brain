# Blender Python Script: Create Modular Game Props
# Generates reusable low-poly props for DaVerse with proper scale and topology

import bpy
import bmesh
import math
import os

class PropBuilder:
    """Creates game-ready modular props"""
    
    def __init__(self):
        self.props = {}
        self.collection = None
        
    def setup_collection(self, name="Props_Base"):
        """Create organized collection for props"""
        if name in bpy.data.collections:
            bpy.data.collections.remove(bpy.data.collections[name])
        
        self.collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(self.collection)
        
        # Set up scene for metric units
        bpy.context.scene.unit_settings.system = 'METRIC'
        bpy.context.scene.unit_settings.scale_length = 1.0
    
    def cleanup(self):
        """Remove existing mesh objects"""
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()
    
    def create_crate(self, size=1.0, damaged=False):
        """
        Create wooden crate prop
        
        Args:
            size: Base size in meters
            damaged: Add damage variations
        """
        bpy.ops.mesh.primitive_cube_add(size=size, location=(0, 0, size/2))
        crate = bpy.context.active_object
        crate.name = "PR_Crate_Wood_01"
        
        # Add wood grain detail
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=2)
        
        if damaged:
            bm = bmesh.from_mesh(crate.data)
            bm.verts.ensure_lookup_table()
            
            # Randomly displace some vertices for damage
            import random
            random.seed(42)
            for vert in bm.verts:
                if random.random() < 0.1:
                    vert.co.x += random.uniform(-0.05, 0.05) * size
                    vert.co.y += random.uniform(-0.05, 0.05) * size
            
            bmesh.to_mesh(bm, crate.data)
            bm.free()
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Add material
        mat = bpy.data.materials.new(name="MAT_Wood_Crate")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (0.4, 0.25, 0.15, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.8
        
        crate.data.materials.append(mat)
        
        # Set origin to bottom
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        crate.location.z = size/2
        
        self.props['crate'] = crate
        return crate
    
    def create_barrel(self, height=1.2, radius=0.4):
        """Create metal barrel with proper topology"""
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=radius,
            depth=height,
            location=(0, 0, height/2)
        )
        barrel = bpy.context.active_object
        barrel.name = "PR_Barrel_Metal_01"
        
        # Bulge the barrel slightly using proportional editing
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.resize(value=(1.08, 1.08, 1.0), orient_type='GLOBAL')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Metal material
        mat = bpy.data.materials.new(name="MAT_Metal_Barrel")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (0.3, 0.35, 0.4, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.9
            bsdf.inputs['Roughness'].default_value = 0.4
        
        barrel.data.materials.append(mat)
        
        self.props['barrel'] = barrel
        return barrel
    
    def create_rock(self, scale=1.0, detail_level='medium'):
        """Create procedural low-poly rock"""
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=2 if detail_level == 'low' else 3,
            radius=0.5 * scale,
            location=(0, 0, 0.3 * scale)
        )
        rock = bpy.context.active_object
        rock.name = f"PR_Rock_01_{detail_level}"
        
        # Randomize shape
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.vertex_random(offset=0.15 * scale)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Flatten bottom
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_mesh(rock.data)
        
        for vert in bm.verts:
            if vert.co.z < 0:
                vert.co.z = 0
        
        bmesh.to_mesh(bm, rock.data)
        bm.free()
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rock material
        mat = bpy.data.materials.new(name="MAT_Rock_Gray")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (0.4, 0.42, 0.45, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.9
        
        rock.data.materials.append(mat)
        
        self.props['rock'] = rock
        return rock
    
    def create_platform_tile(self, size=2.0, style='industrial'):
        """Create modular floor/platform tile"""
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=(0, 0, -0.05)
        )
        tile = bpy.context.active_object
        tile.name = f"EN_Floor_{style.title()}_01"
        tile.scale = (size/2, size/2, 0.05)
        bpy.ops.object.transform_apply(scale=True)
        
        # Add grid pattern
        bpy.ops.object.mode_set(mode='EDIT')
        
        if style == 'industrial':
            # Add beveled edges
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.subdivide(number_cuts=2)
            bpy.ops.mesh.select_all(action='DESELECT')
            
            # Select edge loop and bevel
            bm = bmesh.from_mesh(tile.data)
            for edge in bm.edges:
                if edge.is_boundary:
                    edge.select = True
            bmesh.to_mesh(bm, tile.data)
            bm.free()
            
            bpy.ops.mesh.bevel(offset=0.02, segments=2)
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Material based on style
        mat = bpy.data.materials.new(name=f"MAT_Floor_{style}")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            if style == 'industrial':
                bsdf.inputs['Base Color'].default_value = (0.2, 0.22, 0.25, 1.0)
                bsdf.inputs['Metallic'].default_value = 0.3
                bsdf.inputs['Roughness'].default_value = 0.7
            else:  # concrete
                bsdf.inputs['Base Color'].default_value = (0.6, 0.6, 0.62, 1.0)
                bsdf.inputs['Roughness'].default_value = 0.9
        
        tile.data.materials.append(mat)
        
        self.props[f'floor_{style}'] = tile
        return tile
    
    def create_wall_panel(self, width=2.0, height=2.5, style='metal'):
        """Create modular wall panel"""
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=(0, 0, height/2)
        )
        panel = bpy.context.active_object
        panel.name = f"EN_Wall_{style.title()}_01"
        panel.scale = (0.1, width/2, height/2)
        bpy.ops.object.transform_apply(scale=True)
        
        # Add rivets/panels
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # Add inset panels
        bpy.ops.mesh.primitive_plane_add(size=0.5, location=(0.06, 0, height/2))
        bpy.ops.object.mode_set(mode='OBJECT')
        
        panel_mat = bpy.data.materials.new(name=f"MAT_Wall_{style}")
        panel_mat.use_nodes = True
        nodes = panel_mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            if style == 'metal':
                bsdf.inputs['Base Color'].default_value = (0.35, 0.38, 0.42, 1.0)
                bsdf.inputs['Metallic'].default_value = 0.7
                bsdf.inputs['Roughness'].default_value = 0.5
            else:  # concrete
                bsdf.inputs['Base Color'].default_value = (0.55, 0.55, 0.57, 1.0)
                bsdf.inputs['Roughness'].default_value = 0.95
        
        panel.data.materials.append(panel_mat)
        
        self.props[f'wall_{style}'] = panel
        return panel
    
    def create_weapon_crate(self):
        """Create sci-fi weapon crate"""
        # Base box
        bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, 0, 0.3))
        crate = bpy.context.active_object
        crate.name = "PR_Crate_Weapon_01"
        
        # Detail - add strips
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.3))
        strip_v = bpy.context.active_object
        strip_v.name = "PR_Crate_Weapon_Strip_V"
        strip_v.scale = (0.65, 0.1, 0.62)
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.3))
        strip_h = bpy.context.active_object
        strip_h.name = "PR_Crate_Weapon_Strip_H"
        strip_h.scale = (0.1, 0.65, 0.62)
        
        # Corner guards
        for x, y in [(-0.25, -0.25), (0.25, -0.25), (-0.25, 0.25), (0.25, 0.25)]:
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.05,
                depth=0.65,
                location=(x, y, 0.3)
            )
            corner = bpy.context.active_object
            corner.name = f"PR_Crate_Weapon_Corner_{x}_{y}"
        
        # Sci-fi material
        mat = bpy.data.materials.new(name="MAT_Crate_SciFi")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (0.15, 0.18, 0.22, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.4
            bsdf.inputs['Roughness'].default_value = 0.3
        
        crate.data.materials.append(mat)
        
        self.props['weapon_crate'] = crate
        return crate
    
    def add_to_collection(self):
        """Move all props to collection"""
        for obj in bpy.context.scene.objects:
            if obj.name.startswith(("PR_", "EN_")):
                for coll in obj.users_collection:
                    coll.objects.unlink(obj)
                self.collection.objects.link(obj)
    
    def build_all_props(self):
        """Create complete prop library"""
        print("Building game prop library...")
        
        self.cleanup()
        self.setup_collection()
        
        # Create props
        self.create_crate(size=1.0, damaged=True)
        self.create_barrel(height=1.2, radius=0.4)
        self.create_rock(scale=1.0, detail_level='medium')
        self.create_platform_tile(size=2.0, style='industrial')
        self.create_wall_panel(width=2.0, height=2.5, style='metal')
        self.create_weapon_crate()
        
        self.add_to_collection()
        
        print(f"Created {len(self.props)} props: {list(self.props.keys())}")
        return self.props


def main():
    """Main entry point"""
    builder = PropBuilder()
    return builder.build_all_props()


if __name__ == "__main__":
    main()
to_collection()
        
        print(f"Created {len(self.props)} props: {list(self.props.keys())}")
        return self.props


def main():
    """Main entry point"""
    builder = PropBuilder()
    return builder.build_all_props()


if __name__ == "__main__":
    main()
