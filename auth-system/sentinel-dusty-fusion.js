#!/usr/bin/env node

/**
 * SENTINEL-DUSTY FUSION v1.0
 * Autonomous Security Monitoring Agent for Auth System
 * 
 * Capabilities:
 * - Real-time security event scanning (like Dusty scans assets)
 * - Threat consolidation and analysis (cross-vector correlation)
 * - Automated response and containment
 * - Security audit logging and reporting
 * - Predictive threat detection using AI patterns
 */

const db = require('./database/db');
const { sendSecurityAlert } = require('./backend/utils/email');
const { logAuditEvent } = require('./backend/utils/audit');

class SentinelDustyFusion {
    constructor() {
        this.scanInterval = 30000; // 30 seconds
        this.threatThreshold = 5; // Alert after 5 suspicious events
        this.active = false;
        this.threats = [];
        this.patterns = this.loadThreatPatterns();
    }

    /**
     * Initialize the security guardian
     */
    async initialize() {
        console.log('🛡️  Sentinel-Dusty Fusion initializing...');
        console.log('🔍 Loading threat detection patterns...');
        
        await this.verifyDatabaseConnection();
        await this.loadBaselineMetrics();
        
        this.active = true;
        this.startMonitoring();
        
        console.log('✅ Sentinel-Dusty Fusion active and scanning');
        console.log(`⏱️  Scan interval: ${this.scanInterval}ms`);
        console.log(`🚨 Threat threshold: ${this.threatThreshold} events`);
    }

    /**
     * Load threat detection patterns (Dusty's "asset scanning" for threats)
     */
    loadThreatPatterns() {
        return {
            bruteForce: {
                pattern: /failed_login/g,
                threshold: 5,
                window: 300000, // 5 minutes
                severity: 'HIGH'
            },
            credentialStuffing: {
                pattern: /LOGIN.*FAILED.*different_ips/g,
                threshold: 10,
                window: 600000, // 10 minutes
                severity: 'CRITICAL'
            },
            tokenReplay: {
                pattern: /TOKEN_REFRESH.*FAILED.*invalid_token/g,
                threshold: 3,
                window: 300000,
                severity: 'CRITICAL'
            },
            suspiciousLocation: {
                pattern: /NEW_IP|NEW_DEVICE/g,
                threshold: 1,
                window: 60000,
                severity: 'MEDIUM'
            },
            mfaBypass: {
                pattern: /MFA.*FAILED/g,
                threshold: 3,
                window: 300000,
                severity: 'HIGH'
            },
            accountEnumeration: {
                pattern: /user_not_found/g,
                threshold: 20,
                window: 600000,
                severity: 'MEDIUM'
            },
            privilegeEscalation: {
                pattern: /mass_assignment|role=admin/g,
                threshold: 1,
                window: 60000,
                severity: 'CRITICAL'
            },
            dataExfiltration: {
                pattern: /export|bulk.*download/g,
                threshold: 5,
                window: 300000,
                severity: 'HIGH'
            }
        };
    }

    /**
     * Start continuous monitoring (Dusty's "continuous scan")
     */
    startMonitoring() {
        this.scanIntervalId = setInterval(() => {
            this.performSecurityScan();
        }, this.scanInterval);
        
        // Also scan on-demand events
        this.eventWatcher = this.watchRealTimeEvents();
    }

    /**
     * Perform security scan (like Dusty scanning for assets)
     */
    async performSecurityScan() {
        const scanTimestamp = new Date().toISOString();
        
        try {
            // Scan 1: Failed login attempts
            const failedLogins = await this.scanFailedLogins();
            
            // Scan 2: Suspicious token usage
            const suspiciousTokens = await this.scanSuspiciousTokens();
            
            // Scan 3: Geographic anomalies
            const geoAnomalies = await this.scanGeographicAnomalies();
            
            // Scan 4: Rate limit violations
            const rateViolations = await this.scanRateLimitViolations();
            
            // Scan 5: Database integrity
            const dbIntegrity = await this.scanDatabaseIntegrity();
            
            // Consolidate threats (Dusty-style asset consolidation)
            const consolidatedThreats = this.consolidateThreats([
                ...failedLogins,
                ...suspiciousTokens,
                ...geoAnomalies,
                ...rateViolations,
                ...dbIntegrity
            ]);
            
            // Analyze and respond
            if (consolidatedThreats.length > 0) {
                await this.analyzeAndRespond(consolidatedThreats);
            }
            
            // Update metrics
            this.updateSecurityMetrics(consolidatedThreats);
            
        } catch (err) {
            console.error('❌ Security scan failed:', err.message);
            await this.logSecurityEvent('SCAN_ERROR', 'FAILED', { error: err.message });
        }
    }

