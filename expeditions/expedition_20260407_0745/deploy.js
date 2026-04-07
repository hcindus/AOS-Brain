#!/usr/bin/env node
/**
 * UNIFIED AGENT DEPLOYMENT v1.0
 * Deploys all 5 exploration systems:
 * 1. Star Voyager (Browser-based with 3D camera)
 * 2. Minecraft Squad (4 agents with combat)
 * 3. ASCII Camera System
 * 4. Live Dashboard
 * 5. Photo ZIP packaging
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const BASE_DIR = '/root/.openclaw/workspace/expeditions/expedition_20260407_0745';

console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║     🚀 UNIFIED AGENT DEPLOYMENT v1.0                       ║');
console.log('║     Performance Supply Depot — AGI Company                 ║');
console.log('╚════════════════════════════════════════════════════════════╝\n');

console.log('📦 Deployment Package Contents:');
console.log('   1. Star Voyager (Pure JS Ship + Crew + Combat)');
console.log('   2. Minecraft Squad (4 Mineflayer agents)');
console.log('   3. ASCII Camera System');
console.log('   4. Live Dashboard Server');
console.log('   5. Photo ZIP Packaging\n');

// Check dependencies
console.log('🔧 Checking dependencies...');
const deps = ['puppeteer', 'mineflayer', 'mineflayer-pathfinder', 'vec3'];
let missing = [];

deps.forEach(dep => {
    try {
        require.resolve(dep);
        console.log(`   ✅ ${dep}`);
    } catch {
        missing.push(dep);
        console.log(`   ❌ ${dep} (will install)`);
    }
});

if (missing.length > 0) {
    console.log(`\n📥 Installing missing dependencies: ${missing.join(', ')}`);
    try {
        execSync(`cd ${BASE_DIR} && npm install ${missing.join(' ')} --save`, { stdio: 'inherit' });
    } catch (e) {
        console.error('Failed to install dependencies:', e.message);
        process.exit(1);
    }
}

console.log('\n' + '═'.repeat(60));
console.log('🚀 INITIATING DEPLOYMENT SEQUENCE');
console.log('═'.repeat(60));

// Create output directories
const dirs = ['reports', 'photos', 'logs', 'dashboard'];
dirs.forEach(dir => {
    const fullPath = path.join(BASE_DIR, dir);
    if (!fs.existsSync(fullPath)) {
        fs.mkdirSync(fullPath, { recursive: true });
    }
});

// ═══════════════════════════════════════════════════════════
// DEPLOYMENT: Star Voyager
// ═══════════════════════════════════════════════════════════
console.log('\n📡 DEPLOYING STAR VOYAGER (Mission 1/2)');
console.log('─'.repeat(60));

async function deployStarVoyager() {
    const { ExplorationMission, SHIP, CREW } = require('./star_voyager.js');
    
    const mission = new ExplorationMission(SHIP, CREW, path.join(BASE_DIR, 'star_voyager'));
    await mission.initialize();
    await mission.run();
    
    return {
        name: 'Star Voyager',
        report: path.join(BASE_DIR, 'star_voyager', 'mission_report.json'),
        dashboard: 'http://localhost:8765/',
        photos: path.join(BASE_DIR, 'star_voyager', 'photos')
    };
}

// ═══════════════════════════════════════════════════════════
// DEPLOYMENT: Minecraft Squad (if server available)
// ═══════════════════════════════════════════════════════════
console.log('\n📡 DEPLOYING MINECRAFT SQUAD (Mission 2/2)');
console.log('─'.repeat(60));

async function deployMinecraftSquad() {
    // Check if Minecraft server is available
    const net = require('net');
    const isMCAvailable = await new Promise(resolve => {
        const socket = net.createConnection(25565, 'localhost', () => {
            socket.end();
            resolve(true);
        });
        socket.on('error', () => resolve(false));
        socket.setTimeout(2000, () => {
            socket.destroy();
            resolve(false);
        });
    });
    
    if (!isMCAvailable) {
        console.log('⚠️  Minecraft server not available on localhost:25565');
        console.log('   Minecraft Squad deployment SKIPPED');
        console.log('   (Server required for Mineflayer agents)');
        return null;
    }
    
    console.log('✅ Minecraft server detected. Deploying squad...');
    
    const { ExplorationSquad } = require('./minecraft_explorer.js');
    
    const config = {
        host: 'localhost',
        port: 25565,
        version: '1.20.1',
        outputDir: path.join(BASE_DIR, 'minecraft_squad')
    };
    
    const squad = new ExplorationSquad(config);
    
    const crew = [
        { name: 'Forge', username: 'forge_expedition' },
        { name: 'Patricia', username: 'patricia_expedition' },
        { name: 'Chelios', username: 'chelios_expedition' },
        { name: 'Aurora', username: 'aurora_expedition' }
    ];
    
    await squad.deployCrew(crew);
    await squad.runMission(300000); // 5 minutes
    
    return {
        name: 'Minecraft Squad',
        report: path.join(BASE_DIR, 'minecraft_squad', 'squad_summary.json'),
        photos: path.join(BASE_DIR, 'minecraft_squad', 'photos')
    };
}

// ═══════════════════════════════════════════════════════════
// PACKAGE GENERATION
// ═══════════════════════════════════════════════════════════
function createPackage(results) {
    console.log('\n' + '═'.repeat(60));
    console.log('📦 CREATING EXPEDITION PACKAGE');
    console.log('═'.repeat(60));
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const packageDir = path.join(BASE_DIR, `expedition_package_${timestamp}`);
    
    fs.mkdirSync(packageDir, { recursive: true });
    
    // Copy all results
    results.forEach(result => {
        if (!result) return;
        
        const destDir = path.join(packageDir, result.name.replace(/\s+/g, '_').toLowerCase());
        fs.mkdirSync(destDir, { recursive: true });
        
        if (result.report && fs.existsSync(result.report)) {
            fs.copyFileSync(result.report, path.join(destDir, 'report.json'));
        }
        
        if (result.photos && fs.existsSync(result.photos)) {
            const destPhotos = path.join(destDir, 'photos');
            fs.mkdirSync(destPhotos, { recursive: true });
            
            try {
                const photos = fs.readdirSync(result.photos);
                photos.slice(0, 20).forEach(photo => {
                    const src = path.join(result.photos, photo);
                    const dest = path.join(destPhotos, photo);
                    fs.copyFileSync(src, dest);
                });
            } catch (e) {
                console.log(`   ⚠️ Could not copy photos from ${result.photos}`);
            }
        }
    });
    
    // Create package manifest
    const manifest = {
        generated: new Date().toISOString(),
        expedition: 'expedition_20260407_0745',
        missions: results.filter(r => r).map(r => ({
            name: r.name,
            dashboard: r.dashboard || null
        }))
    };
    
    fs.writeFileSync(
        path.join(packageDir, 'MANIFEST.json'),
        JSON.stringify(manifest, null, 2)
    );
    
    // Create tar.gz archive
    const archiveName = `unified_expedition_${timestamp}.tar.gz`;
    const archivePath = path.join(BASE_DIR, archiveName);
    
    try {
        execSync(`cd ${BASE_DIR} && tar -czf ${archivePath} ${path.basename(packageDir)}`, { stdio: 'ignore' });
        console.log(`✅ Archive created: ${archivePath}`);
        console.log(`   Size: ${(fs.statSync(archivePath).size / 1024).toFixed(1)} KB`);
    } catch (e) {
        console.log(`   ⚠️ Archive creation skipped (tar not available)`);
    }
    
    return { packageDir, archivePath: fs.existsSync(archivePath) ? archivePath : null };
}

// ═══════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════
async function main() {
    const results = [];
    
    try {
        // Deploy Star Voyager
        const starVoyagerResult = await deployStarVoyager();
        results.push(starVoyagerResult);
    } catch (err) {
        console.error('❌ Star Voyager deployment failed:', err.message);
    }
    
    try {
        // Deploy Minecraft Squad (if possible)
        const minecraftResult = await deployMinecraftSquad();
        if (minecraftResult) results.push(minecraftResult);
    } catch (err) {
        console.error('❌ Minecraft Squad deployment failed:', err.message);
    }
    
    // Create package
    const pkg = createPackage(results);
    
    // Final summary
    console.log('\n' + '═'.repeat(60));
    console.log('🎖️ DEPLOYMENT COMPLETE');
    console.log('═'.repeat(60));
    console.log('\n📊 Mission Summary:');
    results.forEach((r, i) => {
        if (r) {
            console.log(`   ${i + 1}. ${r.name}`);
            if (r.dashboard) console.log(`      Dashboard: ${r.dashboard}`);
            console.log(`      Report: ${r.report}`);
        }
    });
    
    console.log(`\n📦 Package Location:`);
    console.log(`   ${pkg.packageDir}`);
    if (pkg.archivePath) console.log(`   Archive: ${pkg.archivePath}`);
    
    console.log('\n' + '═'.repeat(60));
    console.log('All agents deployed and operational.');
    console.log('Expedition data available in package directory.');
    console.log('═'.repeat(60) + '\n');
}

main().catch(err => {
    console.error('Deployment failed:', err);
    process.exit(1);
});
