-- ============================================================
-- AGI IDENTITY PLATFORM - SECURITY LAYER
-- Part A: RLS (Row Level Security) + Triggers
-- Version: 1.1.0
-- Updated: 2026-05-23
-- ============================================================

-- ============================================================
-- 1. RLS SETUP
-- ============================================================

-- Enable RLS on core tables
ALTER TABLE identity ENABLE ROW LEVEL SECURITY;
ALTER TABLE stage_event ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_markers ENABLE ROW LEVEL SECURITY;
ALTER TABLE deletion_requests ENABLE ROW LEVEL SECURITY;

-- Force RLS for table owners too (important!)
ALTER TABLE identity FORCE ROW LEVEL SECURITY;
ALTER TABLE stage_event FORCE ROW LEVEL SECURITY;
ALTER TABLE data_markers FORCE ROW LEVEL SECURITY;

-- ============================================================
-- 2. RLS POLICIES - USER ISOLATION
-- ============================================================

-- Policy: Users can only see their own identity row
CREATE POLICY identity_user_isolation ON identity
 FOR ALL
 USING (identity_id = current_setting('app.current_user_id')::UUID);

-- Policy: Users can only see stage events for their identity
CREATE POLICY stage_event_user_isolation ON stage_event
 FOR ALL
 USING (
   identity_id IN (
     SELECT identity_id
     FROM identity
     WHERE identity_id = current_setting('app.current_user_id')::UUID
   )
 );

-- Policy: Users can only see markers for their events
CREATE POLICY data_markers_user_isolation ON data_markers
 FOR ALL
 USING (
   event_id IN (
     SELECT se.event_id
     FROM stage_event se
     WHERE se.identity_id = current_setting('app.current_user_id')::UUID
   )
 );

-- Policy: Users can only see their own deletion requests
CREATE POLICY deletion_request_user_isolation ON deletion_requests
 FOR ALL
 USING (
   user_id IN (
     SELECT u.id
     FROM users u
     WHERE u.identity_id = current_setting('app.current_user_id')::UUID
   )
 );

-- ============================================================
-- 3. ETL ROLE BYPASS (for connectors)
-- ============================================================

-- Create ETL role that can bypass RLS for ingestion
CREATE ROLE identity_etl WITH NOLOGIN;

-- Grant ETL role bypass RLS
ALTER TABLE identity OWNER TO identity_etl;
ALTER TABLE stage_event OWNER TO identity_etl;
ALTER TABLE data_markers OWNER TO identity_etl;

-- Policy: ETL role can insert/update (bypasses RLS)
CREATE POLICY identity_etl_insert ON identity
 FOR INSERT
 TO identity_etl
 WITH CHECK (true);

CREATE POLICY stage_event_etl_insert ON stage_event
 FOR INSERT
 TO identity_etl
 WITH CHECK (true);

CREATE POLICY data_markers_etl_insert ON data_markers
 FOR INSERT
 TO identity_etl
 WITH CHECK (true);

-- ============================================================
-- 4. TRIGGERS
-- ============================================================

-- Function: Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
 NEW.updated_at = NOW();
 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
CREATE TRIGGER trg_identity_updated
 BEFORE UPDATE ON identity
 FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_stage_event_updated
 BEFORE UPDATE ON stage_event
 FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_users_updated
 BEFORE UPDATE ON users
 FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_connectors_updated
 BEFORE UPDATE ON connectors
 FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ============================================================
-- 5. AUDIT LOGGING TRIGGERS
-- ============================================================

-- Function: Log all data changes
CREATE OR REPLACE FUNCTION audit_data_change()
RETURNS TRIGGER AS $$
BEGIN
 INSERT INTO audit_log (
   user_id,
   action,
   resource_type,
   resource_id,
   accessed_by,
   accessed_at,
   legal_basis
 ) VALUES (
   current_setting('app.current_user_id')::UUID,
   TG_OP,  -- INSERT, UPDATE, DELETE
   TG_TABLE_NAME,
   CASE
     WHEN TG_OP = 'DELETE' THEN OLD.event_id
     ELSE NEW.event_id
   END,
   current_user,
   NOW(),
   'legitimate_interest'
 );
 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to data_markers (sensitive data changes)
