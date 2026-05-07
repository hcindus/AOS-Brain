-- DepotPages Business Directory Schema
-- PostgreSQL/SQLite Compatible
-- Version: 1.0.0
-- Created: 2026-05-07

-- Enable necessary extensions for PostgreSQL
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE EXTENSION IF NOT EXISTS "postgis"; -- For geospatial queries

-- ============================================
-- CORE TABLES
-- ============================================

-- Business Categories Taxonomy
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    level INTEGER DEFAULT 1, -- 1=primary, 2=subcategory, 3=nested
    naics_code VARCHAR(10),
    sic_code VARCHAR(10),
    icon_url VARCHAR(500),
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Regions/Geographic Areas
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('country', 'state', 'province', 'county', 'city', 'metro', 'zip')),
    parent_id INTEGER REFERENCES regions(id) ON DELETE SET NULL,
    country_code CHAR(2),
    state_code VARCHAR(10),
    postal_code VARCHAR(20),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    timezone VARCHAR(100),
    bounding_box JSONB, -- GeoJSON bbox
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Main Business Listings Table
CREATE TABLE businesses (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT gen_random_uuid(),
    
    -- Core Identity
    name VARCHAR(500) NOT NULL,
    legal_name VARCHAR(500),
    slug VARCHAR(500) UNIQUE,
    description TEXT,
    tagline VARCHAR(500),
    
    -- Business Status & Verification
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended', 'closed', 'pending_review')),
    verification_status VARCHAR(50) DEFAULT 'unclaimed' CHECK (verification_status IN ('unclaimed', 'claimed_pending', 'claimed_verified', 'premium_verified')),
    claimed_by_user_id INTEGER, -- References users table if exists
    claimed_at TIMESTAMP,
    verification_method VARCHAR(50), -- 'email', 'phone', 'document', 'manual'
    verification_expires_at TIMESTAMP,
    
    -- Contact Information
    phone_primary VARCHAR(50),
    phone_secondary VARCHAR(50),
    fax VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(500),
    
    -- Address (Physical Location)
    address_street VARCHAR(500),
    address_suite VARCHAR(100),
    address_city VARCHAR(200),
    address_state VARCHAR(100),
    address_zip VARCHAR(20),
    address_country CHAR(2) DEFAULT 'US',
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    geohash VARCHAR(12), -- For efficient geo-queries
    region_id INTEGER REFERENCES regions(id) ON DELETE SET NULL,
    
    -- Business Enrichment Data
    year_founded INTEGER,
    employee_count VARCHAR(50), -- '1-10', '11-50', etc.
    employee_count_min INTEGER,
    employee_count_max INTEGER,
    annual_revenue_bracket VARCHAR(50),
    business_type VARCHAR(100), -- LLC, Corp, Sole Proprietorship, etc.
    
    -- External Identifiers (Enrichment)
    duns_number VARCHAR(20),
    naics_code VARCHAR(10),
    sic_code VARCHAR(10),
    ein VARCHAR(20), -- Employer ID (hashed/encrypted in production)
    google_place_id VARCHAR(255),
    yelp_business_id VARCHAR(255),
    facebook_page_id VARCHAR(255),
    
    -- Review Aggregation
    review_count_total INTEGER DEFAULT 0,
    review_count_google INTEGER DEFAULT 0,
    review_count_yelp INTEGER DEFAULT 0,
    review_score_weighted DECIMAL(3, 2) CHECK (review_score_weighted >= 0 AND review_score_weighted <= 5),
    review_score_google DECIMAL(3, 2),
    review_score_yelp DECIMAL(3, 2),
    review_last_synced TIMESTAMP,
    
    -- Data Freshness Tracking (Update Cadence)
    data_freshness_score INTEGER DEFAULT 100, -- 0-100 scale
    last_verified_at TIMESTAMP,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    next_scheduled_update TIMESTAMP,
    update_frequency VARCHAR(20) DEFAULT 'monthly' CHECK (update_frequency IN ('daily', 'weekly', 'monthly', 'quarterly', 'manual')),
    update_source VARCHAR(100), -- 'api', 'scraper', 'manual', 'user_submission'
    staleness_flags JSONB, -- Array of stale fields
    
    -- Media
    logo_url VARCHAR(500),
    cover_image_url VARCHAR(500),
    photos JSONB, -- Array of photo objects
    videos JSONB,
    
    -- Hours & Availability
    hours_of_operation JSONB, -- Structured hours by day
    is_open_now BOOLEAN,
    is_24_hours BOOLEAN DEFAULT FALSE,
    timezone VARCHAR(100),
    
    -- Social Profiles
    social_profiles JSONB, -- {facebook, twitter, linkedin, instagram, tiktok, youtube}
    
    -- SEO & Discovery
    keywords TEXT[], -- Searchable keywords
    amenities JSONB, -- Feature flags
    service_areas JSONB, -- Array of region IDs
    languages_spoken TEXT[],
    payment_methods_accepted TEXT[],
    
    -- Claimed Listing Management
    claim_token VARCHAR(255), -- For invitation-based claiming
    claim_expires_at TIMESTAMP,
    ownership_documents JSONB, -- Verification documents
    
    -- Metadata
    source VARCHAR(100) DEFAULT 'manual', -- Where this record originated
    source_id VARCHAR(255), -- ID in original source
    import_batch_id VARCHAR(100),
    is_duplicate_of INTEGER REFERENCES businesses(id) ON DELETE SET NULL,
    confidence_score DECIMAL(4, 3) DEFAULT 1.0, -- Data quality score
    metadata JSONB, -- Flexible additional data
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER
);

