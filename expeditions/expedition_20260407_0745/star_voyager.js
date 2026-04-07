#!/usr/bin/env node
/**
 * STAR VOYAGER — Pure JavaScript Exploration Agent v1.0
 * Ship: U.S.S. TRACRAY
 * Crew: 4 Autonomous Exploration Units
 * 
 * Features:
 * - Real browser screenshots via Puppeteer
 * - ASCII-to-PNG color camera
 * - Combat system with weapons/shields
 * - Live telemetry dashboard
 * - Procedural universe generation
 * - Encounter system with hostile creatures
 */

const puppeteer = require('puppeteer');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ═══════════════════════════════════════════════════════════
// SHIP CONFIGURATION
// ═══════════════════════════════════════════════════════════

const SHIP = {
    name: 'U.S.S. TRACRAY',
    registry: 'NCC-1987',
    class: 'Deep Space Exploration Vessel',
    launchDate: '2026-04-07',
    captain: 'Miles',
    
    systems: {
        engines: { status: 'ONLINE', power: 100 },
        shields: { status: 'ONLINE', strength: 100, max: 100 },
        weapons: { status: 'ARMED', loadout: ['phaser_array', 'photon_torpedoes'] },
        sensors: { status: 'ACTIVE', range: 10000 },
        communications: { status: 'ONLINE' },
        lifeSupport: { status: 'STABLE', o2: 100 }
    },
    
    position: { x: 0, y: 0, z: 0, sector: 'Alpha-1' },
    mission: 'Deep space exploration and reconnaissance'
};

// ═══════════════════════════════════════════════════════════
// CREW MANIFEST — 4 Autonomous Units
// ═══════════════════════════════════════════════════════════

const CREW = [
    {
        id: 'forge',
        name: 'Forge',
        rank: 'Commander',
        role: 'Chief Tactical Officer',
        specialty: 'Combat & Security',
        station: 'Bridge — Tactical',
        vitals: { hp: 100, maxHp: 100, energy: 100 },
        loadout: {
            weapon: { name: 'Type-X Phaser Rifle', damage: 25, range: 'long', ammo: '∞' },
            sidearm: { name: 'Mk-12 Phaser Pistol', damage: 15, range: 'medium', ammo: '∞' },
            shield: { name: 'Personal Force Field', absorption: 50 },
            gear: ['Combat Scanner', 'Threat Analyzer', 'MedKit']
        },
        skills: { combat: 95, leadership: 80, science: 40, navigation: 60 },
        status: 'ACTIVE'
    },
    {
        id: 'patricia',
        name: 'Patricia',
        rank: 'Lieutenant Commander',
        role: 'Chief Science Officer',
        specialty: 'Xenobiology & Analysis',
        station: 'Bridge — Science',
        vitals: { hp: 100, maxHp: 100, energy: 100 },
        loadout: {
            weapon: { name: 'Mk-12 Phaser Pistol', damage: 15, range: 'medium', ammo: '∞' },
            sidearm: { name: 'Sample Collection Array', damage: 5, range: 'touch', ammo: '∞' },
            shield: { name: 'Research Shield', absorption: 30 },
            gear: ['Bio-Scanner', 'Geological Analyzer', 'Specimen Containers']
        },
        skills: { combat: 40, leadership: 60, science: 98, navigation: 70 },
        status: 'ACTIVE'
    },
    {
        id: 'chelios',
        name: 'Chelios',
        rank: 'Lieutenant',
        role: 'Security Officer',
        specialty: 'Close Quarters Combat',
        station: 'Bridge — Security',
        vitals: { hp: 120, maxHp: 120, energy: 100 },
        loadout: {
            weapon: { name: 'Heavy Plasma Cannon', damage: 40, range: 'medium', ammo: 100 },
            sidearm: { name: 'Combat Blade', damage: 30, range: 'melee', ammo: '∞' },
            shield: { name: 'Heavy Combat Shield', absorption: 80 },
            gear: ['Motion Tracker', 'Breach Charges', 'Stun Grenades x3']
        },
        skills: { combat: 99, leadership: 50, science: 30, navigation: 55 },
        status: 'ACTIVE'
    },
    {
        id: 'aurora',
        name: 'Aurora',
        rank: 'Ensign',
        role: 'Navigator / Pilot',
        specialty: 'Flight & Cartography',
        station: 'Bridge — Helm',
        vitals: { hp: 90, maxHp: 90, energy: 100 },
        loadout: {
            weapon: { name: 'Mk-12 Phaser Pistol', damage: 15, range: 'medium', ammo: '∞' },
            sidearm: { name: 'Targeting Computer', damage: 0, range: 'n/a', ammo: '∞' },
            shield: { name: 'Light EVA Shield', absorption: 25 },
            gear: ['Star Charts', 'Gravitational Compass', 'Emergency Beacon']
        },
        skills: { combat: 50, leadership: 45, science: 60, navigation: 99 },
        status: 'ACTIVE'
    }
];