CREATE TRIGGER trg_data_markers_audit
 AFTER INSERT OR UPDATE OR DELETE ON data_markers
 FOR EACH ROW EXECUTE FUNCTION audit_data_change();

-- Apply to identity (core identity changes)
CREATE TRIGGER trg_identity_audit
 AFTER UPDATE OR DELETE ON identity
 FOR EACH ROW EXECUTE FUNCTION audit_data_change();

-- ============================================================
-- 6. ENCRYPTION TRIGGER
-- ============================================================

-- Function: Auto-encrypt sensitive marker values
CREATE OR REPLACE FUNCTION encrypt_marker_value()
RETURNS TRIGGER AS $$
BEGIN
 IF NEW.marker_value_encrypted IS NULL AND NEW.marker_value_plain IS NOT NULL THEN
   NEW.marker_value_encrypted = pgp_sym_encrypt(
     NEW.marker_value_plain,
     current_setting('app.encryption_key')
   );
   NEW.marker_value_plain = NULL;  -- Clear plaintext
 END IF;
 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to data_markers
CREATE TRIGGER trg_data_markers_encrypt
 BEFORE INSERT OR UPDATE ON data_markers
 FOR EACH ROW EXECUTE FUNCTION encrypt_marker_value();

-- ============================================================
-- 7. STAGING TABLE (ETL Pattern)
-- ============================================================

CREATE TABLE staging_raw_documents (
 staging_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
 identity_id UUID REFERENCES identity(identity_id),
 source_system VARCHAR(128) NOT NULL, -- 'ANNUAL_CREDIT_REPORT', 'HAVE_I_BEEN_PWNED'
 raw_payload JSONB NOT NULL,
 ingested_at TIMESTAMP DEFAULT NOW(),
 processed_at TIMESTAMP NULL,
 process_status VARCHAR(32) DEFAULT 'PENDING', -- 'PENDING','PROCESSING','DONE','ERROR'
 error_message TEXT NULL,
 retry_count INTEGER DEFAULT 0
);

-- Indexes for ETL performance
CREATE INDEX idx_staging_source_status ON staging_raw_documents(source_system, process_status);
CREATE INDEX idx_staging_identity ON staging_raw_documents(identity_id);
CREATE INDEX idx_staging_ingested ON staging_raw_documents(ingested_at);

-- RLS for staging (users can only see their own)
ALTER TABLE staging_raw_documents ENABLE ROW LEVEL SECURITY;
CREATE POLICY staging_user_isolation ON staging_raw_documents
 FOR ALL
 USING (identity_id = current_setting('app.current_user_id')::UUID);

-- ============================================================
-- 8. ETL HELPER FUNCTIONS
-- ============================================================

-- Function: Create financial credit event (Stage 5)
CREATE OR REPLACE FUNCTION create_financial_credit_event(
 p_identity_id UUID,
 p_event_date DATE,
 p_source_system VARCHAR,
 p_confidence DECIMAL,
 p_markers JSONB
) RETURNS UUID AS $$
DECLARE
 v_event_id UUID;
 v_marker RECORD;
BEGIN
 -- Create stage_event
 INSERT INTO stage_event (identity_id, stage_code, event_date, source_system, confidence_score)
 VALUES (p_identity_id, '05_FINANCIAL_CREDIT', p_event_date, p_source_system, p_confidence)
 RETURNING event_id INTO v_event_id;

 -- Create data_markers from JSON
 FOR v_marker IN
   SELECT key, value::text as val
   FROM jsonb_each(p_markers)
 LOOP
   INSERT INTO data_markers (event_id, marker_key, marker_value_encrypted, pii_classification)
   VALUES (
     v_event_id,
     v_marker.key,
     pgp_sym_encrypt(v_marker.val, current_setting('app.encryption_key')),
     'HIGH'
   );
 END LOOP;

 RETURN v_event_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Create digital breach event (Stage 8)
