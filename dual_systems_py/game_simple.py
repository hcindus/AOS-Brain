#!/usr/bin/env python3
"""
DUAL SYSTEMS - Simple Python Version
Compatible fallback using only pygame (no OpenGL required)

Controls:
- WASD/Arrows: Thrust/Steer
- SPACE: Fire
- SHIFT: Boost
- 1/2/3: Change view
- P: Pause
- ESC: Quit
"""

import pygame
import math
import random
from typing import List, Tuple, Optional

# Initialize pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
BLACK = (0, 0, 0)
DARK_BLUE = (0, 10, 30)
CYAN = (0, 255, 255)
RED = (255, 68, 68)
GREEN = (68, 255, 68)
PURPLE = (170, 68, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 170, 68)
WHITE = (255, 255, 255)

# Faction colors
FACTION_COLORS = {
    'player': CYAN,
    'red': RED,
    'green': GREEN,
    'purple': PURPLE
}

class Vector3:
    """Simple 3D vector class"""
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        l = self.length()
        if l > 0:
            return Vector3(self.x/l, self.y/l, self.z/l)
        return Vector3()
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )


class Particle:
    def __init__(self, x, y, z, vx, vy, vz, color, lifetime, size=2):
        self.x, self.y, self.z = x, y, z
        self.vx, self.vy, self.vz = vx, vy, vz
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
    
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt
        self.lifetime -= dt
        return self.lifetime > 0


class Ship:
    def __init__(self, x, y, z, faction='player'):
        self.pos = Vector3(x, y, z)
        self.vel = Vector3()
        self.rotation = 0  # Yaw
        self.pitch = 0
        self.faction = faction
        
        self.shields = 100
        self.max_shields = 100
        self.power = 100
        self.speed = 0
        self.max_speed = 80
        
        self.weapon_cooldown = 0
        self.thruster_active = False
        self.color = FACTION_COLORS.get(faction, CYAN)
        
        # AI state
        self.ai_timer = 0
        self.ai_state = 'attack'
    
    def get_forward(self):
        """Get forward vector based on rotation"""
        return Vector3(
            -math.sin(self.rotation) * math.cos(self.pitch),
            math.sin(self.pitch),
            -math.cos(self.rotation) * math.cos(self.pitch)
        ).normalize()
    
    def get_right(self):
        """Get right vector"""
        return Vector3(
            math.cos(self.rotation),
            0,
            -math.sin(self.rotation)
        ).normalize()
    
    def get_up(self):
        """Get up vector"""
        fwd = self.get_forward()
        right = self.get_right()
        return Vector3(
            right.y * fwd.z - right.z * fwd.y,
            right.z * fwd.x - right.x * fwd.z,
            right.x * fwd.y - right.y * fwd.x
        ).normalize()
    
    def update(self, dt, solar_systems):
        """Update physics"""
        # Apply gravity from solar systems
        for sun in solar_systems:
            dx = sun['x'] - self.pos.x
            dy = sun['y'] - self.pos.y
            dz = sun['z'] - self.pos.z
            dist_sq = dx*dx + dy*dy + dz*dz
            dist = math.sqrt(dist_sq)
            
            if dist < sun['gravity'] and dist > 10:
                gravity_force = sun['mass'] / dist_sq
                self.vel.x += (dx / dist) * gravity_force * dt * 100
                self.vel.y += (dy / dist) * gravity_force * dt * 100
                self.vel.z += (dz / dist) * gravity_force * dt * 100
        
        # Apply damping
        self.vel = self.vel * 0.98
        self.speed = self.vel.length()
        
        # Update position
        self.pos = self.pos + self.vel * dt
        
        # Update cooldown
        if self.weapon_cooldown > 0:
            self.weapon_cooldown -= dt
        
        # Regenerate shields
        if self.shields < self.max_shields:
            self.shields = min(self.shields + dt * 2, self.max_shields)
    
    def rotate_towards(self, target_dir, dt, speed=3.0):
        """Smoothly rotate towards target direction"""
        current_fwd = self.get_forward()
        
        # Calculate target rotation
        target_yaw = math.atan2(-target_dir.x, -target_dir.z)
        target_pitch = math.asin(max(-1, min(1, target_dir.y)))
        
        # Smooth rotation
        diff_yaw = target_yaw - self.rotation
        while diff_yaw > math.pi: diff_yaw -= 2 * math.pi
        while diff_yaw < -math.pi: diff_yaw += 2 * math.pi
        
        diff_pitch = target_pitch - self.pitch
        
        self.rotation += max(-speed * dt, min(speed * dt, diff_yaw))
        self.pitch += max(-speed * dt, min(speed * dt, diff_pitch))
        self.pitch = max(-1.5, min(1.5, self.pitch))


