const express = require('express');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const MicrosoftStrategy = require('passport-microsoft').Strategy;
const AppleStrategy = require('passport-apple');
const crypto = require('crypto');
const User = require('../../database/models/User');
const { generateAccessToken, generateRefreshToken } = require('../../utils/tokens');
const { logAuditEvent } = require('../../utils/audit');
const { generateDeviceFingerprint } = require('../../utils/crypto');

const router = express.Router();

// Social Auth Configuration
const SOCIAL_PROVIDERS = {
    google: {
        clientID: process.env.GOOGLE_CLIENT_ID,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET,
        callbackURL: '/api/auth/oauth/google/callback',
        scope: ['profile', 'email']
    },
    microsoft: {
        clientID: process.env.MICROSOFT_CLIENT_ID,
        clientSecret: process.env.MICROSOFT_CLIENT_SECRET,
        callbackURL: '/api/auth/oauth/microsoft/callback',
        scope: ['user.read', 'openid', 'profile', 'email']
    },
    apple: {
        clientID: process.env.APPLE_CLIENT_ID,
        teamID: process.env.APPLE_TEAM_ID,
        keyID: process.env.APPLE_KEY_ID,
        privateKeyLocation: process.env.APPLE_PRIVATE_KEY_PATH,
        callbackURL: '/api/auth/oauth/apple/callback'
    }
};

// Configure Passport Strategies
function configurePassport() {
    // Google OAuth
    if (SOCIAL_PROVIDERS.google.clientID) {
        passport.use(new GoogleStrategy({
            clientID: SOCIAL_PROVIDERS.google.clientID,
            clientSecret: SOCIAL_PROVIDERS.google.clientSecret,
            callbackURL: SOCIAL_PROVIDERS.google.callbackURL
        }, async (accessToken, refreshToken, profile, done) => {
            try {
                const result = await handleSocialAuth('google', profile);
                done(null, result);
            } catch (err) {
                done(err, null);
            }
        }));
    }

    // Microsoft OAuth
    if (SOCIAL_PROVIDERS.microsoft.clientID) {
        passport.use(new MicrosoftStrategy({
            clientID: SOCIAL_PROVIDERS.microsoft.clientID,
            clientSecret: SOCIAL_PROVIDERS.microsoft.clientSecret,
            callbackURL: SOCIAL_PROVIDERS.microsoft.callbackURL,
            scope: SOCIAL_PROVIDERS.microsoft.scope
        }, async (accessToken, refreshToken, profile, done) => {
            try {
                const result = await handleSocialAuth('microsoft', profile);
                done(null, result);
            } catch (err) {
                done(err, null);
            }
        }));
    }

    // Apple Sign In
    if (SOCIAL_PROVIDERS.apple.clientID) {
        passport.use(new AppleStrategy({
            clientID: SOCIAL_PROVIDERS.apple.clientID,
            teamID: SOCIAL_PROVIDERS.apple.teamID,
            keyID: SOCIAL_PROVIDERS.apple.keyID,
            privateKeyLocation: SOCIAL_PROVIDERS.apple.privateKeyLocation,
            callbackURL: SOCIAL_PROVIDERS.apple.callbackURL
        }, async (accessToken, refreshToken, profile, done) => {
            try {
                const result = await handleSocialAuth('apple', profile);
                done(null, result);
            } catch (err) {
                done(err, null);
            }
        }));
    }
}

// Handle Social Authentication
async function handleSocialAuth(provider, profile) {
    const email = profile.emails?.[0]?.value;
    if (!email) {
        throw new Error('Email not provided by OAuth provider');
    }

    // Check if user exists
    let user = await User.findByEmail(email);

    if (user) {
        // Link social account to existing user
        await User.linkSocialAccount(user.id, provider, profile.id);
        await logAuditEvent(user.id, 'SOCIAL_LOGIN', 'SUCCESS', null, { provider });
        return user;
    }

    // Create new user
    const userData = {
        email,
        first_name: profile.name?.givenName || profile.displayName?.split(' ')[0] || '',
        last_name: profile.name?.familyName || profile.displayName?.split(' ').slice(1).join(' ') || '',
        email_verified: true,
        provider,
        provider_id: profile.id
    };

    user = await User.createSocial(userData);
    await logAuditEvent(user.id, 'SOCIAL_REGISTER', 'SUCCESS', null, { provider });

    return user;
}

// Google OAuth Routes
router.get('/google',
    passport.authenticate('google', { scope: SOCIAL_PROVIDERS.google.scope })
);

