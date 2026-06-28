#!/usr/bin/env python3
"""
AOS BRAIN SOCKET COMMANDS v1.0
Extracted command execution logic for secure socket server
"""

import json
import time
from liver_v1 import BloodSample, LiverState


def execute_command(brain, cmd: str, params: dict) -> dict:
    """
    Execute a brain command with all security checks already passed
    This is called by the secure socket server after validation
    """
    
    if cmd == 'status':
        status = brain.get_status()
        return status
    
    elif cmd == 'ping':
        return {'pong': True, 'tick': brain.tick_count}
    
    elif cmd == 'pause':
        brain.paused = True
        return {'success': True, 'state': 'paused'}
    
    elif cmd == 'resume':
        brain.paused = False
        return {'success': True, 'state': 'resumed'}
    
    elif cmd == 'get_phase':
        return {'phase': brain.current_phase}
    
    elif cmd == 'get_heart':
        if hasattr(brain, 'heart') and brain.heart:
            return {
                'bpm': brain.heart.rhythm.bpm,
                'state': str(brain.heart.rhythm.state)
            }
        return {'error': 'Heart not available'}
    
    elif cmd == 'thyroid':
        if brain.thyroid:
            return brain.thyroid.get_status()
        return {'error': 'Thyroid not available'}
    
    elif cmd == 'liver':
        if brain.liver:
            return brain.liver.get_status()
        return {'error': 'Liver not available'}
    
    elif cmd == 'kidneys':
        if brain.kidneys:
            return brain.kidneys.get_status()
        return {'error': 'Kidneys not available'}
    
    elif cmd == 'lungs':
        if brain.lungs:
            return brain.lungs.get_status()
        return {'error': 'Lungs not available'}
    
    elif cmd == 'breathe':
        if brain.lungs:
            ambient = params.get('ambient', [])
            valence = params.get('valence', 0.0)
            demand = params.get('demand', 1.0)
            o2, waste = brain.lungs.step(ambient, valence, demand)
            return {
                'oxygen': o2.to_dict(),
                'waste': waste.to_dict()
            }
        return {'error': 'Lungs not available'}
    
    elif cmd == 'hold_breath':
        if brain.lungs:
            brain.lungs.hold_breath()
            return {'status': 'breath_held'}
        return {'error': 'Lungs not available'}
    
    elif cmd == 'release_breath':
        if brain.lungs:
            brain.lungs.release_breath()
            return {'status': 'breath_released'}
        return {'error': 'Lungs not available'}
    
    elif cmd == 'router':
        if brain.router:
            return {
                'models': brain.router.MODELS,
                'stats': brain.router.get_stats()
            }
        return {'error': 'Router not available'}
    
    elif cmd == 'decide':
        context = params.get('context', {})
        if brain.router:
            action, confidence = brain.router.decide(context)
            return {'action': action, 'confidence': confidence}
        return {'error': 'Router not available'}
    
    elif cmd == 'speak':
        message = params.get('message', '')
        context = params.get('context', {})
        if brain.router:
            response = brain.router.speak(message, context)
            return {'response': response}
        return {'error': 'Router not available'}
    
    elif cmd == 'stimulate':
        importance = params.get('importance', 0.8)
        if brain.thyroid:
            stimulated = brain.thyroid.stimulate(importance=importance)
            return {'stimulated': stimulated, 'state': brain.thyroid.state.name}
        return {'error': 'Thyroid not available'}
    
    elif cmd == 'filter':
        content = params.get('content', '')
        source = params.get('source', 'socket')
        if brain.liver:
            sample = BloodSample(source, content, time.time(), 1.0)
            state, result, meta = brain.liver.process(sample)
            return {'state': state.name, 'result': result, 'metadata': meta}
        return {'error': 'Liver not available'}
    
    elif cmd == 'seed_layers':
        seed_path = params.get('path', '/root/.openclaw/workspace/aos/layer_export.json')
        try:
            with open(seed_path, 'r') as f:
                data = json.load(f)
            
            # Seed subconscious
            for item in data.get('subconscious', []):
                brain.consciousness.subconscious.add(
                    item['content'],
                    intensity=item.get('intensity', 0.7),
                    associations=item.get('associations', [])
                )
            
            # Seed unconscious
            for item in data.get('unconscious', []):
                brain.consciousness.unconscious.add(
                    item['content'],
                    intensity=item.get('intensity', 0.8),
                    associations=item.get('associations', [])
                )
            
            sub_count = len(brain.consciousness.subconscious.get_active(min_intensity=0.3))
            unc_count = len(brain.consciousness.unconscious.get_active(min_intensity=0.3))
            
            return {
                'seeded': True,
                'subconscious_seeded': len(data.get('subconscious', [])),
                'unconscious_seeded': len(data.get('unconscious', [])),
                'subconscious_active': sub_count,
                'unconscious_active': unc_count
            }
        except Exception as e:
            return {'error': str(e)}
    
    elif cmd == 'add_to_layer':
        layer = params.get('layer', 'subconscious')
        content = params.get('content', '')
        intensity = params.get('intensity', 0.8)
        associations = params.get('associations', [])
        
        # Content has already been filtered through Liver by security layer
        target_layer = None
        if layer == 'conscious':
            target_layer = brain.consciousness.conscious
        elif layer == 'subconscious':
            target_layer = brain.consciousness.subconscious
        elif layer == 'unconscious':
            target_layer = brain.consciousness.unconscious
        
        if target_layer:
            target_layer.add(content, intensity=intensity, associations=associations)
            active_count = len(target_layer.get_active(min_intensity=0.3))
            return {
                'added': True,
                'layer': layer,
                'content': content[:50],
                'active_items': active_count
            }
        return {'error': f'Unknown layer: {layer}'}
    
    elif cmd == 'perceive':
        observation = params.get('observation', '')
        intensity = params.get('intensity', 0.8)
        if brain.consciousness:
            brain.consciousness.perceive(observation, intensity=intensity)
            brain.consciousness.consolidate()
            con = len(brain.consciousness.conscious.get_active())
            sub = len(brain.consciousness.subconscious.get_active(min_intensity=0.1))
            unc = len(brain.consciousness.unconscious.get_active(min_intensity=0.1))
            return {
                'perceived': True,
                'observation': observation[:50],
                'intensity': intensity,
                'conscious_items': con,
                'subconscious_items': sub,
                'unconscious_items': unc
            }
        return {'error': 'Consciousness not available'}
    
    elif cmd == 'ingest':
        content = params.get('content', '')
        source = params.get('source', 'socket')
        priority = params.get('priority', 0.8)
        
        # SECURITY: Content has already been filtered through Liver
        if brain.stomach:
            brain.stomach.ingest(source, content, priority=priority)
            
            buffer_size = len(brain.stomach.input_buffer)
            state = brain.stomach.state.name if hasattr(brain.stomach.state, 'name') else str(brain.stomach.state)
            
            return {
                'ingested': True,
                'source': source,
                'buffer_size': buffer_size,
                'stomach_state': state,
                'liver_filtered': True,
                'message': 'Content queued in stomach (pre-filtered)'
            }
        return {'error': 'Stomach not available'}
    
    elif cmd == 'save':
        if hasattr(brain, 'persistence') and brain.persistence:
            success = brain.persistence.save_state(force=True)
            tick = getattr(brain, 'tick_count', 0)
            return {
                'saved': success,
                'tick': tick,
                'state_file': str(brain.persistence.STATE_FILE) if success else None
            }
        return {'error': 'Persistence not available'}
    
    elif cmd == 'load':
        if hasattr(brain, 'persistence') and brain.persistence:
            state = brain.persistence.load_state()
            if state:
                return {
                    'loaded': True,
                    'tick': state.get('tick_count', 0),
                    'saved_at': state.get('saved_at', 'unknown'),
                    'has_cortex': state.get('cortex') is not None,
                    'has_tracray': state.get('tracray') is not None
                }
            return {'loaded': False, 'message': 'No saved state found'}
        return {'error': 'Persistence not available'}
    
    elif cmd == 'tick':
        return {
            'tick': getattr(brain, 'tick_count', 0),
            'phase': getattr(brain, 'current_phase', 'unknown')
        }
    
    elif cmd == 'cortex_register':
        agent_id = params.get('agent_id', 'anonymous')
        success = brain.cortex.register_agent(agent_id)
        return {'registered': success, 'agent_id': agent_id}
    
    elif cmd == 'cortex_write':
        from cortex_v25_optimized import AgentWriteRequest
        agent_id = params.get('agent_id', 'anonymous')
        regions = params.get('regions', list(range(8)))
        activations = params.get('activations', [])
        priority = params.get('priority', 1.0)
        ephemeral = params.get('ephemeral', False)
        
        request = AgentWriteRequest(
            agent_id=agent_id,
            region_indices=regions,
            activations=[(a[0], a[1], a[2], a[3]) for a in activations],
            priority=priority,
            ephemeral=ephemeral
        )
        result = brain.cortex.agent_write(request)
        return {'write_result': result}
    
    elif cmd == 'cortex_read':
        from cortex_v25_optimized import AgentReadRequest
        agent_id = params.get('agent_id', 'anonymous')
        regions = params.get('regions', list(range(8)))
        max_hotspots = params.get('max_hotspots', 64)
        
        request = AgentReadRequest(
            agent_id=agent_id,
            region_indices=regions,
            layer_mask=params.get('layer_mask', 0b111),
            max_hotspots=max_hotspots
        )
        snapshot = brain.cortex.agent_read(request)
        return {
            'tick': snapshot.tick,
            'coherence': snapshot.coherence,
            'pattern_hash': snapshot.pattern_hash,
            'hotspot_count': len(snapshot.hotspots),
            'hotspots': [{"x": c[0], "y": c[1], "z": c[2], "val": v} 
                       for c, v in list(snapshot.hotspots.items())[:max_hotspots]]
        }
    
    elif cmd == 'cortex_tick':
        result = brain.cortex.tick_parallel()
        return {
            'tick': result['tick'],
            'active_nodes': result['active_nodes'],
            'sparsity': result['sparsity'],
            'tick_time_ms': result['tick_time_ms']
        }
    
    elif cmd == 'cortex_stats':
        perf = brain.cortex.get_performance_stats()
        agent_stats = brain.cortex.get_agent_stats()
        return {
            'performance': perf,
            'agents': agent_stats,
            'current_tick': brain.cortex.current_tick
        }
    
    elif cmd == 'security':
        """Get security layer status"""
        if hasattr(brain, 'socket_server') and hasattr(brain.socket_server, 'security'):
            return brain.socket_server.security.get_security_status()
        return {'error': 'Security layer not available'}
    
    else:
        return {'error': f'Unknown command: {cmd}'}
