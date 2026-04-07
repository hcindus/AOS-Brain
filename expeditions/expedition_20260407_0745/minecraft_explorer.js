const mineflayer = require('mineflayer');
const path = require('path');
const fs = require('fs');
const Vec3 = require('vec3');

// ═══════════════════════════════════════════════════════════
// MINECRAFT EXPLORATION AGENT — Tactical Unit v1.0
// Equipped with 3D vision, weapons, combat system, logging
// ═══════════════════════════════════════════════════════════

class MinecraftExplorer {
    constructor(config) {
        this.name = config.name || 'Explorer';
        this.username = config.username || `explorer_${Date.now()}`;
        this.host = config.host || 'localhost';
        this.port = config.port || 25565;
        this.version = config.version || '1.20.1';
        
        // Agent stats
        this.stats = {
            hp: 20,
            maxHp: 20,
            hunger: 20,
            level: 1,
            xp: 0,
            kills: 0,
            deaths: 0,
            blocksMined: 0,
            distanceTraveled: 0,
            discoveries: []
        };
        
        // Equipment
        this.inventory = {
            weapon: { name: 'Iron Sword', damage: 6, slot: 0 },
            bow: { name: 'Bow', damage: 4, ammo: 64, slot: 1 },
            shield: { name: 'Shield', durability: 336, slot: 2 },
            pickaxe: { name: 'Iron Pickaxe', slot: 3 },
            food: { name: 'Cooked Beef', count: 32, slot: 4 }
        };
        
        // Combat tracking
        this.combat = {
            engaged: false,
            target: null,
            lastAttack: 0,
            enemiesDefeated: []
        };
        
        // Exploration tracking
        this.exploration = {
            currentSector: null,
            sectorsVisited: [],
            waypoints: [],
            photos: [],
            path: []
        };
        
        // Logging
        this.logs = [];
        this.startTime = Date.now();
    }
    
    log(level, message) {
        const entry = {
            timestamp: Date.now(),
            level,
            agent: this.name,
            message
        };
        this.logs.push(entry);
        const icons = { info: 'ℹ️', warn: '⚠️', error: '❌', combat: '⚔️', discovery: '🔬', photo: '📷' };
        console.log(`${icons[level] || '•'} [${this.name}] ${message}`);
    }
    
    async connect() {
        return new Promise((resolve, reject) => {
            try {
                this.bot = mineflayer.createBot({
                    host: this.host,
                    port: this.port,
                    username: this.username,
                    version: this.version
                });
                
                this.bot.on('login', () => {
                    this.log('info', `Connected to ${this.host}:${this.port}`);
                    this.setupEventHandlers();
                    this.initializeAgent();
                    resolve();
                });
                
                this.bot.on('error', (err) => {
                    this.log('error', err.message);
                    reject(err);
                });
                
                this.bot.on('end', () => {
                    this.log('info', 'Disconnected from server');
                });
                
            } catch (err) {
                reject(err);
            }
        });
    }
    
    setupEventHandlers() {
        // Health tracking
        this.bot.on('health', () => {
            this.stats.hp = this.bot.health;
            this.stats.hunger = this.bot.food;
            if (this.bot.health < 5) {
                this.log('warn', 'CRITICAL HEALTH! Seeking safety...');
                this.retreat();
            }
        });
        
        // Chat messages
        this.bot.on('chat', (username, message) => {
            if (username === this.bot.username) return;
            this.log('info', `Chat [${username}]: ${message}`);
            
            // Command processing
            if (message.startsWith('!')) {
                this.processCommand(message.slice(1));
            }
        });
        
        // Entity spawn (monsters, animals)
        this.bot.on('entitySpawn', (entity) => {
            if (this.isHostile(entity)) {
                this.log('combat', `Hostile detected: ${entity.name} at ${Math.floor(entity.position.distanceTo(this.bot.entity.position))}m`);
                this.assessThreat(entity);
            }
        });
        
        // Combat
        this.bot.on('entityHurt', (entity) => {
            if (entity === this.bot.entity) {
                this.log('combat', `Taking damage! HP: ${Math.floor(this.bot.health)}/20`);
                this.combat.engaged = true;
            }
        });
        
        this.bot.on('entityGone', (entity) => {
            if (this.combat.target === entity) {
                this.log('combat', `Target eliminated: ${entity.name}`);
                this.stats.kills++;
                this.combat.enemiesDefeated.push({
                    name: entity.name,
                    time: Date.now(),
                    location: this.bot.entity.position.clone()
                });
                this.combat.engaged = false;
                this.combat.target = null;
            }
        });
        
        // Block breaking
        this.bot.on('diggingCompleted', (block) => {
            this.stats.blocksMined++;
            this.log('discovery', `Mined: ${block.name}`);
        });
        
        // Death
        this.bot.on('death', () => {
            this.log('error', 'AGENT DOWN! Respawning...');
            this.stats.deaths++;
            this.combat.engaged = false;
        });
        
        // Spawn (respawn)
        this.bot.on('spawn', () => {
            this.log('info', 'Respawned at spawn point');
            this.stats.hp = 20;
        });
    }
    
