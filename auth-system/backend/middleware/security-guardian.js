/**
 * Security Guardian Integration
 * Integrates Sentinel-Dusty Fusion into the Auth System
 */

const SentinelDustyFusion = require('../../sentinel-dusty-fusion');

let guardian = null;

/**
 * Initialize the security guardian
 */
async function initializeSecurityGuardian() {
    if (guardian) {
        console.log('🛡️  Security Guardian already initialized');
        return guardian;
    }
    
    guardian = new SentinelDustyFusion();
    await guardian.initialize();
    
    // Expose API endpoint for security status
    console.log('🔗 Security Guardian integrated with Auth System');
    
    return guardian;
}

/**
 * Get the guardian instance
 */
function getGuardian() {
    return guardian;
}

/**
 * Middleware to log requests through guardian
 */
function securityLoggingMiddleware(req, res, next) {
    // Log sensitive actions through guardian
    if (req.path.includes('/auth/') && req.method !== 'GET') {
        // Guardian will pick this up in its real-time monitoring
        // This is a lightweight hook for future enhancements
    }
    next();
}

/**
 * Express route for security status
 */
function securityStatusRoute(req, res) {
    if (!guardian) {
        return res.status(503).json({ error: 'Security Guardian not initialized' });
    }
    
    const report = guardian.getSecurityReport();
    res.json(report);
}

/**
 * Graceful shutdown
 */
function shutdownSecurityGuardian() {
    if (guardian) {
        guardian.stop();
        guardian = null;
    }
}

module.exports = {
    initializeSecurityGuardian,
    getGuardian,
    securityLoggingMiddleware,
    securityStatusRoute,
    shutdownSecurityGuardian
};