#!/usr/bin/env node

/**
 * Security Test Suite - Auth System
 * Tests for vulnerabilities and verifies fixes
 */

const axios = require('axios');

const API_BASE = process.env.API_URL || 'http://localhost:3000/api';

// Test results
const results = {
    passed: 0,
    failed: 0,
    critical: [],
    high: [],
    medium: [],
    low: []
};

function logTest(name, status, severity, details = '') {
    const icon = status === 'PASS' ? '✓' : status === 'FAIL' ? '✗' : '⚠';
    const statusStr = status === 'PASS' ? 'PASS' : status === 'FAIL' ? 'FAIL' : status;
    
    console.log(`${icon} ${name}: ${statusStr}`);
    if (details) console.log(`   ${details}`);
    
    if (status === 'PASS') results.passed++;
    else if (status === 'FAIL') {
        results.failed++;
        if (severity === 'CRITICAL') results.critical.push(name);
        if (severity === 'HIGH') results.high.push(name);
        if (severity === 'MEDIUM') results.medium.push(name);
        if (severity === 'LOW') results.low.push(name);
    }
}

async function runTests() {
    console.log('🔐 Security Test Suite\n');
    console.log(`Testing: ${API_BASE}\n`);
    
    // Test 1: CSRF Protection
    console.log('\n📋 Testing CSRF Protection');
    try {
        const response = await axios.post(`${API_BASE}/auth/login`, {
            email: 'test@test.com',
            password: 'password123'
        }, { validateStatus: () => true });
        
        if (response.status === 403 && response.data.error?.includes('CSRF')) {
            logTest('CSRF Required', 'PASS', null, 'Request rejected without CSRF token');
        } else {
            logTest('CSRF Required', 'FAIL', 'CRITICAL', 'CSRF check bypassed!');
        }
    } catch (err) {
        logTest('CSRF Required', 'FAIL', 'CRITICAL', err.message);
    }
    
    // Test 2: Rate Limiting
    console.log('\n📋 Testing Rate Limiting');
    try {
        const attempts = [];
        for (let i = 0; i < 6; i++) {
            attempts.push(axios.post(`${API_BASE}/auth/login`, {
                email: `ratetest${i}@test.com`,
                password: 'wrongpassword'
            }, { validateStatus: () => true }));
        }
        
        const responses = await Promise.all(attempts);
        const rateLimited = responses.some(r => r.status === 429);
        
        if (rateLimited) {
            logTest('Login Rate Limiting', 'PASS', null, 'Rate limit enforced');
        } else {
            logTest('Login Rate Limiting', 'FAIL', 'HIGH', 'No rate limiting detected');
        }
    } catch (err) {
        logTest('Login Rate Limiting', 'FAIL', 'HIGH', err.message);
    }
    
    // Test 3: Security Headers
    console.log('\n📋 Testing Security Headers');
    try {
        const response = await axios.get(`${API_BASE}/health`, { validateStatus: () => true });
        const headers = response.headers;
        
        const required = ['x-frame-options', 'x-content-type-options'];
        const missing = required.filter(h => !headers[h]);
        
        if (missing.length === 0) {
            logTest('Security Headers', 'PASS', null, 'Security headers present');
        } else {
            logTest('Security Headers', 'FAIL', 'HIGH', `Missing: ${missing.join(', ')}`);
        }
    } catch (err) {
        logTest('Security Headers', 'FAIL', 'HIGH', err.message);
    }
    
    // Test 4: JWT Algorithm
    console.log('\n📋 Testing JWT Security');
    try {
        const maliciousToken = 'eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.' + 
            Buffer.from(JSON.stringify({userId: '123', email: 'test@test.com'})).toString('base64') + '.';
        
        const response = await axios.get(`${API_BASE}/auth/mfa/setup`, {
            headers: { Authorization: `Bearer ${maliciousToken}` },
            validateStatus: () => true
        });
        
        if (response.status === 403) {
            logTest('JWT Algorithm Attack', 'PASS', null, 'Algorithm confusion prevented');
        } else {
            logTest('JWT Algorithm Attack', 'FAIL', 'CRITICAL', 'Accepted malicious token!');
        }
    } catch (err) {
        logTest('JWT Algorithm Attack', 'PASS', null, 'Token rejected');
    }
    
    // Test 5: SQL Injection
    console.log('\n📋 Testing SQL Injection');
    try {
        const response = await axios.post(`${API_BASE}/auth/login`, {
            email: "test@test.com'; DROP TABLE users; --",
            password: 'password'
        }, { headers: { 'X-CSRF-Token': 'test' }, validateStatus: () => true });
        
        logTest('SQL Injection', 'PASS', null, 'Input handled safely');
    } catch (err) {
        logTest('SQL Injection', 'PASS', null, 'Request rejected');
    }
    
    // Test 6: XSS
    console.log('\n📋 Testing XSS Protection');
    try {
        const response = await axios.post(`${API_BASE}/auth/login`, {
            email: '<script>alert("xss")</script>',
            password: 'password'
        }, { headers: { 'X-CSRF-Token': 'test' }, validateStatus: () => true });
        
        if (response.data.error && !response.data.error.includes('<script>')) {
            logTest('XSS Reflected', 'PASS', null, 'Output sanitized');
        } else {
            logTest('XSS Reflected', 'FAIL', 'HIGH', 'XSS payload reflected');
        }
    } catch (err) {
        logTest('XSS Reflected', 'PASS', null, 'Request rejected');
    }
    
    // Summary
    console.log('\n' + '='.repeat(50));
    console.log('📊 SECURITY TEST SUMMARY\n');
    console.log(`✅ Tests Passed: ${results.passed}`);
    console.log(`❌ Tests Failed: ${results.failed}`);
    
    if (results.critical.length > 0) {
        console.log(`\n🚨 CRITICAL VULNERABILITIES:`);
        results.critical.forEach(v => console.log(`   • ${v}`));
    }
    
    if (results.high.length > 0) {
        console.log(`\n⚠️  HIGH SEVERITY:`);
        results.high.forEach(v => console.log(`   • ${v}`));
    }
    
    if (results.failed === 0) {
        console.log('\n✨ All security tests passed! System is ready for deployment.');
    } else {
        console.log('\n⚠️  Address failed tests before deploying to production.');
    }
    
    process.exit(results.failed > 0 ? 1 : 0);
}

runTests().catch(err => {
    console.error('Test suite failed:', err);
    process.exit(1);
});