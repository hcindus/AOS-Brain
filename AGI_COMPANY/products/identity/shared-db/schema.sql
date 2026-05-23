-- AGI IDENTITY & ANALYTICS DATABASE SCHEMA
-- Version: 1.0.0
-- Created: 2026-05-23
-- Purpose: Parallel track identity tracking system

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- CORE TABLES
-- =====================================================

-- Users table (bridges to existing AGI auth system)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agi_auth_id UUID REFERENCES agi_auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    consent_analytics BOOLEAN DEFAULT FALSE, -- Opt-in to contribute anonymized data
    consent_data_retention INTEGER DEFAULT 365, -- Days to retain data after account deletion
    tier VARCHAR(50) DEFAULT 'free', -- free, basic, premium
    status VARCHAR(50) DEFAULT 'active' -- active, suspended, deleted
);

-- Identity stages tracker (c2g = cradle to grave)
CREATE TABLE identity_stages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    stage_number INTEGER NOT NULL CHECK (stage_number BETWEEN 1 AND 10),
    stage_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, in_progress, completed, failed, skipped
    
    -- Stage-specific metadata
    data_source VARCHAR(255),
    last_checked TIMESTAMP WITH TIME ZONE,
    last_updated TIMESTAMP WITH TIME ZONE,
    
    -- Verification markers
    verification_method VARCHAR(100),
    verification_status VARCHAR(50) DEFAULT 'unverified',
    verified_at TIMESTAMP WITH TIME ZONE,
    
    -- Error tracking
    error_count INTEGER DEFAULT 0,
    last_error TEXT,
    
    -- Progress tracking
    total_markers INTEGER DEFAULT 0,
    completed_markers INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, stage_number)
);

-- Data markers (the actual data points collected)
CREATE TABLE data_markers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stage_id UUID REFERENCES identity_stages(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    -- Marker classification
    marker_type VARCHAR(100) NOT NULL, -- ssn, address, employment, etc.
    marker_category VARCHAR(100) NOT NULL, -- financial, health, digital, etc.
    
    -- Data storage (encrypted)
    data_value_encrypted BYTEA, -- Sensitive data encrypted at rest
    data_hash VARCHAR(255), -- For deduplication without decryption
    
    -- Metadata
    source_system VARCHAR(255), -- Which system provided this
    confidence_score DECIMAL(3,2) DEFAULT 1.00, -- 0.00 to 1.00
    verified BOOLEAN DEFAULT FALSE,
    
    -- Privacy
    pii_classification VARCHAR(50) DEFAULT 'standard', -- standard, sensitive, restricted
    retention_until TIMESTAMP WITH TIME ZONE, -- Auto-delete after this date
    
    -- Analytics (anonymized for aggregate queries)
    analytics_token UUID, -- Links to anonymized analytics table
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Stage dependencies (which stages must complete before others)
CREATE TABLE stage_dependencies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stage_number INTEGER NOT NULL,
    depends_on_stage INTEGER NOT NULL,
    is_blocking BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(stage_number, depends_on_stage)
);

-- =====================================================
-- ANALYTICS TABLES (Aggregate, non-PII)
-- =====================================================

-- Anonymized analytics tokens
CREATE TABLE analytics_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    token_hash VARCHAR(255) UNIQUE NOT NULL, -- One-way hash for privacy
    birth_year_range VARCHAR(20), -- Decade buckets: "1990-1999"
    geographic_region VARCHAR(100), -- State or region, not exact location
    demographic_segment VARCHAR(100), -- Aggregate categories only
    consent_granted_at TIMESTAMP WITH TIME ZONE,
    last_contribution TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Aggregate metrics (no individual identification)
CREATE TABLE aggregate_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(255) NOT NULL,
    metric_category VARCHAR(100) NOT NULL, -- demographic, financial, health, etc.
    
    -- Aggregate values
    value_count BIGINT,
    value_mean DECIMAL(15,4),
    value_median DECIMAL(15,4),
    value_min DECIMAL(15,4),
    value_max DECIMAL(15,4),
    
    -- Segmentation
    region VARCHAR(100),
    time_period VARCHAR(50), -- monthly, quarterly, yearly
    period_start DATE,
    period_end DATE,
    
    -- Data quality
    sample_size INTEGER,
    confidence_level DECIMAL(3,2) DEFAULT 0.95,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Stage completion analytics (aggregate only)
CREATE TABLE stage_completion_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stage_number INTEGER NOT NULL,
    date_bucket DATE NOT NULL,
    
    -- Completion metrics
    attempted_count INTEGER DEFAULT 0,
    completed_count INTEGER DEFAULT 0,
    failed_count INTEGER DEFAULT 0,
    avg_completion_time_minutes INTEGER,
    
    -- Error patterns
    top_error_types JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(stage_number, date_bucket)
);

-- =====================================================
-- AUDIT & COMPLIANCE
-- =====================================================

-- Audit log for all data access
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL, -- read, write, delete, export
    resource_type VARCHAR(100) NOT NULL, -- marker, stage, user
    resource_id UUID,
    
    -- Access details
    accessed_by VARCHAR(255), -- User or system ID
    accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    
    -- For compliance
    legal_basis VARCHAR(100), -- consent, legitimate_interest, legal_obligation
    retention_category VARCHAR(50)
);

-- Data deletion requests (GDPR/CCPA)
CREATE TABLE deletion_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    request_type VARCHAR(50) NOT NULL, -- full_deletion, partial_deletion, export
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed
    
    -- Request details
    requested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    verification_method VARCHAR(100),
    
    -- Scope
    scopes JSONB, -- Which stages/markers to delete
    
    -- Audit trail
    processed_by VARCHAR(255),
    result_details TEXT
);

