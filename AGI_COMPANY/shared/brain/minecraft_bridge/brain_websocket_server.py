#!/usr/bin/env python3
"""
Brain WebSocket Server
Central hub for agent coordination

- Receives OODA updates from agents
- Sends commands to agents
- Coordinates multi-agent behavior
- Integrates with AOS Brain

Usage: python brain_websocket_server.py [--port 8767]
"""

import asyncio
import websockets
import json
import sys
import argparse
from datetime import datetime
from typing import Dict, Set

# Agent connections
agents: Dict[str, websockets.WebSocketServerProtocol] = {}
agent_states: Dict[str, dict] = {}

# Connected observers (brains, dashboards)
observers: Set[websockets.WebSocketServerProtocol] = set()

async def handle_agent(websocket, path):
    """Handle agent connection"""
    agent_id = None
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get('type')
                
                if msg_type == 'register_agent':
                    agent_id = data.get('agent_id')
                    agents[agent_id] = websocket
                    agent_states[agent_id] = {
                        'connected': datetime.now().isoformat(),
                        'capabilities': data.get('capabilities', []),
                        'position': data.get('position'),
                        'tick': 0
                    }
                    print(f"[Brain WS] Agent registered: {agent_id}")
                    
                    # Broadcast to observers
                    await broadcast_to_observers({
                        'type': 'agent_joined',
                        'agent_id': agent_id,
                        'timestamp': datetime.now().isoformat()
                    })
                
                elif msg_type == 'ooda_tick':
                    agent_id = data.get('agent_id')
                    if agent_id:
                        agent_states[agent_id].update({
                            'tick': data.get('tick'),
                            'observation': data.get('observation'),
                            'decision': data.get('decision'),
                            'action': data.get('action'),
                            'last_update': datetime.now().isoformat()
                        })
                        
                        # Forward to observers
                        await broadcast_to_observers({
                            'type': 'ooda_update',
                            'agent_id': agent_id,
                            'tick': data.get('tick'),
                            'decision': data.get('decision'),
                            'action': data.get('action')
                        })
                
                elif msg_type == 'chat_received':
                    # Agent received chat in Minecraft
                    print(f"[Brain WS] {data.get('from')} -> {agent_id}: {data.get('message')[:50]}...")
                    
                elif msg_type == 'action_complete':
                    # Agent completed action
                    print(f"[Brain WS] {agent_id} completed: {data.get('action')}")
                    
            except json.JSONDecodeError:
                print(f"[Brain WS] Invalid JSON from {agent_id}")
                
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if agent_id and agent_id in agents:
            del agents[agent_id]
            if agent_id in agent_states:
                del agent_states[agent_id]
            print(f"[Brain WS] Agent disconnected: {agent_id}")
            
            await broadcast_to_observers({
                'type': 'agent_left',
                'agent_id': agent_id,
                'timestamp': datetime.now().isoformat()
            })

async def handle_observer(websocket, path):
    """Handle observer (brain/dashboard) connection"""
    observers.add(websocket)
    print(f"[Brain WS] Observer connected")
    
    try:
        # Send current agent list
        await websocket.send(json.dumps({
            'type': 'agent_list',
            'agents': list(agent_states.keys()),
            'states': agent_states
        }))
        
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get('type')
                
                if msg_type == 'command_agent':
                    # Send command to specific agent
                    target = data.get('agent_id')
                    if target in agents:
                        await agents[target].send(json.dumps({
                            'type': 'command',
                            'command': data.get('command'),
                            'params': data.get('params', {})
                        }))
                        print(f"[Brain WS] Command sent to {target}: {data.get('command')}")
                
                elif msg_type == 'broadcast':
                    # Broadcast to all agents
                    await broadcast_to_agents({
                        'type': 'broadcast',
                        'message': data.get('message')
                    })
                
                elif msg_type == 'coordination':
                    # Multi-agent coordination
                    await handle_coordination(data)
                    
            except json.JSONDecodeError:
                pass
                
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        observers.discard(websocket)
        print("[Brain WS] Observer disconnected")

async def broadcast_to_agents(message):
    """Send message to all agents"""
    if agents:
        await asyncio.gather(
            *[agent.send(json.dumps(message)) for agent in agents.values()],
            return_exceptions=True
        )

async def broadcast_to_observers(message):
    """Send message to all observers"""
    if observers:
        await asyncio.gather(
            *[obs.send(json.dumps(message)) for obs in observers],
            return_exceptions=True
        )

async def handle_coordination(data):
    """Handle multi-agent coordination tasks"""
    task_type = data.get('task_type')
    
    if task_type == 'formation':
        # Agents form a pattern
        formation = data.get('formation', 'circle')
        agent_list = list(agents.keys())
        
        import math
        radius = 10
        for i, agent_id in enumerate(agent_list):
            angle = (2 * math.pi * i) / len(agent_list)
            x = data.get('center_x', 0) + radius * math.cos(angle)
            z = data.get('center_z', 0) + radius * math.sin(angle)
            y = data.get('center_y', 100)
            
            if agent_id in agents:
                await agents[agent_id].send(json.dumps({
                    'type': 'command',
                    'command': 'move_to',
                    'params': {'x': x, 'y': y, 'z': z}
                }))
    
    elif task_type == 'resource_gathering':
        # Assign agents to gather different resources
        targets = data.get('targets', ['wood', 'stone', 'coal'])
        agent_list = list(agents.keys())
        
        for i, agent_id in enumerate(agent_list):
            target = targets[i % len(targets)]
            if agent_id in agents:
                await agents[agent_id].send(json.dumps({
                    'type': 'command',
                    'command': 'mine_resources',
                    'params': {'target': target}
                }))
    
    elif task_type == 'build_structure':
        # Coordinate building project
        structure = data.get('structure', 'house')
        positions = data.get('positions', [])
        agent_list = list(agents.keys())
        
        for i, agent_id in enumerate(agent_list):
            if i < len(positions) and agent_id in agents:
                await agents[agent_id].send(json.dumps({
                    'type': 'skill_execution',
                    'skill': 'precision_place',
                    'params': positions[i]
                }))

async def status_reporter():
    """Periodic status report"""
    while True:
        await asyncio.sleep(30)
        
        if agent_states:
            print(f"\n[Brain WS] Status: {len(agent_states)} agents connected")
            for agent_id, state in agent_states.items():
                tick = state.get('tick', 0)
                action = state.get('action', {}).get('result', 'idle')
                print(f"  {agent_id:15s} tick={tick:6d} action={action}")

async def main():
    parser = argparse.ArgumentParser(description="Brain WebSocket Server")
    parser.add_argument("--port", type=int, default=8767, help="WebSocket port")
    args = parser.parse_args()
    
    print(f"[Brain WS] Starting server on port {args.port}")
    
    # Start agent endpoint
    agent_server = await websockets.serve(
        handle_agent,
        "0.0.0.0",
        args.port
    )
    
    # Start observer endpoint on different port
    observer_server = await websockets.serve(
        handle_observer,
        "0.0.0.0",
        args.port + 1
    )
    
    print(f"[Brain WS] Agent endpoint: ws://localhost:{args.port}")
    print(f"[Brain WS] Observer endpoint: ws://localhost:{args.port + 1}")
    print("[Brain WS] Press Ctrl+C to stop\n")
    
    # Start status reporter
    asyncio.create_task(status_reporter())
    
    try:
        await asyncio.Future()  # Run forever
    except asyncio.CancelledError:
        pass
    finally:
        agent_server.close()
        observer_server.close()
        await agent_server.wait_closed()
        await observer_server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Brain WS] Server stopped")
