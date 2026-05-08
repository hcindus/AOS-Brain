const jwt = require('jsonwebtoken');
const db = require('../../database/db');
const { generateSecureToken } = require('./crypto');

const ACCESS_TOKEN_EXPIRY = process.env.JWT_ACCESS_EXPIRY || '15m';
const REFRESH_TOKEN_EXPIRY = process.env.JWT_REFRESH_EXPIRY || '7d';

/**
 * Generate access token (short-lived)
 */
function generateAccessToken(userId, email) {
    return jwt.sign(
        { userId, email, type: 'access' },
        process.env.JWT_ACCESS_SECRET,
        { expiresIn: ACCESS_TOKEN_EXPIRY }
    );
}

/**
 * Generate refresh token (long-lived, stored in DB)
 */
async function generateRefreshToken(userId, deviceFingerprint, ipAddress, userAgent) {
    const token = generateSecureToken(64);
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 7); // 7 days
    
    const sessionId = generateSecureToken(32);
    
    return new Promise((resolve, reject) => {
        db.run(
            `INSERT INTO sessions (id, user_id, refresh_token, device_fingerprint, ip_address, user_agent, expires_at)
             VALUES (?, ?, ?, ?, ?, ?, ?)`,
            [sessionId, userId, token, deviceFingerprint, ipAddress, userAgent, expiresAt.toISOString()],
            (err) => {
                if (err) reject(err);
                else resolve(token);
            }
        );
    });
}

/**
 * Verify access token
 */
function verifyAccessToken(token) {
    try {
        return jwt.verify(token, process.env.JWT_ACCESS_SECRET);
    } catch (err) {
        return null;
    }
}

/**
 * Verify refresh token from database
 */
async function verifyRefreshToken(token, deviceFingerprint) {
    return new Promise((resolve, reject) => {
        db.get(
            `SELECT s.*, u.email, u.mfa_enabled 
             FROM sessions s
             JOIN users u ON s.user_id = u.id
             WHERE s.refresh_token = ? AND s.revoked_at IS NULL`,
            [token],
            (err, row) => {
                if (err) {
                    reject(err);
                    return;
                }
                
                if (!row) {
                    resolve(null);
                    return;
                }
                
                // Check expiration
                if (new Date(row.expires_at) < new Date()) {
                    resolve(null);
                    return;
                }
                
                // Optional: verify device fingerprint matches
                if (deviceFingerprint && row.device_fingerprint !== deviceFingerprint) {
                    // Log suspicious activity
                    console.warn('Device fingerprint mismatch for refresh token');
                }
                
                resolve({
                    userId: row.user_id,
                    email: row.email,
                    mfaEnabled: row.mfa_enabled,
                    sessionId: row.id
                });
            }
        );
    });
}

/**
 * Revoke a refresh token
 */
async function revokeRefreshToken(token) {
    return new Promise((resolve, reject) => {
        db.run(
            'UPDATE sessions SET revoked_at = CURRENT_TIMESTAMP WHERE refresh_token = ?',
            [token],
            (err) => {
                if (err) reject(err);
                else resolve();
            }
        );
    });
}

/**
 * Revoke all user sessions
 */
async function revokeAllUserSessions(userId) {
    return new Promise((resolve, reject) => {
        db.run(
            'UPDATE sessions SET revoked_at = CURRENT_TIMESTAMP WHERE user_id = ? AND revoked_at IS NULL',
            [userId],
            (err) => {
                if (err) reject(err);
                else resolve();
            }
        );
    });
}

module.exports = {
    generateAccessToken,
    generateRefreshToken,
    verifyAccessToken,
    verifyRefreshToken,
    revokeRefreshToken,
    revokeAllUserSessions
};