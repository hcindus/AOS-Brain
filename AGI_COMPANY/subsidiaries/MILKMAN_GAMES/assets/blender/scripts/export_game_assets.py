# Blender Game Asset Pipeline - Automated Export Script
# Compatible: Blender 3.0+ (tested on 4.2)
# Usage: Run from Blender Script Editor or headless: blender --python export_game_assets.py

import bpy
import os
import json
from datetime import datetime

class GameAssetExporter:
    """Automated exporter for Unity/Unreal game assets"""
    
    def __init__(self, output_base="/root/.openclaw/workspace/aocros/games/assets/blender/exports"):
        self.output_base = output_base
        self.export_log = []
        
        # Ensure output directories exist
        for fmt in ['fbx', 'gltf', 'obj']:
            os.makedirs(os.path.join(output_base, fmt), exist_ok=True)
    
    def log(self, message):
        """Log export operations"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.export_log.append(f"[{timestamp}] {message}")
        print(message)
    
    def prepare_model(self):
        """Clean up model before export"""
        # Apply all transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Clear custom split normals data (can cause issues)
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj.data.use_auto_smooth = False
                if obj.data.has_custom_normals:
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.mesh.customdata_custom_splitnormals_clear()
        
        self.log("Model prepared: transforms applied, normals cleared")
    
    def export_fbx(self, name, for_engine="unity"):
        """
        Export FBX for Unity or Unreal
        
        Args:
            name: Asset name
            for_engine: 'unity' or 'unreal'
        """
        filepath = os.path.join(self.output_base, "fbx", f"{name}.fbx")
        
        # Base FBX settings
        fbx_settings = {
            'filepath': filepath,
            'use_selection': True,
            'global_scale': 1.0,
            'apply_unit_scale': True,
            'apply_scale_options': 'FBX_SCALE_UNITS',
            'axis_forward': '-Z',
            'axis_up': 'Y',
            'bake_space_transform': True,
            'use_mesh_edges': False,
            'use_mesh_modifiers': True,
            'mesh_smooth_type': 'OFF',
            'use_subsurf': False,
            'use_custom_props': True,
            'add_leaf_bones': False,
            'primary_bone_axis': 'Y',
            'secondary_bone_axis': 'X',
            'use_armature_deform_only': False,
            'bake_anim': True,
            'bake_anim_use_all_bones': True,
            'bake_anim_use_nla_strips': True,
            'bake_anim_use_all_actions': True,
            'bake_anim_force_startend_keying': True,
            'path_mode': 'AUTO',
            'embed_textures': False,
        }
        
        # Engine-specific overrides
        if for_engine == "unreal":
            fbx_settings['global_scale'] = 1.0
            fbx_settings['primary_bone_axis'] = 'Y'
            fbx_settings['secondary_bone_axis'] = 'X'
        else:  # unity
            fbx_settings['global_scale'] = 1.0
            fbx_settings['primary_bone_axis'] = 'Y'
            fbx_settings['secondary_bone_axis'] = 'X'
        
        bpy.ops.export_scene.fbx(**fbx_settings)
        self.log(f"Exported FBX ({for_engine}): {filepath}")
        return filepath
    
    def export_gltf(self, name, format='GLB'):
        """
        Export glTF/glb (WebGL/mobile friendly)
        
        Args:
            name: Asset name
            format: 'GLB' (binary) or 'GLTF_SEPARATE'
        """
        ext = "glb" if format == 'GLB' else "gltf"
        filepath = os.path.join(self.output_base, "gltf", f"{name}.{ext}")
        
        gltf_settings = {
            'filepath': filepath,
            'export_format': format,
            'use_selection': True,
            'export_yup': True,
            'export_apply': True,
            'export_texcoords': True,
            'export_normals': True,
            'export_tangents': True,
            'export_materials': 'EXPORT',
            'export_image_format': 'AUTO',
            'export_skins': True,
            'export_morph': True,
            'export_animations': True,
            'export_animation_mode': 'ACTIONS',
            'export_frame_range': True,
            'export_force_sampling': True,
        }
        
        bpy.ops.export_scene.gltf(**gltf_settings)
        self.log(f"Exported glTF: {filepath}")
        return filepath
    
    def export_obj(self, name):
        """Export OBJ (legacy/import compatibility)"""
        filepath = os.path.join(self.output_base, "obj", f"{name}.obj")
        
        bpy.ops.wm.obj_export(
            filepath=filepath,
            export_selected_objects=True,
            apply_modifiers=True,
            global_scale=1.0,
            forward_axis='NEGATIVE_Z',
            up_axis='Y',
        )
        self.log(f"Exported OBJ: {filepath}")
        return filepath
    
    def export_all_formats(self, name, engines=['unity', 'unreal']):
        """Export asset in all supported formats"""
        self.prepare_model()
        
        results = {}
        
        # FBX for each engine
        for engine in engines:
            engine_name = f"{name}_{engine}"
            results[f'fbx_{engine}'] = self.export_fbx(engine_name, engine)
        
        # glTF (universal)
        results['gltf'] = self.export_gltf(name, 'GLB')
        results['gltf_separate'] = self.export_gltf(f"{name}_separate", 'GLTF_SEPARATE')
        
        # OBJ (legacy)
        results['obj'] = self.export_obj(name)
        
        # Save export log
        self.save_export_log(name)
        
        return results
    
    def save_export_log(self, asset_name):
        """Save export log to JSON"""
        log_path = os.path.join(self.output_base, f"{asset_name}_export_log.json")
        with open(log_path, 'w') as f:
            json.dump({
                'asset_name': asset_name,
                'exports': self.export_log,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        self.log(f"Export log saved: {log_path}")


def batch_export_from_collection(collection_name, prefix=""):
    """
    Export all objects from a collection
    
    Usage:
        batch_export_from_collection("Props", "PR_")
    """
    exporter = GameAssetExporter()
    collection = bpy.data.collections.get(collection_name)
    
    if not collection:
        print(f"Collection '{collection_name}' not found!")
        return
    
    for obj in collection.objects:
        if obj.type == 'MESH':
            # Deselect all
            bpy.ops.object.select_all(action='DESELECT')
            
            # Select object
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            
            # Export
            asset_name = f"{prefix}{obj.name}"
            exporter.export_all_formats(asset_name)
    
    print(f"Batch export complete for collection: {collection_name}")


def export_active_object(asset_name, engines=['unity', 'unreal']):
    """
    Quick export of the active selected object
    
    Usage (in Blender):
        import sys
        sys.path.append('/root/.openclaw/workspace/aocros/games/assets/blender/scripts')
        from export_game_assets import export_active_object
        export_active_object("MyCharacter", ['unity', 'unreal'])
    """
    exporter = GameAssetExporter()
    exporter.export_all_formats(asset_name, engines)
    print(f"Export complete: {asset_name}")


# If run directly in Blender with an active object
if __name__ == "__main__":
    if bpy.context.active_object:
        export_active_object(bpy.context.active_object.name)
    else:
        print("No active object selected!")
