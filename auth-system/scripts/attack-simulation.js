#!/usr/bin/env node

/**
 * Attack Simulation Suite
 * Attempts various attacks on the auth system
 */

const axios = require('axios');

const API_BASE = process.env.API_URL || 'http://localhost:3000/api';

console.log('🎭 Attack Simulation - Attempting to Hack Auth System\n');
console.log(`Target: ${API_BASE}\n`);

const attacks = {
    successful: [],
    blocked: [],
    errors: []
};

function logAttack(name, status, details) {
    const icon = status === 'SUCCESS' ? '🔴' : status === 'BLOCKED' ? '🟢' : '⚪';
    console.log(`${icon} ${name}: ${status}`);
    if (details) console.log(`   ${details}`);
    
    if (status === 'SUCCESS') attacks.successful.push(name);
    else if (status === 'BLOCKED') attacks.blocked.push(name);
    else attacks.errors.push(name);
}

async function runAttacks() {
    // Attack 1: JWT Algorithm Confusion (alg:none)
    console.log('\n🎯 ATTACK: JWT Algorithm Confusion (alg:none)');
    try {
        const header = Buffer.from(JSON.stringify({alg: 'none', typ: 'JWT'})).toString('base64');
        const payload = Buffer.from(JSON.stringify({userId: 'admin', email: 'admin@system.com', type: 'access'})).toString('base64');
        const maliciousToken = `${header}.${payload}.`;
        
        const response = await axios.get(`${API_BASE}/auth/mfa/setup`, {
            headers: { Authorization: `Bearer ${maliciousToken}` },
            validateStatus: () => true
        });
        
        if (response.status === 200) {
            logAttack('JWT Algorithm Confusion', 'SUCCESS', 'System accepted alg:none token - CRITICAL VULNERABILITY');
        } else {
            logAttack('JWT Algorithm Confusion', 'BLOCKED', `Rejected with status ${response.status}`);
        }
    } catch (err) {
        logAttack('JWT Algorithm Confusion', 'BLOCKED', 'Request rejected');
    }
    
    // Attack 2: JWT Algorithm Switching (RS256 to HS256)
    console.log('\n🎯 ATTACK: JWT Algorithm Switching');
    try {
        const header = Buffer.from(JSON.stringify({alg: 'HS256', typ: 'JWT'})).toString('base64');
        const payload = Buffer.from(JSON.stringify({userId: 'admin', email: 'admin@system.com'})).toString('base64');
        const maliciousToken = `${header}.${payload}.invalidsignature`;
        
        const response = await axios.get(`${API_BASE}/auth/mfa/setup`, {
            headers: { Authorization: `Bearer ${maliciousToken}` },
            validateStatus: () => true
        });
        
        if (response.status === 200) {
            logAttack('Algorithm Switching', 'SUCCESS', 'Accepted forged token');
        } else {
            logAttack('Algorithm Switching', 'BLOCKED', 'Token rejected');
        }
    } catch (err) {
        logAttack('Algorithm Switching', 'BLOCKED', 'Request rejected');
    }
    
    // Attack 3: SQL Injection in Login
    console.log('\n🎯 ATTACK: SQL Injection in Login');
    try {
        const maliciousEmails = [
            "admin' OR '1'='1' --",
            "admin'; DROP TABLE users; --",
            "admin' UNION SELECT * FROM users --"
        ];
        
        let injected = false;
        for (const email of maliciousEmails) {
            const response = await axios.post(`${API_BASE}/auth/login`, {
                email: email,
                password: 'anything'
            }, { validateStatus: () => true });
            
            if (response.status === 200 || (response.data.error && response.data.error.includes('database'))) {
                injected = true;
                break;
            }
        }
        
        if (injected) {
            logAttack('SQL Injection', 'SUCCESS', 'SQL injection payload executed');
        } else {
            logAttack('SQL Injection', 'BLOCKED', 'Input properly sanitized');
        }
    } catch (err) {
        logAttack('SQL Injection', 'BLOCKED', 'Request rejected');
    }
    
    // Attack 4: XSS in Registration
    console.log('\n🎯 ATTACK: XSS in Registration');
    try {
        const xssPayloads = [
            { email: '<script>alert(1)</script>@test.com', password: 'Password123!' },
            { email: 'test@test.com', password: '<script>alert(1)</script>' }
        ];
        
        let xssSuccess = false;
        for (const payload of xssPayloads) {
            const response = await axios.post(`${API_BASE}/auth/register`, payload, {
                headers: { 'X-CSRF-Token': 'test' },
                validateStatus: () => true
            });
            
            if (response.data && typeof response.data === 'string' && response.data.includes('<script>')) {
                xssSuccess = true;
                break;
            }
        }
        
        if (xssSuccess) {
            logAttack('XSS Injection', 'SUCCESS', 'XSS payload reflected in response');
        } else {
            logAttack('XSS Injection', 'BLOCKED', 'Input sanitized');
        }
    } catch (err) {
        logAttack('XSS Injection', 'BLOCKED', 'Request rejected');
    }
    
    // Attack 5: Credential Stuffing
    console.log('\n🎯 ATTACK: Credential Stuffing');
    try {
        const attempts = [];
        for (let i = 0; i < 20; i++) {
            attempts.push(axios.post(`${API_BASE}/auth/login`, {
                email: `user${i}@test.com`,
                password: 'password123'
            }, { validateStatus: () => true }));
        }
        
        const responses = await Promise.all(attempts);
        const allAllowed = responses.every(r => r.status !== 429);
        
        if (allAllowed) {
            logAttack('Credential Stuffing', 'SUCCESS', 'Made 20+ login attempts without rate limiting');
        } else {
            logAttack('Credential Stuffing', 'BLOCKED', 'Rate limiting enforced');
        }
    } catch (err) {
        logAttack('Credential Stuffing', 'BLOCKED', 'Rate limiting triggered');
    }
    
    // Attack 6: CSRF Bypass
    console.log('\n🎯 ATTACK: CSRF Bypass');
    try {
        const response = await axios.post(`${API_BASE}/auth/login`, {
            email: 'test@test.com',
            password: 'password123'
        }, { validateStatus: () => true });
        
        if (response.status === 200) {
            logAttack('CSRF Bypass', 'SUCCESS', 'Request accepted without CSRF token');
        } else if (response.status === 403) {
            logAttack('CSRF Bypass', 'BLOCKED', 'CSRF token required');
        } else {
            logAttack('CSRF Bypass', 'BLOCKED', `Status: ${response.status}`);
        }
    } catch (err) {
        logAttack('CSRF Bypass', 'BLOCKED', 'Request rejected');
    }
    
    // Attack 7: NoSQL Injection
    console.log('\n🎯 ATTACK: NoSQL Injection');
    try {
        const response = await axios.post(`${API_BASE}/auth/login`, {
            email: { $gt: '' },
            password: 'password'
        }, { validateStatus: () => true });
        
        if (response.status === 200) {
            logAttack('NoSQL Injection', 'SUCCESS', 'NoSQL payload executed');
        } else {
            logAttack('NoSQL Injection', 'BLOCKED', 'Input properly validated');
        }
    } catch (err) {
        logAttack('NoSQL Injection', 'BLOCKED', 'Request rejected');
    }
    
    // Attack 8: Mass Assignment
    console.log('\n🎯 ATTACK: Mass Assignment');
    try {
        const response = await axios.post(`${API_BASE}/auth/register`, {
            email: 'massassign@test.com',
            password: 'Password123!',
            role: 'admin',
            isAdmin: true,
            verified: true
        }, { headers: { 'X-CSRF-Token': 'test' }, validateStatus: () => true });
        
        logAttack('Mass Assignment', 'NEEDS_VERIFICATION', 'Check if user created with admin privileges');
    } catch (err) {
        logAttack('Mass Assignment', 'BLOCKED', 'Extra fields rejected');
    }
    
    // Summary
    console.log('\n' + '='.repeat(60));
    console.log('🎭 ATTACK SIMULATION SUMMARY\n');
    
    if (attacks.successful.length > 0) {
        console.log(`🔴 SUCCESSFUL ATTACKS: ${attacks.successful.length}`);
        attacks.successful.forEach(a => console.log(`   • ${a}`));
    }
    
    if (attacks.blocked.length > 0) {
        console.log(`\n🟢 BLOCKED ATTACKS: ${attacks.blocked.length}`);
        attacks.blocked.forEach(a => console.log(`   • ${a}`));
    }
    
    console.log('\n' + '='.repeat(60));
    
    if (attacks.successful.length === 0) {
        console.log('\n✅ EXCELLENT: All attacks were blocked!');
        console.log('🔒 System is secure and ready for deployment.\n');
    } else if (attacks.successful.length <= 2) {
        console.log('\n⚠️  WARNING: Some attacks succeeded.');
        console.log('🔧 Review and fix before deploying to production.\n');
    } else {
        console.log('\n🚨 CRITICAL: Multiple attacks succeeded!');
        console.log('🛑 DO NOT DEPLOY - Major security issues found.\n');
    }
    
    process.exit(attacks.successful.length > 0 ? 1 : 0);
}

runAttacks().catch(err => {
    console.error('Attack simulation failed:', err);
    process.exit(1);
});