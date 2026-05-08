/**
 * AuthAPI - Secure Authentication Client Library
 * Handles JWT tokens, CSRF protection, and API calls
 */

const API_BASE = window.location.origin.includes('localhost') 
    ? 'http://localhost:3000/api' 
    : '/api';

let csrfToken = null;

/**
 * Get or fetch CSRF token
 */
async function getCsrfToken() {
    if (!csrfToken) {
        const response = await fetch(`${API_BASE}/csrf-token`, {
            credentials: 'include'
        });
        const data = await response.json();
        csrfToken = data.csrfToken;
    }
    return csrfToken;
}

/**
 * Get device fingerprint
 */
function getDeviceFingerprint() {
    const data = [
        navigator.userAgent,
        navigator.language,
        screen.width + 'x' + screen.height,
        new Date().getTimezoneOffset()
    ].join('|');
    
    // Simple hash (not cryptographic, just for device grouping)
    let hash = 0;
    for (let i = 0; i < data.length; i++) {
        const char = data.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash).toString(16);
}

/**
 * Make authenticated API request
 */
async function apiRequest(endpoint, options = {}) {
    const token = await getCsrfToken();
    const accessToken = localStorage.getItem('accessToken');
    
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRF-Token': token,
        'X-Device-Fingerprint': getDeviceFingerprint(),
        ...options.headers
    };
    
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }
    
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers,
        credentials: 'include'
    });
    
    const data = await response.json();
    
    // Handle token expiration
    if (response.status === 403 && data.error?.includes('token')) {
        // Try to refresh
        const refreshed = await refreshToken();
        if (refreshed) {
            // Retry request
            return apiRequest(endpoint, options);
        } else {
            // Clear auth and redirect
            logout();
            window.location.href = '/index.html';
        }
    }
    
    return { success: response.ok, ...data };
}

/**
 * Refresh access token
 */
async function refreshToken() {
    try {
        const response = await fetch(`${API_BASE}/auth/refresh`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('accessToken', data.accessToken);
            localStorage.setItem('user', JSON.stringify(data.user));
            return true;
        }
    } catch (err) {
        console.error('Token refresh failed:', err);
    }
    return false;
}

/**
 * Auth API methods
 */
const AuthAPI = {
    /**
     * Register new user
     */
    async register({ email, password }) {
        return apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    },
    
    /**
     * Login user
     */
    async login({ email, password, mfaCode }) {
        return apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password, mfaCode })
        });
    },
    
    /**
     * Logout user
     */
    async logout() {
        const result = await apiRequest('/auth/logout', {
            method: 'POST'
        });
        
        // Clear local storage
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user');
        
        return result;
    },
    
    /**
     * Setup MFA
     */
    async setupMFA() {
        return apiRequest('/auth/mfa/setup', {
            method: 'POST'
        });
    },
    
    /**
     * Verify MFA and enable
     */
    async verifyMFA(code) {
        return apiRequest('/auth/mfa/verify', {
            method: 'POST',
            body: JSON.stringify({ code })
        });
    },
    
    /**
     * Request password reset
     */
    async requestPasswordReset(email) {
        return apiRequest('/auth/password-reset/request', {
            method: 'POST',
            body: JSON.stringify({ email })
        });
    },
    
    /**
     * Verify password reset token
     */
    async verifyResetToken(token) {
        return apiRequest('/auth/password-reset/verify', {
            method: 'POST',
            body: JSON.stringify({ token })
        });
    },
    
    /**
     * Confirm password reset
     */
    async confirmPasswordReset(token, newPassword) {
        return apiRequest('/auth/password-reset/confirm', {
            method: 'POST',
            body: JSON.stringify({ token, newPassword })
        });
    },
    
    /**
     * Get current user
     */
    getCurrentUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },
    
    /**
     * Check if authenticated
     */
    isAuthenticated() {
        return !!localStorage.getItem('accessToken');
    }
};

/**
 * Logout helper
 */
function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('user');
    window.location.href = '/index.html';
}

// Check authentication on protected pages
document.addEventListener('DOMContentLoaded', () => {
    // Pre-fetch CSRF token
    getCsrfToken().catch(console.error);
    
    // Auto-check auth on dashboard pages
    if (window.location.pathname.includes('dashboard') && !AuthAPI.isAuthenticated()) {
        window.location.href = '/index.html';
    }
    
    // Redirect logged-in users from login page
    if (window.location.pathname === '/index.html' && AuthAPI.isAuthenticated()) {
        window.location.href = '/dashboard.html';
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AuthAPI, logout };
}