// ═══════════════════════════════════════════════════════════
// ARMORY — Ship & Personal Weapons
// ═══════════════════════════════════════════════════════════

const ARMORY = {
    shipWeapons: [
        { id: 'phaser_array', name: 'Phaser Array', damage: 100, range: 'unlimited', cooldown: 2 },
        { id: 'photon_torpedoes', name: 'Photon Torpedoes', damage: 500, range: 'unlimited', count: 20 },
        { id: 'quantum_torpedoes', name: 'Quantum Torpedoes', damage: 1000, range: 'unlimited', count: 5 }
    ],
    
    personalWeapons: [
        { id: 'phaser_rifle', name: 'Type-X Phaser Rifle', damage: 25, range: 'long', type: 'energy' },
        { id: 'phaser_pistol', name: 'Mk-12 Phaser Pistol', damage: 15, range: 'medium', type: 'energy' },
        { id: 'plasma_cannon', name: 'Heavy Plasma Cannon', damage: 40, range: 'medium', type: 'plasma', ammo: 100 },
        { id: 'combat_blade', name: 'Monomolecular Blade', damage: 30, range: 'melee', type: 'kinetic' }
    ],
    
    shields: [
        { id: 'ship_shield', name: 'Deflector Shields', max: 1000, current: 1000, regen: 10 },
        { id: 'heavy_personal', name: 'Heavy Combat Shield', absorption: 80, durability: 100 },
        { id: 'standard_personal', name: 'Personal Force Field', absorption: 50, durability: 100 },
        { id: 'light_personal', name: 'Light EVA Shield', absorption: 25, durability: 100 }
    ]
};

// ═══════════════════════════════════════════════════════════
// ENEMY DATABASE — Hostile Lifeforms
// ═══════════════════════════════════════════════════════════

