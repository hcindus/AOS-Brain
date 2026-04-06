#!/usr/bin/env python3
"""
DUAL SYSTEMS - 3D Space Combat Game
Python implementation using Pygame + ModernGL

Features:
- 3D wireframe tetrahedron ships (Flash Gordon style)
- Dual solar systems with gravity physics
- Neural network AI enemies with OODA loop decision making
- Three view modes: top-down, first-person, third-person
- Shields, power management, weapons system
- Factions (red, blue, green, purple)
- Procedural debris fields
- Starfield background
- Keyboard controls
- HUD with score, shields, power, speed
"""

import pygame
import moderngl
import numpy as np
from typing import List, Dict, Tuple, Optional
import glm
import math
import random
from dataclasses import dataclass
from enum import Enum
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Faction colors
FACTION_COLORS = {
    'player': (0.267, 0.533, 1.0),    # Blue
    'red': (1.0, 0.267, 0.267),       # Red
    'green': (0.267, 1.0, 0.267),     # Green
    'purple': (0.667, 0.267, 1.0)     # Purple
}

class ViewMode(Enum):
    THIRD_PERSON = "third"
    FIRST_PERSON = "first"
    TOP_DOWN = "top"

@dataclass
class Particle:
    position: glm.vec3
    velocity: glm.vec3
    color: Tuple[float, float, float]
    lifetime: float
    max_lifetime: float
    size: float

@dataclass
class Projectile:
    position: glm.vec3
    velocity: glm.vec3
    faction: str
    damage: float
    lifetime: float = 2.0

class NeuralAI:
    """Neural AI with OODA Loop (Observe-Orient-Decide-Act)"""
    
    def __init__(self):
        # Simple neural network: 8 inputs -> 16 hidden -> 4 outputs
        self.weights1 = np.random.randn(8, 16) * 0.5
        self.weights2 = np.random.randn(16, 4) * 0.5
        self.bias1 = np.zeros(16)
        self.bias2 = np.zeros(4)
        
        # OODA state
        self.observe = {
            'player_distance': 0.0,
            'player_angle': 0.0,
            'health': 100.0,
            'allies': 0
        }
        
        self.orient = {
            'threat_level': 0.0,
            'opportunity': 0.0,
            'tactical_position': 'neutral'
        }
        
        self.decide = {
            'action': 'attack',
            'aggression': 0.5
        }
        
        self.shoot_cooldown = 0.0
        self.state_timer = 0.0
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def predict(self, inputs: np.ndarray) -> np.ndarray:
        hidden = self.sigmoid(np.dot(inputs, self.weights1) + self.bias1)
        outputs = self.sigmoid(np.dot(hidden, self.weights2) + self.bias2)
        return outputs
    
    def update(self, ship, player_pos: glm.vec3, dt: float, enemies: List) -> Tuple[glm.vec3, float, bool]:
        """Returns (steering, thrust, fire)"""
        self.shoot_cooldown -= dt
        self.state_timer -= dt
        
        # OBSERVE
        to_player = player_pos - ship.position
        self.observe['player_distance'] = glm.length(to_player)
        
        forward = ship.get_forward()
        self.observe['player_angle'] = glm.acos(
            glm.clamp(glm.dot(forward, glm.normalize(to_player)), -1.0, 1.0)
        ) if glm.length(to_player) > 0 else 0
        
        self.observe['health'] = ship.shields
        self.observe['allies'] = len([e for e in enemies if e != ship])
        
        # ORIENT
        if self.observe['player_distance'] < 100:
            self.orient['threat_level'] = 1.0
        elif self.observe['player_distance'] < 300:
            self.orient['threat_level'] = 0.6
        else:
            self.orient['threat_level'] = 0.3
            
        if self.observe['player_angle'] < 0.3 and self.observe['player_distance'] < 400:
            self.orient['opportunity'] = 1.0
        elif self.observe['player_angle'] < 0.8:
            self.orient['opportunity'] = 0.5
        else:
            self.orient['opportunity'] = 0.2
            
        if self.observe['health'] < 30:
            self.orient['tactical_position'] = 'retreat'
        elif self.orient['opportunity'] > 0.7:
            self.orient['tactical_position'] = 'attack'
        elif self.orient['threat_level'] > 0.7:
            self.orient['tactical_position'] = 'evade'
        else:
            self.orient['tactical_position'] = 'maneuver'
        
        # DECIDE (Neural Network)
        inputs = np.array([
            self.observe['player_distance'] / 1000,
            self.observe['player_angle'] / math.pi,
            self.observe['health'] / 100,
            self.observe['allies'] / 5,
            self.orient['threat_level'],
            self.orient['opportunity'],
            math.sin(self.state_timer),
            random.random()
        ])
        
        outputs = self.predict(inputs)
        action_idx = np.argmax(outputs)
        actions = ['attack', 'evade', 'maneuver', 'retreat']
        action = actions[action_idx]
        
        # ACT
        target_dir = glm.normalize(to_player)
        thrust = 0.5
        fire = False
        
        if action == 'attack':
            thrust = 0.8
            if self.observe['player_distance'] < 150:
                thrust = 0.3
            if self.observe['player_angle'] < 0.2 and self.observe['player_distance'] < 300:
                if self.shoot_cooldown <= 0:
                    fire = True
                    self.shoot_cooldown = 0.4 + random.random() * 0.3
                    
        elif action == 'evade':
            target_dir = -target_dir
            thrust = 1.0
            target_dir.x += math.sin(pygame.time.get_ticks() * 0.01) * 0.3
            target_dir = glm.normalize(target_dir)
            
        elif action == 'maneuver':
            orbit = glm.normalize(glm.vec3(-to_player.z, 0, to_player.x))
            target_dir = glm.normalize(to_player + orbit * 0.5)
            thrust = 0.6
            
        elif action == 'retreat':
            target_dir = -target_dir
            thrust = 0.4
        
        return target_dir, thrust, fire


