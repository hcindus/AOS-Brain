-- ============================================================
-- AGI IDENTITY PLATFORM - MARKER WHITELIST
-- Controls which data markers are exposed via GraphQL
-- Version: 1.0.0
-- ============================================================

CREATE TABLE marker_whitelist (
 marker_key VARCHAR(100) PRIMARY KEY,
 allowed_stages TEXT[] NOT NULL, -- e.g. '{05_FINANCIAL_CREDIT,08_DIGITAL_BREACH}'
 exposure_level VARCHAR(32) NOT NULL CHECK (exposure_level IN ('FULL', 'MASKED', 'AGGREGATE', 'HIDDEN')),
 description TEXT,
 created_at TIMESTAMP DEFAULT NOW(),
 updated_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast stage filtering
CREATE INDEX idx_whitelist_stages ON marker_whitelist USING GIN (allowed_stages);

-- ============================================================
-- DEFAULT WHITELIST ENTRIES
-- ============================================================

-- Stage 05: FINANCIAL_CREDIT
INSERT INTO marker_whitelist (marker_key, allowed_stages, exposure_level, description) VALUES
('creditor_name', '{05_FINANCIAL_CREDIT}', 'FULL', 'Name of credit grantor'),
('account_type', '{05_FINANCIAL_CREDIT}', 'FULL', 'Type of credit account'),
('opened_date', '{05_FINANCIAL_CREDIT}', 'FULL', 'Account opening date'),
('credit_limit', '{05_FINANCIAL_CREDIT}', 'MASKED', 'Credit limit (shows range)'),
('balance', '{05_FINANCIAL_CREDIT}', 'MASKED', 'Current balance (shows range)'),
('payment_status', '{05_FINANCIAL_CREDIT}', 'FULL', 'Current payment status'),
('account_number_masked', '{05_FINANCIAL_CREDIT}', 'FULL', 'Masked account number'),
('delinquency', '{05_FINANCIAL_CREDIT}', 'FULL', 'Delinquency status'),
('last_reported', '{05_FINANCIAL_CREDIT}', 'FULL', 'Date last reported to bureau');

-- Stage 08: DIGITAL_BREACH
INSERT INTO marker_whitelist (marker_key, allowed_stages, exposure_level, description) VALUES
('breach_name', '{08_DIGITAL_BREACH}', 'FULL', 'Name of data breach'),
('breach_date', '{08_DIGITAL_BREACH}', 'FULL', 'Date breach occurred'),
('data_classes', '{08_DIGITAL_BREACH}', 'FULL', 'Types of data exposed'),
('platform_name', '{08_DIGITAL_BREACH}', 'FULL', 'Platform/service breached'),
('notification_status', '{08_DIGITAL_BREACH}', 'FULL', 'Whether user was notified');

-- Stage 04: EMPLOYMENT
INSERT INTO marker_whitelist (marker_key, allowed_stages, exposure_level, description) VALUES
('employer_name', '{04_EMPLOYMENT}', 'FULL', 'Employer name'),
('employment_type', '{04_EMPLOYMENT}', 'FULL', 'W2, 1099, etc.'),
('start_date', '{04_EMPLOYMENT}', 'FULL', 'Employment start date'),
('end_date', '{04_EMPLOYMENT}', 'FULL', 'Employment end date'),
('industry_code', '{04_EMPLOYMENT}', 'AGGREGATE', 'Industry category only');

-- Stage 01: BIRTH_IDENTITY
INSERT INTO marker_whitelist (marker_key, allowed_stages, exposure_level, description) VALUES
('birth_certificate_no', '{01_BIRTH_IDENTITY}', 'HIDDEN', 'Not exposed via API'),
('issuing_jurisdiction', '{01_BIRTH_IDENTITY}', 'FULL', 'State/jurisdiction of birth'),
('hospital_name', '{01_BIRTH_IDENTITY}', 'MASKED', 'Hospital name (partial)'),
('ssn_last4', '{01_BIRTH_IDENTITY}', 'HIDDEN', 'Last 4 SSN - not exposed');

-- ============================================================
-- MASKING FUNCTIONS
-- ============================================================

-- Function: Mask credit card number
CREATE OR REPLACE FUNCTION mask_credit_card(plaintext TEXT)
RETURNS TEXT AS $$
BEGIN
 IF plaintext IS NULL THEN RETURN NULL; END IF;
 RETURN '****-****-****-' || RIGHT(regexp_replace(plaintext, '[^0-9]', '', 'g'), 4);
END;
$$ LANGUAGE plpgsql;

-- Function: Mask email
CREATE OR REPLACE FUNCTION mask_email(plaintext TEXT)
RETURNS TEXT AS $$
DECLARE
 parts TEXT[];
BEGIN
 IF plaintext IS NULL THEN RETURN NULL; END IF;
 parts = string_to_array(plaintext, '@');
 IF array_length(parts, 1) != 2 THEN RETURN '***@***'; END IF;
 RETURN LEFT(parts[1], 1) || '***@' || parts[2];
END;
$$ LANGUAGE plpgsql;

-- Function: Mask name
CREATE OR REPLACE FUNCTION mask_name(plaintext TEXT)
RETURNS TEXT AS $$
BEGIN
 IF plaintext IS NULL THEN RETURN NULL; END IF;
 RETURN LEFT(plaintext, 1) || REPEAT('*', LENGTH(plaintext) - 1);
END;
$$ LANGUAGE plpgsql;

-- Function: Mask to range (for amounts)
CREATE OR REPLACE FUNCTION mask_to_range(amount NUMERIC)
RETURNS TEXT AS $$
BEGIN
 IF amount IS NULL THEN RETURN NULL; END IF;
 IF amount < 1000 THEN RETURN '< $1,000';
 ELSIF amount < 5000 THEN RETURN '$1,000 - $4,999';
 ELSIF amount < 10000 THEN RETURN '$5,000 - $9,999';
 ELSIF amount < 50000 THEN RETURN '$10,000 - $49,999';
 ELSE RETURN '$50,000+';
 END IF;
END;
$$ LANGUAGE plpgsql;

-- Function: Apply appropriate masking based on marker key
CREATE OR REPLACE FUNCTION apply_masking(marker_key TEXT, plaintext TEXT)
RETURNS TEXT AS $$
BEGIN
 CASE
   WHEN marker_key LIKE '%credit_card%' THEN
     RETURN mask_credit_card(plaintext);
   WHEN marker_key LIKE '%email%' THEN
     RETURN mask_email(plaintext);
   WHEN marker_key LIKE '%name%' AND marker_key NOT LIKE '%_name_%' THEN
     RETURN mask_name(plaintext);
   WHEN marker_key IN ('credit_limit', 'balance', 'annual_income') THEN
     RETURN mask_to_range(plaintext::NUMERIC);
   ELSE
     RETURN plaintext;
 END CASE;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- WHITELIST QUERY FUNCTIONS
-- ============================================================

-- Function: Get allowed markers for stage
CREATE OR REPLACE FUNCTION get_allowed_markers(
 p_stage_code VARCHAR,
 p_exposure_levels TEXT[] DEFAULT '{FULL,MASKED}'
)
RETURNS TABLE(marker_key VARCHAR, exposure_level VARCHAR) AS $$
BEGIN
 RETURN QUERY
 SELECT w.marker_key, w.exposure_level
 FROM marker_whitelist w
 WHERE p_stage_code = ANY(w.allowed_stages)
   AND w.exposure_level = ANY(p_exposure_levels)
 ORDER BY w.marker_key;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- EXAMPLE USAGE
-- ============================================================

-- Get allowed markers for financial credit
-- SELECT * FROM get_allowed_markers('05_FINANCIAL_CREDIT');

-- Get all markers user can see (FULL + MASKED, not AGGREGATE/HIDDEN)
-- SELECT * FROM get_allowed_markers('05_FINANCIAL_CREDIT', '{FULL,MASKED}');