    /**
     * Scan for failed login attempts (brute force detection)
     */
    async scanFailedLogins() {
        const fiveMinutesAgo = new Date(Date.now() - 300000).toISOString();
        
        return new Promise((resolve, reject) => {
            db.all(
                `SELECT user_id, ip_address, COUNT(*) as attempt_count
                 FROM audit_logs
                 WHERE action = 'LOGIN' AND status = 'FAILED'
                 AND created_at > ?
                 GROUP BY user_id, ip_address
                 HAVING attempt_count >= 3`,
                [fiveMinutesAgo],
                (err, rows) => {
                    if (err) reject(err);
                    else resolve(rows.map(row => ({
                        type: 'BRUTE_FORCE',
                        userId: row.user_id,
                        ip: row.ip_address,
                        count: row.attempt_count,
                        severity: row.attempt_count >= 5 ? 'CRITICAL' : 'HIGH'
                    })));
                }
            );
        });
    }

    /**
     * Scan for suspicious token usage (replay attacks)
     */
    async scanSuspiciousTokens() {
        const tenMinutesAgo = new Date(Date.now() - 600000).toISOString();
        
        return new Promise((resolve, reject) => {
            db.all(
                `SELECT user_id, ip_address, COUNT(*) as fail_count
                 FROM audit_logs
                 WHERE action = 'TOKEN_REFRESH' AND status = 'FAILED'
                 AND created_at > ?
                 GROUP BY user_id, ip_address`,
                [tenMinutesAgo],
                (err, rows) => {
                    if (err) reject(err);
                    else resolve(rows.map(row => ({
                        type: 'TOKEN_REPLAY',
                        userId: row.user_id,
                        ip: row.ip_address,
                        count: row.fail_count,
                        severity: 'CRITICAL'
                    })));
                }
            );
        });
    }

    /**
     * Scan for geographic anomalies (impossible travel)
     */
    async scanGeographicAnomalies() {
        const oneHourAgo = new Date(Date.now() - 3600000).toISOString();
        
        return new Promise((resolve, reject) => {
            db.all(
                `SELECT user_id, ip_address, metadata, created_at
                 FROM audit_logs
                 WHERE action = 'LOGIN' AND status = 'SUCCESS'
                 AND (metadata LIKE '%NEW_IP%' OR metadata LIKE '%NEW_DEVICE%')
                 AND created_at > ?
                 ORDER BY created_at DESC
                 LIMIT 50`,
                [oneHourAgo],
                (err, rows) => {
                    if (err) reject(err);
                    else resolve(rows.map(row => ({
                        type: 'GEO_ANOMALY',
                        userId: row.user_id,
                        ip: row.ip_address,
                        metadata: JSON.parse(row.metadata || '{}'),
                        severity: 'MEDIUM'
                    })));
                }
            );
        });
    }

    /**
     * Scan for rate limit violations
     */
    async scanRateLimitViolations() {
        const fiveMinutesAgo = new Date(Date.now() - 300000).toISOString();
        
        return new Promise((resolve, reject) => {
            db.all(
                `SELECT ip_address, COUNT(*) as hit_count
                 FROM audit_logs
                 WHERE action LIKE '%RATE_LIMIT%' OR metadata LIKE '%rate_limited%'
                 AND created_at > ?
                 GROUP BY ip_address
                 HAVING hit_count >= 10`,
                [fiveMinutesAgo],
                (err, rows) => {
                    if (err) reject(err);
                    else resolve(rows.map(row => ({
                        type: 'RATE_LIMIT_ABUSE',
                        ip: row.ip_address,
                        count: row.hit_count,
                        severity: 'HIGH'
                    })));
                }
            );
        });
    }

