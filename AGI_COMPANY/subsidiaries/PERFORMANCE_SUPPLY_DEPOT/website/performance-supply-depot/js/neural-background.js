// Neural Network Background - Three.js
// Embeddable in any page as background or widget

class NeuralBackground {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;
        
        this.options = {
            nodeCount: options.nodeCount || 40,
            radius: options.radius || 6,
            color: options.color || 0xed8936,
            backgroundColor: options.backgroundColor || 0x0a0a1a,
            autoRotate: options.autoRotate !== false,
            interactive: options.interactive !== false,
            ...options
        };
        
        this.init();
    }
    
    init() {
        // Scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(this.options.backgroundColor);
        this.scene.fog = new THREE.Fog(this.options.backgroundColor, 10, 50);
        
        // Camera
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
        this.camera.position.z = 15;
        
        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.container.appendChild(this.renderer.domElement);
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
        this.scene.add(ambientLight);
        
        const pointLight1 = new THREE.PointLight(this.options.color, 1, 100);
        pointLight1.position.set(10, 10, 10);
        this.scene.add(pointLight1);
        
        // Create nodes
        this.nodes = [];
        this.connections = [];
        this.createNetwork();
        
        // Interactivity
        if (this.options.interactive) {
            this.setupInteraction();
        }
        
        // Animation
        this.time = 0;
        this.rotationSpeed = { x: 0, y: 0 };
        this.animate();
        
        // Resize handler
        window.addEventListener('resize', () => this.onResize());
    }
    
    createNetwork() {
        const nodeGeometry = new THREE.SphereGeometry(0.12, 16, 16);
        const nodeMaterial = new THREE.MeshStandardMaterial({
            color: this.options.color,
            emissive: this.options.color,
            emissiveIntensity: 0.5,
            metalness: 0.8,
            roughness: 0.2
        });
        
        // Create nodes
        for (let i = 0; i < this.options.nodeCount; i++) {
            const phi = Math.acos(-1 + (2 * i) / this.options.nodeCount);
            const theta = Math.sqrt(this.options.nodeCount * Math.PI) * phi;
            
            const x = this.options.radius * Math.cos(theta) * Math.sin(phi);
            const y = this.options.radius * Math.sin(theta) * Math.sin(phi);
            const z = this.options.radius * Math.cos(phi);
            
            const node = new THREE.Mesh(nodeGeometry, nodeMaterial.clone());
            node.position.set(x, y, z);
            node.userData.originalPos = node.position.clone();
            node.userData.phase = Math.random() * Math.PI * 2;
            node.userData.speed = 0.5 + Math.random() * 0.5;
            
            this.scene.add(node);
            this.nodes.push(node);
        }
        
        // Create connections
        const lineMaterial = new THREE.LineBasicMaterial({
            color: this.options.color,
            transparent: true,
            opacity: 0.1
        });
        
        for (let i = 0; i < this.nodes.length; i++) {
            for (let j = i + 1; j < this.nodes.length; j++) {
                const dist = this.nodes[i].position.distanceTo(this.nodes[j].position);
                if (dist < 4) {
                    const geometry = new THREE.BufferGeometry().setFromPoints([
                        this.nodes[i].position,
                        this.nodes[j].position
                    ]);
                    const line = new THREE.Line(geometry, lineMaterial);
                    line.userData.nodeIndices = [i, j];
                    this.scene.add(line);
                    this.connections.push(line);
                }
            }
        }
        
        // Center glow
        const glowGeometry = new THREE.SphereGeometry(1.5, 32, 32);
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: this.options.color,
            transparent: true,
            opacity: 0.08
        });
        this.glow = new THREE.Mesh(glowGeometry, glowMaterial);
        this.scene.add(this.glow);
    }
    
    setupInteraction() {
        let isDragging = false;
        let previousMousePosition = { x: 0, y: 0 };
        
        this.container.addEventListener('mousemove', (e) => {
            if (isDragging) {
                this.rotationSpeed.x = (e.clientX - previousMousePosition.x) * 0.005;
                this.rotationSpeed.y = (e.clientY - previousMousePosition.y) * 0.005;
            }
            previousMousePosition = { x: e.clientX, y: e.clientY };
        });
        
        this.container.addEventListener('mousedown', () => isDragging = true);
        this.container.addEventListener('mouseup', () => isDragging = false);
        
        this.container.addEventListener('wheel', (e) => {
            this.camera.position.z += e.deltaY * 0.01;
            this.camera.position.z = Math.max(8, Math.min(30, this.camera.position.z));
        });
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        this.time += 0.01;
        
        // Auto-rotate
        if (this.options.autoRotate) {
            this.scene.rotation.y += 0.001 + this.rotationSpeed.x;
            this.scene.rotation.x += this.rotationSpeed.y;
        }
        
        // Damping
        this.rotationSpeed.x *= 0.95;
        this.rotationSpeed.y *= 0.95;
        
        // Animate nodes
        this.nodes.forEach((node, i) => {
            const pulse = Math.sin(this.time * node.userData.speed + node.userData.phase) * 0.3;
            node.scale.setScalar(1 + pulse * 0.5);
            
            node.position.x = node.userData.originalPos.x + Math.sin(this.time + i) * 0.15;
            node.position.y = node.userData.originalPos.y + Math.cos(this.time + i) * 0.15;
            node.position.z = node.userData.originalPos.z + Math.sin(this.time * 0.5 + i) * 0.15;
        });
        
        // Update connections
        this.connections.forEach(line => {
            const [i, j] = line.userData.nodeIndices;
            const positions = line.geometry.attributes.position.array;
            positions[0] = this.nodes[i].position.x;
            positions[1] = this.nodes[i].position.y;
            positions[2] = this.nodes[i].position.z;
            positions[3] = this.nodes[j].position.x;
            positions[4] = this.nodes[j].position.y;
            positions[5] = this.nodes[j].position.z;
            line.geometry.attributes.position.needsUpdate = true;
        });
        
        // Pulse glow
        if (this.glow) {
            this.glow.scale.setScalar(1 + Math.sin(this.time) * 0.1);
        }
        
        this.renderer.render(this.scene, this.camera);
    }
    
    onResize() {
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.aspect = aspect;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
    
    destroy() {
        this.renderer.dispose();
        this.container.removeChild(this.renderer.domElement);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Full background
    const bgContainer = document.getElementById('neural-background');
    if (bgContainer) {
        new NeuralBackground('neural-background', {
            nodeCount: 50,
            radius: 8,
            autoRotate: true,
            interactive: true
        });
    }
    
    // Dashboard widget
    const widgetContainer = document.getElementById('neural-widget');
    if (widgetContainer) {
        new NeuralBackground('neural-widget', {
            nodeCount: 25,
            radius: 4,
            autoRotate: true,
            interactive: false
        });
    }
    
    // Agent status background
    const agentBg = document.getElementById('agent-neural-bg');
    if (agentBg) {
        new NeuralBackground('agent-neural-bg', {
            nodeCount: 40,
            radius: 6,
            autoRotate: true,
            interactive: true
        });
    }
});
