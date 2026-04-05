#!/usr/bin/env node
/**
 * Enhanced Ternary OODA Agent v2.0
 * Features: Heart sync, Memory, Skills, Coordination, Emotional State
 */

const mineflayer = require('mineflayer');
const pathfinder = require('mineflayer-pathfinder').pathfinder;
const { Movements, goals } = require('mineflayer-pathfinder');
const { GoalNear, GoalFollow } = goals;
const WebSocket = require('ws');
const Vec3 = require('vec3');

// Configuration
const AGENT_ID = process.argv[2] || 'enhanced_agent';
const MC_HOST = process.argv[3] || 'localhost';
const MC_PORT = parseInt(process.argv[4]) || 25566;
const BRAIN_URL = process.argv[5] || 'ws://localhost:8767';

console.log(`[${AGENT_ID}] Enhanced Ternary OODA Agent v2.0 starting...`);

// Create bot
const bot = mineflayer.createBot({
    host: MC_HOST,
    port: MC_PORT,
    username: AGENT_ID,
    version: '1.20.4',
    auth: 'offline'
});

bot.loadPlugin(pathfinder);

// ============================================================================
// TERNARY HEART SYNC - REST/BALANCE/ACTIVE
// ============================================================================
const TernaryState = {
    REST: 'REST',         // Night/low resources - sleep, hide
    BALANCE: 'BALANCE',     // Day/stable - gather, build, explore
    ACTIVE: 'ACTIVE'      // Threats/opportunities - combat, sprint
};

// ============================================================================
// MEMORY SYSTEM
// ============================================================================
const AgentMemory = {
    locations: {},        // Named locations: {home: {x,y,z}, camp: {...}}
    resources: [],      // Known resource spots: [{type, pos, quantity, timestamp}]
    dangers: [],        // Danger zones: [{cause, pos, timestamp}]
    deaths: [],         // Death locations: [{pos, timestamp, inventory}]
    successes: [],      // Successful actions: [{action, pos, result}]
    agentLocations: {}, // Other agent positions: {agent_id: {x,y,z,timestamp}}
    
    remember(key, data) {
        this.locations[key] = { ...data, timestamp: Date.now() };
    },
    
    recall(key) {
        return this.locations[key] || null;
    },
    
    addResource(type, pos, quantity = 1) {
        this.resources.push({
            type, pos: {...pos}, quantity,
            timestamp: Date.now()
        });
        // Keep only last 50
        if (this.resources.length > 50) this.resources.shift();
    },
    
    addDanger(cause, pos) {
        this.dangers.push({
            cause, pos: {...pos},
            timestamp: Date.now()
        });
        // Keep only last 20
        if (this.dangers.length > 20) this.dangers.shift();
    },
    
    isDangerous(pos, radius = 20) {
        return this.dangers.some(d => {
            const dist = Math.sqrt(
                Math.pow(d.pos.x - pos.x, 2) +
                Math.pow(d.pos.z - pos.z, 2)
            );
            return dist < radius && (Date.now() - d.timestamp) < 300000; // 5 min
        });
    },
    
    getNearestResource(type, pos) {
        return this.resources
            .filter(r => r.type === type)
            .sort((a, b) => {
                const distA = Math.sqrt(
                    Math.pow(a.pos.x - pos.x, 2) +
                    Math.pow(a.pos.z - pos.z, 2)
                );
                const distB = Math.sqrt(
                    Math.pow(b.pos.x - pos.x, 2) +
                    Math.pow(b.pos.z - pos.z, 2)
                );
                return distA - distB;
            })[0] || null;
    }
};

// ============================================================================
// EMOTIONAL STATE
// ============================================================================
const EmotionalState = {
    confidence: 0.5,      // 0-1: affects exploration range
    fear: 0.0,            // 0-1: affects retreat behavior
    curiosity: 0.5,       // 0-1: affects investigation
    socialDrive: 0.5,     // 0-1: affects grouping behavior
    
    update(health, food, inventory, threats) {
        // Confidence: high health, food, good inventory
        this.confidence = Math.min(1.0, 
            (health / 20) * 0.4 + 
            (food / 20) * 0.3 + 
            (Math.min(inventory.length, 10) / 10) * 0.3
        );
        
        // Fear: low health, nearby threats, past deaths
        const threatLevel = threats.length * 0.2;
        const healthRisk = health < 10 ? 0.5 : 0;
        this.fear = Math.min(1.0, threatLevel + healthRisk);
        
        // Curiosity: varies with confidence, decreases with fear
        this.curiosity = this.confidence * (1 - this.fear);
        
        // Social: moderate baseline
        this.socialDrive = 0.3 + this.confidence * 0.4;
    },
    
    getMode() {
        if (this.fear > 0.6) return 'DEFENSIVE';
        if (this.confidence > 0.7) return 'AGGRESSIVE';
        if (this.curiosity > 0.5) return 'EXPLORATORY';
        return 'CAUTIOUS';
    }
};

