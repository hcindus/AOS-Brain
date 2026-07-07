/**
 * CRP Consent API Routes
 * GDPR-compliant cookie consent logging
 */

const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');
const { logAuditEvent } = require('../utils/audit');

/**
 * POST /api/consent/log
 * Log consent change from client
 * Public endpoint - no auth required
 */
router.post('/log', async (req, res) => {
    try {
        const { 
            version, 
            timestamp, 
            choices, 
            action, // 'accept_all', 'reject_all', 'custom'
            userAgent 
        } = req.body;

        // Validate required fields
        if (!version || !timestamp || !choices) {
            return res.status(400).json({ 
                error: 'Missing required consent data' 
            });
        }

        // Build consent summary
        const consentedCategories = Object.entries(choices)
            .filter(([_, value]) => value)
            .map(([key, _]) => key)
            .join(',');

        // Log to audit system
        await logAuditEvent(
            null, // No user ID for anonymous
            'COOKIE_CONSENT',
            action?.toUpperCase() || 'UPDATE',
            req,
            {
                version,
                timestamp,
                consentedCategories,
                choices: JSON.stringify(choices),
                userAgent: userAgent || req.headers['user-agent']
            }
        );

        res.json({ 
            success: true,
            message: 'Consent logged'
        });

    } catch (err) {
        console.error('Consent logging error:', err);
        res.status(500).json({ 
            error: 'Failed to log consent' 
        });
    }
});

/**
 * GET /api/consent/status
 * Get current user's consent status
 * Requires authentication
 */
router.get('/status', authenticateToken, async (req, res) => {
    try {
        // Return placeholder - actual consent stored in client cookie
        // This endpoint can be extended to sync with DB if needed
        res.json({
            message: 'Consent stored client-side',
            hint: 'Check localStorage/cookies for CRP_consent'
        });
    } catch (err) {
        res.status(500).json({ error: 'Failed to get consent status' });
    }
});

/**
 * POST /api/consent/withdraw
 * Handle consent withdrawal
 * Requires authentication
 */
router.post('/withdraw', authenticateToken, async (req, res) => {
    try {
        await logAuditEvent(
            req.userId,
            'COOKIE_CONSENT',
            'WITHDRAWN',
            req,
            { reason: 'User requested full withdrawal' }
        );

        res.json({ 
            success: true,
            message: 'Consent withdrawal logged',
            action: 'Please clear your cookies to complete withdrawal'
        });
    } catch (err) {
        res.status(500).json({ error: 'Failed to process withdrawal' });
    }
});

module.exports = router;
