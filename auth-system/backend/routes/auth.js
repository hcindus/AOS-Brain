const express = require('express');
const { body, validationResult } = require('express-validator');
const speakeasy = require('speakeasy');
const QRCode = require('qrcode');
const User = require('../../database/models/User');
const { hashPassword, verifyPassword, generateSecureToken, generateDeviceFingerprint, hashToken } = require('../utils/crypto');
const { generateAccessToken, generateRefreshToken, revokeRefreshToken, revokeAllUserSessions } = require('../utils/tokens');
const { logAuditEvent, detectSuspiciousActivity } = require('../utils/audit');
const { checkPasswordBreach } = require('../utils/breachCheck');
const { loginLimiter, registerLimiter, passwordResetLimiter } = require('../middleware/rateLimit');
const { refreshLimiter } = require('../middleware/additionalRateLimits');
const { authenticateToken, authenticateRefreshToken, csrfProtection } = require('../middleware/auth');
const { sendWelcomeEmail, sendSecurityAlert } = require('../utils/email');

const router = express.Router();

/**
 * POST /api/auth/register
 * Register new user with password breach checking
 */
router.post('/register',
    registerLimiter,
    csrfProtection,
    [
        body('email').isEmail().normalizeEmail(),
        body('password')
            .isLength({ min: 8, max: 128 })
            .withMessage('Password must be between 8 and 128 characters')
    ],
    async (req, res) => {
        try {
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({ errors: errors.array() });
            }

            const { email, password } = req.body;

            // Check if user exists
            const existingUser = await User.findByEmail(email);
            if (existingUser) {
                await logAuditEvent(null, 'REGISTER', 'FAILED', req, { reason: 'email_exists', email });
                return res.status(409).json({ error: 'Email already registered' });
            }

            // Check password against breach database
            const breachCheck = await checkPasswordBreach(password);
            if (breachCheck.breached) {
                await logAuditEvent(null, 'REGISTER', 'FAILED', req, { 
                    reason: 'breached_password', 
                    email,
                    breachCount: breachCheck.count 
                });
                return res.status(400).json({ 
                    error: 'This password has been compromised. Please choose a different password.',
                    breachCount: breachCheck.count
                });
            }

            // Hash password with Argon2id
            const passwordHash = await hashPassword(password);

            // Create user
            const user = await User.create(email, passwordHash);

            await logAuditEvent(user.id, 'REGISTER', 'SUCCESS', req, { email });

            res.status(201).json({
                message: 'Registration successful. Please check your email to verify your account.',
                userId: user.id
            });
        } catch (err) {
            console.error('Registration error:', err);
            res.status(500).json({ error: 'Registration failed' });
        }
    }
);

/**
 * POST /api/auth/login
 * Login with rate limiting and MFA support
 */
router.post('/login',
    loginLimiter,
    csrfProtection,
    [
        body('email').isEmail().normalizeEmail(),
        body('password')
            .isLength({ min: 1, max: 128 })
            .withMessage('Invalid credentials')
    ],
    async (req, res) => {
        try {
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({ errors: errors.array() });
            }

            const { email, password, mfaCode } = req.body;
            const deviceFingerprint = generateDeviceFingerprint(req);

            // Find user
            const user = await User.findByEmail(email);
            if (!user) {
                await logAuditEvent(null, 'LOGIN', 'FAILED', req, { reason: 'user_not_found', email });
                return res.status(401).json({ error: 'Invalid credentials' });
            }

            // Check if account is locked
            if (user.locked_until && new Date(user.locked_until) > new Date()) {
                const minutesLeft = Math.ceil((new Date(user.locked_until) - Date.now()) / 60000);
                await logAuditEvent(user.id, 'LOGIN', 'FAILED', req, { reason: 'account_locked' });
                return res.status(403).json({ 
                    error: `Account locked. Try again in ${minutesLeft} minutes.` 
                });
            }

            // Verify password
            const validPassword = await verifyPassword(password, user.password_hash);
            if (!validPassword) {
                await User.incrementFailedAttempts(user.id);
                
                // Lock account after 5 failed attempts
                if (user.failed_attempts >= 4) {
                    await User.lockAccount(user.id, 15);
                    await logAuditEvent(user.id, 'LOGIN', 'FAILED', req, { reason: 'account_locked' });
                    return res.status(403).json({ 
                        error: 'Account locked due to too many failed attempts. Try again in 15 minutes.' 
                    });
                }

                await logAuditEvent(user.id, 'LOGIN', 'FAILED', req, { reason: 'invalid_password' });
                return res.status(401).json({ error: 'Invalid credentials' });
            }

            // Check MFA if enabled
            if (user.mfa_enabled) {
                if (!mfaCode) {
                    return res.status(401).json({ 
                        error: 'MFA code required',
                        requiresMFA: true 
                    });
                }

                const verified = speakeasy.totp.verify({
                    secret: user.mfa_secret,
                    encoding: 'base32',
                    token: mfaCode,
                    window: 1 // Allow 30 second drift
                });

                if (!verified) {
                    await logAuditEvent(user.id, 'LOGIN', 'FAILED', req, { reason: 'invalid_mfa' });
                    return res.status(401).json({ error: 'Invalid MFA code' });
                }
            }

            // Reset failed attempts and update last login
            await User.resetFailedAttempts(user.id);

            // Generate tokens
            const accessToken = generateAccessToken(user.id, user.email);
            const refreshToken = await generateRefreshToken(
                user.id, 
                deviceFingerprint, 
                req.ip, 
                req.headers['user-agent']
            );

            // Check for suspicious activity
            const alerts = await detectSuspiciousActivity(user.id, 'LOGIN', req);
            if (alerts.length > 0) {
                console.warn(`Suspicious login detected for user ${user.id}:`, alerts);
            }

            await logAuditEvent(user.id, 'LOGIN', 'SUCCESS', req, { 
                mfaUsed: user.mfa_enabled,
                alerts 
            });

            // Set refresh token in httpOnly cookie
            res.cookie('refreshToken', refreshToken, {
                httpOnly: true,
                secure: process.env.NODE_ENV === 'production',
                sameSite: 'strict',
                maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
            });

            res.json({
                accessToken,
                user: {
                    id: user.id,
                    email: user.email,
                    mfaEnabled: user.mfa_enabled === 1
                },
                alerts: alerts.length > 0 ? alerts : undefined
            });
        } catch (err) {
            console.error('Login error:', err);
            res.status(500).json({ error: 'Login failed' });
        }
    }
);