class Projectile:
    def __init__(self, x, y, z, vx, vy, vz, faction='player', damage=15):
        self.pos = Vector3(x, y, z)
        self.vel = Vector3(vx, vy, vz)
        self.faction = faction
        self.damage = damage
        self.lifetime = 2.0


class DualSystemsGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("⚡ DUAL SYSTEMS ⚡ - Neural Space Combat")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 72)
        
        self.reset_game()
        self.load_sounds()
    
    def load_sounds(self):
        """Generate simple sound effects"""
        self.sounds = {}
        # Simple beep generation
        sample_rate = 44100
        
        # Laser sound
        duration = 0.15
        samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(samples):
            t = i / sample_rate
            freq = 880 * (0.1 ** t)
            val = int(127 + 127 * math.sin(2 * math.pi * freq * t) * (1 - i/samples))
            buf.extend([val, val])
        self.sounds['laser'] = pygame.mixer.Sound(buffer=bytes(buf))
        self.sounds['laser'].set_volume(0.3)
        
        # Explosion sound
        duration = 0.5
        samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(samples):
            t = i / sample_rate
            noise = random.randint(-127, 127)
            val = int(noise * (1 - i/samples))
            buf.extend([val, val])
        self.sounds['explosion'] = pygame.mixer.Sound(buffer=bytes(buf))
        self.sounds['explosion'].set_volume(0.4)
        
        # Hit sound
        duration = 0.1
        samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(samples):
            t = i / sample_rate
            val = int(127 * (1 - i/samples))
            buf.extend([val, val])
        self.sounds['hit'] = pygame.mixer.Sound(buffer=bytes(buf))
        self.sounds['hit'].set_volume(0.3)
    
    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
    
    def reset_game(self):
        self.state = 'menu'  # menu, playing, paused, gameover
        self.score = 0
        self.kills = 0
        self.wave = 1
        self.view_mode = 'third'  # third, first, top
        
        self.player = None
        self.enemies = []
        self.projectiles = []
        self.particles = []
        
        # Solar systems
        self.solar_systems = [
            {'x': -400, 'y': 200, 'z': -400, 'mass': 1000, 'gravity': 1500, 'radius': 60, 'color': ORANGE},
            {'x': 400, 'y': -100, 'z': 400, 'mass': 800, 'gravity': 1200, 'radius': 50, 'color': (68, 170, 255)}
        ]
        
        # Debris field
        self.debris = []
        for _ in range(100):
            angle = random.random() * 2 * math.pi
            dist = 300 + random.random() * 500
            self.debris.append({
                'x': math.cos(angle) * dist,
                'y': (random.random() - 0.5) * 200,
                'z': math.sin(angle) * dist,
                'rot': random.random() * 2 * math.pi,
                'rot_speed': (random.random() - 0.5) * 0.02,
                'size': 2 + random.random() * 6
            })
        
        # Stars
        self.stars = []
        for _ in range(500):
            self.stars.append({
                'x': random.uniform(-2000, 2000),
                'y': random.uniform(-2000, 2000),
                'z': random.uniform(-2000, 2000),
                'size': random.uniform(1, 3)
            })
        
        self.start_time = 0
        self.camera_offset = Vector3(0, 20, 50)
    
    def start_game(self):
        self.state = 'playing'
        self.player = Ship(0, 0, 0, 'player')
        self.enemies = []
        self.projectiles = []
        self.particles = []
        self.score = 0
        self.kills = 0
        self.wave = 1
        self.start_time = pygame.time.get_ticks()
        self.spawn_wave()
    
    def spawn_wave(self):
        enemy_count = 3 + self.wave * 2
        factions = ['red', 'green', 'purple']
        
        for i in range(enemy_count):
            angle = random.random() * 2 * math.pi
            dist = 200 + random.random() * 200
            
            if self.player:
                ex = self.player.pos.x + math.cos(angle) * dist
                ey = self.player.pos.y + (random.random() - 0.5) * 100
                ez = self.player.pos.z + math.sin(angle) * dist
            else:
                ex = math.cos(angle) * dist
                ey = (random.random() - 0.5) * 100
                ez = math.sin(angle) * dist
            
            faction = random.choice(factions)
            self.enemies.append(Ship(ex, ey, ez, faction))
    
    def project_3d(self, x, y, z, camera_pos, camera_rot):
        """Project 3D point to 2D screen coordinates"""
        # Translate to camera space
        dx = x - camera_pos.x
        dy = y - camera_pos.y
        dz = z - camera_pos.z
        
        # Rotate around Y axis
        cos_y = math.cos(-camera_rot)
        sin_y = math.sin(-camera_rot)
        x_rot = dx * cos_y - dz * sin_y
        z_rot = dx * sin_y + dz * cos_y
        y_rot = dy
        
        # Perspective projection
        if z_rot <= 0:
            return None
        
        fov = 800
        scale = fov / z_rot
        
        screen_x = SCREEN_WIDTH // 2 + int(x_rot * scale)
        screen_y = SCREEN_HEIGHT // 2 - int(y_rot * scale)
        
        return (screen_x, screen_y, z_rot)
    
    def draw_tetrahedron_ship(self, screen, ship, camera_pos, camera_rot):
        """Draw a tetrahedron ship"""
        size = 5
        
        # Ship vertices
        fwd = ship.get_forward()
        up = ship.get_up()
        right = ship.get_right()
        
        center = (ship.pos.x, ship.pos.y, ship.pos.z)
        
        # Define vertices relative to center
        vertices = [
            (center[0] + fwd.x * size, center[1] + fwd.y * size, center[2] + fwd.z * size),
            (center[0] + right.x * size - fwd.x * size, center[1] + right.y * size, center[2] + right.z * size - fwd.z * size),
            (center[0] - right.x * size - fwd.x * size, center[1] - right.y * size, center[2] - right.z * size - fwd.z * size),
            (center[0] - up.x * size, center[1] - up.y * size, center[2] - up.z * size)
        ]
        
        # Project vertices
        projected = []
        for v in vertices:
            p = self.project_3d(v[0], v[1], v[2], camera_pos, camera_rot)
            if p:
                projected.append(p)
        
        if len(projected) < 4:
            return
        
        # Draw wireframe
        color = ship.color
        lines = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
        
        for i, j in lines:
            if i < len(projected) and j < len(projected):
                pygame.draw.line(screen, color, 
                    (projected[i][0], projected[i][1]),
                    (projected[j][0], projected[j][1]), 2)
        
        # Draw center glow
        if len(projected) > 0:
            center_proj = projected[0]  # Approximate center
            glow_size = max(3, int(10 * 800 / projected[0][2]))
            pygame.draw.circle(screen, color, 
                (center_proj[0], center_proj[1]), glow_size // 2)
    
    def draw_sphere(self, screen, x, y, z, radius, color, camera_pos, camera_rot):
        """Draw a sphere (simplified as circle)"""
        p = self.project_3d(x, y, z, camera_pos, camera_rot)
        if not p:
            return
        
        # Calculate apparent size
        scale = 800 / p[2]
        apparent_radius = int(radius * scale * 0.5)
        
        if apparent_radius > 2:
            # Glow effect
            for i in range(3, 0, -1):
                glow_color = tuple(min(255, int(c * (0.3 + i * 0.2))) for c in color[:3])
                pygame.draw.circle(screen, glow_color, 
                    (p[0], p[1]), apparent_radius + i * 5, 1)
            
            pygame.draw.circle(screen, color[:3], (p[0], p[1]), apparent_radius)
    
    def update(self, dt):
        if self.state != 'playing':
            return
        
        keys = pygame.key.get_pressed()
        
        # Player controls
        if self.player:
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
            
            boost = 1.5 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else 1.0
            
            # Apply thrust
            fwd = self.player.get_forward()
            right = self.player.get_right()
            up = self.player.get_up()
            
            accel = 40 * dt * boost
            self.player.vel = self.player.vel + fwd * input_z * accel
            self.player.vel = self.player.vel + right * input_x * accel * 0.5
            self.player.vel = self.player.vel + up * input_y * accel * 0.3
            
            self.player.thruster_active = input_z != 0 or input_x != 0
            
            # Turn into movement
            if self.player.speed > 0.1:
                target_dir = self.player.vel.normalize()
                self.player.rotate_towards(target_dir, dt, 2.0)
            
            # Fire
            if keys[pygame.K_SPACE] and self.player.weapon_cooldown <= 0:
                proj_pos = self.player.pos + fwd * 8
                self.projectiles.append(Projectile(
                    proj_pos.x, proj_pos.y, proj_pos.z,
                    fwd.x * 15, fwd.y * 15, fwd.z * 15,
                    'player', 15
                ))
                self.player.weapon_cooldown = 0.15
                self.play_sound('laser')
            
            self.player.update(dt, self.solar_systems)
            
            # Engine particles
            if self.player.thruster_active:
                for _ in range(2):
                    self.particles.append(Particle(
                        self.player.pos.x - fwd.x * 5,
                        self.player.pos.y - fwd.y * 5,
                        self.player.pos.z - fwd.z * 5,
                        -fwd.x * 5 + random.uniform(-2, 2),
                        -fwd.y * 5 + random.uniform(-2, 2),
                        -fwd.z * 5 + random.uniform(-2, 2),
                        (0, random.randint(150, 255), 255),
                        0.5, 2
                    ))
        
        # Update enemies
        for enemy in self.enemies[:]:
            # Simple AI
            if self.player:
                to_player = Vector3(
                    self.player.pos.x - enemy.pos.x,
                    self.player.pos.y - enemy.pos.y,
                    self.player.pos.z - enemy.pos.z
                )
                dist = to_player.length()
                
                if dist > 0:
                    target_dir = to_player.normalize()
                    enemy.rotate_towards(target_dir, dt, 3.0)
                    
                    # Fire if close and aligned
                    if dist < 300:
                        enemy.vel = enemy.vel + enemy.get_forward() * 30 * dt
                    
                    if dist < 200 and enemy.weapon_cooldown <= 0:
                        if random.random() < 0.02:  # 2% chance per frame
                            fwd = enemy.get_forward()
                            proj_pos = enemy.pos + fwd * 8
                            self.projectiles.append(Projectile(
                                proj_pos.x, proj_pos.y, proj_pos.z,
                                fwd.x * 15, fwd.y * 15, fwd.z * 15,
                                enemy.faction, 15
                            ))
                            enemy.weapon_cooldown = 0.4 + random.random() * 0.3
            
            enemy.update(dt, self.solar_systems)
            
            if enemy.shields <= 0:
                self.create_explosion(enemy.pos.x, enemy.pos.y, enemy.pos.z, 1.5)
                self.enemies.remove(enemy)
                self.score += 100
                self.kills += 1
        
        # Update projectiles
        for proj in self.projectiles[:]:
            proj.pos = proj.pos + proj.vel * dt
            proj.lifetime -= dt
            
            if proj.lifetime <= 0:
                self.projectiles.remove(proj)
                continue
            
            # Collision
            targets = self.enemies if proj.faction == 'player' else [self.player]
            for target in targets:
                if not target:
                    continue
                dx = proj.pos.x - target.pos.x
                dy = proj.pos.y - target.pos.y
                dz = proj.pos.z - target.pos.z
                dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                
                if dist < 8:
                    target.shields -= proj.damage
                    self.create_explosion(proj.pos.x, proj.pos.y, proj.pos.z, 0.5)
                    self.play_sound('hit')
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    
                    if target == self.player and target.shields <= 0:
                        self.state = 'gameover'
                    break
        
        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]
        
        # Update debris
        for debris in self.debris:
            debris['rot'] += debris['rot_speed']
        
        # Check wave
        if len(self.enemies) == 0 and self.state == 'playing':
            self.wave += 1
            self.spawn_wave()
    
    def create_explosion(self, x, y, z, scale=1.0):
        """Create explosion particles"""
        for _ in range(int(20 * scale)):
            self.particles.append(Particle(
                x, y, z,
                random.uniform(-10, 10) * scale,
                random.uniform(-10, 10) * scale,
                random.uniform(-10, 10) * scale,
                (255, random.randint(100, 200), 50),
                1.0, 3 * scale
            ))
        self.play_sound('explosion')
    
    def get_camera(self):
        """Get camera position and rotation"""
        if not self.player:
            return Vector3(0, 30, 50), 0
        
        fwd = self.player.get_forward()
        up = Vector3(0, 1, 0)
        
        if self.view_mode == 'first':
            cam_pos = self.player.pos + fwd * 5
            return cam_pos, self.player.rotation
        elif self.view_mode == 'top':
            cam_pos = Vector3(self.player.pos.x, self.player.pos.y + 60, self.player.pos.z)
            return cam_pos, self.player.rotation
        else:  # third
            cam_pos = self.player.pos - fwd * 25 + up * 8
            return cam_pos, self.player.rotation
    
    def draw(self):
        """Render the game"""
        self.screen.fill(DARK_BLUE)
        
        camera_pos, camera_rot = self.get_camera()
        
        # Draw stars
        for star in self.stars:
            p = self.project_3d(star['x'], star['y'], star['z'], camera_pos, camera_rot)
            if p and p[2] > 0:
                brightness = max(0.3, min(1.0, 1.0 - p[2] / 2000))
                size = max(1, int(star['size'] * (1 - p[2] / 3000)))
                color = (int(255 * brightness), int(255 * brightness), int(255 * brightness))
                pygame.draw.circle(self.screen, color, (p[0], p[1]), size)
        
        # Draw solar systems
        for sun in self.solar_systems:
            self.draw_sphere(self.screen, sun['x'], sun['y'], sun['z'], 
                           sun['radius'], sun['color'], camera_pos, camera_rot)
        
        # Draw debris
        for debris in self.debris:
            p = self.project_3d(debris['x'], debris['y'], debris['z'], camera_pos, camera_rot)
            if p and p[2] > 0:
                size = max(2, int(debris['size'] * 800 / p[2] * 0.3))
                color = (100, 80, 60)
                pygame.draw.circle(self.screen, color, (p[0], p[1]), size)
        
        # Draw projectiles
        for proj in self.projectiles:
            color = CYAN if proj.faction == 'player' else RED
            p = self.project_3d(proj.pos.x, proj.pos.y, proj.pos.z, camera_pos, camera_rot)
            if p and p[2] > 0:
                pygame.draw.circle(self.screen, color, (p[0], p[1]), 3)
        
        # Draw particles
        for particle in self.particles:
            p = self.project_3d(particle.x, particle.y, particle.z, camera_pos, camera_rot)
            if p and p[2] > 0:
                size = max(1, int(particle.size * 800 / p[2] * 0.5))
                alpha = particle.lifetime / particle.max_lifetime
                color = tuple(int(c * alpha) for c in particle.color)
                pygame.draw.circle(self.screen, color, (p[0], p[1]), size)
        
        # Draw player
        if self.player:
            self.draw_tetrahedron_ship(self.screen, self.player, camera_pos, camera_rot)
        
        # Draw enemies
        for enemy in self.enemies:
            self.draw_tetrahedron_ship(self.screen, enemy, camera_pos, camera_rot)
        
        # Draw HUD
        self.draw_hud()
        
        pygame.display.flip()
    
    def draw_hud(self):
        """Draw HUD elements"""
        if self.state == 'menu':
            title = self.big_font.render("⚡ DUAL SYSTEMS ⚡", True, CYAN)
            subtitle = self.small_font.render("Neural Warfare in the Twin Suns", True, (136, 204, 255))
            prompt = self.font.render("Press ENTER to Start", True, YELLOW)
            
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 250))
            self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 320))
            self.screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 400))
            
            # Controls
            controls = [
                "CONTROLS:",
                "WASD/Arrows - Thrust/Steer",
                "Q/E - Roll",
                "SPACE - Fire",
                "SHIFT - Boost",
                "1/2/3 - Change View",
                "P - Pause"
            ]
            y = 500
            for line in controls:
                text = self.small_font.render(line, True, (170, 170, 255))
                self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y))
                y += 30
        
        elif self.state == 'playing':
            if self.player:
                # Top left
                score_text = self.font.render(f"SCORE: {self.score}", True, CYAN)
                kills_text = self.small_font.render(f"KILLS: {self.kills}", True, CYAN)
                self.screen.blit(score_text, (20, 20))
                self.screen.blit(kills_text, (20, 60))
                
                # Top right
                wave_text = self.font.render(f"WAVE: {self.wave}", True, CYAN)
                elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
                mins = elapsed // 60
                secs = elapsed % 60
                time_text = self.small_font.render(f"TIME: {mins:02d}:{secs:02d}", True, CYAN)
                self.screen.blit(wave_text, (SCREEN_WIDTH - wave_text.get_width() - 20, 20))
                self.screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 60))
                
                # Bottom left - Bars
                y = SCREEN_HEIGHT - 100
                
                # Shield bar
                shield_text = self.small_font.render("SHIELDS", True, CYAN)
                self.screen.blit(shield_text, (20, y))
                pygame.draw.rect(self.screen, (50, 50, 50), (20, y + 25, 200, 20))
                shield_fill = int((self.player.shields / self.player.max_shields) * 200)
                pygame.draw.rect(self.screen, CYAN, (20, y + 25, shield_fill, 20))
                
                # Power bar
                y += 50
                power_text = self.small_font.render("POWER", True, YELLOW)
                self.screen.blit(power_text, (20, y))
                pygame.draw.rect(self.screen, (50, 50, 50), (20, y + 25, 200, 20))
                power_fill = int((self.player.power / self.player.max_power) * 200)
                pygame.draw.rect(self.screen, YELLOW, (20, y + 25, power_fill, 20))
                
                # Bottom center
                speed_text = self.font.render(f"SPEED: {int(self.player.speed)}", True, GREEN)
                self.screen.blit(speed_text, (SCREEN_WIDTH//2 - speed_text.get_width()//2, SCREEN_HEIGHT - 50))
                
                # View mode
                view_text = self.small_font.render(f"VIEW: {self.view_mode.upper()}", True, (170, 170, 255))
                self.screen.blit(view_text, (SCREEN_WIDTH - view_text.get_width() - 20, SCREEN_HEIGHT - 80))
                
                # Crosshair
                pygame.draw.line(self.screen, CYAN, 
                    (SCREEN_WIDTH//2 - 20, SCREEN_HEIGHT//2),
                    (SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT//2), 1)
                pygame.draw.line(self.screen, CYAN,
                    (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20),
                    (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20), 1)
        
        elif self.state == 'gameover':
            over_text = self.big_font.render("MISSION END", True, RED)
            score_text = self.font.render(f"Score: {self.score} | Kills: {self.kills}", True, WHITE)
            restart_text = self.small_font.render("Press R to Restart", True, CYAN)
            
            self.screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, 300))
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 380))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 450))
        
        elif self.state == 'paused':
            pause_text = self.big_font.render("PAUSED", True, YELLOW)
            self.screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    elif self.state == 'menu':
                        if event.key == pygame.K_RETURN:
                            self.start_game()
                    
                    elif self.state == 'playing':
                        if event.key == pygame.K_p:
                            self.state = 'paused'
                        elif event.key == pygame.K_1:
                            self.view_mode = 'third'
                        elif event.key == pygame.K_2:
                            self.view_mode = 'first'
                        elif event.key == pygame.K_3:
                            self.view_mode = 'top'
                    
                    elif self.state == 'paused':
                        if event.key == pygame.K_p:
                            self.state = 'playing'
                    
                    elif self.state == 'gameover':
                        if event.key == pygame.K_r:
                            self.start_game()
            
            self.update(dt)
            self.draw()
        
        pygame.quit()


def main():
    print("⚡ DUAL SYSTEMS ⚡")
    print("Simple Python Version (Software Renderer)")
    print()
    print("Controls:")
    print("  WASD/Arrows - Thrust/Steer")
    print("  Q/E - Roll")
    print("  SPACE - Fire")
    print("  SHIFT - Boost")
    print("  1/2/3 - Change View")
    print("  P - Pause")
    print("  ESC - Quit")
    print()
    
    game = DualSystemsGame()
    game.run()


if __name__ == "__main__":
    main()
