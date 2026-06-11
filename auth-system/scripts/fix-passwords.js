#!/usr/bin/env node
/**
 * Fix Test User Passwords for Auth System
 */

require('dotenv').config();
const sqlite3 = require('sqlite3').verbose();
const argon2 = require('argon2');
const path = require('path');

const DB_PATH = path.join(__dirname, '../data/auth.db');

async function fixPasswords() {
    console.log('🔧 Fixing test user passwords...\n');
    
    const db = new sqlite3.Database(DB_PATH);
    
    const pepper = process.env.BCRYPT_PEPPER || '';
    
    // Fix test@psdepot.com
    const testPassword = 'TestPass123!';
    const testHash = await argon2.hash(testPassword + pepper, {
        type: argon2.argon2id,
        memoryCost: 19456,
        timeCost: 2,
        parallelism: 1,
        hashLength: 32
    });
    
    // Fix admin@psdepot.com
    const adminPassword = 'AdminPass456!';
    const adminHash = await argon2.hash(adminPassword + pepper, {
        type: argon2.argon2id,
        memoryCost: 19456,
        timeCost: 2,
        parallelism: 1,
        hashLength: 32
    });
    
    return new Promise((resolve, reject) => {
        db.serialize(() => {
            db.run('UPDATE users SET password_hash = ? WHERE email = ?', [testHash, 'test@psdepot.com'], function(err) {
                if (err) {
                    console.error('Error updating test user:', err);
                } else {
                    console.log('✅ Test user password updated (test@psdepot.com)');
                }
            });
            
            db.run('UPDATE users SET password_hash = ? WHERE email = ?', [adminHash, 'admin@psdepot.com'], function(err) {
                if (err) {
                    console.error('Error updating admin user:', err);
                } else {
                    console.log('✅ Admin user password updated (admin@psdepot.com)');
                }
            });
        });
        
        setTimeout(() => {
            db.close();
            console.log('\n🎉 Passwords fixed!');
            resolve();
        }, 500);
    });
}

fixPasswords().catch(console.error);
