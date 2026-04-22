/**
 * Space Universe Background - Three.js Animated Space
 * Floating agents with connection lines
 */

class SpaceUniverse {
    constructor() {
        this.canvas = document.getElementById('universe');
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, alpha: true });
        
        this.stars = [];
        this.nebulas = [];
        this.agents = [];
        this.connections = [];
        
        this.init();
    }
    
    init() {
        // Setup renderer
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        
        // Camera position
        this.camera.position.z = 50;
        
        // Create starfield
        this.createStarfield();
        
        // Create nebula background
        this.createNebula();
        
        // Add ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
        this.scene.add(ambientLight);
        
        // Point lights for neon glow
        const cyanLight = new THREE.PointLight(0x00f3ff, 1, 100);
        cyanLight.position.set(20, 20, 20);
        this.scene.add(cyanLight);
        
        const purpleLight = new THREE.PointLight(0x8b5cf6, 1, 100);
        purpleLight.position.set(-20, -20, 20);
        this.scene.add(purpleLight);
        
        // Start animation
        this.animate();
        
        // Handle resize
        window.addEventListener('resize', () => this.onResize());
    }
    
    createStarfield() {
        const starGeometry = new THREE.BufferGeometry();
        const starCount = 3000;
        const positions = new Float32Array(starCount * 3);
        const colors = new Float32Array(starCount * 3);
        
        for (let i = 0; i < starCount * 3; i += 3) {
            // Random positions in large sphere
            const r = 100 + Math.random() * 400;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            
            positions[i] = r * Math.sin(phi) * Math.cos(theta);
            positions[i + 1] = r * Math.sin(phi) * Math.sin(theta);
            positions[i + 2] = r * Math.cos(phi);
            
            // Star colors (blue-white to purple)
            const colorType = Math.random();
            if (colorType < 0.7) {
                // Blue-white
                colors[i] = 0.8 + Math.random() * 0.2;
                colors[i + 1] = 0.9 + Math.random() * 0.1;
                colors[i + 2] = 1.0;
            } else if (colorType < 0.9) {
                // Cyan
                colors[i] = 0.0;
                colors[i + 1] = 0.9 + Math.random() * 0.1;
                colors[i + 2] = 1.0;
            } else {
                // Purple
                colors[i] = 0.5 + Math.random() * 0.2;
                colors[i + 1] = 0.2;
                colors[i + 2] = 0.9 + Math.random() * 0.1;
            }
        }
        
        starGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        starGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        
        const starMaterial = new THREE.PointsMaterial({
            size: 0.5,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            sizeAttenuation: true
        });
        
        this.starField = new THREE.Points(starGeometry, starMaterial);
        this.scene.add(this.starField);
    }
    
    createNebula() {
        // Create nebula clouds using particle systems
        const nebulaColors = [0x00f3ff, 0x8b5cf6, 0xff7a00, 0xff00ff];
        
        nebulaColors.forEach((color, index) => {
            const particleCount = 500;
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            
            for (let i = 0; i < particleCount * 3; i += 3) {
                positions[i] = (Math.random() - 0.5) * 200;
                positions[i + 1] = (Math.random() - 0.5) * 200;
                positions[i + 2] = (Math.random() - 0.5) * 100 - 50;
            }
            
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            
            const material = new THREE.PointsMaterial({
                color: color,
                size: 2 + Math.random() * 2,
                transparent: true,
                opacity: 0.1 + Math.random() * 0.1,
                blending: THREE.AdditiveBlending
            });
            
            const nebula = new THREE.Points(geometry, material);
            nebula.userData = {
                rotationSpeed: 0.0005 * (Math.random() - 0.5),
                driftSpeed: {
                    x: (Math.random() - 0.5) * 0.02,
                    y: (Math.random() - 0.5) * 0.02
                }
            };
            
            this.nebulas.push(nebula);
            this.scene.add(nebula);
        });
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Rotate starfield slowly
        this.starField.rotation.y += 0.0002;
        this.starField.rotation.x += 0.0001;
        
        // Animate nebulas
        this.nebulas.forEach(nebula => {
            nebula.rotation.z += nebula.userData.rotationSpeed;
            nebula.position.x += nebula.userData.driftSpeed.x;
            nebula.position.y += nebula.userData.driftSpeed.y;
            
            // Wrap around
            if (Math.abs(nebula.position.x) > 100) {
                nebula.position.x *= -0.9;
            }
            if (Math.abs(nebula.position.y) > 100) {
                nebula.position.y *= -0.9;
            }
        });
        
        // Update agent positions if they exist in 3D space
        this.updateAgentPositions();
        
        this.renderer.render(this.scene, this.camera);
    }
    
    updateAgentPositions() {
        // Map DOM agent positions to 3D connections
        const agents = document.querySelectorAll('.agent-widget');
        agents.forEach((agent, i) => {
            const rect = agent.getBoundingClientRect();
            // Normalize to 3D space
            const x = (rect.left / window.innerWidth) * 2 - 1;
            const y = -(rect.top / window.innerHeight) * 2 + 1;
            
            // Could create 3D agents here
        });
    }
    
    onResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// Initialize when DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.universe = new SpaceUniverse();
});
