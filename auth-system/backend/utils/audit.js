const db = require('../../database/db');

/**
 * Log authentication event
 */
async function logAuditEvent(userId, action, status, req, metadata = {}) {
    const deviceFingerprint = req.headers['x-device-fingerprint'] || null;
    
    return new Promise((resolve, reject) => {
        db.run(
            `INSERT INTO audit_logs (user_id, action, status, ip_address, user_agent, device_fingerprint, metadata)
             VALUES (?, ?, ?, ?, ?, ?, ?)`,
            [
                userId || null,
                action,
                status,
                req.ip,
                req.headers['user-agent'] || null,
                deviceFingerprint,
                JSON.stringify(metadata)
            ],
            (err) => {
                if (err) {
                    console.error('Audit log error:', err);
                    reject(err);
                } else {
                    resolve();
                }
            }
        );
    });
}

/**
 * Get user's recent audit logs
 */
async function getUserAuditLogs(userId, limit = 50) {
    return new Promise((resolve, reject) => {
        db.all(
            `SELECT action, status, ip_address, created_at, metadata
             FROM audit_logs
             WHERE user_id = ?
             ORDER BY created_at DESC
             LIMIT ?`,
            [userId, limit],
            (err, rows) => {
                if (err) reject(err);
                else resolve(rows.map(row => ({
                    ...row,
                    metadata: row.metadata ? JSON.parse(row.metadata) : null
                })));
            }
        );
    });
}

/**
 * Detect suspicious activity
 */
async function detectSuspiciousActivity(userId, action, req) {
    const ip = req.ip;
    const deviceFingerprint = req.headers['x-device-fingerprint'];
    
    return new Promise((resolve, reject) => {
        // Get recent successful logins
        db.all(
            `SELECT DISTINCT ip_address, device_fingerprint
             FROM audit_logs
             WHERE user_id = ? AND action = 'LOGIN' AND status = 'SUCCESS'
             AND created_at > datetime('now', '-30 days')`,
            [userId],
            (err, rows) => {
                if (err) {
                    reject(err);
                    return;
                }
                
                const knownIPs = new Set(rows.map(r => r.ip_address));
                const knownDevices = new Set(rows.map(r => r.device_fingerprint).filter(Boolean));
                
                const alerts = [];
                
                // New IP check
                if (knownIPs.size > 0 && !knownIPs.has(ip)) {
                    alerts.push('NEW_IP');
                }
                
                // New device check
                if (knownDevices.size > 0 && deviceFingerprint && !knownDevices.has(deviceFingerprint)) {
                    alerts.push('NEW_DEVICE');
                }
                
                resolve(alerts);
            }
        );
    });
}

module.exports = {
    logAuditEvent,
    getUserAuditLogs,
    detectSuspiciousActivity
};