// CREAM Syntax & Structure Tests
const fs = require('fs');
const path = require('path');

console.log('🧪 CREAM Test Suite\n');
console.log('='.repeat(50));

const testsDir = './src/pages';
const files = fs.readdirSync(testsDir).filter(f => f.endsWith('.js'));

let passed = 0;
let failed = 0;

files.forEach(file => {
    const content = fs.readFileSync(path.join(testsDir, file), 'utf8');
    
    // Skip Utils.js (not a page module)
    if (file === 'Utils.js') {
        console.log(`⏭️  ${file}: Skipped (utility module)`);
        return;
    }
    
    const funcName = file.replace('.js', '');
    
    // Test 1: File has content
    if (content.length > 0) {
        console.log(`✅ ${file}: File loaded (${content.length} bytes)`);
        passed++;
    } else {
        console.log(`❌ ${file}: Empty file`);
        failed++;
    }
    
    // Test 2: Has constructor function
    if (content.includes(`function ${funcName}(`)) {
        console.log(`✅ ${file}: Has ${funcName} constructor`);
        passed++;
    } else {
        console.log(`❌ ${file}: Missing ${funcName} constructor`);
        failed++;
    }
    
    // Test 3: Has Show method
    if (content.includes('.Show = function')) {
        console.log(`✅ ${file}: Has Show method`);
        passed++;
    } else {
        console.log(`❌ ${file}: Missing Show method`);
        failed++;
    }
    
    // Test 4: Has IsVisible method
    if (content.includes('.IsVisible = function')) {
        console.log(`✅ ${file}: Has IsVisible method`);
        passed++;
    } else {
        console.log(`❌ ${file}: Missing IsVisible method`);
        failed++;
    }
});

console.log('\n' + '='.repeat(50));
console.log(`\n📊 Page Module Results: ${passed} passed, ${failed} failed\n`);

// Test main app file
console.log('📦 Main App Files:');
const mainFiles = ['CREAM.js', 'cream.js'];
let mainPassed = 0;
mainFiles.forEach(file => {
    try {
        const content = fs.readFileSync(`./src/${file}`, 'utf8');
        console.log(`  ✅ ${file}: ${content.length} bytes`);
        mainPassed++;
    } catch (e) {
        console.log(`  ❌ ${file}: ${e.message}`);
    }
});

console.log(`\n📊 Main Files: ${mainPassed}/${mainFiles.length} loaded\n`);

// Summary
console.log('='.repeat(50));
if (failed === 0) {
    console.log('🎉 All page structure tests passed!\n');
} else {
    console.log(`❌ ${failed} tests failed\n`);
    process.exit(1);
}
