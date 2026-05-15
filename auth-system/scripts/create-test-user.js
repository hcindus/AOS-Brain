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

function hashPassword(password) {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512').toString('hex');
    return `${salt}:${hash}`;
}

function generateUUID() {
    return crypto.randomUUID();
}

async function createTestUser() {
    console.log('🧪 Creating test user for PSD Appointments...');
    console.log('');
    
    const db = new sqlite3.Database(DB_PATH);
    
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
            `);

            // Check if test user exists
            db.get('SELECT id FROM users WHERE email = ?', [TEST_USER.email], (err, row) => {
                if (err) {
                    reject(err);
                    return;
                }
                
                if (row) {
                    console.log('⚠️  Test user already exists');
                    console.log('');
                    console.log('✅ Test User Credentials (EXISTING):');
                    console.log('   Email:    test@psdepot.com');
                    console.log('   Password: TestPass123!');
                    console.log('');
                    resolve();
                    return;
                }

                // Create test user
                const userId = generateUUID();
                const passwordHash = hashPassword(TEST_USER.password);
                
                db.run(`
                    INSERT INTO users (id, email, password_hash, first_name, last_name, company, email_verified)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                `, [userId, TEST_USER.email, passwordHash, TEST_USER.firstName, TEST_USER.lastName, TEST_USER.company, 1], function(err) {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    console.log('✅ Test user created successfully!');
                    console.log('');
                    console.log('═══════════════════════════════════════════');
                    console.log('           TEST USER CREDENTIALS           ');
                    console.log('═══════════════════════════════════════════');
                    console.log('');
                    console.log('   📧 Email:    test@psdepot.com');
                    console.log('   🔑 Password: TestPass123!');
                    console.log('   🏢 Company:  Performance Supply Depot');
                    console.log('');
                    console.log('═══════════════════════════════════════════');
                    console.log('');
                    console.log('📝 Login URL: https://psdepot.com/appointments/web/login.html');
                    console.log('');
                    resolve();
                });
            });
        });
    });
    
    await new Promise(resolve => setTimeout(resolve, 100));
}

// Also create a "backdoor" admin user for development
async function createAdminUser() {
    const db = new sqlite3.Database(DB_PATH);
    
    const ADMIN_USER = {
        email: 'admin@psdepot.com',
        password: 'AdminPass456!',
        firstName: 'Admin',
        lastName: 'User',
        company: 'Performance Supply Depot'
    };
    
    return new Promise((resolve, reject) => {
        db.get('SELECT id FROM users WHERE email = ?', [ADMIN_USER.email], (err, row) => {
            if (err) {
                reject(err);
                return;
            }
            
            if (row) {
                console.log('⚠️  Admin user already exists');
                resolve();
                return;
            }

            const userId = generateUUID();
            const passwordHash = hashPassword(ADMIN_USER.password);
            
            db.run(`
                INSERT INTO users (id, email, password_hash, first_name, last_name, company, email_verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            `, [userId, ADMIN_USER.email, passwordHash, ADMIN_USER.firstName, ADMIN_USER.lastName, ADMIN_USER.company, 1], function(err) {
                if (err) {
                    reject(err);
                    return;
                }
                
                console.log('✅ Admin user created successfully!');
                console.log('');
                console.log('═══════════════════════════════════════════');
                console.log('           ADMIN USER CREDENTIALS          ');
                console.log('═══════════════════════════════════════════');
                console.log('');
                console.log('   📧 Email:    admin@psdepot.com');
                console.log('   🔑 Password: AdminPass456!');
                console.log('   🏢 Company:  Performance Supply Depot');
                console.log('');
                console.log('═══════════════════════════════════════════');
                resolve();
            });
        });
    });
}

createTestUser()
    .then(() => createAdminUser())
    .then(() => {
        console.log('');
        console.log('🎉 All test users created!');
        console.log('');
        console.log('💡 To start the auth server, run:');
        console.log('   cd /root/.openclaw/workspace/auth-system && npm start');
        process.exit(0);
    })
    .catch(err => {
        console.error('❌ Error:', err);
        process.exit(1);
    });