class Ship:
    """Base ship class"""
    
    def __init__(self, position: glm.vec3, faction: str = 'player'):
        self.position = position
        self.rotation = glm.quat(1, 0, 0, 0)
        self.velocity = glm.vec3(0, 0, 0)
        self.faction = faction
        
        # Stats
        self.shields = 100
        self.max_shields = 100
        self.power = 100
        self.max_power = 100
        self.speed = 0
        self.max_speed = 80
        
        # Weapon
        self.weapon_cooldown = 0.0
        
        # Visual
        self.color = FACTION_COLORS[faction]
        self.thruster_active = False
        
        # AI
        self.ai = None if faction == 'player' else NeuralAI()
        
    def get_forward(self) -> glm.vec3:
        return glm.rotate(self.rotation, glm.vec3(0, 0, -1))
    
    def get_up(self) -> glm.vec3:
        return glm.rotate(self.rotation, glm.vec3(0, 1, 0))
    
    def get_right(self) -> glm.vec3:
        return glm.rotate(self.rotation, glm.vec3(1, 0, 0))
    
    def rotate_towards(self, target_dir: glm.vec3, dt: float, speed: float = 3.0):
        """Smoothly rotate towards target direction"""
        if glm.length(target_dir) < 0.001:
            return
            
        target_dir = glm.normalize(target_dir)
        current_forward = self.get_forward()
        
        # Calculate rotation axis and angle
        dot = glm.dot(current_forward, target_dir)
        dot = glm.clamp(dot, -1.0, 1.0)
        
        if dot > 0.9999:
            return
            
        angle = math.acos(dot)
        axis = glm.normalize(glm.cross(current_forward, target_dir))
        
        if glm.length(axis) < 0.001:
            return
            
        # Smooth rotation
        rotation_amount = min(angle, speed * dt)
        rotation = glm.angleAxis(rotation_amount, axis)
        self.rotation = glm.normalize(rotation * self.rotation)
    
    def apply_thrust(self, direction: glm.vec3, amount: float, dt: float):
        """Apply thrust in given direction"""
        self.velocity += direction * amount * dt * 40
        self.thruster_active = amount > 0.5
        
        # Limit speed
        speed = glm.length(self.velocity)
        if speed > self.max_speed:
            self.velocity = glm.normalize(self.velocity) * self.max_speed
    
    def update(self, dt: float, solar_systems: List[Dict]):
        """Update ship physics"""
        # Apply gravity from solar systems
        for sun in solar_systems:
            dist = glm.length(self.position - sun['position'])
            if dist < sun['gravity'] and dist > 10:
                gravity_force = sun['mass'] / (dist * dist)
                direction = glm.normalize(sun['position'] - self.position)
                self.velocity += direction * gravity_force * dt * 100
        
        # Apply damping
        self.velocity *= 0.98
        self.speed = glm.length(self.velocity)
        
        # Update position
        self.position += self.velocity * dt
        
        # Update weapon cooldown
        if self.weapon_cooldown > 0:
            self.weapon_cooldown -= dt
            
        # Regenerate power
        self.power = min(self.power + dt * 5, self.max_power)
        
        # Regenerate shields slowly
        if self.shields < self.max_shields:
            self.shields = min(self.shields + dt * 2, self.max_shields)