/**
 * POST /api/auth/mfa/setup
 * Setup MFA (generate secret and QR code)
 */
router.post('/mfa/setup', authenticateToken, csrfProtection, async (req, res) => {
    try {
        const secret = speakeasy.generateSecret({
            name: `AGI Company (${req.userEmail})`,
            length: 32
        });

        // Store temporary secret (not enabled until verified)
        await User.updateMFA(req.userId, secret.base32, false);

        // Generate QR code
        const qrCodeUrl = await QRCode.toDataURL(secret.otpauth_url);

        await logAuditEvent(req.userId, 'MFA_SETUP', 'SUCCESS', req);

        res.json({
            // Never expose the raw secret - only QR code
            qrCode: qrCodeUrl,
            manualEntryKey: secret.base32.slice(0, 4) + '****...' // Show only first 4 chars
        });
    } catch (err) {
        console.error('MFA setup error:', err);
        res.status(500).json({ error: 'MFA setup failed' });
    }
});

/**
 * POST /api/auth/mfa/verify
 * Verify MFA code and enable MFA
 */
router.post('/mfa/verify', authenticateToken, csrfProtection, async (req, res) => {
    try {
        const { code } = req.body;
        const user = await User.findById(req.userId);

        if (!user || !user.mfa_secret) {
            return res.status(400).json({ error: 'MFA not set up' });
        }

        const verified = speakeasy.totp.verify({
            secret: user.mfa_secret,
            encoding: 'base32',
            token: code,
            window: 1
        });

        if (!verified) {
            return res.status(400).json({ error: 'Invalid verification code' });
        }

        // Enable MFA
        await User.updateMFA(req.userId, user.mfa_secret, true);

        await logAuditEvent(req.userId, 'MFA_ENABLE', 'SUCCESS', req);

        res.json({ message: 'MFA enabled successfully' });
    } catch (err) {
        console.error('MFA verify error:', err);
        res.status(500).json({ error: 'Verification failed' });
    }
});

/**
 * POST /api/auth/logout
 * Logout and revoke refresh token
 */
router.post('/logout', authenticateToken, async (req, res) => {
    try {
        const { refreshToken } = req.cookies;
        
        if (refreshToken) {
            await revokeRefreshToken(refreshToken);
        }

        res.clearCookie('refreshToken');
        
        await logAuditEvent(req.userId, 'LOGOUT', 'SUCCESS', req);
        
        res.json({ message: 'Logged out successfully' });
    } catch (err) {
        console.error('Logout error:', err);
        res.status(500).json({ error: 'Logout failed' });
    }
});

/**
 * POST /api/auth/refresh
 * Refresh access token
 */
router.post('/refresh', refreshLimiter, authenticateRefreshToken, async (req, res) => {
    try {
        // Revoke old refresh token
        await revokeRefreshToken(req.refreshToken);
        
        // Generate new tokens
        const accessToken = generateAccessToken(req.userId, req.userEmail);
        const deviceFingerprint = generateDeviceFingerprint(req);
        const newRefreshToken = await generateRefreshToken(
            req.userId,
            deviceFingerprint,
            req.ip,
            req.headers['user-agent']
        );

        await logAuditEvent(req.userId, 'TOKEN_REFRESH', 'SUCCESS', req);

        res.cookie('refreshToken', newRefreshToken, {
            httpOnly: true,
            secure: process.env.NODE_ENV === 'production',
            sameSite: 'strict',
            maxAge: 7 * 24 * 60 * 60 * 1000
        });

        res.json({
            accessToken,
            user: {
                id: req.userId,
                email: req.userEmail,
                mfaEnabled: req.mfaEnabled === 1
            }
        });
    } catch (err) {
        console.error('Token refresh error:', err);
        res.status(500).json({ error: 'Token refresh failed' });
    }
});

module.exports = router;