router.get('/google/callback',
    passport.authenticate('google', { session: false, failureRedirect: '/login?error=social_auth_failed' }),
    async (req, res) => {
        try {
            const deviceFingerprint = generateDeviceFingerprint(req);
            const accessToken = generateAccessToken(req.user.id, req.user.email);
            const refreshToken = await generateRefreshToken(
                req.user.id,
                deviceFingerprint,
                req.ip,
                req.headers['user-agent']
            );

            // Redirect to frontend with tokens
            const redirectUrl = `${process.env.FRONTEND_URL}/oauth/callback?` +
                `accessToken=${encodeURIComponent(accessToken)}&` +
                `refreshToken=${encodeURIComponent(refreshToken)}`;

            res.redirect(redirectUrl);
        } catch (err) {
            console.error('OAuth callback error:', err);
            res.redirect('/login?error=oauth_callback_failed');
        }
    }
);

// Microsoft OAuth Routes
router.get('/microsoft',
    passport.authenticate('microsoft')
);

router.get('/microsoft/callback',
    passport.authenticate('microsoft', { session: false, failureRedirect: '/login?error=social_auth_failed' }),
    async (req, res) => {
        try {
            const deviceFingerprint = generateDeviceFingerprint(req);
            const accessToken = generateAccessToken(req.user.id, req.user.email);
            const refreshToken = await generateRefreshToken(
                req.user.id,
                deviceFingerprint,
                req.ip,
                req.headers['user-agent']
            );

            const redirectUrl = `${process.env.FRONTEND_URL}/oauth/callback?` +
                `accessToken=${encodeURIComponent(accessToken)}&` +
                `refreshToken=${encodeURIComponent(refreshToken)}`;

            res.redirect(redirectUrl);
        } catch (err) {
            console.error('OAuth callback error:', err);
            res.redirect('/login?error=oauth_callback_failed');
        }
    }
);

// Apple Sign In Routes
router.post('/apple',
    passport.authenticate('apple')
);

router.post('/apple/callback',
    passport.authenticate('apple', { session: false, failureRedirect: '/login?error=social_auth_failed' }),
    async (req, res) => {
        try {
            const deviceFingerprint = generateDeviceFingerprint(req);
            const accessToken = generateAccessToken(req.user.id, req.user.email);
            const refreshToken = await generateRefreshToken(
                req.user.id,
                deviceFingerprint,
                req.ip,
                req.headers['user-agent']
            );

            const redirectUrl = `${process.env.FRONTEND_URL}/oauth/callback?` +
                `accessToken=${encodeURIComponent(accessToken)}&` +
                `refreshToken=${encodeURIComponent(refreshToken)}`;

            res.redirect(redirectUrl);
        } catch (err) {
            console.error('OAuth callback error:', err);
            res.redirect('/login?error=oauth_callback_failed');
        }
    }
);

// Link/Unlink Social Accounts (for authenticated users)
router.post('/link/:provider',
    authenticateToken,
    async (req, res) => {
        try {
            const { provider } = req.params;
            const { providerId, email } = req.body;

            await User.linkSocialAccount(req.user.userId, provider, providerId);
            await logAuditEvent(req.user.userId, 'SOCIAL_LINK', 'SUCCESS', req, { provider });

            res.json({ success: true, message: `${provider} account linked successfully` });
        } catch (err) {
            console.error('Link social account error:', err);
            res.status(500).json({ error: 'Failed to link account' });
        }
    }
);

router.post('/unlink/:provider',
    authenticateToken,
    async (req, res) => {
        try {
            const { provider } = req.params;

            await User.unlinkSocialAccount(req.user.userId, provider);
            await logAuditEvent(req.user.userId, 'SOCIAL_UNLINK', 'SUCCESS', req, { provider });

            res.json({ success: true, message: `${provider} account unlinked successfully` });
        } catch (err) {
            console.error('Unlink social account error:', err);
            res.status(500).json({ error: 'Failed to unlink account' });
        }
    }
);

// Get user's linked social accounts
router.get('/accounts',
    authenticateToken,
    async (req, res) => {
        try {
            const accounts = await User.getSocialAccounts(req.user.userId);
            res.json({ accounts });
        } catch (err) {
            console.error('Get social accounts error:', err);
            res.status(500).json({ error: 'Failed to get social accounts' });
        }
    }
);

// Initialize passport
configurePassport();

module.exports = router;