// ============================================================================
// SKILL SYSTEM
// ============================================================================
const Skills = {
    // Combat skills (from martial arts training)
    combat: {
        stance: 'neutral',     // neutral/defensive/aggressive
        lastAttack: 0,
        comboCount: 0,
        
        engage(target) {
            if (!target) return false;
            
            const now = Date.now();
            if (now - this.lastAttack < 500) return false; // Attack cooldown
            
            // Martial arts decision tree
            const dist = bot.entity.position.distanceTo(target.position);
            
            if (dist > 3) {
                // Too far - move closer
                return { action: 'approach', target };
            } else if (dist < 1.5 && this.stance === 'defensive') {
                // Counter-attack (from self-defense training)
                this.comboCount++;
                this.lastAttack = now;
                return { action: 'counter', target };
            } else {
                // Standard attack
                this.comboCount++;
                this.lastAttack = now;
                return { action: 'attack', target };
            }
        },
        
        disengage() {
            this.stance = 'defensive';
            this.comboCount = 0;
            return { action: 'retreat' };
        }
    },
    
    // Building skills
    building: {
        materials: {},
        
        hasMaterials(type) {
            return bot.inventory.items().some(item => item.name.includes(type));
        },
        
        async placeShelter(pos) {
            // Build simple dirt shelter (3x3x2)
            const pattern = [
                {x: 0, y: -1, z: 0}, {x: 1, y: -1, z: 0}, {x: -1, y: -1, z: 0},
                {x: 0, y: -1, z: 1}, {x: 0, y: -1, z: -1}
            ];
            
            for (const offset of pattern) {
                const blockPos = pos.offset(offset.x, offset.y, offset.z);
                const block = bot.blockAt(blockPos);
                if (block && block.name === 'air') {
                    // Would place block here
                }
            }
            return true;
        }
    },
    
    // Evasion (from self-defense course)
    evasion: {
        async executeManeuver(type) {
            const pos = bot.entity.position;
            let targetPos;
            
            switch(type) {
                case 'evasion_basics':
                    // Quick lateral movement
                    targetPos = pos.offset(Math.random() > 0.5 ? 2 : -2, 0, 0);
                    break;
                case 'doorway_defense':
                    // Back through doorway
                    targetPos = pos.offset(0, 0, -3);
                    break;
                case 'stair_defense':
                    // Up stairs for advantage
                    targetPos = pos.offset(0, 2, -2);
                    break;
                default:
                    // Random evasion
                    targetPos = pos.offset(
                        (Math.random() - 0.5) * 4,
                        0,
                        (Math.random() - 0.5) * 4
                    );
            }
            
            return targetPos;
        }
    }
};

// ============================================================================
// ENHANCED OODA LOOP
// ============================================================================
let tick = 0;
let brainWs = null;
let brainConnected = false;
let currentTernaryState = TernaryState.BALANCE;

