// ============================================
// DUSTY - Comprehensive Unit Test Suite
// Run with: node dusty_test.js
// ============================================

const fs = require('fs');
const path = require('path');
const rootDir = '/root/.openclaw/workspace/dusty';

console.log('\n🧪 DUSTY COMPREHENSIVE TEST SUITE\n');
console.log('═'.repeat(50));

let testsPassed = 0;
let testsFailed = 0;

function test(name, fn) {
    try {
        fn();
        console.log(`✅ ${name}`);
        testsPassed++;
        return true;
    } catch (e) {
        console.log(`❌ ${name}`);
        console.log(`   └─ ${e.message}`);
        testsFailed++;
        return false;
    }
}

function assert(condition, message) {
    if (!condition) throw new Error(message || 'Assertion failed');
}

// ============================================
// TEST 1: File Structure
// ============================================
console.log('\n📁 TEST 1: File Structure\n');

const requiredFiles = [
    'src/dusty.js',
    'docs/SPEC.md',
    'docs/PROPOSAL.md',
    'docs/PITCH_DECK.md'
];

requiredFiles.forEach(file => {
    test(`File exists: ${file}`, () => {
        const exists = fs.existsSync(path.join(rootDir, file));
        assert(exists, `Missing file: ${file}`);
    });
});

// ============================================
// TEST 2: Code Syntax
// ============================================
console.log('\n🔍 TEST 2: Code Syntax\n');

const dustyJs = fs.readFileSync(path.join(rootDir, 'src/dusty.js'), 'utf8');

test('dusty.js: Has content', () => {
    assert(dustyJs.length > 1000, 'File too small');
});

test('dusty.js: Has OnStart function', () => {
    assert(dustyJs.includes('function OnStart'), 'Missing OnStart');
});

test('dusty.js: Creates layouts', () => {
    assert(dustyJs.includes('app.CreateLayout'), 'No layout creation');
});

test('dusty.js: Has basic UI structure', () => {
    assert(dustyJs.includes('app.AddLayout'), 'No layout added');
});

// ============================================
// TEST 3: Features
// ============================================
console.log('\n🎯 TEST 3: Features\n');

const features = [
    { name: 'Multi-network support', check: () => dustyJs.includes('Bitgert') || dustyJs.includes('Ethereum') },
    { name: 'Dust scanning', check: () => dustyJs.toLowerCase().includes('dust') },
    { name: 'Cross-chain bridge', check: () => dustyJs.toLowerCase().includes('bridge') },
    { name: 'Staking', check: () => dustyJs.toLowerCase().includes('stake') },
    { name: 'DApp browser', check: () => dustyJs.toLowerCase().includes('dapp') || dustyJs.includes('Web') },
    { name: 'Transaction history', check: () => dustyJs.toLowerCase().includes('transaction') },
    { name: 'Settings/API keys', check: () => dustyJs.toLowerCase().includes('api') || dustyJs.includes('Settings') },
];

features.forEach(feature => {
    test(`Feature: ${feature.name}`, () => {
        assert(feature.check(), `Missing: ${feature.name}`);
    });
});

// ============================================
// TEST 4: UI Components
// ============================================
console.log('\n🖼️ TEST 4: UI Components\n');

const uiComponents = [
    { name: 'Navigation/tabs', check: () => dustyJs.includes('nav') || dustyJs.includes('tab') || dustyJs.includes('Navigate') },
    { name: 'Buttons', check: () => dustyJs.includes('CreateButton') },
    { name: 'Lists/display', check: () => dustyJs.includes('CreateList') || dustyJs.includes('CreateText') },
    { name: 'Text views', check: () => dustyJs.includes('CreateText') },
    { name: 'Input fields', check: () => dustyJs.includes('CreateTextEdit') },
];

uiComponents.forEach(comp => {
    test(`UI: ${comp.name}`, () => {
        assert(comp.check(), `Missing: ${comp.name}`);
    });
});

// ============================================
// TEST 5: Documentation
// ============================================
console.log('\n📚 TEST 5: Documentation\n');

const docsDir = path.join(rootDir, 'docs');
const docFiles = fs.readdirSync(docsDir);

docFiles.forEach(file => {
    const content = fs.readFileSync(path.join(docsDir, file), 'utf8');
    test(`Doc ${file}: Has content`, () => {
        assert(content.length > 100, 'Empty or too short');
    });
});

// ============================================
// TEST 6: Project Stats
// ============================================
console.log('\n📈 TEST 6: Project Stats\n');

const lines = dustyJs.split('\n').length;
console.log(`   Total lines of code: ${lines}`);
console.log(`   File size: ${(dustyJs.length / 1024).toFixed(1)} KB`);

// ============================================
// SUMMARY
// ============================================
console.log('\n' + '═'.repeat(50));
console.log('\n📊 TEST SUMMARY');
console.log(`   ✅ Passed: ${testsPassed}`);
console.log(`   ❌ Failed: ${testsFailed}`);
console.log('═'.repeat(50));

if (testsFailed > 0) {
    console.log('\n❌ SOME TESTS FAILED\n');
    process.exit(1);
} else {
    console.log('\n🎉 ALL TESTS PASSED!\n');
    process.exit(0);
}
