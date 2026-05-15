const { verifyAccessToken, verifyRefreshToken, revokeRefreshToken } = require('../utils/tokens');
const { logAuditEvent } = require('../utils/audit');

/**
 * JWT authentication middleware
 */
async function authenticateToken(req, res, next) {
    try {
        const authHeader = req.headers['authorization'];
        const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
        
        if (!token) {
            return res.status(401).json({ error: 'Access token required' });
        }
        
        const decoded = verifyAccessToken(token);
        
        if (!decoded) {
            return res.status(403).json({ error: 'Invalid or expired access token' });
        }
        
        req.userId = decoded.userId;
        req.userEmail = decoded.email;
        next();
    } catch (err) {
        return res.status(403).json({ error: 'Authentication failed' });
    }
}

/**
 * Refresh token middleware
 */
async function authenticateRefreshToken(req, res, next) {
    try {
        const { refreshToken } = req.body;
        
        if (!refreshToken) {
            return res.status(401).json({ error: 'Refresh token required' });
        }
        
        const deviceFingerprint = req.headers['x-device-fingerprint'];
        const session = await verifyRefreshToken(refreshToken, deviceFingerprint);
        
        if (!session) {
            // Log suspicious token usage
            await logAuditEvent(null, 'TOKEN_REFRESH', 'FAILED', req, { reason: 'invalid_token' });
            return res.status(403).json({ error: 'Invalid or expired refresh token' });
        }
        
        req.userId = session.userId;
        req.userEmail = session.email;
        req.mfaEnabled = session.mfaEnabled;
        req.refreshToken = refreshToken;
        req.sessionId = session.sessionId;
        
        next();
    } catch (err) {
        return res.status(403).json({ error: 'Token verification failed' });
    }
}

/**
 * CSRF protection middleware
 * Uses double-submit cookie pattern
 */
function csrfProtection(req, res, next) {
    // Skip for GET, HEAD, OPTIONS
    if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
        return next();
    }
    
    const csrfToken = req.headers['x-csrf-token'];
    const csrfCookie = req.cookies?.csrfToken;
    
    if (!csrfToken || !csrfCookie || csrfToken !== csrfCookie) {
        return res.status(403).json({ error: 'CSRF token mismatch' });
    }
    
    next();
}

/**
 * Generate and set CSRF token cookie
 */
function setCsrfToken(req, res, next) {
    let token = req.cookies?.csrfToken;
    if (!token) {
        token = require('crypto').randomBytes(32).toString('hex');
        res.cookie('csrfToken', token, {
            httpOnly: false, // Must be accessible by JavaScript
            secure: process.env.NODE_ENV === 'production',
            sameSite: 'strict',
            maxAge: 24 * 60 * 60 * 1000 // 24 hours
        });
    }
    req.csrfToken = token;
    next();
}

module.exports = {
    authenticateToken,
    authenticateRefreshToken,
    csrfProtection,
    setCsrfToken
};