class ParticleSystem:
    """Particle effects system"""
    
    def __init__(self):
        self.particles: List[Particle] = []
        
    def spawn_explosion(self, position: glm.vec3, scale: float = 1.0, count: int = 30):
        """Create explosion particles"""
        for _ in range(count):
            velocity = glm.vec3(
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            ) * random.uniform(5, 15) * scale
            
            color = (
                1.0,
                random.uniform(0.3, 0.9),
                random.uniform(0, 0.3)
            )
            
            self.particles.append(Particle(
                position=position + velocity * 0.05,
                velocity=velocity,
                color=color,
                lifetime=1.5,
                max_lifetime=1.5,
                size=random.uniform(2, 5) * scale
            ))
    
    def spawn_engine_trail(self, position: glm.vec3, direction: glm.vec3, intensity: float = 1.0):
        """Create engine trail particles"""
        for _ in range(int(3 * intensity)):
            offset = glm.vec3(
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5)
            )
            
            velocity = -direction * random.uniform(5, 10) + offset * 2
            
            self.particles.append(Particle(
                position=position + offset,
                velocity=velocity,
                color=(0, random.uniform(0.5, 1), 1),
                lifetime=random.uniform(0.3, 0.6),
                max_lifetime=0.6,
                size=random.uniform(1, 3) * intensity
            ))
    
    def update(self, dt: float):
        """Update all particles"""
        for p in self.particles:
            p.position += p.velocity * dt
            p.lifetime -= dt
            
        self.particles = [p for p in self.particles if p.lifetime > 0]