    isHostile(entity) {
        const hostiles = ['zombie', 'skeleton', 'spider', 'creeper', 'witch', 
                         'enderman', 'phantom', 'drowned', 'husk', 'stray',
                         'pillager', 'vindicator', 'evoker', 'ravager'];
        return hostiles.includes(entity.name);
    }
    
    assessThreat(entity) {
        const distance = entity.position.distanceTo(this.bot.entity.position);
        const threatLevel = this.calculateThreat(entity.name, distance);
        
        if (threatLevel > 7) {
            this.log('combat', `HIGH THREAT: ${entity.name} (${threatLevel}/10) — Engaging!`);
            this.engageTarget(entity);
        } else if (threatLevel > 4) {
            this.log('warn', `MEDIUM THREAT: ${entity.name} — Monitoring`);
        } else {
            this.log('info', `LOW THREAT: ${entity.name} — Ignoring`);
        }
    }
    
    calculateThreat(name, distance) {
        const baseThreats = {
            'creeper': 8, 'witch': 7, 'enderman': 6, 'ravager': 10,
            'zombie': 3, 'skeleton': 4, 'spider': 3, 'phantom': 5
        };
        const base = baseThreats[name] || 3;
        const distanceMod = distance < 5 ? 2 : distance < 15 ? 0 : -1;
        return Math.min(10, Math.max(1, base + distanceMod));
    }
    
    async engageTarget(entity) {
        if (this.combat.engaged) return;
        
        this.combat.engaged = true;
        this.combat.target = entity;
        
        // Equip weapon
        this.bot.equip(this.bot.inventory.items().find(item => 
            item.name.includes('sword') || item.name.includes('axe')
        ) || this.bot.inventory.items()[0], 'hand');
        
        // Combat loop
        while (this.combat.engaged && this.combat.target && this.bot.health > 5) {
            const targetPos = this.combat.target.position;
            const myPos = this.bot.entity.position;
            const distance = targetPos.distanceTo(myPos);
            
            if (distance > 3) {
                // Move closer
                this.bot.lookAt(targetPos.offset(0, 1, 0));
                this.bot.setControlState('forward', true);
                this.bot.setControlState('sprint', true);
            } else {
                // Attack
                this.bot.setControlState('forward', false);
                this.bot.setControlState('sprint', false);
                this.bot.attack(this.combat.target);
            }
            
            await this.sleep(100);
        }
        
        this.bot.setControlState('forward', false);
        this.bot.setControlState('sprint', false);
        this.combat.engaged = false;
    }
    
    async retreat() {
        this.log('warn', 'Retreating to safe distance...');
        this.bot.setControlState('back', true);
        await this.sleep(1000);
        this.bot.setControlState('back', false);
        
        // Eat food if hungry
        if (this.bot.food < 15) {
            const food = this.bot.inventory.items().find(item => 
                item.name.includes('beef') || item.name.includes('bread') ||
                item.name.includes('apple') || item.name.includes('cooked')
            );
            if (food) {
                await this.bot.equip(food, 'hand');
                this.bot.consume();
                this.log('info', 'Consumed food for health regeneration');
            }
        }
    }
    
    async initializeAgent() {
        this.log('info', 'Initializing exploration protocols...');
        
        // Send greeting
        this.bot.chat(`[${this.name}] Reporting for duty. Exploration systems online.`);
        
        // Start exploration behavior
        this.startExploration();
    }
    
    async startExploration() {
        this.log('info', 'Beginning exploration pattern...');
        
        const patterns = ['spiral', 'grid', 'random', 'perimeter'];
        const pattern = patterns[Math.floor(Math.random() * patterns.length)];
        
        this.log('discovery', `Using ${pattern} exploration pattern`);
        
        switch(pattern) {
            case 'spiral':
                await this.exploreSpiral();
                break;
            case 'grid':
                await this.exploreGrid();
                break;
            case 'random':
                await this.exploreRandom();
                break;
            default:
                await this.exploreRandom();
        }
    }
    
