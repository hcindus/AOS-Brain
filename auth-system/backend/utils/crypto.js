const argon2 = require('argon2');
const crypto = require('crypto');

// Argon2id configuration (NIST recommended)
const ARGON2_CONFIG = {
    type: argon2.argon2id,
    memoryCost: 19456, // 19 MiB
    timeCost: 2,       // 2 iterations
    parallelism: 1,    // 1 parallel thread
    hashLength: 32     // 256 bits
};

/**
 * Hash password with Argon2id + pepper
 */
async function hashPassword(password) {
    const pepper = process.env.BCRYPT_PEPPER || '';
    const pepperedPassword = password + pepper;
    return await argon2.hash(pepperedPassword, ARGON2_CONFIG);
}

/**
 * Verify password against hash
 */
async function verifyPassword(password, hash) {
    try {
        const pepper = process.env.BCRYPT_PEPPER || '';
        const pepperedPassword = password + pepper;
        return await argon2.verify(hash, pepperedPassword);
    } catch (err) {
        return false;
    }
}

/**
 * Generate cryptographically secure random token
 */
function generateSecureToken(length = 32) {
    return crypto.randomBytes(length).toString('hex');
}

/**
 * Generate device fingerprint from request
 */
function generateDeviceFingerprint(req) {
    const data = [
        req.headers['user-agent'] || '',
        req.headers['accept-language'] || '',
        req.headers['accept-encoding'] || '',
        req.ip
    ].join('|');
    
    return crypto.createHash('sha256').update(data).digest('hex');
}

/**
 * Hash a token for database storage (for password reset, etc.)
 */
function hashToken(token) {
    return crypto.createHash('sha256').update(token).digest('hex');
}

/**
 * Generate TOTP backup codes
 */
function generateBackupCodes(count = 10) {
    const codes = [];
    for (let i = 0; i < count; i++) {
        codes.push(crypto.randomBytes(4).toString('hex').toUpperCase());
    }
    return codes;
}

module.exports = {
    hashPassword,
    verifyPassword,
    generateSecureToken,
    generateDeviceFingerprint,
    hashToken,
    generateBackupCodes
};