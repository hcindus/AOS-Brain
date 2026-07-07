/**
 * CRP - Cookie Consent Manager v1.0
 * Lightweight GDPR-compliant cookie banner for AGI Auth System
 */

(function() {
    'use strict';

    // Default config
    const CONFIG = {
        cookieName: 'crp_consent',
        cookieExpiry: 365, // days
        bannerPosition: 'bottom', // 'bottom' | 'top'
        theme: 'dark', // 'dark' | 'light'
        categories: [
            { id: 'necessary', label: 'Necessary', required: true, description: 'Essential for the site to function' },
            { id: 'analytics', label: 'Analytics', required: false, description: 'Helps us improve our website' },
            { id: 'marketing', label: 'Marketing', required: false, description: 'Used for personalized ads' }
        ]
    };

    // Consent state
    let consentState = null;

    /**
     * Get cookie value
     */
    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? decodeURIComponent(match[2]) : null;
    }

    /**
     * Set cookie with security flags
     */
    function setCookie(name, value, days) {
        const expires = days 
            ? '; expires=' + new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString()
            : '';
        const secure = window.location.protocol === 'https:' ? '; Secure' : '';
        document.cookie = `${name}=${encodeURIComponent(value)}${expires}; path=/; SameSite=Lax${secure}`;
    }

    /**
     * Load consent from cookie
     */
    function loadConsent() {
        const saved = getCookie(CONFIG.cookieName);
        if (saved) {
            try {
                consentState = JSON.parse(saved);
                return true;
            } catch (e) {
                console.warn('CRP: Invalid consent cookie');
            }
        }
        return false;
    }

    /**
     * Save consent to cookie and log to backend
     */
    function saveConsent(choices, action = 'custom') {
        consentState = {
            version: '1.0',
            timestamp: new Date().toISOString(),
            choices: choices
        };
        setCookie(CONFIG.cookieName, JSON.stringify(consentState), CONFIG.cookieExpiry);
        
        // Dispatch event for other scripts
        window.dispatchEvent(new CustomEvent('crpConsentUpdated', { detail: consentState }));
        
        // Log to backend (fire-and-forget)
        logConsentToBackend(choices, action);
    }
    
    /**
     * Log consent change to backend API
     */
    function logConsentToBackend(choices, action) {
        const payload = {
            version: '1.0',
            timestamp: new Date().toISOString(),
            choices: choices,
            action: action,
            userAgent: navigator.userAgent
        };
        
        fetch('/api/consent/log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        }).catch(err => {
            // Silent fail - consent still saved locally
            console.warn('CRP: Failed to log consent to backend', err);
        });
    }

    /**
     * Check if category is allowed
     */
    function isAllowed(category) {
        if (!consentState) return false;
        if (category === 'necessary') return true;
        return consentState.choices[category] === true;
    }

    /**
     * Create banner HTML
     */
    function createBanner() {
        const existing = document.getElementById('crp-banner');
        if (existing) existing.remove();

        const banner = document.createElement('div');
        banner.id = 'crp-banner';
        banner.className = `crp-banner crp-${CONFIG.bannerPosition} crp-${CONFIG.theme}`;
        banner.setAttribute('role', 'dialog');
        banner.setAttribute('aria-label', 'Cookie consent');

        const categoriesHtml = CONFIG.categories.map(cat => `
            <label class="crp-category">
                <input type="checkbox" 
                       name="crp-${cat.id}" 
                       ${cat.required ? 'checked disabled' : ''}
                       ${cat.required ? '' : 'class="crp-cat-checkbox" data-category="' + cat.id + '"'}
                >
                <span class="crp-cat-label">
                    ${cat.label}
                    ${cat.required ? '<span class="crp-required">(required)</span>' : ''}
                </span>
                <span class="crp-cat-desc">${cat.description}</span>
            </label>
        `).join('');

        banner.innerHTML = `
            <div class="crp-content">
                <div class="crp-text">
                    <h3>🍪 Cookie Preferences</h3>
                    <p>We use cookies to enhance your experience. Necessary cookies are always active. 
                       You can choose which other cookies to accept.</p>
                </div>
                <div class="crp-categories">
                    ${categoriesHtml}
                </div>
                <div class="crp-actions">
                    <button class="crp-btn crp-btn-secondary" id="crp-reject">
                        Reject All
                    </button>
                    <button class="crp-btn crp-btn-secondary" id="crp-customize">
                        Customize
                    </button>
                    <button class="crp-btn crp-btn-primary" id="crp-accept">
                        Accept All
                    </button>
                </div>
            </div>
        `;

        // Insert into DOM
        document.body.appendChild(banner);

        // Bind events
        banner.querySelector('#crp-accept').addEventListener('click', () => acceptAll());
        banner.querySelector('#crp-reject').addEventListener('click', () => rejectAll());
        banner.querySelector('#crp-customize').addEventListener('click', () => toggleCustomize());

        // Animate in
        requestAnimationFrame(() => {
            banner.classList.add('crp-visible');
        });
    }

    /**
     * Accept all cookies
     */
    function acceptAll() {
        const choices = {};
        CONFIG.categories.forEach(cat => {
            choices[cat.id] = true;
        });
        saveConsent(choices, 'accept_all');
        hideBanner();
    }

    /**
     * Reject non-essential cookies
     */
    function rejectAll() {
        const choices = {};
        CONFIG.categories.forEach(cat => {
            choices[cat.id] = cat.required;
        });
        saveConsent(choices, 'reject_all');
        hideBanner();
    }

    /**
     * Toggle customize view
     */
    function toggleCustomize() {
        const banner = document.getElementById('crp-banner');
        banner.classList.toggle('crp-customize');
        
        // Update button text
        const btn = banner.querySelector('#crp-customize');
        btn.textContent = banner.classList.contains('crp-customize') ? 'Save Preferences' : 'Customize';
        
        if (!banner.classList.contains('crp-customize')) {
            // Save custom selections
            const choices = {};
            banner.querySelectorAll('.crp-cat-checkbox').forEach(cb => {
                choices[cb.dataset.category] = cb.checked;
            });
            // Always include necessary
            choices.necessary = true;
            saveConsent(choices, 'custom');
            hideBanner();
        }
    }

    /**
     * Hide banner with animation
     */
    function hideBanner() {
        const banner = document.getElementById('crp-banner');
        if (banner) {
            banner.classList.remove('crp-visible');
            setTimeout(() => banner.remove(), 300);
        }
    }

    /**
     * Show banner
     */
    function showBanner() {
        if (!consentState) {
            createBanner();
        }
    }

    /**
     * Re-open consent manager
     */
    function reopen() {
        consentState = null;
        document.cookie = `${CONFIG.cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
        createBanner();
    }

    /**
     * Get current consent status
     */
    function getConsent() {
        return consentState;
    }

    /**
     * Initialize
     */
    function init(options = {}) {
        Object.assign(CONFIG, options);
        
        // Inject styles if not present
        if (!document.getElementById('crp-styles')) {
            injectStyles();
        }

        // Check for existing consent
        if (!loadConsent()) {
            // Show banner after short delay
            setTimeout(showBanner, 500);
        }

        // Expose API
        window.CRP = {
            isAllowed,
            getConsent,
            reopen,
            version: '1.0'
        };
    }

    /**
     * Inject CSS styles
     */
    function injectStyles() {
        const css = document.createElement('style');
        css.id = 'crp-styles';
        css.textContent = `
            /* CRP Cookie Consent Styles */
            #crp-banner {
                position: fixed;
                left: 0;
                right: 0;
                z-index: 999999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                transform: translateY(100%);
                opacity: 0;
                transition: transform 0.3s ease, opacity 0.3s ease;
            }

            #crp-banner.crp-visible {
                transform: translateY(0);
                opacity: 1;
            }

            #crp-banner.crp-bottom {
                bottom: 0;
            }

            #crp-banner.crp-top {
                top: 0;
            }

            /* Dark theme (default) */
            #crp-banner.crp-dark {
                background: rgba(30, 30, 40, 0.95);
                backdrop-filter: blur(10px);
                color: #fff;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }

            #crp-banner.crp-dark .crp-btn-primary {
                background: #6366f1;
                color: white;
            }

            #crp-banner.crp-dark .crp-btn-secondary {
                background: rgba(255, 255, 255, 0.1);
                color: #fff;
            }

            /* Light theme */
            #crp-banner.crp-light {
                background: rgba(255, 255, 255, 0.98);
                color: #1f2937;
                border-top: 1px solid #e5e7eb;
                box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
            }

            #crp-banner.crp-light .crp-btn-primary {
                background: #6366f1;
                color: white;
            }

            #crp-banner.crp-light .crp-btn-secondary {
                background: #f3f4f6;
                color: #374151;
            }

            .crp-content {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }

            .crp-text h3 {
                margin: 0 0 10px 0;
                font-size: 1.2rem;
            }

            .crp-text p {
                margin: 0;
                opacity: 0.8;
                font-size: 0.95rem;
                line-height: 1.5;
            }

            .crp-categories {
                display: none;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }

            #crp-banner.crp-customize .crp-categories {
                display: grid;
            }

            .crp-category {
                display: flex;
                flex-direction: column;
                gap: 5px;
                padding: 15px;
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.05);
                cursor: pointer;
                transition: background 0.2s;
            }

            .crp-dark .crp-category:hover {
                background: rgba(255, 255, 255, 0.1);
            }

            .crp-light .crp-category {
                background: #f9fafb;
                border: 1px solid #e5e7eb;
            }

            .crp-category input[type="checkbox"] {
                width: 18px;
                height: 18px;
                margin: 0;
                accent-color: #6366f1;
            }

            .crp-cat-label {
                display: flex;
                align-items: center;
                gap: 8px;
                font-weight: 500;
            }

            .crp-required {
                font-size: 0.75rem;
                opacity: 0.6;
                font-weight: normal;
            }

            .crp-cat-desc {
                font-size: 0.85rem;
                opacity: 0.7;
                margin-left: 26px;
            }

            .crp-actions {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-top: 20px;
            }

            .crp-btn {
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                font-size: 0.95rem;
                font-weight: 500;
                cursor: pointer;
                transition: transform 0.1s, opacity 0.2s;
            }

            .crp-btn:hover {
                transform: translateY(-1px);
                opacity: 0.9;
            }

            .crp-btn:active {
                transform: translateY(0);
            }

            .crp-btn-primary {
                margin-left: auto;
            }

            /* Mobile responsive */
            @media (max-width: 640px) {
                .crp-content {
                    padding: 15px;
                }

                .crp-actions {
                    flex-direction: column;
                }

                .crp-btn {
                    width: 100%;
                }

                .crp-btn-primary {
                    margin-left: 0;
                    order: -1;
                }
            }
        `;
        document.head.appendChild(css);
    }

    // Auto-init when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => init());
    } else {
        init();
    }
})();