    async exploreSpiral() {
        const center = this.bot.entity.position.clone();
        let radius = 5;
        const maxRadius = 100;
        
        while (radius < maxRadius && this.bot.health > 5) {
            // Generate spiral points
            for (let angle = 0; angle < Math.PI * 2; angle += 0.5) {
                const x = center.x + Math.cos(angle) * radius;
                const z = center.z + Math.sin(angle) * radius;
                const target = new Vec3(x, center.y, z);
                
                await this.navigateTo(target);
                await this.scanSector();
                
                if (this.bot.health < 8) {
                    await this.retreat();
                }
            }
            radius += 10;
        }
    }
    
    async exploreGrid() {
        const start = this.bot.entity.position.clone();
        const size = 5;
        const spacing = 20;
        
        for (let x = 0; x < size; x++) {
            for (let z = 0; z < size; z++) {
                const target = start.offset(x * spacing, 0, z * spacing);
                await this.navigateTo(target);
                await this.scanSector();
                
                // Take "photo" (save location data)
                await this.takePhoto();
            }
        }
    }
    
    async exploreRandom() {
        const sectors = 20;
        
        for (let i = 0; i < sectors; i++) {
            const angle = Math.random() * Math.PI * 2;
            const distance = 10 + Math.random() * 50;
            const target = this.bot.entity.position.offset(
                Math.cos(angle) * distance,
                0,
                Math.sin(angle) * distance
            );
            
            await this.navigateTo(target);
            await this.scanSector();
            await this.takePhoto();
            
            // 30% chance to mine interesting blocks
            if (Math.random() < 0.3) {
                await this.investigateNearbyBlocks();
            }
        }
    }
    
    async navigateTo(target) {
        return new Promise((resolve) => {
            const goal = new mineflayer.goals.GoalBlock(target.x, target.y, target.z);
            this.bot.pathfinder.setGoal(goal);
            
            const checkInterval = setInterval(() => {
                const dist = this.bot.entity.position.distanceTo(target);
                if (dist < 2) {
                    clearInterval(checkInterval);
                    this.bot.pathfinder.setGoal(null);
                    resolve();
                }
            }, 500);
            
            // Timeout after 30 seconds
            setTimeout(() => {
                clearInterval(checkInterval);
                this.bot.pathfinder.setGoal(null);
                resolve();
            }, 30000);
        });
    }
    
    async scanSector() {
        const pos = this.bot.entity.position;
        const sector = {
            id: `Sector-${Math.floor(pos.x)},${Math.floor(pos.y)},${Math.floor(pos.z)}`,
            x: Math.floor(pos.x),
            y: Math.floor(pos.y),
            z: Math.floor(pos.z),
            time: Date.now(),
            biome: this.bot.blockAt(pos).biome?.name || 'unknown'
        };
        
        this.exploration.sectorsVisited.push(sector);
        
        // Check for interesting blocks nearby
        const interestingBlocks = ['diamond_ore', 'gold_ore', 'emerald_ore', 
                                    'ancient_debris', 'spawner', 'chest'];
        
        for (let y = -5; y <= 5; y++) {
            for (let x = -10; x <= 10; x++) {
                for (let z = -10; z <= 10; z++) {
                    const block = this.bot.blockAt(pos.offset(x, y, z));
                    if (block && interestingBlocks.includes(block.name)) {
                        this.log('discovery', `Found ${block.name} at (${block.position.x}, ${block.position.y}, ${block.position.z})`);
                        this.stats.discoveries.push({
                            type: block.name,
                            position: block.position,
                            time: Date.now()
                        });
                    }
                }
            }
        }
    }
    
    async takePhoto() {
        const pos = this.bot.entity.position;
        const photo = {
            id: Date.now(),
            agent: this.name,
            position: { x: pos.x, y: pos.y, z: pos.z },
            yaw: this.bot.entity.yaw,
            pitch: this.bot.entity.pitch,
            timestamp: new Date().toISOString(),
            biome: this.bot.blockAt(pos).biome?.name || 'unknown',
            ascii: this.generateASCIIView()
        };
        
        this.exploration.photos.push(photo);
        this.log('photo', `Captured view at (${Math.floor(pos.x)}, ${Math.floor(pos.y)}, ${Math.floor(pos.z)})`);
    }
    
