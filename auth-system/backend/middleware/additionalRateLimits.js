const rateLimit = require('express-rate-limit');

/**
 * Refresh token rate limiter
 * Prevents token refresh abuse and replay attacks
 */
const refreshLimiter = rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: 10, // 10 refresh attempts per minute per IP
    message: {
        error: 'Too many token refresh attempts. Please try again later.'
    },
    standardHeaders: true,
    legacyHeaders: false,
    keyGenerator: (req) => {
        // Also limit by refresh token to prevent token enumeration
        return req.ip + (req.body.refreshToken?.slice(0, 10) || '');
    }
});

/**
 * CSRF endpoint rate limiter
 */
const csrfLimiter = rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: 30, // 30 CSRF token requests per minute
    message: {
        error: 'Too many requests'
    }
});

module.exports = {
    refreshLimiter,
    csrfLimiter
};