async function enhancedOODA() {
    while (true) {
        tick++;
        
        if (!bot.entity) {
            await new Promise(r => setTimeout(r, 1000));
            continue;
        }
        
        const pos = bot.entity.position;
        const health = bot.health;
        const food = bot.food;
        const inventory = bot.inventory.items();
        
        // =====================================================================
        // OBSERVE (Enhanced with memory)
        // =====================================================================
        const observation = {
            tick,
            timestamp: Date.now(),
            position: { x: pos.x, y: pos.y, z: pos.z },
            health,
            food,
            inventory: inventory.map(i => ({ name: i.name, count: i.count })),
            timeOfDay: bot.time.timeOfDay,
            isDay: bot.time.timeOfDay < 12000,
            ternaryState: currentTernaryState,
            emotional: { ...EmotionalState }
        };
        
        // Scan for entities with memory
        const nearby = Object.values(bot.entities)
            .filter(e => e.position && e.position.distanceTo(pos) < 32)
            .map(e => ({
                type: e.name,
                pos: { ...e.position },
                distance: e.position.distanceTo(pos),
                isHostile: ['zombie', 'skeleton', 'creeper', 'spider'].includes(e.name),
                isFood: ['pig', 'cow', 'sheep', 'chicken'].includes(e.name),
                isPlayer: e.type === 'player'
            }));
        
        observation.nearby = nearby;
        
        // =====================================================================
        // TERNARY STATE DETECTION
        // =====================================================================
        const threats = nearby.filter(e => e.isHostile && e.distance < 10);
        const isNight = !observation.isDay;
        const isLowHealth = health < 8;
        const isHungry = food < 10;
        
        // Determine ternary state
        if (isNight || isLowHealth) {
            currentTernaryState = TernaryState.REST;
        } else if (threats.length > 0) {
            currentTernaryState = TernaryState.ACTIVE;
        } else {
            currentTernaryState = TernaryState.BALANCE;
        }
        
        // =====================================================================
        // UPDATE EMOTIONAL STATE
        // =====================================================================
        EmotionalState.update(health, food, inventory, threats);
        observation.emotional = { ...EmotionalState };
        
        // =====================================================================
        // ORIENT (with memory and emotional context)
        // =====================================================================
        const orientation = {
            threats: threats.map(t => ({
                ...t,
                urgency: t.distance < 5 ? 'CRITICAL' : t.distance < 10 ? 'HIGH' : 'MEDIUM'
            })),
            opportunities: nearby
                .filter(e => e.isFood && e.distance < 20)
                .sort((a, b) => a.distance - b.distance),
            memory: {
                home: AgentMemory.recall('home'),
                lastCamp: AgentMemory.recall('camp'),
                nearestResource: AgentMemory.getNearestResource('log', pos)
            },
            emotionalMode: EmotionalState.getMode(),
            isDangerous: AgentMemory.isDangerous(pos)
        };
        
        // =====================================================================
        // DECIDE (Hierarchical goals with ternary awareness)
        // =====================================================================
        let decision = { type: 'idle', params: {} };
        
        // TERNARY-BASED DECISIONS
        switch(currentTernaryState) {
            case TernaryState.REST:
                // Night or low health - find shelter
                if (AgentMemory.recall('camp')) {
                    decision = { 
                        type: 'return_to_camp', 
                        params: { target: AgentMemory.recall('camp') }
                    };
                } else {
                    decision = { type: 'dig_shelter', params: {} };
                }
                break;
                
            case TernaryState.ACTIVE:
                // Threat present - fight or flight
                if (EmotionalState.fear > 0.7) {
                    // Too scared - flee using evasion skills
                    const evadeTarget = await Skills.evasion.executeManeuver('evasion_basics');
                    decision = { type: 'evade', params: { target: evadeTarget } };
                    AgentMemory.addDanger('combat', pos);
                } else {
                    // Fight using combat skills
                    const target = orientation.threats[0];
                    const combatDecision = Skills.combat.engage(target);
                    decision = { 
                        type: 'combat', 
                        params: { ...combatDecision, target }
                    };
                }
                break;
                
            case TernaryState.BALANCE:
                // Normal operation - emotional mode decides
                switch(EmotionalState.getMode()) {
                    case 'DEFENSIVE':
                        decision = { type: 'fortify', params: {} };
                        break;
                        
                    case 'AGGRESSIVE':
                        // Explore far, gather resources
                        if (orientation.opportunities.length > 0) {
                            decision = { 
                                type: 'hunt', 
                                params: { target: orientation.opportunities[0] }
                            };
                        } else {
                            decision = { 
                                type: 'explore_far', 
                                params: { distance: 50 + EmotionalState.confidence * 50 }
                            };
                        }
                        break;
                        
                    case 'EXPLORATORY':
                        // Search for resources, buildings
                        decision = { type: 'scout', params: {} };
                        break;
                        
                    case 'CAUTIOUS':
                        // Stay near known safe areas
                        if (AgentMemory.recall('home')) {
                            decision = { 
                                type: 'patrol', 
                                params: { center: AgentMemory.recall('home'), radius: 30 }
                            };
                        } else {
                            decision = { type: 'establish_camp', params: {} };
                        }
                        break;
                }
                break;
        }
        
        // =====================================================================
        // ACT (Execute with skills)
        // =====================================================================
        const actionResult = await executeEnhancedAction(decision);
        
        // =====================================================================
        // LEARN (Update memory)
        // =====================================================================
        if (actionResult.success) {
            if (decision.type === 'establish_camp' || decision.type === 'dig_shelter') {
                AgentMemory.remember('camp', { ...pos, time: Date.now() });
            }
            if (decision.type === 'hunt' && actionResult.killed) {
                AgentMemory.addResource('food', pos, actionResult.quantity);
            }
        }
        
        // =====================================================================
        // REPORT TO BRAIN
        // =====================================================================
        if (brainConnected) {
            brainWs.send(JSON.stringify({
                type: 'enhanced_ooda_tick',
                agent_id: AGENT_ID,
                tick,
                ternaryState: currentTernaryState,
                emotional: EmotionalState.getMode(),
                decision: decision.type,
                memorySize: Object.keys(AgentMemory.locations).length
            }));
        }
        
        // Dynamic tick rate based on ternary state
        const tickRate = currentTernaryState === TernaryState.ACTIVE ? 250 : 500;
        await new Promise(r => setTimeout(r, tickRate));
    }
}

