const rateLimit = require('express-rate-limit');
const Redis = require('ioredis');

// Simple in-memory store for development
const memoryStore = new Map();

// Redis client for production
let redis;
if (process.env.REDIS_URL) {
    redis = new Redis(process.env.REDIS_URL);
}

/**
 * Create rate limiter middleware
 */
function createRateLimiter(options = {}) {
    const {
        windowMs = 15 * 60 * 1000, // 15 minutes
        max = 5, // 5 requests per window
        message = 'Too many attempts, please try again later.',
        keyGenerator = (req) => req.ip
    } = options;

    return rateLimit({
        windowMs,
        max,
        message: { error: message },
        standardHeaders: true,
        legacyHeaders: false,
        keyGenerator,
        handler: (req, res) => {
            res.status(429).json({
                error: message,
                retryAfter: Math.ceil(windowMs / 1000)
            });
        }
    });
}

// Rate limiters for different endpoints
const loginLimiter = createRateLimiter({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // 5 attempts
    message: 'Too many login attempts. Please try again in 15 minutes.',
    keyGenerator: (req) => `login:${req.ip}:${req.body.email || 'unknown'}`
});

const registerLimiter = createRateLimiter({
    windowMs: 60 * 60 * 1000, // 1 hour
    max: 3, // 3 registrations per hour per IP
    message: 'Too many registration attempts. Please try again later.',
    keyGenerator: (req) => `register:${req.ip}`
});

const passwordResetLimiter = createRateLimiter({
    windowMs: 60 * 60 * 1000, // 1 hour
    max: 3, // 3 reset requests per hour
    message: 'Too many password reset attempts. Please try again later.',
    keyGenerator: (req) => `reset:${req.ip}`
});

const apiLimiter = createRateLimiter({
    windowMs: 60 * 1000, // 1 minute
    max: 100, // 100 requests per minute
    keyGenerator: (req) => `api:${req.ip}`
});

module.exports = {
    loginLimiter,
    registerLimiter,
    passwordResetLimiter,
    apiLimiter,
    createRateLimiter
};
