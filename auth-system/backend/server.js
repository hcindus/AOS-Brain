require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const cookieParser = require('cookie-parser');
const path = require('path');

const authRoutes = require('./routes/auth');
const passwordResetRoutes = require('./routes/password-reset');
const { setCsrfToken, apiLimiter } = require('./middleware/rateLimit');
const { securityHeaders } = require('./middleware/security');
const { csrfLimiter } = require('./middleware/additionalRateLimits');
const { initializeSecurityGuardian, securityStatusRoute, securityLoggingMiddleware } = require('./middleware/security-guardian');

const app = express();
const PORT = process.env.PORT || 3000;

// Security headers (custom + helmet)
app.use(securityHeaders);
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            scriptSrc: ["'self'"],
            imgSrc: ["'self'", "data:", "blob:"],
            connectSrc: ["'self'"],
            fontSrc: ["'self'"],
            objectSrc: ["'none'"],
            mediaSrc: ["'self'"],
            frameSrc: ["'none'"],
        },
    },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
    },
    referrerPolicy: { policy: 'strict-origin-when-cross-origin' }
}));

// CORS
app.use(cors({
    origin: process.env.FRONTEND_URL || 'http://localhost:8080',
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'X-CSRF-Token', 'X-Device-Fingerprint']
}));

// Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

// Security guardian logging
app.use(securityLoggingMiddleware);

// Rate limiting for all API routes
app.use('/api', apiLimiter);

// CSRF token endpoint (with rate limiting)
app.get('/api/csrf-token', csrfLimiter, setCsrfToken, (req, res) => {
    res.json({ csrfToken: req.cookies.csrfToken });
});

// API routes
app.use('/api/auth', authRoutes);
app.use('/api/auth', passwordResetRoutes);

// Security guardian status endpoint
app.get('/api/security/status', securityStatusRoute);

// Health check
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Serve static frontend files
app.use(express.static(path.join(__dirname, '../frontend')));

// SPA fallback
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// Error handler
app.use((err, req, res, next) => {
    console.error('Unhandled error:', err);
    res.status(500).json({ error: 'Internal server error' });
});

// Initialize security guardian and start server
async function startServer() {
    // Initialize Sentinel-Dusty Fusion
    await initializeSecurityGuardian();
    
    app.listen(PORT, () => {
        console.log(`🔐 Secure Auth Server running on port ${PORT}`);
        console.log(`🛡️  Sentinel-Dusty Fusion: ACTIVE`);
        console.log(`📁 Database: ${process.env.DATABASE_URL || './data/auth.db'}`);
        console.log(`🌐 Frontend: ${process.env.FRONTEND_URL || 'http://localhost:8080'}`);
    });
}

startServer().catch(err => {
    console.error('Failed to start server:', err);
    process.exit(1);
});

module.exports = app;