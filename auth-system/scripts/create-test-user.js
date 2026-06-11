#!/usr/bin/env node
/**
 * Create Test User for PSD Appointments
 * Run: node scripts/create-test-user.js
 */

const sqlite3 = require('sqlite3').verbose();
const crypto = require('crypto');
const path = require('path');

const DB_PATH = path.join(__dirname, '../data/auth.db');

// Test user credentials
const TEST_USER = {
    email: 'test@psdepot.com',
    password: 'TestPass123!',
    firstName: 'Test',
    lastName: 'User',
    company: 'Performance Supply Depot'
};

// PBKDF2 password hashing (matches the auth system pattern if it was using this)
// But the actual auth system uses Argon2, so we need to note that this is for compatibility mode
async function hashPasswordPBKDF2(password) {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512').toString('hex');
    return `${salt}:${hash}`;
}

function generateUUID() {
    return crypto.randomUUID();
}

function initDatabase(db) {
    return new Promise((resolve, reject) => {
        db.serialize(() => {
            // Create users table
            db.run(`
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    company TEXT,
                    mfa_secret TEXT,
                    mfa_enabled INTEGER DEFAULT 0,
                    mfa_verified INTEGER DEFAULT 0,
                    email_verified INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_login DATETIME,
                    failed_attempts INTEGER DEFAULT 0,
                    locked_until DATETIME,
                    password_changed_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            `);

            // Create sessions table
            db.run(`
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    refresh_token TEXT NOT NULL,
                    device_fingerprint TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expires_at DATETIME NOT NULL,
                    revoked_at DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            `);

            // Create audit logs table
            db.run(`
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    device_fingerprint TEXT,
                    metadata TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                )
            `, (err) => {
                if (err) reject(err);
                else resolve();
            });
        });
    });
}

async function createUserWithArgon2(db, user) {
    const argon2 = require('argon2');
    
    return new Promise(async (resolve, reject) => {
        const userId = generateUUID();
        
        try {
            const passwordHash = await argon2.hash(user.password + (process.env.BCRYPT_PEPPER || ''), {
                type: argon2.argon2id,
                memoryCost: 19456,
                timeCost: 2,
                parallelism: 1,
                hashLength: 32
            });
            
            db.run(`
                INSERT INTO users (id, email, password_hash, first_name, last_name, company, email_verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            `, [userId, user.email, passwordHash, user.firstName, user.lastName, user.company, 1], function(err) {
                if (err) {
                    if (err.message.includes('UNIQUE constraint failed')) {
                        resolve({ exists: true });
                    } else {
                        reject(err);
                    }
                } else {
                    resolve({ exists: false, id: userId });
                }
            });
        } catch (err) {
            reject(err);
        }
    });
}

async function main() {
    console.log('🧪 Creating test users for PSD Appointments...\n');
    
    const db = new sqlite3.Database(DB_PATH);
    
    try {
        await initDatabase(db);
        
        // Create test user with Argon2
        const testResult = await createUserWithArgon2(db, TEST_USER);
        if (testResult.exists) {
            console.log('⚠️  Test user already exists (test@psdepot.com)\n');
        } else {
            console.log('✅ Test user created successfully!\n');
        }
        
        // Create admin user
        const ADMIN_USER = {
            email: 'admin@psdepot.com',
            password: 'AdminPass456!',
            firstName: 'Admin',
            lastName: 'User',
            company: 'Performance Supply Depot'
        };
        
        const adminResult = await createUserWithArgon2(db, ADMIN_USER);
        if (adminResult.exists) {
            console.log('⚠️  Admin user already exists (admin@psdepot.com)\n');
        } else {
            console.log('✅ Admin user created successfully!\n');
        }
        
        console.log('═══════════════════════════════════════════════════════════');
        console.log('                    TEST CREDENTIALS                        ');
        console.log('═══════════════════════════════════════════════════════════\n');
        
        console.log('   📧 Test Email:     test@psdepot.com');
        console.log('   🔑 Test Password:  TestPass123!');
        console.log('');
        console.log('   📧 Admin Email:    admin@psdepot.com');
        console.log('   🔑 Admin Password: AdminPass456!');
        console.log('');
        console.log('   🏢 Company:        Performance Supply Depot');
        console.log('   ✅ Status:         Email verified\n');
        
        console.log('═══════════════════════════════════════════════════════════\n');
        console.log('📝 Login URL: https://psdepot.com/appointments/web/login.html\n');
        
    } catch (err) {
        console.error('❌ Error:', err);
        process.exit(1);
    } finally {
        db.close();
    }
}

main();