const HOSTILES = [
    {
        id: 'void_drifter',
        name: 'Void Drifter',
        classification: 'Energy-Based Lifeform',
        threat: 'low',
        hp: 50,
        damage: 10,
        behavior: 'Curious, non-aggressive unless provoked',
        loot: ['Void Essence', 'Energy Residue'],
        weakTo: 'kinetic'
    },
    {
        id: 'crystal_horror',
        name: 'Crystal Horror',
        classification: 'Silicate Predator',
        threat: 'moderate',
        hp: 150,
        damage: 25,
        behavior: 'Territorial, attacks on sight',
        loot: ['Crystal Shard', 'Mineral Sample'],
        weakTo: 'energy'
    },
    {
        id: 'shadow_stalker',
        name: 'Shadow Stalker',
        classification: 'Extra-Dimensional Entity',
        threat: 'high',
        hp: 200,
        damage: 35,
        behavior: 'Ambush predator, hunts in darkness',
        loot: ['Shadow Essence', 'Dark Matter Sample'],
        weakTo: 'light'
    },
    {
        id: 'graviton_beast',
        name: 'Graviton Beast',
        classification: 'Gravitational Anomaly',
        threat: 'extreme',
        hp: 500,
        damage: 60,
        behavior: 'Attracted to ship mass, causes hull stress',
        loot: ['Graviton Core', 'Singularity Fragment'],
        weakTo: 'quantum'
    },
    {
        id: 'quantum_phantom',
        name: 'Quantum Phantom',
        classification: 'Probability Entity',
        threat: 'high',
        hp: 100,
        damage: 45,
        behavior: 'Phase shifts, unpredictable attacks',
        loot: ['Quantum Data', 'Probability Crystal'],
        weakTo: 'phased'
    },
    {
        id: 'nebula_swarmer',
        name: 'Nebula Swarmer',
        classification: 'Collective Organism',
        threat: 'moderate',
        hp: 75,
        damage: 15,
        behavior: 'Swarm tactics, overwhelming numbers',
        loot: ['Biomass', 'Organic Compound'],
        weakTo: 'area'
    }
];

// ═══════════════════════════════════════════════════════════
// 3D CAMERA SYSTEM — Screenshot & ASCII Converter
// ═══════════════════════════════════════════════════════════

class Camera3D {
    constructor(outputDir) {
        this.outputDir = outputDir;
        this.session = Date.now();
        this.photos = [];
    }
    
    async initialize() {
        this.browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--window-size=1280,720']
        });
        this.page = await this.browser.newPage();
        await this.page.setViewport({ width: 1280, height: 720 });
        return this;
    }
    
    async capture(targetUrl, metadata = {}) {
        await this.page.goto(targetUrl, { waitUntil: 'networkidle0', timeout: 30000 });
        await this.page.waitForTimeout(3000); // Let universe render
        
        const timestamp = Date.now();
        const filename = `capture_${this.session}_${timestamp}.png`;
        const filepath = path.join(this.outputDir, filename);
        
        await this.page.screenshot({ 
            path: filepath, 
            fullPage: false,
            type: 'png'
        });
        
        // Generate ASCII version
        const asciiFile = path.join(this.outputDir, `ascii_${this.session}_${timestamp}.txt`);
        const ascii = this.generateASCII(metadata);
        fs.writeFileSync(asciiFile, ascii);
        
        const photo = {
            id: timestamp,
            filename,
            asciiFile: `ascii_${this.session}_${timestamp}.txt`,
            timestamp: new Date().toISOString(),
            ...metadata
        };
        
        this.photos.push(photo);
        return photo;
    }
    
    generateASCII(metadata) {
        const chars = '@%#*+=-:. ';
        const colors = ['RED', 'GREEN', 'BLUE', 'YELLOW', 'CYAN', 'MAGENTA'];
        
        let ascii = '╔' + '═'.repeat(78) + '╗\n';
        ascii += `║ 3D CAMERA CAPTURE — ${metadata.crew || 'Unknown'}                    ${metadata.sector || 'Unknown Sector'} ║\n`;
        ascii += '╠' + '═'.repeat(78) + '╣\n';
        ascii += `║ Timestamp: ${new Date().toISOString()}                                      ║\n`;
        ascii += `║ Coordinates: (${metadata.x || 0}, ${metadata.y || 0}, ${metadata.z || 0})                                    ║\n`;
        ascii += `║ Color Filter: ${colors[Math.floor(Math.random() * colors.length)]}                                            ║\n`;
        ascii += '╠' + '═'.repeat(78) + '╣\n';
        
        // Generate procedural ASCII art
        for (let y = 0; y < 40; y++) {
            let line = '║';
            for (let x = 0; x < 78; x++) {
                const noise = Math.sin(x * 0.1) * Math.cos(y * 0.15) * Math.random();
                const charIndex = Math.floor(Math.abs(noise) * chars.length);
                line += chars[Math.min(charIndex, chars.length - 1)];
            }
            ascii += line + '║\n';
        }
        
        ascii += '╠' + '═'.repeat(78) + '╣\n';
        ascii += `║ END TRANSMISSION — TRACRAY EXPEDITIONARY FORCE                              ║\n`;
        ascii += '╚' + '═'.repeat(78) + '╝\n';
        
        return ascii;
    }
    
    async close() {
        if (this.browser) {
            await this.browser.close();
        }
    }
}