-- Business-Category Many-to-Many Relationship
CREATE TABLE business_categories (
    id SERIAL PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    is_primary BOOLEAN DEFAULT FALSE,
    confidence_score DECIMAL(4, 3) DEFAULT 1.0,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by INTEGER,
    UNIQUE(business_id, category_id)
);

-- Competitive Intelligence: Service Providers Relationships
CREATE TABLE service_relationships (
    id SERIAL PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    provider_id INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL CHECK (relationship_type IN ('competitor', 'supplier', 'customer', 'partner', 'subsidiary', 'parent', 'franchisee', 'franchisor')),
    service_categories INTEGER[], -- Category IDs for the service provided
    is_verified BOOLEAN DEFAULT FALSE,
    relationship_strength INTEGER DEFAULT 50 CHECK (relationship_strength >= 0 AND relationship_strength <= 100),
    evidence_notes TEXT,
    evidence_sources JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(business_id, provider_id, relationship_type)
);

-- Update History / Audit Log for Data Freshness
CREATE TABLE update_history (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    field_name VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    update_type VARCHAR(50) DEFAULT 'automatic' CHECK (update_type IN ('automatic', 'manual', 'user_submission', 'api_import', 'scraped')),
    update_source VARCHAR(200),
    update_batch_id VARCHAR(100),
    performed_by INTEGER,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    change_hash VARCHAR(64), -- For deduplication
    confidence_score DECIMAL(4, 3) DEFAULT 1.0
);

-- Verification Queue (For Claim Workflow)
CREATE TABLE verification_queue (
    id SERIAL PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    verification_type VARCHAR(50) NOT NULL CHECK (verification_type IN ('claim', 'data_update', 'premium_upgrade', 'dispute')),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'in_review', 'approved', 'rejected', 'escalated')),
    submitted_by INTEGER,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_by INTEGER,
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    documents_provided JSONB,
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    priority INTEGER DEFAULT 50,
    due_date TIMESTAMP
);

-- API Integration Hooks / API Keys
CREATE TABLE api_integrations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    api_key_hash VARCHAR(255) NOT NULL,
    api_key_prefix VARCHAR(20),
    organization VARCHAR(200),
    contact_email VARCHAR(255),
    permissions JSONB NOT NULL DEFAULT '["read:public"]', -- Array of permissions
    rate_limit_requests INTEGER DEFAULT 1000,
    rate_limit_window VARCHAR(20) DEFAULT 'hourly', -- hourly, daily
    allowed_endpoints JSONB, -- NULL = all
    allowed_ips INET[], -- IP whitelist
    webhook_url VARCHAR(500),
    webhook_secret VARCHAR(255),
    last_used_at TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER
);

-- API Request Logging
CREATE TABLE api_logs (
    id BIGSERIAL PRIMARY KEY,
    integration_id INTEGER REFERENCES api_integrations(id) ON DELETE SET NULL,
    endpoint VARCHAR(500) NOT NULL,
    method VARCHAR(10) NOT NULL,
    params JSONB,
    response_status INTEGER,
    response_time_ms INTEGER,
    ip_address INET,
    user_agent TEXT,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scheduled Update Queue (For Cadence Tracking)
CREATE TABLE scheduled_updates (
    id SERIAL PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    scheduled_for TIMESTAMP NOT NULL,
    priority INTEGER DEFAULT 50,
    update_type VARCHAR(50) DEFAULT 'full_refresh' CHECK (update_type IN ('full_refresh', 'reviews_only', 'hours_only', 'verification_check')),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'failed', 'skipped')),
    assigned_to_worker VARCHAR(100),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    result_data JSONB
);

