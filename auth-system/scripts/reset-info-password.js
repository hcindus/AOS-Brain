#!/usr/bin/env node
/**
 * Reset password for info@psdepot.com
 */

require('dotenv').config();
const sqlite3 = require('sqlite3').verbose();
const argon2 = require('argon2');
const path = require('path');

const DB_PATH = path.join(__dirname, '../data/auth.db');

async function resetPassword() {
    console.log('🔧 Resetting password for info@psdepot.com...\n');
    
    const db = new sqlite3.Database(DB_PATH);
    
    const email = 'info@psdepot.com';
    const newPassword = 'InfoPass123!'; // Temporary password
    
    const pepper = process.env.BCRYPT_PEPPER || '';
    
    try {
        const passwordHash = await argon2.hash(newPassword + pepper, {
            type: argon2.argon2id,
            memoryCost: 19456,
            timeCost: 2,
            parallelism: 1,
            hashLength: 32
        });
        
        return new Promise((resolve, reject) => {
            db.run(
                'UPDATE users SET password_hash = ?, password_changed_at = CURRENT_TIMESTAMP WHERE email = ?',
                [passwordHash, email],
                function(err) {
                    if (err) {
                        reject(err);
                    } else if (this.changes === 0) {
                        console.log('⚠️  User not found: ' + email);
                        resolve(false);
                    } else {
                        console.log('✅ Password reset successfully!');
                        console.log('');
                        console.log('═══════════════════════════════════════════════════════════');
                        console.log('              UPDATED CREDENTIALS                        ');
                        console.log('═══════════════════════════════════════════════════════════');
                        console.log('');
                        console.log('   📧 Email:    info@psdepot.com');
                        console.log('   🔑 Password: ' + newPassword);
                        console.log('');
                        console.log('═══════════════════════════════════════════════════════════\n');
                        resolve(true);
                    }
                }
            );
        });
    } catch (err) {
        console.error('❌ Error:', err);
        throw err;
    } finally {
        db.close();
    }
}

resetPassword().catch(console.error);