class Renderer:
    """ModernGL 3D Renderer"""
    
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        
        # Vertex shader
        vertex_shader = '''
            #version 330
            uniform mat4 mvp;
            uniform mat4 model;
            uniform vec3 color;
            uniform float time;
            
            in vec3 in_vert;
            in vec3 in_normal;
            
            out vec3 v_color;
            out vec3 v_normal;
            out float v_depth;
            
            void main() {
                gl_Position = mvp * vec4(in_vert, 1.0);
                v_depth = gl_Position.w;
                v_color = color;
                v_normal = mat3(model) * in_normal;
            }
        '''
        
        # Fragment shader
        fragment_shader = '''
            #version 330
            in vec3 v_color;
            in vec3 v_normal;
            in float v_depth;
            
            out vec4 fragColor;
            
            uniform vec3 light_pos;
            uniform float is_wireframe;
            uniform float glow;
            
            void main() {
                vec3 light = normalize(light_pos);
                float diff = max(dot(normalize(v_normal), light), 0.0);
                
                vec3 ambient = v_color * 0.3;
                vec3 diffuse = v_color * diff * 0.7;
                
                // Add glow
                vec3 final_color = ambient + diffuse + (v_color * glow);
                
                // Fog
                float fog = exp(-v_depth * 0.0005);
                final_color = mix(vec3(0.0, 0.01, 0.02), final_color, fog);
                
                if (is_wireframe > 0.5) {
                    fragColor = vec4(v_color, 0.8);
                } else {
                    fragColor = vec4(final_color, 1.0);
                }
            }
        '''
        
        self.program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
        
        # Create mesh geometries
        self.meshes = {}
        self.create_tetrahedron_ship()
        self.create_sphere(32)
        self.create_debris()
        
    def create_tetrahedron_ship(self):
        """Create tetrahedron ship mesh (Flash Gordon style)"""
        # Tetrahedron vertices
        size = 5
        vertices = [
            # Front point
            [0, 0, -size],
            # Back triangle
            [size, 0, size],
            [-size, 0, size],
            [0, size * 0.8, size],
            [0, -size * 0.8, size]
        ]
        
        # Faces (triangles)
        faces = [
            [0, 1, 2],  # Top
            [0, 2, 3],  # Left
            [0, 3, 1],  # Right
            [0, 2, 4],  # Bottom left
            [0, 4, 1],  # Bottom right
        ]
        
        vertex_data = []
        for face in faces:
            # Calculate normal
            v0 = glm.vec3(vertices[face[0]])
            v1 = glm.vec3(vertices[face[1]])
            v2 = glm.vec3(vertices[face[2]])
            normal = glm.cross(v1 - v0, v2 - v0)
            normal = glm.normalize(normal)
            
            for idx in face:
                vertex_data.extend(vertices[idx])
                vertex_data.extend([normal.x, normal.y, normal.z])
        
        self.meshes['ship'] = self.create_vao(vertex_data)
        
        # Create wireframe version
        edges = [
            [0, 1], [0, 2], [0, 3], [0, 4],
            [1, 2], [2, 3], [3, 1],
            [1, 4], [2, 4], [3, 4]
        ]
        
        wire_data = []
        for edge in edges:
            for idx in edge:
                wire_data.extend(vertices[idx])
                wire_data.extend([0, 0, 0])  # No normals for wireframe
        
        self.meshes['ship_wire'] = self.create_vao(wire_data)
    
    def create_sphere(self, segments: int):
        """Create sphere mesh (for suns)"""
        vertices = []
        
        for i in range(segments + 1):
            lat = math.pi * i / segments
            for j in range(segments + 1):
                lon = 2 * math.pi * j / segments
                
                x = math.sin(lat) * math.cos(lon)
                y = math.cos(lat)
                z = math.sin(lat) * math.sin(lon)
                
                vertices.extend([x, y, z])
                vertices.extend([x, y, z])  # Normal = position for sphere
        
        self.meshes['sphere'] = self.create_vao(vertices)
    
    def create_debris(self):
        """Create debris/asteroid mesh"""
        # Icosahedron-ish shape
        vertices = []
        
        phi = (1 + math.sqrt(5)) / 2
        
        raw_verts = [
            [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
            [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
            [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1]
        ]
        
        # Normalize and add noise
        for v in raw_verts:
            vec = glm.vec3(v[0], v[1], v[2])
            vec = glm.normalize(vec) * (3 + random.random() * 2)
            vertices.extend([vec.x, vec.y, vec.z])
            vertices.extend(glm.normalize(vec).to_tuple())
        
        self.meshes['debris'] = self.create_vao(vertices)
    
    def create_vao(self, data: List[float]):
        """Create vertex array object from data"""
        data = np.array(data, dtype='f4')
        vbo = self.ctx.buffer(data.tobytes())
        
        vao = self.ctx.simple_vertex_array(
            self.program, vbo, 'in_vert', 'in_normal'
        )
        
        return {'vao': vao, 'count': len(data) // 6}
    
    def render_mesh(self, mesh_name: str, mvp: glm.mat4, model: glm.mat4, 
                    color: Tuple[float, float, float], is_wireframe: bool = False,
                    glow: float = 0.0):
        """Render a mesh"""
        mesh = self.meshes.get(mesh_name)
        if not mesh:
            return
            
        self.program['mvp'].write(bytes(mvp))
        self.program['model'].write(bytes(model))
        self.program['color'].value = color
        self.program['light_pos'].value = (100, 200, 100)
        self.program['is_wireframe'].value = 1.0 if is_wireframe else 0.0
        self.program['glow'].value = glow
        
        mesh['vao'].render(mode=moderngl.LINES if is_wireframe else moderngl.TRIANGLES)


class Game:
    """Main game class"""
    
    def __init__(self):
        # Pygame setup
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.OPENGL | pygame.DOUBLEBUF
        )
        pygame.display.set_caption("⚡ DUAL SYSTEMS ⚡ - Neural Space Combat")
        
        # ModernGL context
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        
        # Renderer
        self.renderer = Renderer(self.ctx)
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'  # start, playing, paused, gameover
        self.view_mode = ViewMode.THIRD_PERSON
        
        # Game data
        self.score = 0
        self.kills = 0
        self.wave = 1
        self.start_time = 0
        
        # Entities
        self.player: Optional[Ship] = None
        self.enemies: List[Ship] = []
        self.projectiles: List[Projectile] = []
        self.solar_systems: List[Dict] = []
        self.debris: List[Dict] = []
        
        # Particle system
        self.particles = ParticleSystem()
        
        # Camera
        self.camera_pos = glm.vec3(0, 30, 50)
        self.camera_target = glm.vec3(0, 0, 0)
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Create world
        self.create_solar_systems()
        self.create_debris_field()
        self.create_starfield()
        
        # Sounds
        self.sounds = {}
        self.load_sounds()
        
    def load_sounds(self):
        """Generate procedural sound effects"""
        # Simple beep sounds using pygame mixer
        def create_sound(frequency: float, duration: float, fade: bool = True):
            sample_rate = 44100
            samples = int(sample_rate * duration)
            
            buffer = bytearray()
            for i in range(samples):
                t = i / sample_rate
                # Sine wave with decay
                value = int(127 + 127 * math.sin(2 * math.pi * frequency * t))
                if fade:
                    value = int(value * (1 - i / samples))
                buffer.append(value)
                buffer.append(value)  # Stereo
            
            sound = pygame.mixer.Sound(buffer=bytes(buffer))
            sound.set_volume(0.3)
            return sound
        
        self.sounds['laser'] = create_sound(880, 0.15)
        self.sounds['explosion'] = create_sound(150, 0.5)
        self.sounds['hit'] = create_sound(300, 0.1)
        self.sounds['boost'] = create_sound(400, 0.3)
    
    def play_sound(self, name: str):
        """Play sound effect"""
        if name in self.sounds:
            self.sounds[name].play()
    
    def create_solar_systems(self):
        """Create dual solar systems"""
        self.solar_systems = [
            {
                'position': glm.vec3(-400, 200, -400),
                'mass': 1000,
                'gravity': 1500,
                'radius': 60,
                'color': (1.0, 0.67, 0.27)  # Orange
            },
            {
                'position': glm.vec3(400, -100, 400),
                'mass': 800,
                'gravity': 1200,
                'radius': 50,
                'color': (0.27, 0.67, 1.0)  # Blue
            }
        ]
    
    def create_debris_field(self):
        """Create debris field"""
        for _ in range(100):
            angle = random.random() * math.pi * 2
            distance = 300 + random.random() * 500
            height = (random.random() - 0.5) * 200
            
            self.debris.append({
                'position': glm.vec3(
                    math.cos(angle) * distance,
                    height,
                    math.sin(angle) * distance
                ),
                'rotation': glm.quat(
                    random.random(),
                    random.random(),
                    random.random(),
                    random.random()
                ),
                'rotation_speed': glm.vec3(
                    (random.random() - 0.5) * 0.02,
                    (random.random() - 0.5) * 0.02,
                    (random.random() - 0.5) * 0.02
                ),
                'size': 2 + random.random() * 6,
                'health': 20
            })
    
    def create_starfield(self):
        """Create background stars"""
        self.stars = []
        for _ in range(500):
            self.stars.append({
                'position': glm.vec3(
                    random.uniform(-2000, 2000),
                    random.uniform(-2000, 2000),
                    random.uniform(-2000, 2000)
                ),
                'size': random.uniform(1, 3),
                'color': (
                    random.uniform(0.8, 1.0),
                    random.uniform(0.8, 1.0),
                    random.uniform(0.9, 1.0)
                )
            })
    
    def start_game(self):
        """Start a new game"""
        self.state = 'playing'
        self.score = 0
        self.kills = 0
        self.wave = 1
        self.start_time = pygame.time.get_ticks()
        
        # Create player
        self.player = Ship(glm.vec3(0, 0, 0), 'player')
        self.enemies = []
        self.projectiles = []
        
        self.spawn_wave()
    
    def spawn_wave(self):
        """Spawn enemy wave"""
        enemy_count = 3 + self.wave * 2
        factions = ['red', 'green', 'purple']
        
        for i in range(enemy_count):
            angle = random.random() * math.pi * 2
            distance = 200 + random.random() * 200
            
            if self.player:
                pos = self.player.position + glm.vec3(
                    math.cos(angle) * distance,
                    (random.random() - 0.5) * 100,
                    math.sin(angle) * distance
                )
            else:
                pos = glm.vec3(
                    math.cos(angle) * distance,
                    (random.random() - 0.5) * 100,
                    math.sin(angle) * distance
                )
            
            faction = random.choice(factions)
            self.enemies.append(Ship(pos, faction))
    
    def fire_projectile(self, ship: Ship, direction: Optional[glm.vec3] = None):
        """Fire a projectile"""
        if ship.weapon_cooldown > 0:
            return
        
        if direction is None:
            direction = ship.get_forward()
        
        proj_pos = ship.position + direction * 8
        
        self.projectiles.append(Projectile(
            position=proj_pos,
            velocity=direction * 15,
            faction=ship.faction,
            damage=15
        ))
        
        ship.weapon_cooldown = 0.15
        self.play_sound('laser')
    
    def create_explosion(self, position: glm.vec3, scale: float = 1.0):
        """Create explosion effect"""
        self.particles.spawn_explosion(position, scale)
        self.play_sound('explosion')
    
    def update(self, dt: float):
        """Update game state"""
        if self.state != 'playing':
            return
        
        # Update player
        if self.player:
            self.update_player(dt)
        
        # Update enemies
        self.update_enemies(dt)
        
        # Update projectiles
        self.update_projectiles(dt)
        
        # Update particles
        self.particles.update(dt)
        
        # Update debris
        for debris in self.debris:
            debris['rotation'] = glm.normalize(
                debris['rotation'] + glm.quat(
                    0,
                    debris['rotation_speed'].x * dt,
                    debris['rotation_speed'].y * dt,
                    debris['rotation_speed'].z * dt
                ) * debris['rotation']
            )
        
        # Check wave completion
        if len(self.enemies) == 0:
            self.wave += 1
            self.spawn_wave()
    
    def update_player(self, dt: float):
        """Update player ship"""
        keys = pygame.key.get_pressed()
        
        # Movement input
        input_x = 0
        input_y = 0
        input_z = 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            input_z -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            input_z += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            input_x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            input_x += 1
        if keys[pygame.K_q]:
            input_y -= 1
        if keys[pygame.K_e]:
            input_y += 1
        
        # Apply thrust
        boost = 1.5 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else 1.0
        
        forward = self.player.get_forward()
        right = self.player.get_right()
        up = self.player.get_up()
        
        self.player.apply_thrust(forward, input_z * boost, dt)
        self.player.apply_thrust(right, input_x * boost * 0.5, dt)
        self.player.apply_thrust(up, input_y * boost * 0.3, dt)
        
        # Turn into movement direction
        if self.player.speed > 0.1:
            target_dir = glm.normalize(self.player.velocity)
            self.player.rotate_towards(target_dir, dt, 2.0)
        
        # Fire weapon
        if keys[pygame.K_SPACE]:
            self.fire_projectile(self.player)
        
        # Update physics
        self.player.update(dt, self.solar_systems)
        
        # Engine particles
        if self.player.thruster_active:
            self.particles.spawn_engine_trail(
                self.player.position - self.player.get_forward() * 5,
                self.player.get_forward(),
                1.0
            )
        
        # Check death
        if self.player.shields <= 0:
            self.create_explosion(self.player.position, 2.0)
            self.state = 'gameover'
    
    def update_enemies(self, dt: float):
        """Update enemy ships"""
        if not self.player:
            return
        
        for enemy in self.enemies[:]:
            # AI update
            if enemy.ai:
                target_dir, thrust, fire = enemy.ai.update(
                    enemy, self.player.position, dt, self.enemies
                )
                
                # Apply AI decisions
                enemy.rotate_towards(target_dir, dt, 3.0)
                enemy.apply_thrust(enemy.get_forward(), thrust, dt)
                
                if fire:
                    self.fire_projectile(enemy)
            
            # Update physics
            enemy.update(dt, self.solar_systems)
            
            # Engine particles
            if enemy.thruster_active:
                self.particles.spawn_engine_trail(
                    enemy.position - enemy.get_forward() * 5,
                    enemy.get_forward(),
                    0.7
                )
            
            # Check death
            if enemy.shields <= 0:
                self.create_explosion(enemy.position, 1.5)
                self.enemies.remove(enemy)
                self.score += 100
                self.kills += 1
    
    def update_projectiles(self, dt: float):
        """Update projectiles and check collisions"""
        for proj in self.projectiles[:]:
            proj.position += proj.velocity * dt
            proj.lifetime -= dt
            
            if proj.lifetime <= 0:
                self.projectiles.remove(proj)
                continue
            
            # Collision detection
            targets = self.enemies if proj.faction == 'player' else [self.player] if self.player else []
            
            for target in targets:
                if not target:
                    continue
                
                dist = glm.length(proj.position - target.position)
                if dist < 8:
                    # Hit!
                    target.shields -= proj.damage
                    
                    # Hit particles
                    self.particles.spawn_explosion(proj.position, 0.5, 10)
                    self.play_sound('hit')
                    
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    break
    
    def get_view_matrix(self) -> Tuple[glm.mat4, glm.mat4]:
        """Get view and projection matrices"""
        if not self.player:
            return glm.lookAt(
                self.camera_pos,
                self.camera_target,
                glm.vec3(0, 1, 0)
            ), glm.perspective(
                glm.radians(75),
                SCREEN_WIDTH / SCREEN_HEIGHT,
                0.1,
                10000
            )
        
        player_pos = self.player.position
        forward = self.player.get_forward()
        up = self.player.get_up()
        
        if self.view_mode == ViewMode.FIRST_PERSON:
            camera_pos = player_pos + forward * 5
            target = player_pos + forward * 100
        elif self.view_mode == ViewMode.THIRD_PERSON:
            camera_pos = player_pos - forward * 25 + up * 8
            target = player_pos + forward * 50
        else:  # Top down
            camera_pos = player_pos + glm.vec3(0, 60, 0)
            target = player_pos
        
        view = glm.lookAt(camera_pos, target, glm.vec3(0, 1, 0))
        proj = glm.perspective(
            glm.radians(75),
            SCREEN_WIDTH / SCREEN_HEIGHT,
            0.1,
            10000
        )
        
        return view, proj
    
    def render(self):
        """Render the game"""
        # Clear screen
        self.ctx.clear(0.0, 0.008, 0.02)
        
        view, proj = self.get_view_matrix()
        
        # Render solar systems
        for sun in self.solar_systems:
            model = glm.translate(glm.mat4(1.0), sun['position'])
            model = glm.scale(model, glm.vec3(sun['radius']))
            mvp = proj * view * model
            
            self.renderer.render_mesh(
                'sphere', mvp, model, sun['color'], 
                glow=1.0
            )
        
        # Render debris
        for debris in self.debris:
            model = glm.translate(glm.mat4(1.0), debris['position'])
            model *= glm.mat4_cast(debris['rotation'])
            model = glm.scale(model, glm.vec3(debris['size'] / 3))
            mvp = proj * view * model
            
            self.renderer.render_mesh(
                'debris', mvp, model, (0.5, 0.4, 0.3)
            )
        
        # Render player
        if self.player:
            model = glm.translate(glm.mat4(1.0), self.player.position)
            model *= glm.mat4_cast(self.player.rotation)
            mvp = proj * view * model
            
            self.renderer.render_mesh(
                'ship', mvp, model, self.player.color,
                glow=0.3
            )
            self.renderer.render_mesh(
                'ship_wire', mvp, model, (1, 1, 1),
                is_wireframe=True
            )
        
        # Render enemies
        for enemy in self.enemies:
            model = glm.translate(glm.mat4(1.0), enemy.position)
            model *= glm.mat4_cast(enemy.rotation)
            mvp = proj * view * model
            
            glow = 0.3 if enemy.thruster_active else 0.1
            self.renderer.render_mesh(
                'ship', mvp, model, enemy.color,
                glow=glow
            )
            self.renderer.render_mesh(
                'ship_wire', mvp, model, (1, 1, 1),
                is_wireframe=True
            )
        
        # Render projectiles
        for proj in self.projectiles:
            model = glm.translate(glm.mat4(1.0), proj.position)
            # Orient to velocity
            if glm.length(proj.velocity) > 0:
                direction = glm.normalize(proj.velocity)
                up = glm.vec3(0, 1, 0)
                if abs(glm.dot(direction, up)) > 0.99:
                    up = glm.vec3(1, 0, 0)
                right = glm.normalize(glm.cross(direction, up))
                up = glm.cross(right, direction)
                rot_matrix = glm.mat3(right, up, -direction)
                model = model * glm.mat4(rot_matrix)
            
            model = glm.scale(model, glm.vec3(0.5, 2, 0.5))
            mvp = proj * view * model
            
            color = (0, 1, 1) if proj.faction == 'player' else (1, 0.27, 0)
            self.renderer.render_mesh(
                'debris', mvp, model, color,
                glow=0.8
            )
        
        # Render particles (as simple billboards)
        for particle in self.particles.particles:
            model = glm.translate(glm.mat4(1.0), particle.position)
            model = glm.scale(model, glm.vec3(particle.size * 0.3))
            mvp = proj * view * model
            
            alpha = particle.lifetime / particle.max_lifetime
            glow = alpha * 0.5
            
            self.renderer.render_mesh(
                'sphere', mvp, model, particle.color,
                glow=glow
            )
        
        # Swap buffers
        pygame.display.flip()
    
    def draw_hud(self):
        """Draw HUD elements using pygame"""
        # This is called before render to keep pygame surface
        # We use OpenGL for 3D, but pygame for HUD text
        pass  # HUD is handled in pygame events/draw
    
    def render_hud(self):
        """Render 2D HUD"""
        # Create a separate pygame surface for HUD
        hud_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        if self.state == 'start':
            # Title screen
            title = self.font.render("⚡ DUAL SYSTEMS ⚡", True, (0, 255, 255))
            subtitle = self.small_font.render("Neural Warfare in the Twin Suns", True, (136, 204, 255))
            
            hud_surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 200))
            hud_surface.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 250))
            
            controls = [
                "CONTROLS:",
                "WASD / Arrows - Thrust / Steer",
                "Q / E - Roll Up/Down",
                "SPACE - Fire Weapons",
                "SHIFT - Boost Speed",
                "1 / 2 / 3 - Change View",
                "P - Pause",
                "",
                "Press ENTER to Start"
            ]
            
            y = 350
            for line in controls:
                text = self.small_font.render(line, True, (170, 170, 255))
                hud_surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y))
                y += 30
                
        elif self.state == 'playing' and self.player:
            # HUD panels
            # Top left - Score
            score_text = self.font.render(f"SCORE: {self.score}", True, (0, 255, 255))
            kills_text = self.small_font.render(f"KILLS: {self.kills}", True, (0, 255, 255))
            hud_surface.blit(score_text, (20, 20))
            hud_surface.blit(kills_text, (20, 60))
            
            # Top right - Wave/Time
            wave_text = self.font.render(f"WAVE: {self.wave}", True, (0, 255, 255))
            elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
            mins = elapsed // 60
            secs = elapsed % 60
            time_text = self.small_font.render(f"TIME: {mins:02d}:{secs:02d}", True, (0, 255, 255))
            hud_surface.blit(wave_text, (SCREEN_WIDTH - wave_text.get_width() - 20, 20))
            hud_surface.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 60))
            
            # Bottom left - Shields and Power bars
            y = SCREEN_HEIGHT - 100
            
            # Shields
            shield_text = self.small_font.render("SHIELDS", True, (0, 255, 255))
            hud_surface.blit(shield_text, (20, y))
            
            bar_width = 200
            bar_height = 20
            pygame.draw.rect(hud_surface, (50, 50, 50), (20, y + 25, bar_width, bar_height))
            shield_fill = (self.player.shields / self.player.max_shields) * bar_width
            pygame.draw.rect(hud_surface, (0, 200, 255), (20, y + 25, shield_fill, bar_height))
            
            # Power
            y += 50
            power_text = self.small_font.render("POWER", True, (255, 255, 0))
            hud_surface.blit(power_text, (20, y))
            
            pygame.draw.rect(hud_surface, (50, 50, 50), (20, y + 25, bar_width, bar_height))
            power_fill = (self.player.power / self.player.max_power) * bar_width
            pygame.draw.rect(hud_surface, (255, 200, 0), (20, y + 25, power_fill, bar_height))
            
            # Bottom center - Speed
            speed_text = self.font.render(f"SPEED: {int(self.player.speed)} km/s", True, (0, 255, 100))
            hud_surface.blit(speed_text, (SCREEN_WIDTH//2 - speed_text.get_width()//2, SCREEN_HEIGHT - 50))
            
            # View mode indicator
            view_text = self.small_font.render(f"VIEW: {self.view_mode.value.upper()}", True, (170, 170, 255))
            hud_surface.blit(view_text, (SCREEN_WIDTH - view_text.get_width() - 20, SCREEN_HEIGHT - 80))
            
        elif self.state == 'gameover':
            # Game over screen
            over_text = self.font.render("⚡ MISSION END ⚡", True, (255, 100, 100))
            score_text = self.small_font.render(f"Final Score: {self.score} | Kills: {self.kills}", True, (255, 255, 255))
            restart_text = self.small_font.render("Press R to Restart", True, (0, 255, 255))
            
            hud_surface.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, 300))
            hud_surface.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 360))
            hud_surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 420))
        
        elif self.state == 'paused':
            pause_text = self.font.render("PAUSED", True, (255, 255, 0))
            hud_surface.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2))
        
        return hud_surface
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    
                    elif self.state == 'start':
                        if event.key == pygame.K_RETURN:
                            self.start_game()
                    
                    elif self.state == 'playing':
                        if event.key == pygame.K_p:
                            self.state = 'paused' if self.state == 'playing' else 'playing'
                        elif event.key == pygame.K_1:
                            self.view_mode = ViewMode.THIRD_PERSON
                        elif event.key == pygame.K_2:
                            self.view_mode = ViewMode.FIRST_PERSON
                        elif event.key == pygame.K_3:
                            self.view_mode = ViewMode.TOP_DOWN
                    
                    elif self.state == 'paused':
                        if event.key == pygame.K_p:
                            self.state = 'playing'
                    
                    elif self.state == 'gameover':
                        if event.key == pygame.K_r:
                            self.start_game()
            
            # Update
            self.update(dt)
            
            # Render 3D
            self.render()
            
            # Render HUD using pygame
            hud = self.render_hud()
            
            # Convert pygame surface to OpenGL texture and render
            # For simplicity, we'll just display the HUD differently
            # In a full implementation, you'd use imgui or text rendering in OpenGL
            
            # For now, let's use pygame's display for HUD overlay
            pygame.display.flip()
            
            # Draw HUD on pygame surface
            self.screen.blit(hud, (0, 0))
            pygame.display.update()


def main():
    """Entry point"""
    print("⚡ DUAL SYSTEMS ⚡")
    print("Neural Warfare in the Twin Suns")
    print()
    print("Controls:")
    print("  WASD / Arrows - Thrust / Steer")
    print("  Q / E - Roll Up/Down")
    print("  SPACE - Fire Weapons")
    print("  SHIFT - Boost Speed")
    print("  1 / 2 / 3 - Change View (Third/First/Top)")
    print("  P - Pause")
    print("  ESC - Quit")
    print()
    print("Press ENTER in game to start...")
    
    game = Game()
    game.run()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