// ============================================================================
// ENHANCED ACTION EXECUTION
// ============================================================================
async function executeEnhancedAction(decision) {
    const pos = bot.entity.position;
    
    switch(decision.type) {
        case 'evade':
            const target = decision.params.target;
            if (target) {
                bot.pathfinder.setMovements(new Movements(bot));
                await bot.pathfinder.goto(new GoalNear(target.x, target.y, target.z, 1))
                    .catch(() => {});
            }
            return { success: true, action: 'evaded' };
            
        case 'combat':
            const combat = decision.params;
            if (combat.action === 'attack' && combat.target) {
                await bot.pathfinder.goto(
                    new GoalNear(combat.target.pos.x, combat.target.pos.y, combat.target.pos.z, 2)
                ).catch(() => {});
                await bot.attack(bot.nearestEntity(e => e.name === combat.target.type));
                return { success: true, action: 'attacked', killed: false };
            }
            return { success: false };
            
        case 'dig_shelter':
            // Dig down 2 blocks and cover
            const shelterPos = pos.offset(0, -2, 0);
            await bot.dig(bot.blockAt(pos.offset(0, -1, 0))).catch(() => {});
            await bot.dig(bot.blockAt(shelterPos)).catch(() => {});
            // Would place block on top
            return { success: true, action: 'shelter_dug' };
            
        case 'explore_far':
            const dist = decision.params.distance || 50;
            const angle = Math.random() * Math.PI * 2;
            const explorePos = {
                x: pos.x + Math.cos(angle) * dist,
                y: pos.y,
                z: pos.z + Math.sin(angle) * dist
            };
            bot.pathfinder.setMovements(new Movements(bot));
            await bot.pathfinder.goto(new GoalNear(explorePos.x, explorePos.y, explorePos.z, 5))
                .catch(() => {});
            return { success: true, action: 'explored' };
            
        case 'establish_camp':
            // Mark current location as camp
            AgentMemory.remember('camp', { ...pos, time: Date.now() });
            return { success: true, action: 'camp_established' };
            
        case 'return_to_camp':
            const camp = decision.params.target;
            if (camp) {
                bot.pathfinder.setMovements(new Movements(bot));
                await bot.pathfinder.goto(new GoalNear(camp.x, camp.y, camp.z, 2))
                    .catch(() => {});
            }
            return { success: true, action: 'returned_to_camp' };
            
        case 'patrol':
            const center = decision.params.center;
            const radius = decision.params.radius;
            const patrolAngle = Math.random() * Math.PI * 2;
            const patrolPos = {
                x: center.x + Math.cos(patrolAngle) * radius,
                y: center.y,
                z: center.z + Math.sin(patrolAngle) * radius
            };
            bot.pathfinder.setMovements(new Movements(bot));
            await bot.pathfinder.goto(new GoalNear(patrolPos.x, patrolPos.y, patrolPos.z, 3))
                .catch(() => {});
            return { success: true, action: 'patrolled' };
            
        case 'scout':
            // Look around for resources/structures
            const lookPos = {
                x: pos.x + (Math.random() - 0.5) * 30,
                y: pos.y,
                z: pos.z + (Math.random() - 0.5) * 30
            };
            bot.pathfinder.setMovements(new Movements(bot));
            await bot.pathfinder.goto(new GoalNear(lookPos.x, lookPos.y, lookPos.z, 3))
                .catch(() => {});
            // Scan for interesting blocks
            return { success: true, action: 'scouted' };
            
        case 'hunt':
            const food = decision.params.target;
            if (food) {
                await bot.pathfinder.goto(
                    new GoalNear(food.pos.x, food.pos.y, food.pos.z, 1)
                ).catch(() => {});
                const entity = bot.nearestEntity(e => e.name === food.type);
                if (entity) {
                    await bot.attack(entity);
                    return { success: true, action: 'hunted', killed: true, quantity: 1 };
                }
            }
            return { success: false };
            
        case 'fortify':
            // Build up defenses around current position
            return { success: true, action: 'fortified' };
            
        case 'idle':
        default:
            await new Promise(r => setTimeout(r, 500));
            return { success: true, action: 'idled' };
    }
}

