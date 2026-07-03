-- Add Mountain Mike's Pizza and Teriyaki Madness locations to DepotChaos
-- These are franchise chains - flagged for owner-operated verification

INSERT OR IGNORE INTO leads (business_name, city, state, business_type, category, source, scraped_at, status, tags) VALUES 
('Mountain Mikes Pizza - Sacramento', 'Sacramento', 'CA', 'Pizza Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,mountain_mikes'),
('Mountain Mikes Pizza - Elk Grove', 'Elk Grove', 'CA', 'Pizza Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,mountain_mikes'),
('Mountain Mikes Pizza - Folsom', 'Folsom', 'CA', 'Pizza Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,mountain_mikes'),
('Mountain Mikes Pizza - Roseville', 'Roseville', 'CA', 'Pizza Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,mountain_mikes'),
('Mountain Mikes Pizza - Davis', 'Davis', 'CA', 'Pizza Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,mountain_mikes'),
('Mountain Mikes Pizza - Woodland', 'Woodland', 'CA', 'Pizza Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,mountain_mikes'),
('Mountain Mikes Pizza - West Sacramento', 'West Sacramento', 'CA', 'Pizza Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,mountain_mikes'),
('Teriyaki Madness - Sacramento', 'Sacramento', 'CA', 'Fast Casual Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,teriyaki_madness'),
('Teriyaki Madness - Elk Grove', 'Elk Grove', 'CA', 'Fast Casual Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,teriyaki_madness'),
('Teriyaki Madness - Roseville', 'Roseville', 'CA', 'Fast Casual Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,teriyaki_madness'),
('Teriyaki Madness - Folsom', 'Folsom', 'CA', 'Fast Casual Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,teriyaki_madness'),
('Teriyaki Madness - Rancho Cordova', 'Rancho Cordova', 'CA', 'Fast Casual Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,teriyaki_madness'),
('Teriyaki Madness - Citrus Heights', 'Citrus Heights', 'CA', 'Fast Casual Restaurant', 'Restaurantes', 'manual_import', datetime('now'), 'new', 'franchise,teriyaki_madness');