-- =====================================================
-- CONNECTORS & INTEGRATIONS
-- =====================================================

-- External data source connectors
CREATE TABLE connectors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    connector_type VARCHAR(100) NOT NULL, -- api, scraper, sftp, manual
    stage_number INTEGER NOT NULL,
    
    -- Configuration (encrypted)
    config_encrypted BYTEA,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_run TIMESTAMP WITH TIME ZONE,
    next_scheduled_run TIMESTAMP WITH TIME ZONE,
    
    -- Rate limiting
    rate_limit_requests INTEGER DEFAULT 100,
    rate_limit_window_minutes INTEGER DEFAULT 60,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Connector run history
CREATE TABLE connector_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    connector_id UUID REFERENCES connectors(id) ON DELETE CASCADE,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    status VARCHAR(50) DEFAULT 'running', -- running, success, failed, partial
    records_processed INTEGER DEFAULT 0,
    records_inserted INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    
    error_log TEXT,
    metadata JSONB
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_agi_auth_id ON users(agi_auth_id);
CREATE INDEX idx_users_consent ON users(consent_analytics) WHERE consent_analytics = TRUE;

CREATE INDEX idx_stages_user_id ON identity_stages(user_id);
CREATE INDEX idx_stages_status ON identity_stages(status);
CREATE INDEX idx_stages_stage_number ON identity_stages(stage_number);

CREATE INDEX idx_markers_stage_id ON data_markers(stage_id);
CREATE INDEX idx_markers_user_id ON data_markers(user_id);
CREATE INDEX idx_markers_type ON data_markers(marker_type);
CREATE INDEX idx_markers_analytics_token ON data_markers(analytics_token) WHERE analytics_token IS NOT NULL;

CREATE INDEX idx_audit_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_accessed_at ON audit_log(accessed_at);

CREATE INDEX idx_analytics_token_hash ON analytics_tokens(token_hash);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- User progress summary
CREATE VIEW user_progress_summary AS
SELECT 
    u.id as user_id,
    u.email,
    u.tier,
    COUNT(DISTINCT s.stage_number) as stages_attempted,
    COUNT(DISTINCT CASE WHEN s.status = 'completed' THEN s.stage_number END) as stages_completed,
    COUNT(DISTINCT m.id) as total_markers,
    COUNT(DISTINCT CASE WHEN m.verified THEN m.id END) as verified_markers
FROM users u
LEFT JOIN identity_stages s ON u.id = s.user_id
LEFT JOIN data_markers m ON s.id = m.stage_id
GROUP BY u.id, u.email, u.tier;

-- Stage completion rates (aggregate)
CREATE VIEW stage_completion_rates AS
SELECT 
    stage_number,
    COUNT(*) as total_users,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_count,
    ROUND(
        COUNT(CASE WHEN status = 'completed' THEN 1 END) * 100.0 / COUNT(*), 
        2
    ) as completion_rate
FROM identity_stages
GROUP BY stage_number
ORDER BY stage_number;

-- =====================================================
-- FUNCTIONS & TRIGGERS
-- =====================================================

-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stages_updated_at BEFORE UPDATE ON identity_stages
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_markers_updated_at BEFORE UPDATE ON data_markers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Auto-anonymization trigger
CREATE OR REPLACE FUNCTION create_analytics_token()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.consent_analytics = TRUE AND NEW.analytics_token IS NULL THEN
        INSERT INTO analytics_tokens (user_id, token_hash)
        VALUES (NEW.id, encode(digest(NEW.id::text || NOW()::text, 'sha256'), 'hex'))
        RETURNING id INTO NEW.analytics_token;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- =====================================================
-- INITIAL DATA
-- =====================================================

-- Populate stage dependencies
INSERT INTO stage_dependencies (stage_number, depends_on_stage, is_blocking) VALUES
(2, 1, TRUE),   -- SSN requires birth certificate
(3, 2, FALSE),  -- IRS works better with SSN but not strictly required
(4, 2, TRUE),   -- Credit bureaus require SSN
(5, 1, FALSE),  -- Education can proceed with basic identity
(6, 2, FALSE),  -- Health can proceed with basic identity
(7, 2, TRUE),   -- Employment typically requires SSN
(8, 4, FALSE),  -- Digital benefits from credit data but not required
(9, 1, FALSE),  -- Census works with basic demographics
(10, 2, TRUE); -- Death certificate requires SSN for proper closure

-- Sample connectors
INSERT INTO connectors (name, connector_type, stage_number, is_active) VALUES
('AnnualCreditReport', 'api', 4, TRUE),
('HaveIBeenPwned', 'api', 8, TRUE),
('SSA_Earnings', 'scraper', 2, TRUE),
('IRS_Transcript', 'api', 3, TRUE),
('DataBroker_OptOut', 'scraper', 8, TRUE);

-- =====================================================
-- COMMENTS
-- =====================================================

COMMENT ON TABLE users IS 'Core user table bridging to AGI auth system';
COMMENT ON TABLE identity_stages IS 'Tracks progress through 10 cradle-to-grave stages';
COMMENT ON TABLE data_markers IS 'Individual data points collected, encrypted at rest';
COMMENT ON TABLE analytics_tokens IS 'Privacy-preserving tokens for aggregate analytics';
COMMENT ON TABLE aggregate_metrics IS 'Population-level statistics, no PII';
COMMENT ON TABLE audit_log IS 'Complete audit trail for compliance';