// ═══════════════════════════════════════════════════════════
// COMBAT SYSTEM
// ═══════════════════════════════════════════════════════════

class CombatSystem {
    constructor() {
        this.log = [];
        this.activeCombat = false;
    }
    
    roll(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    
    calculateHit(attacker, target) {
        const attackRoll = this.roll(1, 100);
        const defense = target.skills ? target.skills.combat : 50;
        return attackRoll > (100 - defense);
    }
    
    calculateDamage(weapon, target) {
        let damage = weapon.damage + this.roll(1, 10);
        
        // Check for weaknesses
        if (target.weakTo && weapon.type === target.weakTo) {
            damage *= 2;
            this.logEvent(`CRITICAL: ${target.name} weak to ${weapon.type}! Double damage!`);
        }
        
        // Apply shield absorption
        if (target.loadout && target.loadout.shield) {
            const absorbed = Math.min(damage, target.loadout.shield.absorption);
            damage -= absorbed;
            this.logEvent(`${target.name}'s shield absorbed ${absorbed} damage`);
        }
        
        return Math.max(0, damage);
    }
    
    engage(crew, hostile) {
        this.activeCombat = true;
        this.logEvent(`⚔️ COMBAT INITIATED: ${crew.name} vs ${hostile.name}`);
        this.logEvent(`Threat Level: ${hostile.threat.toUpperCase()}`);
        
        let combatant = { ...crew };
        let enemy = { ...hostile, currentHp: hostile.hp };
        let rounds = 0;
        const maxRounds = 20;
        
        while (combatant.vitals.hp > 0 && enemy.currentHp > 0 && rounds < maxRounds) {
            rounds++;
            this.logEvent(`\n--- Round ${rounds} ---`);
            
            // Crew attacks
            if (this.calculateHit(combatant, enemy)) {
                const damage = this.calculateDamage(combatant.loadout.weapon, enemy);
                enemy.currentHp -= damage;
                this.logEvent(`${combatant.name} hits ${enemy.name} for ${damage} damage! (${enemy.currentHp}/${enemy.hp} HP)`);
                
                if (enemy.currentHp <= 0) {
                    this.logEvent(`🎯 ${combatant.name} DEFEATS ${enemy.name}!`);
                    this.logEvent(`💎 Loot: ${hostile.loot.join(', ')}`);
                    this.activeCombat = false;
                    return { victory: true, loot: hostile.loot, rounds };
                }
            } else {
                this.logEvent(`${combatant.name} misses!`);
            }
            
            // Enemy attacks
            if (this.calculateHit(enemy, combatant)) {
                const damage = this.roll(hostile.damage - 5, hostile.damage + 5);
                combatant.vitals.hp -= damage;
                this.logEvent(`${enemy.name} strikes ${combatant.name} for ${damage} damage! (${combatant.vitals.hp}/${crew.vitals.maxHp} HP)`);
                
                if (combatant.vitals.hp <= 0) {
                    this.logEvent(`💀 ${combatant.name} has fallen!`);
                    this.activeCombat = false;
                    return { victory: false, casualty: combatant.name, rounds };
                }
            } else {
                this.logEvent(`${enemy.name} misses!`);
            }
        }
        
        this.activeCombat = false;
        return { victory: false, reason: 'timeout', rounds };
    }
    
    logEvent(message) {
        const entry = `[${new Date().toISOString()}] ${message}`;
        this.log.push(entry);
        console.log(entry);
    }
    
    getCombatLog() {
        return this.log.join('\n');
    }
}

// ═══════════════════════════════════════════════════════════
// EXPLORATION MISSION
// ═══════════════════════════════════════════════════════════

class ExplorationMission {
    constructor(ship, crew, outputDir) {
        this.ship = ship;
        this.crew = crew;
        this.outputDir = outputDir;
        this.camera = null;
        this.combat = new CombatSystem();
        this.logs = [];
        this.discoveries = [];
        this.encounters = [];
        this.photos = [];
        this.startTime = Date.now();
    }
    
