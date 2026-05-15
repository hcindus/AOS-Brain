const express = require('express');
const { body, validationResult } = require('express-validator');
const db = require('../../database/db');
const User = require('../../database/models/User');
const { hashPassword, generateSecureToken, hashToken } = require('../utils/crypto');
const { logAuditEvent } = require('../utils/audit');
const { revokeAllUserSessions } = require('../utils/tokens');
const { passwordResetLimiter } = require('../middleware/rateLimit');
const { csrfProtection } = require('../middleware/auth');
const { sendPasswordResetEmail } = require('../utils/email');

const router = express.Router();

/**
 * POST /api/auth/password-reset/request
 * Request password reset (sends email with token)
 */
router.post('/password-reset/request',
    passwordResetLimiter,
    csrfProtection,
    [body('email').isEmail().normalizeEmail()],
    async (req, res) => {
        try {
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({ errors: errors.array() });
            }

            const { email } = req.body;
            const user = await User.findByEmail(email);

            // Don't reveal if user exists
            if (!user) {
                await logAuditEvent(null, 'PASSWORD_RESET_REQUEST', 'FAILED', req, { 
                    reason: 'user_not_found', 
                    email 
                });
                return res.json({ 
                    message: 'If an account exists with this email, a reset link has been sent.' 
                });
            }

            // Generate secure token
            const token = generateSecureToken(32);
            const tokenHash = hashToken(token);
            const expiresAt = new Date(Date.now() + 60 * 60 * 1000); // 1 hour
            
            const resetId = generateSecureToken(16);

            // Store token hash in database
            await new Promise((resolve, reject) => {
                db.run(
                    `INSERT INTO password_resets (id, user_id, token_hash, expires_at)
                     VALUES (?, ?, ?, ?)`,
                    [resetId, user.id, tokenHash, expiresAt.toISOString()],
                    (err) => {
                        if (err) reject(err);
                        else resolve();
                    }
                );
            });

            // Send email
            const resetUrl = `${process.env.FRONTEND_URL || 'http://localhost:3000'}/reset-password.html?token=${token}`;
            
            try {
                const emailResult = await sendPasswordResetEmail(email, token, resetUrl);
                
                // In development, include preview URL and token
                if (emailResult.test) {
                    console.log('🔑 Reset token:', token);
                    return res.json({
                        message: 'If an account exists with this email, a reset link has been sent.',
                        devToken: token,
                        previewUrl: emailResult.previewUrl
                    });
                }
            } catch (emailErr) {
                console.error('Email send failed:', emailErr);
                // Still return success to prevent email enumeration
            }

            await logAuditEvent(user.id, 'PASSWORD_RESET_REQUEST', 'SUCCESS', req);

            res.json({
                message: 'If an account exists with this email, a reset link has been sent.'
            });
        } catch (err) {
            console.error('Password reset request error:', err);
            res.status(500).json({ error: 'Password reset request failed' });
        }
    }
);

/**
 * POST /api/auth/password-reset/verify
 * Verify reset token
 */
router.post('/password-reset/verify',
    csrfProtection,
    [body('token').isLength({ min: 32 })],
    async (req, res) => {
        try {
            const { token } = req.body;
            const tokenHash = hashToken(token);

            const resetRecord = await new Promise((resolve, reject) => {
                db.get(
                    `SELECT pr.*, u.email FROM password_resets pr
                     JOIN users u ON pr.user_id = u.id
                     WHERE pr.token_hash = ? AND pr.used_at IS NULL`,
                    [tokenHash],
                    (err, row) => {
                        if (err) reject(err);
                        else resolve(row);
                    }
                );
            });

            if (!resetRecord) {
                return res.status(400).json({ error: 'Invalid token' });
            }

            if (new Date(resetRecord.expires_at) < new Date()) {
                return res.status(400).json({ error: 'Token has expired' });
            }

            res.json({
                valid: true,
                email: resetRecord.email
            });
        } catch (err) {
            console.error('Token verification error:', err);
            res.status(500).json({ error: 'Token verification failed' });
        }
    }
);

/**
 * POST /api/auth/password-reset/confirm
 * Confirm password reset with new password
 */
router.post('/password-reset/confirm',
    passwordResetLimiter,
    csrfProtection,
    [
        body('token').isLength({ min: 32 }),
        body('newPassword').isLength({ min: 8 })
    ],
    async (req, res) => {
        try {
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({ errors: errors.array() });
            }

            const { token, newPassword } = req.body;
            const tokenHash = hashToken(token);

            // Get reset record
            const resetRecord = await new Promise((resolve, reject) => {
                db.get(
                    `SELECT pr.*, u.id as user_id, u.email FROM password_resets pr
                     JOIN users u ON pr.user_id = u.id
                     WHERE pr.token_hash = ? AND pr.used_at IS NULL`,
                    [tokenHash],
                    (err, row) => {
                        if (err) reject(err);
                        else resolve(row);
                    }
                );
            });

            if (!resetRecord) {
                await logAuditEvent(null, 'PASSWORD_RESET_CONFIRM', 'FAILED', req, { 
                    reason: 'invalid_token' 
                });
                return res.status(400).json({ error: 'Invalid token' });
            }

            if (new Date(resetRecord.expires_at) < new Date()) {
                await logAuditEvent(resetRecord.user_id, 'PASSWORD_RESET_CONFIRM', 'FAILED', req, { 
                    reason: 'expired_token' 
                });
                return res.status(400).json({ error: 'Token has expired' });
            }

            // Hash new password
            const passwordHash = await hashPassword(newPassword);

            // Update password
            await User.updatePassword(resetRecord.user_id, passwordHash);

            // Mark token as used
            await new Promise((resolve, reject) => {
                db.run(
                    'UPDATE password_resets SET used_at = CURRENT_TIMESTAMP WHERE id = ?',
                    [resetRecord.id],
                    (err) => {
                        if (err) reject(err);
                        else resolve();
                    }
                );
            });

            // Revoke all sessions for security
            await revokeAllUserSessions(resetRecord.user_id);

            await logAuditEvent(resetRecord.user_id, 'PASSWORD_RESET_CONFIRM', 'SUCCESS', req);

            res.json({ 
                message: 'Password reset successful. Please log in with your new password.' 
            });
        } catch (err) {
            console.error('Password reset confirm error:', err);
            res.status(500).json({ error: 'Password reset failed' });
        }
    }
);

module.exports = router;