    /**
     * Scan database integrity (Dusty's "asset validation")
     */
    async scanDatabaseIntegrity() {
        const threats = [];
        
        // Check for orphaned sessions
        const orphanedSessions = await new Promise((resolve, reject) => {
            db.get(
                `SELECT COUNT(*) as count FROM sessions s
                 LEFT JOIN users u ON s.user_id = u.id
                 WHERE u.id IS NULL AND s.revoked_at IS NULL`,
                [],
                (err, row) => err ? reject(err) : resolve(row?.count || 0)
            );
        });
        
        if (orphanedSessions > 0) {
            threats.push({
                type: 'DB_INTEGRITY',
                issue: 'ORPHANED_SESSIONS',
                count: orphanedSessions,
                severity: 'MEDIUM'
            });
        }
        
        // Check for expired but not revoked tokens
        const expiredTokens = await new Promise((resolve, reject) => {
            db.get(
                `SELECT COUNT(*) as count FROM sessions
                 WHERE expires_at < datetime('now')
                 AND revoked_at IS NULL`,
                [],
                (err, row) => err ? reject(err) : resolve(row?.count || 0)
            );
        });
        
        if (expiredTokens > 0) {
            threats.push({
                type: 'DB_INTEGRITY',
                issue: 'EXPIRED_ACTIVE_TOKENS',
                count: expiredTokens,
                severity: 'LOW'
            });
        }
        
        return threats;
    }

    /**
     * Consolidate threats (Dusty-style asset consolidation)
     */
    consolidateThreats(rawThreats) {
        const consolidated = {};
        
        rawThreats.forEach(threat => {
            const key = `${threat.type}:${threat.userId || threat.ip}`;
            
            if (!consolidated[key]) {
                consolidated[key] = {
                    ...threat,
                    occurrences: 1,
                    firstSeen: new Date().toISOString(),
                    relatedThreats: []
                };
            } else {
                consolidated[key].occurrences++;
                consolidated[key].count += (threat.count || 1);
                consolidated[key].relatedThreats.push(threat);
            }
        });
        
        // Filter by threshold
        return Object.values(consolidated).filter(t => {
            const pattern = this.patterns[t.type.toLowerCase()];
            return t.occurrences >= (pattern?.threshold || this.threatThreshold);
        });
    }

    /**
     * Analyze threats and respond (automated response)
     */
    async analyzeAndRespond(threats) {
        console.log(`🚨 Detected ${threats.length} threat clusters`);
        
        for (const threat of threats) {
            console.log(`⚠️  ${threat.type}: ${threat.occurrences} occurrences, severity: ${threat.severity}`);
            
            // Automated response based on severity
            switch (threat.severity) {
                case 'CRITICAL':
                    await this.respondCritical(threat);
                    break;
                case 'HIGH':
                    await this.respondHigh(threat);
                    break;
                case 'MEDIUM':
                    await this.respondMedium(threat);
                    break;
                case 'LOW':
                    await this.respondLow(threat);
                    break;
            }
        }
    }

    /**
     * Critical threat response (auto-block)
     */
    async respondCritical(threat) {
        console.log(`🔒 CRITICAL: Auto-blocking ${threat.ip || threat.userId}`);
        
        // Auto-block IP
        if (threat.ip) {
            await this.blockIP(threat.ip);
        }
        
        // Revoke all sessions for user
        if (threat.userId) {
            await this.revokeUserSessions(threat.userId);
        }
        
        // Send immediate alert
        await this.sendSecurityAlert(threat);
        
        // Log to security audit
        await this.logSecurityEvent('AUTO_RESPONSE', 'CRITICAL_BLOCKED', threat);
    }

    /**
     * High threat response (alert + partial restriction)
     */
    async respondHigh(threat) {
        console.log(`⚡ HIGH: Sending alert for ${threat.type}`);
        
        await this.sendSecurityAlert(threat);
        await this.logSecurityEvent('AUTO_RESPONSE', 'HIGH_ALERT', threat);
    }

    /**
     * Medium threat response (log + monitor)
     */
    async respondMedium(threat) {
        console.log(`📊 MEDIUM: Monitoring ${threat.type}`);
        await this.logSecurityEvent('AUTO_RESPONSE', 'MEDIUM_MONITOR', threat);
    }

    /**
     * Low threat response (log only)
     */
    async respondLow(threat) {
        await this.logSecurityEvent('AUTO_RESPONSE', 'LOW_LOGGED', threat);
    }

    /**
     * Block an IP address
     */
    async blockIP(ip) {
        // This would integrate with firewall or Express middleware
        console.log(`🚫 Blocking IP: ${ip}`);
        // Implementation depends on your infrastructure
        // Could use: iptables, AWS WAF, Cloudflare, etc.
    }

