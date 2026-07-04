/**
 * AGI CMP - Consent Management Platform
 * GDPR/CCPA compliant cookie consent with IAB TCF 2.2 support
 * @version 1.0.0
 */

(function(window) {
    'use strict';

    // Configuration
    const CONFIG = {
        version: '1.0.0',
        storageKey: 'agi_cmp_consent',
        tcfVersion: '2.2',
        cookieExpiry: 365, // days
        bannerDelay: 500, // ms
        apiEndpoint: '/api/consent',
    };

    // Consent Categories (TCF 2.2 aligned)
    const CATEGORIES = {
        essential: {
            id: 1,
            name: 'Essential',
            description: 'Required for the website to function properly',
            required: true,
            cookies: ['session', 'csrf', 'auth'],
            vendors: []
        },
        functional: {
            id: 2,
            name: 'Functional',
            description: 'Enable enhanced functionality and personalization',
            required: false,
            cookies: ['preferences', 'language', 'theme'],
            vendors: []
        },
        analytics: {
            id: 3,
            name: 'Analytics',
            description: 'Help us understand how visitors interact with our site',
            required: false,
            cookies: ['_ga', '_gid', '_gat', 'visitor_id'],
            vendors: ['google_analytics', 'plausible', 'mixpanel']
        },
        marketing: {
            id: 4,
            name: 'Marketing',
            description: 'Used to deliver personalized advertisements',
            required: false,
            cookies: ['_fbp', '_gcl_au', 'ad_id'],
            vendors: ['facebook', 'google_ads', 'linkedin']
        },
        social: {
            id: 5,
            name: 'Social Media',
            description: 'Enable social sharing and embedded content',
            required: false,
            cookies: ['fb_cookie', 'twitter_id'],
            vendors: ['facebook_sdk', 'twitter', 'linkedin_widget']
        }
    };

    // IAB TCF 2.2 Purposes
    const TCF_PURPOSES = {
        1: 'Store and/or access information on a device',
        2: 'Use limited data to select advertising',
        3: 'Create profiles for personalised advertising',
        4: 'Use profiles to select personalised advertising',
        5: 'Create profiles to personalise content',
        6: 'Use profiles to select personalised content',
        7: 'Measure advertising performance',
        8: 'Measure content performance',
        9: 'Use limited data to select content',
        10: 'Understand audiences through statistics',
        11: 'Use limited data to select advertising',
    };

    // State Management
    class ConsentState {
        constructor() {
            this.consent = this.load();
            this.queue = [];
            this.ready = false;
        }

        load() {
            try {
                const stored = localStorage.getItem(CONFIG.storageKey);
                if (stored) {
                    return JSON.parse(stored);
                }
            } catch (e) {
                console.warn('AGI CMP: Could not load consent from localStorage');
            }
            return null;
        }

        save(consentData) {
            this.consent = {
                ...consentData,
                timestamp: Date.now(),
                version: CONFIG.version,
                tcf: CONFIG.tcfVersion
            };
            try {
                localStorage.setItem(CONFIG.storageKey, JSON.stringify(this.consent));
                this.setCookie(consentData);
            } catch (e) {
                console.warn('AGI CMP: Could not save consent');
            }
        }

        setCookie(consentData) {
            const value = btoa(JSON.stringify({
                essential: true,
                functional: consentData.functional || false,
                analytics: consentData.analytics || false,
                marketing: consentData.marketing || false,
                social: consentData.social || false,
                timestamp: Date.now()
            }));
            const expiry = new Date();
            expiry.setDate(expiry.getDate() + CONFIG.cookieExpiry);
            document.cookie = `agi_consent=${value};expires=${expiry.toUTCString()};path=/;SameSite=Lax`;
        }

        hasConsent(category) {
            if (!this.consent) return category === 'essential';
            return this.consent[category] === true || category === 'essential';
        }

        getAllConsents() {
            return {
                essential: true,
                functional: this.hasConsent('functional'),
                analytics: this.hasConsent('analytics'),
                marketing: this.hasConsent('marketing'),
                social: this.hasConsent('social'),
                timestamp: this.consent?.timestamp || null
            };
        }
    }

    // Script Manager - Blocks/Allows scripts based on consent
    class ScriptManager {
        constructor(state) {
            this.state = state;
            this.blockedScripts = [];
        }

        init() {
            // Block scripts before consent
            this.blockExternalScripts();
            // Process existing scripts
            this.processExistingScripts();
        }

        blockExternalScripts() {
            // Intercept script injections
            const originalCreateElement = document.createElement;
            document.createElement = function(tagName, options) {
                const element = originalCreateElement.call(document, tagName, options);
                if (tagName.toLowerCase() === 'script') {
                    const originalSetAttribute = element.setAttribute;
                    element.setAttribute = function(name, value) {
                        if (name === 'src') {
                            const category = AGICMP.getCategoryForUrl(value);
                            if (category && category !== 'essential') {
                                element.dataset.agiCategory = category;
                                element.dataset.agiBlocked = 'true';
                                element.dataset.agiSrc = value;
                                return;
                            }
                        }
                        return originalSetAttribute.call(this, name, value);
                    };
                }
                return element;
            };
        }

        processExistingScripts() {
            // Find and process scripts with data-agi-category
            const scripts = document.querySelectorAll('script[data-agi-category]');
            scripts.forEach(script => {
                const category = script.dataset.agiCategory;
                if (!this.state.hasConsent(category)) {
                    this.blockScript(script);
                } else {
                    this.allowScript(script);
                }
            });
        }

        blockScript(script) {
            script.type = 'text/plain';
            script.dataset.agiBlocked = 'true';
            this.blockedScripts.push(script);
        }

        allowScript(script) {
            if (script.dataset.agiBlocked === 'true') {
                script.type = 'text/javascript';
                delete script.dataset.agiBlocked;
                
                // If it has a blocked src, restore it
                if (script.dataset.agiSrc) {
                    script.src = script.dataset.agiSrc;
                    delete script.dataset.agiSrc;
                }
            }
        }

        updateAllScripts() {
            this.blockedScripts.forEach(script => {
                const category = script.dataset.agiCategory;
                if (this.state.hasConsent(category)) {
                    this.allowScript(script);
                }
            });
        }
    }

    // UI Component
    class ConsentBanner {
        constructor(state, onConsent) {
            this.state = state;
            this.onConsent = onConsent;
            this.element = null;
            this.modal = null;
        }

        show() {
            if (this.state.consent) return;
            
            setTimeout(() => {
                this.createBanner();
                this.attachEvents();
            }, CONFIG.bannerDelay);
        }

        createBanner() {
            const banner = document.createElement('div');
            banner.id = 'agi-cmp-banner';
            banner.innerHTML = `
                <style>
                    #agi-cmp-banner {
                        position: fixed;
                        bottom: 0;
                        left: 0;
                        right: 0;
                        background: #1a1a2e;
                        color: #fff;
                        padding: 20px;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        z-index: 999999;
                        box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
                    }
                    #agi-cmp-banner .agi-cmp-container {
                        max-width: 1200px;
                        margin: 0 auto;
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        flex-wrap: wrap;
                        gap: 20px;
                    }
                    #agi-cmp-banner .agi-cmp-text {
                        flex: 1;
                        min-width: 300px;
                    }
                    #agi-cmp-banner h3 {
                        margin: 0 0 10px;
                        font-size: 18px;
                        color: #ed8936;
                    }
                    #agi-cmp-banner p {
                        margin: 0;
                        font-size: 14px;
                        line-height: 1.5;
                        color: #ccc;
                    }
                    #agi-cmp-banner .agi-cmp-buttons {
                        display: flex;
                        gap: 10px;
                        flex-wrap: wrap;
                    }
                    #agi-cmp-banner button {
                        padding: 12px 24px;
                        border: none;
                        border-radius: 6px;
                        cursor: pointer;
                        font-size: 14px;
                        font-weight: 600;
                        transition: all 0.2s;
                    }
                    #agi-cmp-banner .agi-btn-accept {
                        background: #ed8936;
                        color: #fff;
                    }
                    #agi-cmp-banner .agi-btn-accept:hover {
                        background: #dd7825;
                    }
                    #agi-cmp-banner .agi-btn-reject {
                        background: transparent;
                        color: #fff;
                        border: 1px solid #555;
                    }
                    #agi-cmp-banner .agi-btn-reject:hover {
                        background: rgba(255,255,255,0.1);
                    }
                    #agi-cmp-banner .agi-btn-settings {
                        background: transparent;
                        color: #ed8936;
                        text-decoration: underline;
                    }
                    #agi-cmp-banner .agi-btn-settings:hover {
                        color: #fff;
                    }
                    @media (max-width: 768px) {
                        #agi-cmp-banner .agi-cmp-container {
                            flex-direction: column;
                            text-align: center;
                        }
                        #agi-cmp-banner .agi-cmp-buttons {
                            width: 100%;
                            justify-content: center;
                        }
                    }
                </style>
                <div class="agi-cmp-container">
                    <div class="agi-cmp-text">
                        <h3>🍪 We value your privacy</h3>
                        <p>We use cookies to enhance your experience, analyze site traffic, and serve personalized content. 
                        By clicking "Accept All", you consent to our use of cookies. <a href="/privacy" style="color: #ed8936;">Learn more</a></p>
                    </div>
                    <div class="agi-cmp-buttons">
                        <button class="agi-btn-settings" data-action="settings">Preferences</button>
                        <button class="agi-btn-reject" data-action="reject">Reject All</button>
                        <button class="agi-btn-accept" data-action="accept">Accept All</button>
                    </div>
                </div>
            `;
            document.body.appendChild(banner);
            this.element = banner;
        }

        createModal() {
            const modal = document.createElement('div');
            modal.id = 'agi-cmp-modal';
            modal.innerHTML = `
                <style>
                    #agi-cmp-modal {
                        position: fixed;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: rgba(0,0,0,0.8);
                        z-index: 9999999;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        padding: 20px;
                    }
                    #agi-cmp-modal .agi-modal-content {
                        background: #1a1a2e;
                        border-radius: 12px;
                        max-width: 600px;
                        width: 100%;
                        max-height: 80vh;
                        overflow-y: auto;
                        color: #fff;
                    }
                    #agi-cmp-modal .agi-modal-header {
                        padding: 24px;
                        border-bottom: 1px solid #333;
                    }
                    #agi-cmp-modal .agi-modal-header h2 {
                        margin: 0;
                        color: #ed8936;
                    }
                    #agi-cmp-modal .agi-modal-body {
                        padding: 24px;
                    }
                    #agi-cmp-modal .agi-category {
                        margin-bottom: 20px;
                        padding: 16px;
                        background: rgba(255,255,255,0.05);
                        border-radius: 8px;
                    }
                    #agi-cmp-modal .agi-category-header {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 8px;
                    }
                    #agi-cmp-modal .agi-category h4 {
                        margin: 0;
                        color: #fff;
                    }
                    #agi-cmp-modal .agi-category p {
                        margin: 0;
                        font-size: 13px;
                        color: #aaa;
                    }
                    #agi-cmp-modal .agi-toggle {
                        position: relative;
                        width: 48px;
                        height: 24px;
                    }
                    #agi-cmp-modal .agi-toggle input {
                        opacity: 0;
                        width: 0;
                        height: 0;
                    }
                    #agi-cmp-modal .agi-toggle-slider {
                        position: absolute;
                        cursor: pointer;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: #444;
                        border-radius: 24px;
                        transition: 0.3s;
                    }
                    #agi-cmp-modal .agi-toggle-slider:before {
                        content: "";
                        position: absolute;
                        height: 18px;
                        width: 18px;
                        left: 3px;
                        bottom: 3px;
                        background: #fff;
                        border-radius: 50%;
                        transition: 0.3s;
                    }
                    #agi-cmp-modal .agi-toggle input:checked + .agi-toggle-slider {
                        background: #ed8936;
                    }
                    #agi-cmp-modal .agi-toggle input:checked + .agi-toggle-slider:before {
                        transform: translateX(24px);
                    }
                    #agi-cmp-modal .agi-toggle input:disabled + .agi-toggle-slider {
                        opacity: 0.5;
                        cursor: not-allowed;
                    }
                    #agi-cmp-modal .agi-modal-footer {
                        padding: 24px;
                        border-top: 1px solid #333;
                        display: flex;
                        justify-content: flex-end;
                        gap: 12px;
                    }
                    #agi-cmp-modal button {
                        padding: 12px 24px;
                        border: none;
                        border-radius: 6px;
                        cursor: pointer;
                        font-size: 14px;
                        font-weight: 600;
                    }
                    #agi-cmp-modal .agi-btn-save {
                        background: #ed8936;
                        color: #fff;
                    }
                    #agi-cmp-modal .agi-btn-cancel {
                        background: transparent;
                        color: #aaa;
                        border: 1px solid #555;
                    }
                </style>
                <div class="agi-modal-content">
                    <div class="agi-modal-header">
                        <h2>Cookie Preferences</h2>
                    </div>
                    <div class="agi-modal-body">
                        ${Object.entries(CATEGORIES).map(([key, cat]) => `
                            <div class="agi-category">
                                <div class="agi-category-header">
                                    <h4>${cat.name} ${cat.required ? '(Required)' : ''}</h4>
                                    <label class="agi-toggle">
                                        <input type="checkbox" data-category="${key}" 
                                            ${cat.required ? 'checked disabled' : ''}>
                                        <span class="agi-toggle-slider"></span>
                                    </label>
                                </div>
                                <p>${cat.description}</p>
                            </div>
                        `).join('')}
                    </div>
                    <div class="agi-modal-footer">
                        <button class="agi-btn-cancel" data-action="cancel">Cancel</button>
                        <button class="agi-btn-save" data-action="save">Save Preferences</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
            this.modal = modal;
        }

        attachEvents() {
            this.element.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                if (!action) return;

                switch(action) {
                    case 'accept':
                        this.handleAcceptAll();
                        break;
                    case 'reject':
                        this.handleRejectAll();
                        break;
                    case 'settings':
                        this.openSettings();
                        break;
                }
            });
        }

        handleAcceptAll() {
            const consent = {
                essential: true,
                functional: true,
                analytics: true,
                marketing: true,
                social: true
            };
            this.onConsent(consent);
            this.hide();
        }

        handleRejectAll() {
            const consent = {
                essential: true,
                functional: false,
                analytics: false,
                marketing: false,
                social: false
            };
            this.onConsent(consent);
            this.hide();
        }

        openSettings() {
            this.createModal();
            this.modal.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                if (action === 'cancel') {
                    this.closeSettings();
                } else if (action === 'save') {
                    this.savePreferences();
                }
            });
        }

        closeSettings() {
            if (this.modal) {
                this.modal.remove();
                this.modal = null;
            }
        }

        savePreferences() {
            const checkboxes = this.modal.querySelectorAll('input[type="checkbox"]');
            const consent = { essential: true };
            checkboxes.forEach(cb => {
                if (cb.dataset.category) {
                    consent[cb.dataset.category] = cb.checked;
                }
            });
            this.onConsent(consent);
            this.closeSettings();
            this.hide();
        }

        hide() {
            if (this.element) {
                this.element.remove();
                this.element = null;
            }
        }
    }

    // Main CMP Class
    class AGICMP {
        constructor(options = {}) {
            this.options = { ...CONFIG, ...options };
            this.state = new ConsentState();
            this.scriptManager = new ScriptManager(this.state);
            this.banner = new ConsentBanner(this.state, (consent) => this.handleConsent(consent));
            this.callbacks = [];
        }

        init() {
            // Block scripts immediately
            this.scriptManager.init();
            
            // Show banner if no consent
            if (!this.state.consent) {
                this.banner.show();
            } else {
                // Apply existing consent
                this.scriptManager.updateAllScripts();
            }

            // Expose to window
            window.__agi_cmp = this;
            this.state.ready = true;
            this.flushQueue();

            // Emit ready event
            this.emit('ready');
        }

        handleConsent(consent) {
            this.state.save(consent);
            this.scriptManager.updateAllScripts();
            this.syncToServer(consent);
            this.emit('consent', consent);
        }

        syncToServer(consent) {
            // Send to analytics endpoint
            fetch(CONFIG.apiEndpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    consent: consent,
                    timestamp: Date.now(),
                    url: window.location.href,
                    userAgent: navigator.userAgent
                })
            }).catch(() => {}); // Silent fail
        }

        getCategoryForUrl(url) {
            // Match URL patterns to categories
            const patterns = {
                analytics: [/google-analytics/, /googletagmanager/, /gtag/, /plausible/, /mixpanel/],
                marketing: [/facebook\.com\/tr/, /googleads/, /doubleclick/, /adform/],
                social: [/facebook\.com\/sdk/, /platform\.twitter/, /linkedin/],
                functional: [/recaptcha/, /maps\.google/]
            };

            for (const [category, regexes] of Object.entries(patterns)) {
                for (const regex of regexes) {
                    if (regex.test(url)) return category;
                }
            }
            return null;
        }

        // Public API
        hasConsent(category) {
            return this.state.hasConsent(category);
        }

        getConsent() {
            return this.state.getAllConsents();
        }

        reset() {
            localStorage.removeItem(CONFIG.storageKey);
            document.cookie = `agi_consent=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
            location.reload();
        }

        openSettings() {
            this.banner.openSettings();
        }

        on(event, callback) {
            if (!this.callbacks[event]) this.callbacks[event] = [];
            this.callbacks[event].push(callback);
        }

        emit(event, data) {
            if (this.callbacks[event]) {
                this.callbacks[event].forEach(cb => cb(data));
            }
        }

        flushQueue() {
            if (this.state.queue) {
                this.state.queue.forEach(fn => fn(this));
                this.state.queue = [];
            }
        }

        // Google Consent Mode v2
        gtagConsent() {
            const consent = this.getConsent();
            if (typeof gtag === 'function') {
                gtag('consent', 'update', {
                    ad_storage: consent.marketing ? 'granted' : 'denied',
                    analytics_storage: consent.analytics ? 'granted' : 'denied',
                    functionality_storage: consent.functional ? 'granted' : 'denied',
                    personalization_storage: consent.functional ? 'granted' : 'denied',
                    security_storage: 'granted',
                    ad_user_data: consent.marketing ? 'granted' : 'denied',
                    ad_personalization: consent.marketing ? 'granted' : 'denied'
                });
            }
        }
    }

    // Auto-initialize when DOM is ready
    function init() {
        const cmp = new AGICMP();
        cmp.init();
        return cmp;
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose for module systems
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = AGICMP;
    }

    window.AGICMP = AGICMP;

})(window);