    log(message, type = 'info') {
        const entry = { time: Date.now(), message, type };
        this.logs.push(entry);
        const icon = type === 'combat' ? '⚔️' : type === 'discovery' ? '🔬' : type === 'danger' ? '⚠️' : '📡';
        console.log(`${icon} ${message}`);
    }
    
    async initialize() {
        this.camera = await new Camera3D(`${this.outputDir}/photos`).initialize();
        this.log(`${this.ship.name} systems initialized. All stations report ready.`, 'info');
        return this;
    }
    
    generateSector() {
        const types = ['Nebula', 'Asteroid Field', 'Binary Star', 'Void', 'Crystal Formation', 'Wormhole'];
        const anomalies = ['Gravitational Lens', 'Radiation Surge', 'Temporal Distortion', 'Dark Matter Cloud', 'None'];
        
        return {
            id: `Sector-${Math.floor(Math.random() * 9999)}`,
            type: types[Math.floor(Math.random() * types.length)],
            anomaly: anomalies[Math.floor(Math.random() * anomalies.length)],
            x: Math.floor(Math.random() * 1000) - 500,
            y: Math.floor(Math.random() * 1000) - 500,
            z: Math.floor(Math.random() * 1000) - 500
        };
    }
    
    async exploreSector(sector, crewMember) {
        this.log(`${crewMember.name} launching EVA probe to ${sector.id}...`);
        
        // Take photo
        try {
            const photo = await this.camera.capture('http://myl0nr0s.cloud/nog', {
                crew: crewMember.name,
                sector: sector.id,
                x: sector.x, y: sector.y, z: sector.z,
                ship: this.ship.name
            });
            this.photos.push({ ...photo, crew: crewMember.name, sector: sector.id });
            this.log(`${crewMember.name} transmitted visual data from ${sector.id}`, 'discovery');
        } catch (e) {
            this.log(`Camera malfunction: ${e.message}`, 'danger');
        }
        
        // Discover something
        const discoveries = [
            `Unusual ${['crystalline', 'metallic', 'organic', 'energy-based'].sort(() => Math.random() - 0.5)[0]} formations`,
            `Anomalous ${['gravitational', 'magnetic', 'thermal', 'quantum'].sort(() => Math.random() - 0.5)[0]} readings`,
            `Traces of ${['ancient', 'alien', 'unknown', 'advanced'].sort(() => Math.random() - 0.5)[0]} civilization`,
            `${['Rare', 'Exotic', 'Unstable', 'Stable'].sort(() => Math.random() - 0.5)[0]} mineral deposits`,
            `Biological ${['markers', 'signatures', 'activity', 'remains'].sort(() => Math.random() - 0.5)[0]} detected`
        ];
        const discovery = discoveries[Math.floor(Math.random() * discoveries.length)];
        this.discoveries.push({ sector: sector.id, discovery, crew: crewMember.name, time: Date.now() });
        this.log(`${crewMember.name}: "${discovery} in ${sector.id}"`, 'discovery');
        
        // Random encounter (30% chance)
        if (Math.random() < 0.3) {
            const hostile = HOSTILES[Math.floor(Math.random() * HOSTILES.length)];
            this.log(`⚠️ HOSTILE DETECTED: ${hostile.name} (${hostile.threat.toUpperCase()})`, 'danger');
            
            const result = this.combat.engage(crewMember, hostile);
            this.encounters.push({
                sector: sector.id,
                hostile: hostile.name,
                threat: hostile.threat,
                result: result.victory ? 'VICTORY' : 'DEFEAT',
                rounds: result.rounds,
                crew: crewMember.name
            });
            
            if (result.victory) {
                this.log(`${crewMember.name} secured ${sector.id}. Loot: ${result.loot.join(', ')}`, 'combat');
            } else {
                this.log(`EMERGENCY BEACON: ${crewMember.name} requires immediate extraction!`, 'danger');
                crewMember.vitals.hp = Math.max(1, crewMember.vitals.hp); // Emergency heal
            }
        }
        
        await new Promise(r => setTimeout(r, 2000));
    }
    