// ============================================================================
// BRAIN CONNECTION
// ============================================================================
function connectBrain() {
    console.log(`[${AGENT_ID}] Connecting to Brain...`);
    
    try {
        brainWs = new WebSocket(BRAIN_URL);
        
        brainWs.on('open', () => {
            console.log(`[${AGENT_ID}] ✅ Brain connected`);
            brainConnected = true;
            
            brainWs.send(JSON.stringify({
                type: 'register_enhanced_agent',
                agent_id: AGENT_ID,
                capabilities: ['ternary_ooda', 'memory', 'emotions', 'skills', 'combat', 'building'],
                version: '2.0'
            }));
        });
        
        brainWs.on('message', (data) => {
            try {
                const msg = JSON.parse(data);
                handleBrainMessage(msg);
            } catch(e) {}
        });
        
        brainWs.on('close', () => {
            brainConnected = false;
            setTimeout(connectBrain, 5000);
        });
        
        brainWs.on('error', () => {});
        
    } catch (e) {
        setTimeout(connectBrain, 5000);
    }
}

function handleBrainMessage(msg) {
    if (msg.type === 'coordination') {
        // Receive locations from other agents
        if (msg.agent_locations) {
            msg.agent_locations.forEach(loc => {
                AgentMemory.agentLocations[loc.id] = {
                    x: loc.x, y: loc.y, z: loc.z,
                    timestamp: Date.now()
                };
            });
        }
    }
}

// ============================================================================
// EVENT HANDLERS
// ============================================================================
bot.once('spawn', () => {
    console.log(`[${AGENT_ID}] ✅ Spawned! Ternary OODA v2.0 active`);
    bot.chat(`${AGENT_ID} online - Enhanced OODA v2.0`);
    
    // Set initial home
    AgentMemory.remember('home', { ...bot.entity.position, time: Date.now() });
    
    connectBrain();
    enhancedOODA();
});

bot.on('death', () => {
    console.log(`[${AGENT_ID}] ☠️ Died`);
    // Record death location
    if (bot.entity) {
        AgentMemory.addDanger('death', bot.entity.position);
    }
    EmotionalState.fear = 0.8; // Fear increases after death
});

bot.on('chat', (username, message) => {
    if (username === bot.username) return;
    
    // Parse commands
    if (message.includes(AGENT_ID) || message.includes('all agents')) {
        if (message.includes('status')) {
            const mode = EmotionalState.getMode();
            const ternary = currentTernaryState;
            bot.chat(`${AGENT_ID}: ${mode} | ${ternary} | Mem:${Object.keys(AgentMemory.locations).length}`);
        }
    }
});

bot.on('error', (err) => {
    console.error(`[${AGENT_ID}] Error:`, err.message);
});

bot.on('end', () => {
    if (brainWs) brainWs.close();
    process.exit(0);
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log(`[${AGENT_ID}] Shutting down...`);
    if (brainWs) brainWs.close();
    bot.quit();
    process.exit(0);
});

console.log(`[${AGENT_ID}] Waiting for spawn...`);