CREATE OR REPLACE FUNCTION create_digital_breach_event(
 p_identity_id UUID,
 p_event_date DATE,
 p_source_system VARCHAR,
 p_confidence DECIMAL,
 p_markers JSONB
) RETURNS UUID AS $$
DECLARE
 v_event_id UUID;
 v_marker RECORD;
BEGIN
 INSERT INTO stage_event (identity_id, stage_code, event_date, source_system, confidence_score)
 VALUES (p_identity_id, '08_DIGITAL_BREACH', p_event_date, p_source_system, p_confidence)
 RETURNING event_id INTO v_event_id;

 FOR v_marker IN
   SELECT key, value::text as val
   FROM jsonb_each(p_markers)
 LOOP
   INSERT INTO data_markers (event_id, marker_key, marker_value_encrypted, pii_classification)
   VALUES (
     v_event_id,
     v_marker.key,
     pgp_sym_encrypt(v_marker.val, current_setting('app.encryption_key')),
     'HIGH'
   );
 END LOOP;

 RETURN v_event_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Mark staging document as processed
CREATE OR REPLACE FUNCTION mark_staging_processed(
 p_staging_id UUID,
 p_status VARCHAR DEFAULT 'DONE',
 p_error_message TEXT DEFAULT NULL
) RETURNS VOID AS $$
BEGIN
 UPDATE staging_raw_documents
 SET 
   process_status = p_status,
   processed_at = NOW(),
   error_message = p_error_message
 WHERE staging_id = p_staging_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- 9. SESSION CONFIGURATION HELPERS
-- ============================================================

-- Function: Set current user for RLS
CREATE OR REPLACE FUNCTION set_app_user(p_user_id UUID)
RETURNS VOID AS $$
BEGIN
 PERFORM set_config('app.current_user_id', p_user_id::text, false);
END;
$$ LANGUAGE plpgsql;

-- Function: Set encryption key for session
CREATE OR REPLACE FUNCTION set_encryption_key(p_key TEXT)
RETURNS VOID AS $$
BEGIN
 PERFORM set_config('app.encryption_key', p_key, false);
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- 10. USAGE EXAMPLES
-- ============================================================

-- Example: Set user context (must run before queries)
-- SELECT set_app_user('550e8400-e29b-41d4-a716-446655440000'::UUID);
-- SELECT set_encryption_key('your-256-bit-key-here');

-- Example: Create financial credit event
/*
SELECT create_financial_credit_event(
 '550e8400-e29b-41d4-a716-446655440000'::UUID,
 '2025-01-10'::DATE,
 'ANNUAL_CREDIT_REPORT',
 0.95,
 '{
   "creditor_name": "CHASE BANK",
   "account_type": "CREDIT_CARD",
   "opened_date": "2018-03-01",
   "credit_limit": "15000",
   "balance": "3200"
 }'::jsonb
);
*/

-- Example: Query with RLS (automatic filtering)
-- SELECT * FROM stage_event; -- Only shows current user's events

-- Example: ETL batch processing
/*
SELECT * FROM staging_raw_documents
WHERE source_system = 'ANNUAL_CREDIT_REPORT'
 AND process_status = 'PENDING'
LIMIT 100;
*/

-- ============================================================
-- NOTES
-- ============================================================
--
-- 1. RLS requires setting app.current_user_id before every query
-- 2. ETL role bypasses RLS for ingestion
-- 3. All markers auto-encrypt via trigger
-- 4. Audit logging captures all data changes
-- 5. Staging table enables async ETL processing
--