    async run() {
        this.log(`🚀 ${this.ship.name} embarking on exploration mission...`);
        this.log(`Crew complement: ${this.crew.length} autonomous units`);
        
        // Each crew member explores different sectors
        for (const crewMember of this.crew) {
            this.log(`\n══════════ ${crewMember.name.toUpperCase()} DEPLOYING ══════════`);
            this.log(`Loadout: ${crewMember.loadout.weapon.name}, ${crewMember.loadout.shield.name}`);
            
            // Explore 3 sectors each
            for (let i = 0; i < 3; i++) {
                const sector = this.generateSector();
                await this.exploreSector(sector, crewMember);
            }
            
            this.log(`${crewMember.name} returning to ship...`);
            await new Promise(r => setTimeout(r, 1000));
        }
        
        await this.generateReport();
        await this.camera.close();
        
        return this;
    }
    
    async generateReport() {
        const duration = ((Date.now() - this.startTime) / 1000).toFixed(1);
        
        const report = {
            mission: {
                ship: this.ship,
                startTime: new Date(this.startTime).toISOString(),
                duration: `${duration}s`,
                status: 'COMPLETE'
            },
            crew: this.crew.map(c => ({
                name: c.name,
                role: c.role,
                vitals: c.vitals,
                loadout: c.loadout
            })),
            discoveries: this.discoveries,
            encounters: this.encounters,
            photos: this.photos,
            combatLog: this.combat.getCombatLog(),
            logs: this.logs
        };
        
        // Save JSON report
        const reportPath = path.join(this.outputDir, 'mission_report.json');
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
        
        // Generate HTML dashboard
        await this.generateHTMLDashboard(report);
        
        this.log(`\n📊 MISSION COMPLETE — Report saved to ${reportPath}`);
        return report;
    }
    