-- Search Index (For Full-Text Search)
CREATE TABLE search_index (
    id SERIAL PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    search_vector tsvector, -- PostgreSQL full-text search
    search_text TEXT,
    keywords TEXT[],
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(business_id)
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Business search indexes
CREATE INDEX idx_businesses_verification ON businesses(verification_status);
CREATE INDEX idx_businesses_status ON businesses(status);
CREATE INDEX idx_businesses_region ON businesses(region_id);
CREATE INDEX idx_businesses_geohash ON businesses(geohash);
CREATE INDEX idx_businesses_coordinates ON businesses(latitude, longitude);
CREATE INDEX idx_businesses_freshness ON businesses(data_freshness_score);
CREATE INDEX idx_businesses_last_verified ON businesses(last_verified_at);
CREATE INDEX idx_businesses_review_score ON businesses(review_score_weighted);
CREATE INDEX idx_businesses_slug ON businesses(slug);
CREATE INDEX idx_businesses_uuid ON businesses(uuid);
CREATE INDEX idx_businesses_naics ON businesses(naics_code);
CREATE INDEX idx_businesses_duns ON businesses(duns_number);

-- Composite indexes for common queries
CREATE INDEX idx_businesses_region_verification ON businesses(region_id, verification_status);
CREATE INDEX idx_businesses_region_rating ON businesses(region_id, review_score_weighted);
CREATE INDEX idx_businesses_staleness ON businesses(next_scheduled_update, data_freshness_score);

-- Category indexes
CREATE INDEX idx_categories_parent ON categories(parent_id);
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_naics ON categories(naics_code);

-- Business-Category relationship indexes
CREATE INDEX idx_business_categories_business ON business_categories(business_id);
CREATE INDEX idx_business_categories_category ON business_categories(category_id);
CREATE INDEX idx_business_categories_primary ON business_categories(business_id, is_primary);

-- Competitive intelligence indexes
CREATE INDEX idx_service_rel_business ON service_relationships(business_id);
CREATE INDEX idx_service_rel_provider ON service_relationships(provider_id);
CREATE INDEX idx_service_rel_type ON service_relationships(relationship_type);

-- Update tracking indexes
CREATE INDEX idx_update_history_business ON update_history(business_id);
CREATE INDEX idx_update_history_date ON update_history(performed_at);
CREATE INDEX idx_update_history_batch ON update_history(update_batch_id);

-- Scheduled update indexes
CREATE INDEX idx_scheduled_updates_date ON scheduled_updates(scheduled_for);
CREATE INDEX idx_scheduled_updates_status ON scheduled_updates(status);

-- Full-text search index (PostgreSQL)
CREATE INDEX idx_search_vector ON search_index USING GIN(search_vector);

-- ============================================
-- VIEWS
-- ============================================

-- Stale Data Report View
CREATE VIEW stale_data_report AS
SELECT 
    b.id,
    b.name,
    b.verification_status,
    b.last_verified_at,
    b.next_scheduled_update,
    b.data_freshness_score,
    CASE 
        WHEN b.next_scheduled_update < NOW() THEN 'overdue'
        WHEN b.next_scheduled_update < NOW() + INTERVAL '7 days' THEN 'due_soon'
        ELSE 'current'
    END as update_status,
    NOW() - b.last_verified_at as days_since_verified
FROM businesses b
WHERE b.status = 'active';

-- Competitive Intelligence Summary View
CREATE VIEW competitor_summary AS
SELECT 
    b.id as business_id,
    b.name as business_name,
    c.id as category_id,
    c.name as category_name,
    COUNT(DISTINCT sr.provider_id) as competitor_count,
    AVG(sr.relationship_strength) as avg_competition_strength,
    json_agg(DISTINCT jsonb_build_object(
        'competitor_id', comp.id,
        'competitor_name', comp.name,
        'strength', sr.relationship_strength
    )) as top_competitors
FROM businesses b
JOIN business_categories bc ON b.id = bc.business_id AND bc.is_primary = TRUE
JOIN categories c ON bc.category_id = c.id
LEFT JOIN service_relationships sr ON b.id = sr.business_id AND sr.relationship_type = 'competitor'
LEFT JOIN businesses comp ON sr.provider_id = comp.id
GROUP BY b.id, b.name, c.id, c.name;

-- ============================================
-- FUNCTIONS & TRIGGERS
-- ============================================

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update timestamp triggers
CREATE TRIGGER update_businesses_updated_at BEFORE UPDATE ON businesses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_regions_updated_at BEFORE UPDATE ON regions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_service_rel_updated_at BEFORE UPDATE ON service_relationships
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Calculate data freshness score
CREATE OR REPLACE FUNCTION calculate_freshness_score()
RETURNS TRIGGER AS $$
DECLARE
    days_since_update INTEGER;
    staleness_penalty INTEGER;
BEGIN
    -- Calculate days since last verification
    days_since_update := EXTRACT(DAY FROM (NOW() - COALESCE(NEW.last_verified_at, NEW.created_at)));
    
    -- Calculate penalty based on update frequency
    CASE NEW.update_frequency
        WHEN 'daily' THEN staleness_penalty := days_since_update * 10;
        WHEN 'weekly' THEN staleness_penalty := days_since_update * 3;
        WHEN 'monthly' THEN staleness_penalty := days_since_update;
        WHEN 'quarterly' THEN staleness_penalty := days_since_update / 3;
        ELSE staleness_penalty := days_since_update / 7;
    END CASE;
    
    -- Update freshness score (max 100)
    NEW.data_freshness_score := GREATEST(0, 100 - LEAST(100, staleness_penalty));
    
    -- Set next scheduled update if not set
    IF NEW.next_scheduled_update IS NULL THEN
        CASE NEW.update_frequency
            WHEN 'daily' THEN NEW.next_scheduled_update := NOW() + INTERVAL '1 day';
            WHEN 'weekly' THEN NEW.next_scheduled_update := NOW() + INTERVAL '7 days';
            WHEN 'monthly' THEN NEW.next_scheduled_update := NOW() + INTERVAL '1 month';
            WHEN 'quarterly' THEN NEW.next_scheduled_update := NOW() + INTERVAL '3 months';
            ELSE NEW.next_scheduled_update := NOW() + INTERVAL '1 month';
        END CASE;
    END IF;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER calculate_business_freshness BEFORE INSERT OR UPDATE OF last_verified_at, update_frequency ON businesses
    FOR EACH ROW EXECUTE FUNCTION calculate_freshness_score();

-- Log changes to update_history
CREATE OR REPLACE FUNCTION log_business_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        -- Log key field changes
        IF OLD.name IS DISTINCT FROM NEW.name THEN
            INSERT INTO update_history (business_id, table_name, record_id, field_name, old_value, new_value, update_type, performed_at)
            VALUES (NEW.id, 'businesses', NEW.id, 'name', OLD.name, NEW.name, 'automatic', NOW());
        END IF;
        
        IF OLD.phone_primary IS DISTINCT FROM NEW.phone_primary THEN
            INSERT INTO update_history (business_id, table_name, record_id, field_name, old_value, new_value, update_type, performed_at)
            VALUES (NEW.id, 'businesses', NEW.id, 'phone_primary', OLD.phone_primary, NEW.phone_primary, 'automatic', NOW());
        END IF;
        
        IF OLD.address_street IS DISTINCT FROM NEW.address_street THEN
            INSERT INTO update_history (business_id, table_name, record_id, field_name, old_value, new_value, update_type, performed_at)
            VALUES (NEW.id, 'businesses', NEW.id, 'address_street', OLD.address_street, NEW.address_street, 'automatic', NOW());
        END IF;
        
        IF OLD.verification_status IS DISTINCT FROM NEW.verification_status THEN
            INSERT INTO update_history (business_id, table_name, record_id, field_name, old_value, new_value, update_type, performed_at)
            VALUES (NEW.id, 'businesses', NEW.id, 'verification_status', OLD.verification_status, NEW.verification_status, 'automatic', NOW());
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER log_business_changes_trigger AFTER UPDATE ON businesses
    FOR EACH ROW EXECUTE FUNCTION log_business_changes();

-- Geohash generation function (simplified - production would use PostGIS)
CREATE OR REPLACE FUNCTION update_geohash()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
        -- Simplified geohash - in production use proper geohash library
        NEW.geohash := substring(
            encode(digest(
                NEW.latitude::text || ',' || NEW.longitude::text, 'sha256'
            ), 'hex') from 1 for 12
        );
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- ============================================
-- INITIAL DATA INSERTS
-- ============================================

-- Insert root region (for testing)
INSERT INTO regions (name, slug, type, country_code, is_active) VALUES
    ('United States', 'united-states', 'country', 'US', TRUE),
    ('Canada', 'canada', 'country', 'CA', TRUE);

-- ============================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================

COMMENT ON TABLE businesses IS 'Core business listings table with verification and enrichment data';
COMMENT ON COLUMN businesses.verification_status IS 'unclaimed|claimed_pending|claimed_verified|premium_verified';
COMMENT ON COLUMN businesses.data_freshness_score IS '0-100 score indicating data freshness based on update cadence';
COMMENT ON COLUMN businesses.geohash IS 'Geohash for efficient spatial indexing and queries';

COMMENT ON TABLE service_relationships IS 'Competitive intelligence: tracks relationships between businesses including competitors, suppliers, and partners';

COMMENT ON TABLE update_history IS 'Audit log for tracking all changes to business data for freshness monitoring';

COMMENT ON TABLE scheduled_updates IS 'Queue for tracking scheduled data refreshes based on update cadence';

COMMENT ON TABLE api_integrations IS 'API keys and webhook configurations for external integrations';