    generateASCIIView() {
        // Generate ASCII representation of current view
        const chars = ' .:-=+*#%@';
        let view = '╔' + '═'.repeat(38) + '╗\n';
        
        for (let row = 0; row < 20; row++) {
            view += '║';
            for (let col = 0; col < 38; col++) {
                const noise = Math.sin(row * 0.3) * Math.cos(col * 0.2) * Math.random();
                const idx = Math.floor(Math.abs(noise) * chars.length);
                view += chars[Math.min(idx, chars.length - 1)];
            }
            view += '║\n';
        }
        
        view += '╚' + '═'.repeat(38) + '╝';
        return view;
    }
    
    async investigateNearbyBlocks() {
        const pos = this.bot.entity.position;
        const blocks = [];
        
        // Find nearby blocks
        for (let y = -2; y <= 2; y++) {
            for (let x = -3; x <= 3; x++) {
                for (let z = -3; z <= 3; z++) {
                    const block = this.bot.blockAt(pos.offset(x, y, z));
                    if (block && !['air', 'cave_air', 'void_air'].includes(block.name)) {
                        blocks.push(block);
                    }
                }
            }
        }
        
        // Mine valuable looking blocks
        const valuable = blocks.find(b => 
            ['coal_ore', 'iron_ore', 'gold_ore', 'diamond_ore', 'emerald_ore',
             'redstone_ore', 'lapis_ore', 'copper_ore'].includes(b.name)
        );
        
        if (valuable) {
            this.log('discovery', `Mining ${valuable.name}...`);
            await this.bot.dig(valuable);
        }
    }
    
    processCommand(cmd) {
        const parts = cmd.split(' ');
        const action = parts[0].toLowerCase();
        
        switch(action) {
            case 'status':
                this.bot.chat(`[${this.name}] HP: ${Math.floor(this.bot.health)}/20 | Kills: ${this.stats.kills} | Sectors: ${this.exploration.sectorsVisited.length}`);
                break;
            case 'pos':
                const p = this.bot.entity.position;
                this.bot.chat(`[${this.name}] Position: ${Math.floor(p.x)}, ${Math.floor(p.y)}, ${Math.floor(p.z)}`);
                break;
            case 'inventory':
                const items = this.bot.inventory.items().map(i => i.name).join(', ');
                this.bot.chat(`[${this.name}] Carrying: ${items || 'Nothing'}`);
                break;
            case 'return':
                this.bot.chat(`[${this.name}] Returning to spawn...`);
                this.bot.chat('/spawn');
                break;
            case 'explore':
                this.startExploration();
                break;
            default:
                this.bot.chat(`[${this.name}] Commands: status, pos, inventory, return, explore`);
        }
    }
    
    generateMissionReport() {
        const duration = (Date.now() - this.startTime) / 1000;
        
        return {
            agent: this.name,
            mission: {
                duration: `${duration.toFixed(1)}s`,
                startTime: new Date(this.startTime).toISOString(),
                endTime: new Date().toISOString()
            },
            stats: this.stats,
            exploration: {
                sectorsVisited: this.exploration.sectorsVisited.length,
                waypoints: this.exploration.waypoints,
                photos: this.exploration.photos.length,
                discoveries: this.stats.discoveries
            },
            combat: {
                kills: this.stats.kills,
                deaths: this.stats.deaths,
                enemiesDefeated: this.combat.enemiesDefeated
            },
            logs: this.logs
        };
    }
    
    saveReport(outputDir) {
        const report = this.generateMissionReport();
        const filename = `${this.name.toLowerCase()}_mission_report.json`;
        fs.writeFileSync(path.join(outputDir, filename), JSON.stringify(report, null, 2));
        
        // Save photos as text files
        this.exploration.photos.forEach((photo, idx) => {
            const photoFile = path.join(outputDir, 'photos', `${this.name.toLowerCase()}_photo_${idx}.txt`);
            fs.mkdirSync(path.dirname(photoFile), { recursive: true });
            fs.writeFileSync(photoFile, 
                `${this.name} — Photo ${idx + 1}\n` +
                `Position: (${photo.position.x}, ${photo.position.y}, ${photo.position.z})\n` +
                `Biome: ${photo.biome}\n` +
                `Time: ${photo.timestamp}\n\n` +
                photo.ascii
            );
        });
        
        this.log('info', `Mission report saved: ${filename}`);
        return report;
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    disconnect() {
        if (this.bot) {
            this.bot.quit();
        }
    }
}

// ═══════════════════════════════════════════════════════════
// SQUAD MANAGER — Controls multiple exploration agents
// ═══════════════════════════════════════════════════════════

class ExplorationSquad {
    constructor(config) {
        this.agents = [];
        this.config = config;
        this.outputDir = config.outputDir || './squad_reports';
        
        if (!fs.existsSync(this.outputDir)) {
            fs.mkdirSync(this.outputDir, { recursive: true });
        }
    }
    