    async generateHTMLDashboard(report) {
        const html = this.buildDashboardHTML(report);
        const dashboardPath = path.join(this.outputDir, 'dashboard.html');
        fs.writeFileSync(dashboardPath, html);
        
        // Start HTTP server
        const server = http.createServer((req, res) => {
            if (req.url === '/') {
                res.writeHead(200, { 'Content-Type': 'text/html' });
                res.end(html);
            } else if (req.url === '/api/status') {
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    ship: this.ship,
                    crew: this.crew.map(c => ({ name: c.name, vitals: c.vitals })),
                    discoveries: this.discoveries.length,
                    encounters: this.encounters.length,
                    photos: this.photos.length
                }));
            } else {
                res.writeHead(404);
                res.end('Not found');
            }
        });
        
        const PORT = 8765;
        server.listen(PORT, () => {
            this.log(`🌐 Live Dashboard: http://localhost:${PORT}/`);
        });
        
        return dashboardPath;
    }
    
    buildDashboardHTML(report) {
        const victories = report.encounters.filter(e => e.result === 'VICTORY').length;
        const defeats = report.encounters.filter(e => e.result === 'DEFEAT').length;
        
        return `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>${this.ship.name} — Mission Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Courier New', monospace; 
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%); 
            color: #00ff00; 
            min-height: 100vh;
            padding: 20px;
        }
        .header { 
            text-align: center; 
            padding: 30px; 
            border-bottom: 3px solid #00ff00;
            margin-bottom: 30px;
            background: rgba(0, 255, 0, 0.05);
        }
        .header h1 { 
            font-size: 2.5em; 
            text-shadow: 0 0 20px #00ff00;
            margin-bottom: 10px;
        }
        .ship-status { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px;
            margin-bottom: 30px;
        }
        .status-card {
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid #00ff00;
            padding: 20px;
            border-radius: 8px;
        }
        .status-card h3 { margin-bottom: 10px; color: #4ecdc4; }
        .stat-value { font-size: 2em; color: #ffeaa7; }
        .crew-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .crew-card {
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #4ecdc4;
            padding: 20px;
            border-radius: 8px;
        }
        .crew-card .name { 
            font-size: 1.5em; 
            color: #4ecdc4; 
            border-bottom: 1px solid #4ecdc4;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }
        .hp-bar { 
            height: 20px; 
            background: #333; 
            border-radius: 10px; 
            overflow: hidden;
            margin: 10px 0;
        }
        .hp-fill { 
            height: 100%; 
            background: linear-gradient(90deg, #ff6b6b, #ffeaa7, #96ceb4);
            transition: width 0.3s;
        }
        .discovery-list, .encounter-list {
            max-height: 300px;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
        }
        .discovery-item, .encounter-item {
            padding: 10px;
            margin: 5px 0;
            background: rgba(255, 255, 255, 0.05);
            border-left: 3px solid #ffeaa7;
        }
        .encounter-item.victory { border-left-color: #96ceb4; }
        .encounter-item.defeat { border-left-color: #ff6b6b; }
        .combat-log {
            background: #000;
            padding: 20px;
            border-radius: 8px;
            font-size: 0.9em;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            color: #74b9ff;
        }
        .photo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        .photo-item {
            background: rgba(0, 0, 0, 0.5);
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }
        .photo-item img {
            max-width: 100%;
            border-radius: 4px;
            border: 1px solid #00ff00;
        }
        h2 {
            color: #00ff00;
            margin: 30px 0 15px;
            border-bottom: 2px solid #00ff00;
            padding-bottom: 10px;
        }
        .live-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #ff6b6b;
            border-radius: 50%;
            margin-right: 10px;
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="live-indicator"></div>
        <h1>🚀 ${this.ship.name}</h1>
        <p>Registry: ${this.ship.registry} | Class: ${this.ship.class}</p>
        <p>Mission: ${this.ship.mission} | Status: <span style="color: #96ceb4;">${report.mission.status}</span></p>
        <p>Duration: ${report.mission.duration} | Logged: ${new Date().toISOString()}</p>
    </div>
    
    <div class="ship-status">
        <div class="status-card">
            <h3>📊 Discoveries</h3>
            <div class="stat-value">${report.discoveries.length}</div>
        </div>
        <div class="status-card">
            <h3>⚔️ Encounters</h3>
            <div class="stat-value">${report.encounters.length}</div>
            <p>Victories: ${victories} | Defeats: ${defeats}</p>
        </div>
        <div class="status-card">
            <h3>📸 Photos</h3>
            <div class="stat-value">${report.photos.length}</div>
        </div>
        <div class="status-card">
            <h3>👥 Crew Status</h3>
            <div class="stat-value">${report.crew.filter(c => c.vitals.hp > 0).length}/${report.crew.length}</div>
            <p>All stations operational</p>
        </div>
    </div>
    
    <h2>👥 Crew Manifest</h2>
    <div class="crew-grid">
        ${report.crew.map(c => `
            <div class="crew-card">
                <div class="name">${c.name} — ${c.role}</div>
                <p><strong>Weapon:</strong> ${c.loadout.weapon.name}</p>
                <p><strong>Shield:</strong> ${c.loadout.shield.name}</p>
                <div class="hp-bar">
                    <div class="hp-fill" style="width: ${(c.vitals.hp / c.vitals.maxHp) * 100}%"></div>
                </div>
                <p>HP: ${c.vitals.hp}/${c.vitals.maxHp} | Energy: ${c.vitals.energy}%</p>
            </div>
        `).join('')}
    </div>
    
    <h2>🔬 Discoveries</h2>
    <div class="discovery-list">
        ${report.discoveries.map(d => `
            <div class="discovery-item">
                <strong>[${d.sector}]</strong> ${d.discovery}
                <br><small>— ${d.crew}, ${new Date(d.time).toLocaleTimeString()}</small>
            </div>
        `).join('')}
    </div>
    
    <h2>⚔️ Combat Encounters</h2>
    <div class="encounter-list">
        ${report.encounters.map(e => `
            <div class="encounter-item ${e.result === 'VICTORY' ? 'victory' : 'defeat'}">
                <strong>${e.hostile}</strong> — ${e.threat.toUpperCase()}
                <br>Sector: ${e.sector} | Result: ${e.result} (${e.rounds} rounds)
                <br><small>— Agent: ${e.crew}</small>
            </div>
        `).join('') || '<p>No hostile encounters recorded.</p>'}
    </div>
    
    <h2>📸 Visual Captures</h2>
    <div class="photo-grid">
        ${report.photos.map(p => `
            <div class="photo-item">
                <p><strong>${p.crew}</strong></p>
                <p>${p.sector}</p>
                <p style="color: #74b9ff; font-size: 0.8em;">${p.filename}</p>
            </div>
        `).join('')}
    </div>
    
    <h2>📜 Combat Log</h2>
    <div class="combat-log">${report.combatLog}</div>
    
    <script>
        // Auto-refresh every 5 seconds
        setInterval(() => {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => console.log('Status update:', data))
                .catch(e => console.log('Status check failed'));
        }, 5000);
    </script>
</body>
</html>`;
    }
}

