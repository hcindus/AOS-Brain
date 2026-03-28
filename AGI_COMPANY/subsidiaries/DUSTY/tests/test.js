// Dusty Syntax & Structure Tests
const fs = require('fs');
const path = require('path');

console.log('🧪 Dusty Test Suite\n');
console.log('='.repeat(50));

const srcDir = './src';
const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.js'));

let passed = 0;
let failed = 0;

files.forEach(file => {
    const content = fs.readFileSync(path.join(srcDir, file), 'utf8');
    
    // Test 1: File has content
    if (content.length > 0) {
        console.log(`✅ ${file}: File loaded (${content.length} bytes)`);
        passed++;
    } else {
        console.log(`❌ ${file}: Empty file`);
        failed++;
    }
    
    // Test 2: Has OnStart function (main entry point)
    if (content.includes('function OnStart')) {
        console.log(`✅ ${file}: Has OnStart function`);
        passed++;
    } else {
        console.log(`❌ ${file}: Missing OnStart function`);
        failed++;
    }
    
    // Test 3: Has layout creation
    if (content.includes('CreateLayout')) {
        console.log(`✅ ${file}: Has layout creation`);
        passed++;
    } else {
        console.log(`❌ ${file}: Missing layout creation`);
        failed++;
    }
    
    // Test 4: Has app.AddLayout
    if (content.includes('app.AddLayout')) {
        console.log(`✅ ${file}: Has app.AddLayout`);
        passed++;
    } else {
        console.log(`❌ ${file}: Missing app.AddLayout`);
        failed++;
    }
});

console.log('\n' + '='.repeat(50));

// Test docs
console.log('\n📄 Documentation Files:');
const docsDir = './docs';
const docFiles = fs.readdirSync(docsDir).filter(f => f.endsWith('.md'));
docFiles.forEach(file => {
    const content = fs.readFileSync(path.join(docsDir, file), 'utf8');
    console.log(`  ✅ ${file}: ${content.length} bytes`);
    passed++;
});

console.log('\n' + '='.repeat(50));
console.log(`\n📊 Results: ${passed} passed, ${failed} failed\n`);

if (failed === 0) {
    console.log('🎉 All Dusty structure tests passed!\n');
} else {
    console.log(`❌ ${failed} tests failed\n`);
    process.exit(1);
}
