-- PSD Tier System Backup - 2026-05-11
-- Performance Supply Depot Customer Tier Configuration
-- 
-- To restore: sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db < tier_system_backup_20260511.sql

-- Schema for tier column (if not exists)
-- ALTER TABLE psd_customers ADD COLUMN tier TEXT;

-- ========================================
-- TIER DEFINITIONS (from tier_system.json)
-- ========================================
-- Tier      | Spend Range      | Level | Description
-- Stone     | $0 - $4,999      | 1     | Supply-only accounts
-- Bronze    | $5K - $9,999      | 2     | PPCL - Price Conscious
-- Silver    | $10K - $24,999    | 3     | Prime - Standard tier
-- Gold      | $25K - $49,999    | 4     | Spot On Target - High potential
-- Platinum  | $50K - $99,999    | 5     | Top 165 - Priority accounts
-- Diamond   | $100K+            | 6     | VIP Elite - Highest value

-- ========================================
-- TIER CATEGORIZATION SQL (REVENUE-BASED)
-- ========================================

-- Reset all tiers first
UPDATE psd_customers SET tier = NULL;

-- Stone: <$5,000 (supply-only accounts)
UPDATE psd_customers SET tier = 'stone' WHERE id IN (
    SELECT c.id FROM psd_customers c 
    LEFT JOIN psd_customer_sales s ON c.id = s.customer_id 
    GROUP BY c.id HAVING COALESCE(SUM(s.amount), 0) < 5000
);

-- Bronze (PPCL): $5,000 - $9,999
UPDATE psd_customers SET tier = 'bronze' WHERE id IN (
    SELECT c.id FROM psd_customers c 
    LEFT JOIN psd_customer_sales s ON c.id = s.customer_id 
    GROUP BY c.id HAVING COALESCE(SUM(s.amount), 0) >= 5000 AND COALESCE(SUM(s.amount), 0) < 10000
);

-- Silver (Prime): $10,000 - $24,999
UPDATE psd_customers SET tier = 'silver' WHERE id IN (
    SELECT c.id FROM psd_customers c 
    LEFT JOIN psd_customer_sales s ON c.id = s.customer_id 
    GROUP BY c.id HAVING COALESCE(SUM(s.amount), 0) >= 10000 AND COALESCE(SUM(s.amount), 0) < 25000
);

-- Gold (Spot On Target): $25,000 - $49,999
UPDATE psd_customers SET tier = 'gold' WHERE id IN (
    SELECT c.id FROM psd_customers c 
    LEFT JOIN psd_customer_sales s ON c.id = s.customer_id 
    GROUP BY c.id HAVING COALESCE(SUM(s.amount), 0) >= 25000 AND COALESCE(SUM(s.amount), 0) < 50000
);

-- Platinum (Top 165): $50,000 - $99,999
UPDATE psd_customers SET tier = 'platinum' WHERE id IN (
    SELECT c.id FROM psd_customers c 
    LEFT JOIN psd_customer_sales s ON c.id = s.customer_id 
    GROUP BY c.id HAVING COALESCE(SUM(s.amount), 0) >= 50000 AND COALESCE(SUM(s.amount), 0) < 100000
);

-- Diamond (VIP Elite): $100,000+
UPDATE psd_customers SET tier = 'diamond' WHERE id IN (
    SELECT c.id FROM psd_customers c 
    LEFT JOIN psd_customer_sales s ON c.id = s.customer_id 
    GROUP BY c.id HAVING COALESCE(SUM(s.amount), 0) >= 100000
);

-- ========================================
-- VERIFICATION QUERIES
-- ========================================

-- Check distribution
-- SELECT tier, COUNT(*), SUM(spend) as total_revenue
-- FROM (
--     SELECT c.id, c.tier, COALESCE(SUM(s.amount), 0) as spend
--     FROM psd_customers c
--     LEFT JOIN psd_customer_sales s ON c.id = s.customer_id
--     GROUP BY c.id
-- )
-- GROUP BY tier;

-- Check min/max/average spend
-- SELECT MIN(total_spend), MAX(total_spend), AVG(total_spend)
-- FROM (
--     SELECT c.id, COALESCE(SUM(s.amount), 0) as total_spend
--     FROM psd_customers c
--     LEFT JOIN psd_customer_sales s ON c.id = s.customer_id
--     GROUP BY c.id
-- );

-- ========================================
-- BACKUP INFO
-- ========================================
-- Date: 2026-05-11 21:30 UTC
-- Database: /root/.openclaw/workspace/data/depot_chaos/unified.db
-- Total Customers: 501
-- Distribution after categorization:
--   - Stone:    395 customers (avg spend ~$3,100)
--   - Bronze:   105 customers (PPCL tier)
--   - Silver:     1 customer  (Prime tier)
--   - Gold:       0 customers (Spot On Target)
--   - Platinum:   0 customers (Top 165)
--   - Diamond:    0 customers (VIP Elite)