// ═══════════════════════════════════════════════════════════
// MAIN EXECUTION
// ═══════════════════════════════════════════════════════════

async function main() {
    const expeditionDir = path.join(__dirname, 'star_voyager_expedition');
    if (!fs.existsSync(expeditionDir)) {
        fs.mkdirSync(expeditionDir, { recursive: true });
        fs.mkdirSync(path.join(expeditionDir, 'photos'), { recursive: true });
    }
    
    console.log('╔════════════════════════════════════════════════════════╗');
    console.log('║  STAR VOYAGER — Deep Space Exploration System          ║');
    console.log('║  Version 1.0 | JavaScript Pure Implementation          ║');
    console.log('╚════════════════════════════════════════════════════════╝\n');
    
    console.log(`🚀 Initializing ${SHIP.name}...`);
    console.log(`👥 Crew complement: ${CREW.length} units`);
    console.log(`⚔️ Combat systems: ONLINE`);
    console.log(`📷 3D Camera: STANDBY`);
    console.log(`🌐 Live Dashboard: PREPARING\n`);
    
    const mission = new ExplorationMission(SHIP, CREW, expeditionDir);
    await mission.initialize();
    await mission.run();
    
    console.log('\n' + '═'.repeat(60));
    console.log('🎖️ EXPEDITION COMPLETE');
    console.log('═'.repeat(60));
    console.log(`Mission logs: ${expeditionDir}/mission_report.json`);
    console.log(`Live dashboard: http://localhost:8765/`);
    console.log(`Photo archive: ${expeditionDir}/photos/`);
    console.log('═'.repeat(60));
}

// Run if called directly
if (require.main === module) {
    main().catch(err => {
        console.error('Mission failed:', err);
        process.exit(1);
    });
}

module.exports = { SHIP, CREW, ARMORY, HOSTILES, ExplorationMission, CombatSystem, Camera3D };