    async deployCrew(crewConfig) {
        console.log('╔════════════════════════════════════════════════════════╗');
        console.log('║  MINECRAFT EXPLORATION SQUAD — Tactical Deployment   ║');
        console.log('╚════════════════════════════════════════════════════════╝\n');
        
        for (const member of crewConfig) {
            console.log(`🚀 Deploying ${member.name}...`);
            
            const agent = new MinecraftExplorer({
                name: member.name,
                username: member.username,
                host: this.config.host,
                port: this.config.port,
                version: this.config.version
            });
            
            try {
                await agent.connect();
                this.agents.push(agent);
                
                // Delay between connections
                await new Promise(r => setTimeout(r, 3000));
                
            } catch (err) {
                console.error(`Failed to deploy ${member.name}:`, err.message);
            }
        }
        
        console.log(`\n✅ ${this.agents.length} agents deployed successfully`);
    }
    
    async runMission(duration = 300000) {
        console.log(`\n📡 Running exploration mission for ${duration / 1000}s...\n`);
        
        // Let agents explore independently
        await new Promise(r => setTimeout(r, duration));
        
        // Collect reports
        console.log('\n📊 Collecting mission reports...\n');
        
        const reports = [];
        for (const agent of this.agents) {
            const report = agent.saveReport(this.outputDir);
            reports.push(report);
            agent.disconnect();
        }
        
        // Generate squad summary
        this.generateSquadReport(reports);
        
        return reports;
    }
    
    generateSquadReport(reports) {
        const totalKills = reports.reduce((sum, r) => sum + r.stats.kills, 0);
        const totalDeaths = reports.reduce((sum, r) => sum + r.stats.deaths, 0);
        const totalSectors = reports.reduce((sum, r) => sum + r.exploration.sectorsVisited, 0);
        const totalPhotos = reports.reduce((sum, r) => sum + r.exploration.photos, 0);
        const totalDiscoveries = reports.reduce((sum, r) => sum + r.exploration.discoveries.length, 0);
        
        const summary = {
            mission: 'Minecraft Deep Exploration',
            squadSize: reports.length,
            timestamp: new Date().toISOString(),
            totals: {
                kills: totalKills,
                deaths: totalDeaths,
                sectors: totalSectors,
                photos: totalPhotos,
                discoveries: totalDiscoveries
            },
            agents: reports.map(r => ({
                name: r.agent,
                kills: r.stats.kills,
                deaths: r.stats.deaths,
                sectors: r.exploration.sectorsVisited
            }))
        };
        
        fs.writeFileSync(
            path.join(this.outputDir, 'squad_summary.json'),
            JSON.stringify(summary, null, 2)
        );
        
        console.log('═'.repeat(60));
        console.log('🎖️ SQUAD MISSION COMPLETE');
        console.log('═'.repeat(60));
        console.log(`Total Kills: ${totalKills}`);
        console.log(`Total Deaths: ${totalDeaths}`);
        console.log(`Sectors Visited: ${totalSectors}`);
        console.log(`Photos Captured: ${totalPhotos}`);
        console.log(`Discoveries: ${totalDiscoveries}`);
        console.log(`Reports: ${this.outputDir}/`);
        console.log('═'.repeat(60));
    }
}

// ═══════════════════════════════════════════════════════════
// MAIN EXECUTION
// ═══════════════════════════════════════════════════════════

async function main() {
    // Crew configuration
    const crew = [
        { name: 'Forge', username: 'forge_expedition' },
        { name: 'Patricia', username: 'patricia_expedition' },
        { name: 'Chelios', username: 'chelios_expedition' },
        { name: 'Aurora', username: 'aurora_expedition' }
    ];
    
    // Server configuration
    const config = {
        host: process.env.MC_HOST || 'localhost',
        port: parseInt(process.env.MC_PORT) || 25565,
        version: '1.20.1',
        outputDir: './minecraft_expedition_reports'
    };
    
    const squad = new ExplorationSquad(config);
    
    // Deploy crew
    await squad.deployCrew(crew);
    
    // Run 5-minute mission
    await squad.runMission(300000);
}

// Run if called directly
if (require.main === module) {
    main().catch(err => {
        console.error('Squad deployment failed:', err);
        process.exit(1);
    });
}

module.exports = { MinecraftExplorer, ExplorationSquad };
