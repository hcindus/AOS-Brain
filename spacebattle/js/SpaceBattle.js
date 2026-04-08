/**
 * SpaceBattle.js - Arcade Space Combat Game
 * Forked from N'og nog v1 - Simplified for fast-paced action
 */

class SpaceBattle {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 5000);
        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true });
        
        this.clock = new THREE.Clock();
        this.state = 'loading';
        
        // Game state
        this.score = 0;
        this.kills = 0;
        this.wave = 1;
        this.gameTime = 0;
        this.startTime = 0;
        
        // Player
        this.player = null;
        this.playerBullets = [];
        
        // Enemies
        this.enemies = [];
        this.enemyBullets = [];
        this.particles = [];
        
        // Starfield
        this.starField = null;
        
        // Input
        this.keys = {};
        this.mouse = { x: 0, y: 0 };
        this.joystick = { x: 0, y: 0, active: false };
        
        // Wave management
        this.waveInProgress = false;
        this.waveCooldown = 0;
        
        this.setupInput();
    }
    
    async init() {
        // Setup renderer
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setClearColor(0x050008);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        
        // Create starfield
        this.createStarField();
        
        // Create player
        this.player = new PlayerShip(this.scene);
        
        // Setup camera
        this.camera.position.set(0, 30, 50);
        this.camera.lookAt(0, 0, 0);
        
        // Lighting
        const ambient = new THREE.AmbientLight(0x333333);
        this.scene.add(ambient);
        
        const sun = new THREE.DirectionalLight(0xff4400, 0.8);
        sun.position.set(100, 200, 100);
        this.scene.add(sun);
        
        // Resize handler
        window.addEventListener('resize', () => this.onResize());
        
        // Simulate loading
        await this.simulateLoading();
    }
    
    async simulateLoading() {
        const progress = document.getElementById('loadingProgress');
        for (let i = 0; i <= 100; i += 10) {
            progress.style.width = i + '%';
            await new Promise(r => setTimeout(r, 100));
        }
        document.getElementById('loading').style.display = 'none';
        document.getElementById('hud').style.display = 'block';
    }
    
    createStarField() {
        const geometry = new THREE.BufferGeometry();
        const positions = [];
        const colors = [];
        
        for (let i = 0; i < 3000; i++) {
            const x = (Math.random() - 0.5) * 4000;
            const y = (Math.random() - 0.5) * 4000;
            const z = (Math.random() - 0.5) * 4000;
            positions.push(x, y, z);
            
            // Star colors: mostly white/red/orange
            const colorChoice = Math.random();
            if (colorChoice < 0.7) {
                colors.push(1, 0.9, 0.8); // White-ish
            } else if (colorChoice < 0.9) {
                colors.push(1, 0.6, 0.4); // Orange
            } else {
                colors.push(1, 0.3, 0.3); // Red
            }
        }
        
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
        
        const material = new THREE.PointsMaterial({
            size: 2,
            vertexColors: true,
            transparent: true,
            opacity: 0.8
        });
        
        this.starField = new THREE.Points(geometry, material);
        this.scene.add(this.starField);
    }
    
    start() {
        this.state = 'playing';
        this.startTime = Date.now();
        this.wave = 1;
        this.score = 0;
        this.kills = 0;
        
        // Lock pointer
        this.canvas.requestPointerLock();
        
        // Start wave
        this.startWave();
        
        // Start loop
        this.animate();
    }
    
    startWave() {
        this.waveInProgress = true;
        this.showWaveNotification();
        
        // Spawn enemies based on wave
        const enemyCount = 3 + this.wave * 2;
        for (let i = 0; i < enemyCount; i++) {
            setTimeout(() => {
                this.spawnEnemy();
            }, i * 800);
        }
    }
    
    showWaveNotification() {
        const notif = document.getElementById('waveNotification');
        notif.textContent = `WAVE ${this.wave}`;
        notif.classList.add('visible');
        setTimeout(() => notif.classList.remove('visible'), 3000);
    }
    
    spawnEnemy() {
        const types = ['fighter', 'interceptor', 'bomber'];
        const type = types[Math.floor(Math.random() * types.length)];
        
        // Spawn around player at distance
        const angle = Math.random() * Math.PI * 2;
        const distance = 150 + Math.random() * 100;
        const x = this.player.mesh.position.x + Math.cos(angle) * distance;
        const z = this.player.mesh.position.z + Math.sin(angle) * distance;
        const y = (Math.random() - 0.5) * 50;
        
        const enemy = new EnemyShip(this.scene, type, x, y, z);
        this.enemies.push(enemy);
    }
    
    setupInput() {
        // Keyboard
        document.addEventListener('keydown', (e) => {
            this.keys[e.code] = true;
            if (e.code === 'Space') e.preventDefault();
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
        
        // Mouse
        document.addEventListener('mousemove', (e) => {
            if (document.pointerLockElement === this.canvas) {
                this.mouse.x += e.movementX * 0.002;
                this.mouse.y += e.movementY * 0.002;
                this.mouse.y = Math.max(-1, Math.min(1, this.mouse.y));
            }
        });
        
        document.addEventListener('mousedown', () => {
            if (this.state === 'playing') {
                this.player.fire();
            }
        });
        
        // Touch controls
        this.setupTouchControls();
    }
    
    setupTouchControls() {
        const joystickZone = document.getElementById('joystickZone');
        const joystickKnob = document.getElementById('joystickKnob');
        const fireButton = document.getElementById('fireButton');
        
        let joystickStart = { x: 0, y: 0 };
        
        joystickZone.addEventListener('touchstart', (e) => {
            e.preventDefault();
            const touch = e.touches[0];
            const rect = joystickZone.getBoundingClientRect();
            joystickStart.x = rect.left + rect.width / 2;
            joystickStart.y = rect.top + rect.height / 2;
            this.joystick.active = true;
        });
        
        joystickZone.addEventListener('touchmove', (e) => {
            e.preventDefault();
            if (!this.joystick.active) return;
            
            const touch = e.touches[0];
            const dx = (touch.clientX - joystickStart.x) / 35;
            const dy = (touch.clientY - joystickStart.y) / 35;
            
            this.joystick.x = Math.max(-1, Math.min(1, dx));
            this.joystick.y = Math.max(-1, Math.min(1, dy));
            
            joystickKnob.style.transform = `translate(${dx * 35}px, ${dy * 35}px)`;
        });
        
        joystickZone.addEventListener('touchend', () => {
            this.joystick.active = false;
            this.joystick.x = 0;
            this.joystick.y = 0;
            joystickKnob.style.transform = 'translate(0, 0)';
        });
        
        fireButton.addEventListener('touchstart', (e) => {
            e.preventDefault();
            if (this.state === 'playing') {
                this.player.fire();
            }
        });
    }
    
    update(delta) {
        if (this.state !== 'playing') return;
        
        this.gameTime = (Date.now() - this.startTime) / 1000;
        
        // Update player
        this.updatePlayer(delta);
        
        // Update enemies
        this.updateEnemies(delta);
        
        // Update bullets
        this.updateBullets(delta);
        
        // Update particles
        this.updateParticles(delta);
        
        // Check wave completion
        this.checkWaveStatus();
        
        // Update HUD
        this.updateHUD();
        
        // Update radar
        this.updateRadar();
    }
    
    updatePlayer(delta) {
        if (!this.player) return;
        
        // Movement
        let thrust = 0;
        let turn = 0;
        
        if (this.keys['KeyW']) thrust = 1;
        if (this.keys['KeyS']) thrust = -0.5;
        if (this.keys['KeyA']) turn = 1;
        if (this.keys['KeyD']) turn = -1;
        
        // Joystick override
        if (this.joystick.active) {
            thrust = -this.joystick.y;
            turn = -this.joystick.x;
        }
        
        this.player.update(delta, thrust, turn, this.mouse);
        
        // Camera follow
        const targetPos = this.player.mesh.position.clone();
        targetPos.y += 25;
        targetPos.z += 40;
        this.camera.position.lerp(targetPos, 0.1);
        this.camera.lookAt(this.player.mesh.position);
    }
    
    updateEnemies(delta) {
        for (let i = this.enemies.length - 1; i >= 0; i--) {
            const enemy = this.enemies[i];
            enemy.update(delta, this.player);
            
            // Check if enemy fires
            if (enemy.canFire()) {
                const bullet = enemy.fire();
                this.enemyBullets.push(bullet);
            }
            
            // Check collision with player bullets
            for (let j = this.playerBullets.length - 1; j >= 0; j--) {
                const bullet = this.playerBullets[j];
                if (enemy.checkHit(bullet.mesh.position)) {
                    this.createExplosion(enemy.mesh.position, enemy.color);
                    enemy.destroy();
                    this.enemies.splice(i, 1);
                    this.playerBullets.splice(j, 1);
                    this.score += enemy.scoreValue;
                    this.kills++;
                    break;
                }
            }
            
            // Check collision with player
            if (enemy.checkHit(this.player.mesh.position)) {
                this.player.takeDamage(20);
                this.createExplosion(enemy.mesh.position, 0xff0000);
                enemy.destroy();
                this.enemies.splice(i, 1);
            }
        }
    }
    
    updateBullets(delta) {
        // Player bullets
        for (let i = this.playerBullets.length - 1; i >= 0; i--) {
            const bullet = this.playerBullets[i];
            bullet.update(delta);
            
            if (bullet.life <= 0 || bullet.distanceTraveled > 500) {
                bullet.destroy();
                this.playerBullets.splice(i, 1);
            }
        }
        
        // Enemy bullets
        for (let i = this.enemyBullets.length - 1; i >= 0; i--) {
            const bullet = this.enemyBullets[i];
            bullet.update(delta);
            
            // Check hit on player
            const dist = bullet.mesh.position.distanceTo(this.player.mesh.position);
            if (dist < 5) {
                this.player.takeDamage(10);
                bullet.destroy();
                this.enemyBullets.splice(i, 1);
                continue;
            }
            
            if (bullet.life <= 0) {
                bullet.destroy();
                this.enemyBullets.splice(i, 1);
            }
        }
    }
    
    updateParticles(delta) {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.update(delta);
            if (p.life <= 0) {
                p.destroy();
                this.particles.splice(i, 1);
            }
        }
    }
    
    createExplosion(position, color) {
        for (let i = 0; i < 20; i++) {
            this.particles.push(new Particle(this.scene, position, color));
        }
    }
    
    checkWaveStatus() {
        if (this.enemies.length === 0 && this.waveInProgress) {
            this.waveInProgress = false;
            this.waveCooldown = 3; // 3 seconds before next wave
            
            setTimeout(() => {
                this.wave++;
                this.startWave();
            }, 3000);
        }
    }
    
    updateHUD() {
        document.getElementById('score').textContent = this.score.toLocaleString();
        document.getElementById('kills').textContent = this.kills;
        document.getElementById('waveNum').textContent = this.wave;
        document.getElementById('gameTime').textContent = this.formatTime(this.gameTime);
        document.getElementById('shieldBar').style.width = (this.player.shield / this.player.maxShield * 100) + '%';
        document.getElementById('hullBar').style.width = (this.player.hull / this.player.maxHull * 100) + '%';
        document.getElementById('heat').textContent = Math.floor(this.player.weaponHeat) + '%';
        
        if (this.player.hull <= 0) {
            this.gameOver();
        }
    }
    
    updateRadar() {
        const canvas = document.getElementById('radarCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 180;
        canvas.height = 180;
        
        // Background
        ctx.fillStyle = 'rgba(0, 20, 40, 0.8)';
        ctx.fillRect(0, 0, 180, 180);
        
        // Grid
        ctx.strokeStyle = 'rgba(255, 68, 0, 0.3)';
        ctx.beginPath();
        ctx.arc(90, 90, 60, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(90, 90, 30, 0, Math.PI * 2);
        ctx.stroke();
        
        // Player (center)
        ctx.fillStyle = '#00ff00';
        ctx.fillRect(87, 87, 6, 6);
        
        // Enemies
        this.enemies.forEach(enemy => {
            const dx = enemy.mesh.position.x - this.player.mesh.position.x;
            const dz = enemy.mesh.position.z - this.player.mesh.position.z;
            const rx = dx / 5 + 90;
            const ry = dz / 5 + 90;
            
            if (rx > 0 && rx < 180 && ry > 0 && ry < 180) {
                ctx.fillStyle = '#ff0000';
                ctx.beginPath();
                ctx.arc(rx, ry, 4, 0, Math.PI * 2);
                ctx.fill();
            }
        });
        
        // Sweep line
        const time = Date.now() * 0.002;
        ctx.strokeStyle = 'rgba(0, 255, 0, 0.5)';
        ctx.beginPath();
        ctx.moveTo(90, 90);
        ctx.lineTo(90 + Math.cos(time) * 85, 90 + Math.sin(time) * 85);
        ctx.stroke();
    }
    
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    
    gameOver() {
        this.state = 'gameover';
        document.exitPointerLock();
        document.getElementById('gameOver').style.display = 'flex';
        document.getElementById('finalScore').textContent = `Score: ${this.score.toLocaleString()}`;
    }
    
    restart() {
        // Cleanup
        this.enemies.forEach(e => e.destroy());
        this.playerBullets.forEach(b => b.destroy());
        this.enemyBullets.forEach(b => b.destroy());
        this.particles.forEach(p => p.destroy());
        
        this.enemies = [];
        this.playerBullets = [];
        this.enemyBullets = [];
        this.particles = [];
        
        // Reset player
        this.player.reset();
        
        // Restart
        this.start();
    }
    
    cleanup() {
        this.state = 'menu';
        // Cleanup logic if needed
    }
    
    onResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        const delta = Math.min(this.clock.getDelta(), 0.1);
        this.update(delta);
        this.renderer.render(this.scene, this.camera);
    }
}

// Player Ship Class
class PlayerShip {
    constructor(scene) {
        this.scene = scene;
        this.maxShield = 100;
        this.maxHull = 100;
        this.shield = 100;
        this.hull = 100;
        this.weaponHeat = 0;
        this.lastFireTime = 0;
        this.fireRate = 150; // ms
        
        this.mesh = this.createMesh();
        scene.add(this.mesh);
    }
    
    createMesh() {
        const group = new THREE.Group();
        
        // Main body
        const body = new THREE.Mesh(
            new THREE.ConeGeometry(2, 8, 6),
            new THREE.MeshPhongMaterial({ color: 0x4488ff, emissive: 0x112244 })
        );
        body.rotation.x = -Math.PI / 2;
        group.add(body);
        
        // Wings
        const wings = new THREE.Mesh(
            new THREE.BoxGeometry(10, 0.5, 3),
            new THREE.MeshPhongMaterial({ color: 0x3366cc })
        );
        wings.position.set(0, 0, 2);
        group.add(wings);
        
        // Engines
        const engineGeo = new THREE.CylinderGeometry(1, 1.5, 2, 8);
        engineGeo.rotateX(Math.PI / 2);
        const engineMat = new THREE.MeshPhongMaterial({ 
            color: 0xff6600,
            emissive: 0xff2200,
            emissiveIntensity: 0.5
        });
        
        const leftEngine = new THREE.Mesh(engineGeo, engineMat);
        leftEngine.position.set(-3, 0, 4);
        group.add(leftEngine);
        
        const rightEngine = new THREE.Mesh(engineGeo, engineMat);
        rightEngine.position.set(3, 0, 4);
        group.add(rightEngine);
        
        // Engine glow
        const glowGeo = new THREE.SphereGeometry(2, 8, 8);
        const glowMat = new THREE.MeshBasicMaterial({ 
            color: 0x4488ff,
            transparent: true,
            opacity: 0.3
        });
        const glow = new THREE.Mesh(glowGeo, glowMat);
        glow.position.set(0, 0, 5);
        group.add(glow);
        this.engineGlow = glow;
        
        return group;
    }
    
    update(delta, thrust, turn, mouse) {
        // Rotation from mouse/joystick
        this.mesh.rotation.y -= mouse.x * 2;
        this.mesh.rotation.x = mouse.y * 0.5;
        this.mesh.rotation.z += turn * delta * 2;
        
        // Movement
        const speed = thrust * 80 * delta;
        this.mesh.translateZ(-speed);
        
        // Engine effect
        const scale = 1 + thrust * 0.3 + Math.random() * 0.1;
        this.engineGlow.scale.setScalar(scale);
        
        // Weapon cooldown
        if (this.weaponHeat > 0) {
            this.weaponHeat -= delta * 30;
            if (this.weaponHeat < 0) this.weaponHeat = 0;
        }
        
        // Boundary check
        this.mesh.position.x = Math.max(-500, Math.min(500, this.mesh.position.x));
        this.mesh.position.z = Math.max(-500, Math.min(500, this.mesh.position.z));
    }
    
    fire() {
        if (this.weaponHeat >= 100) return;
        if (Date.now() - this.lastFireTime < this.fireRate) return;
        
        this.lastFireTime = Date.now();
        this.weaponHeat += 10;
        
        // Get bullet spawn position
        const pos = this.mesh.position.clone();
        pos.y += 1;
        
        const bullet = new Bullet(this.scene, pos, this.mesh.rotation, 300, 0x00ffff, true);
        game.playerBullets.push(bullet);
    }
    
    takeDamage(amount) {
        if (this.shield > 0) {
            this.shield -= amount;
            if (this.shield < 0) {
                this.hull += this.shield;
                this.shield = 0;
            }
        } else {
            this.hull -= amount;
        }
    }
    
    reset() {
        this.shield = this.maxShield;
        this.hull = this.maxHull;
        this.weaponHeat = 0;
        this.mesh.position.set(0, 0, 0);
        this.mesh.rotation.set(0, 0, 0);
    }
}

// Enemy Ship Class
class EnemyShip {
    constructor(scene, type, x, y, z) {
        this.scene = scene;
        this.type = type;
        this.lastFireTime = 0;
        
        // Type stats
        switch(type) {
            case 'interceptor':
                this.speed = 40;
                this.health = 30;
                this.scoreValue = 200;
                this.color = 0xff4400;
                this.fireRate = 2000;
                break;
            case 'bomber':
                this.speed = 20;
                this.health = 80;
                this.scoreValue = 500;
                this.color = 0xff0044;
                this.fireRate = 3000;
                break;
            default: // fighter
                this.speed = 30;
                this.health = 50;
                this.scoreValue = 100;
                this.color = 0xff8844;
                this.fireRate = 1500;
        }
        
        this.mesh = this.createMesh();
        this.mesh.position.set(x, y, z);
        scene.add(this.mesh);
    }
    
    createMesh() {
        const group = new THREE.Group();
        
        const material = new THREE.MeshPhongMaterial({ 
            color: this.color,
            emissive: this.color,
            emissiveIntensity: 0.3
        });
        
        // Body
        const body = new THREE.Mesh(new THREE.ConeGeometry(2, 6, 6), material);
        body.rotation.x = Math.PI / 2;
        group.add(body);
        
        // Wings
        const wings = new THREE.Mesh(
            new THREE.BoxGeometry(8, 0.5, 2),
            material
        );
        group.add(wings);
        
        return group;
    }
    
    update(delta, player) {
        // Chase player
        const direction = new THREE.Vector3();
        direction.subVectors(player.mesh.position, this.mesh.position).normalize();
        
        // Move toward player
        this.mesh.position.add(direction.multiplyScalar(this.speed * delta));
        
        // Face player
        this.mesh.lookAt(player.mesh.position);
    }
    
    canFire() {
        return Date.now() - this.lastFireTime > this.fireRate;
    }
    
    fire() {
        this.lastFireTime = Date.now();
        const bullet = new Bullet(
            this.scene, 
            this.mesh.position.clone(), 
            this.mesh.rotation, 
            150, 
            0xff0000, 
            false
        );
        return bullet;
    }
    
    checkHit(position) {
        return this.mesh.position.distanceTo(position) < 4;
    }
    
    destroy() {
        this.scene.remove(this.mesh);
    }
}

// Bullet Class
class Bullet {
    constructor(scene, position, rotation, speed, color, isPlayer) {
        this.scene = scene;
        this.speed = speed;
        this.life = 3;
        this.distanceTraveled = 0;
        this.isPlayer = isPlayer;
        
        this.mesh = new THREE.Mesh(
            new THREE.SphereGeometry(0.5, 8, 8),
            new THREE.MeshBasicMaterial({ color: color })
        );
        
        this.mesh.position.copy(position);
        this.mesh.rotation.copy(rotation);
        
        // Add glow
        const glow = new THREE.Mesh(
            new THREE.SphereGeometry(1, 8, 8),
            new THREE.MeshBasicMaterial({ 
                color: color,
                transparent: true,
                opacity: 0.3
            })
        );
        this.mesh.add(glow);
        
        scene.add(this.mesh);
    }
    
    update(delta) {
        const velocity = new THREE.Vector3(0, 0, -this.speed * delta);
        velocity.applyEuler(this.mesh.rotation);
        
        this.mesh.position.add(velocity);
        this.distanceTraveled += this.speed * delta;
        this.life -= delta;
    }
    
    destroy() {
        this.scene.remove(this.mesh);
    }
}

// Particle Class (explosions)
class Particle {
    constructor(scene, position, color) {
        this.scene = scene;
        this.life = 1 + Math.random();
        this.velocity = new THREE.Vector3(
            (Math.random() - 0.5) * 30,
            (Math.random() - 0.5) * 30,
            (Math.random() - 0.5) * 30
        );
        
        this.mesh = new THREE.Mesh(
            new THREE.SphereGeometry(0.5 + Math.random(), 4, 4),
            new THREE.MeshBasicMaterial({ 
                color: color,
                transparent: true,
                opacity: 1
            })
        );
        this.mesh.position.copy(position);
        scene.add(this.mesh);
    }
    
    update(delta) {
        this.mesh.position.add(this.velocity.clone().multiplyScalar(delta));
        this.life -= delta;
        this.mesh.material.opacity = this.life / 1.5;
        this.mesh.scale.multiplyScalar(0.98);
    }
    
    destroy() {
        this.scene.remove(this.mesh);
    }
}

// Global game reference
let game;
