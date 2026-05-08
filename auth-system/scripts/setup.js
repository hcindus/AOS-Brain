#!/usr/bin/env node

/**
 * Setup script for Secure Auth System
 * Creates necessary directories and generates secrets
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

console.log('🔐 Setting up Secure Auth System...\n');

// Create directories
const dirs = [
    './data',
    './logs',
    './uploads'
];

dirs.forEach(dir => {
    const fullPath = path.resolve(dir);
    if (!fs.existsSync(fullPath)) {
        fs.mkdirSync(fullPath, { recursive: true });
        console.log(`✅ Created directory: ${dir}`);
    }
});

// Check if .env exists
if (!fs.existsSync('.env')) {
    console.log('\n📝 Creating .env file...');
    
    const envContent = `# Database
DATABASE_URL=./data/auth.db

# JWT Secrets (KEEP THESE SECRET!)
JWT_ACCESS_SECRET=${crypto.randomBytes(32).toString('hex')}
JWT_REFRESH_SECRET=${crypto.randomBytes(32).toString('hex')}
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# Server
PORT=3000
NODE_ENV=development
FRONTEND_URL=http://localhost:8080

# Redis (optional - for production rate limiting)
# REDIS_URL=redis://localhost:6379

# Security
BCRYPT_PEPPER=${crypto.randomBytes(32).toString('hex')}
SESSION_TIMEOUT=900000
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=900000

# Email (for password reset)
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=
# SMTP_PASS=
# FROM_EMAIL=noreply@yourdomain.com

# Logging
LOG_LEVEL=info
AUDIT_LOG_PATH=./logs/audit.log
`;
    
    fs.writeFileSync('.env', envContent);
    console.log('✅ Created .env file with generated secrets');
    console.log('⚠️  IMPORTANT: Review and customize .env before production!');
} else {
    console.log('✅ .env file already exists');
}

console.log('\n🚀 Setup complete!');
console.log('\nNext steps:');
console.log('  1. npm install');
console.log('  2. Review .env configuration');
console.log('  3. npm run dev (or npm start for production)');
console.log('  4. Open http://localhost:3000');