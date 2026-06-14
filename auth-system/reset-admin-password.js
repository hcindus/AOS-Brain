#!/usr/bin/env node
/**
 * Reset admin password script
 * Usage: node reset-admin-password.js <new-password>
 */

const argon2 = require('argon2');
const sqlite3 = require('sqlite3').verbose();
require('dotenv').config();

const ARGON2_CONFIG = {
    type: argon2.argon2id,
    memoryCost: 19456,
    timeCost: 2,
    parallelism: 1,
    hashLength: 32
};

async function hashPassword(password) {
    const pepper = process.env.BCRYPT_PEPPER || '';
    const pepperedPassword = password + pepper;
    return await argon2.hash(pepperedPassword, ARGON2_CONFIG);
}

async function resetPassword() {
    const newPassword = process.argv[2];
    
    if (!newPassword || newPassword.length < 8) {
        console.error('Error: Password must be at least 8 characters');
        console.error('Usage: node reset-admin-password.js <new-password>');
        process.exit(1);
    }
    
    const dbPath = process.env.DATABASE_URL || './data/auth.db';
    const db = new sqlite3.Database(dbPath);
    
    try {
        const passwordHash = await hashPassword(newPassword);
        
        db.run(
            'UPDATE users SET password_hash = ?, failed_attempts = 0, locked_until = NULL WHERE email = ?',
            [passwordHash, 'admin@psdepot.com'],
            function(err) {
                if (err) {
                    console.error('Database error:', err);
                    process.exit(1);
                }
                
                if (this.changes === 0) {
                    console.error('Error: User admin@psdepot.com not found');
                    process.exit(1);
                }
                
                console.log('✅ Password reset successful for admin@psdepot.com');
                console.log('🔐 Account unlocked and failed attempts cleared');
                db.close();
                process.exit(0);
            }
        );
    } catch (err) {
        console.error('Error:', err);
        db.close();
        process.exit(1);
    }
}

resetPassword();