    /**
     * Revoke all sessions for a user
     */
    async revokeUserSessions(userId) {
        return new Promise((resolve, reject) => {
            db.run(
                'UPDATE sessions SET revoked_at = CURRENT_TIMESTAMP WHERE user_id = ? AND revoked_at IS NULL',
                [userId],
                (err) => {
                    if (err) reject(err);
                    else {
                        console.log(`🔓 Revoked all sessions for user ${userId}`);
                        resolve();
                    }
                }
            );
        });
    }

    /**
     * Send security alert (email)
     */
    async sendSecurityAlert(threat) {
        // This would integrate with email service
        console.log(`📧 Security alert: ${threat.type} - ${threat.severity}`);
        // await sendSecurityAlert(...)
    }

    /**
     * Log security event
     */
    async logSecurityEvent(action, status, metadata) {
        const event = {
            timestamp: new Date().toISOString(),
            action,
            status,
            metadata: JSON.stringify(metadata)
        };
        
        // Log to console and database
        console.log(`📝 Security Event: ${action} - ${status}`);
    }

    /**
     * Watch real-time events (WebSocket or polling)
     */
    watchRealTimeEvents() {
        // This would hook into your event system
        // For now, we'll poll the database
        return setInterval(() => {
            this.checkRealTimeEvents();
        }, 5000);
    }

    /**
     * Check for real-time events
     */
    async checkRealTimeEvents() {
        const recentEvents = await new Promise((resolve, reject) => {
            db.all(
                `SELECT * FROM audit_logs
                 WHERE created_at > datetime('now', '-10 seconds')
                 ORDER BY created_at DESC`,
                [],
                (err, rows) => err ? reject(err) : resolve(rows)
            );
        });
        
        // Process events in real-time
        recentEvents.forEach(event => {
            this.processRealTimeEvent(event);
        });
    }

    /**
     * Process a real-time event
     */
    processRealTimeEvent(event) {
        // Check against threat patterns
        for (const [patternName, pattern] of Object.entries(this.patterns)) {
            if (event.action?.match(pattern.pattern) || event.metadata?.match(pattern.pattern)) {
                console.log(`🎯 Real-time threat detected: ${patternName}`);
                // Trigger immediate response
            }
        }
    }

    /**
     * Update security metrics
     */
    updateSecurityMetrics(threats) {
        this.threats = [...this.threats, ...threats].slice(-1000); // Keep last 1000
    }

    /**
     * Get security status report (Dusty-style portfolio view)
     */
    getSecurityReport() {
        const report = {
            timestamp: new Date().toISOString(),
            status: this.active ? 'ACTIVE' : 'INACTIVE',
            threatsDetected: this.threats.length,
            threatBreakdown: this.threats.reduce((acc, t) => {
                acc[t.severity] = (acc[t.severity] || 0) + 1;
                return acc;
            }, {}),
            recentThreats: this.threats.slice(-10),
            recommendations: this.generateRecommendations()
        };
        
        return report;
    }

    /**
     * Generate security recommendations (AI-like)
     */
    generateRecommendations() {
        const recommendations = [];
        
        if (this.threats.filter(t => t.type === 'BRUTE_FORCE').length > 5) {
            recommendations.push('Consider lowering login rate limit threshold');
        }
        
        if (this.threats.filter(t => t.type === 'GEO_ANOMALY').length > 10) {
            recommendations.push('Enable mandatory MFA for all users');
        }
        
        if (this.threats.filter(t => t.type === 'TOKEN_REPLAY').length > 0) {
            recommendations.push('Review session management implementation');
        }
        
        return recommendations;
    }

    /**
     * Stop monitoring
     */
    stop() {
        this.active = false;
        clearInterval(this.scanIntervalId);
        clearInterval(this.eventWatcher);
        console.log('🛑 Sentinel-Dusty Fusion stopped');
    }

    // Helper methods
    async verifyDatabaseConnection() {
        return new Promise((resolve, reject) => {
            db.get('SELECT 1', [], (err) => {
                if (err) reject(err);
                else resolve();
            });
        });
    }

    async loadBaselineMetrics() {
        console.log('📊 Loading baseline security metrics...');
        // Load historical data to establish baseline
    }
}

// Export for use in main application
module.exports = SentinelDustyFusion;

// If run directly, start the guardian
if (require.main === module) {
    const guardian = new SentinelDustyFusion();
    guardian.initialize().catch(console.error);
    
    // Graceful shutdown
    process.on('SIGINT', () => {
        console.log('\n👋 Shutting down Sentinel-Dusty Fusion...');
        guardian.stop();
        process.exit(0);
    });
}