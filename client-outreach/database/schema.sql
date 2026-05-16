-- Client Outreach Database Schema
-- Based on DepotChaos leads table, simplified for mobile CRM use

CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    company TEXT,
    business_type TEXT,
    city TEXT,
    state TEXT DEFAULT 'CA',
    tier TEXT DEFAULT 'Stone',
    status TEXT DEFAULT 'new',
    pos_system TEXT,
    replacement_score INTEGER,
    last_contact TEXT,
    next_contact TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS email_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    template TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT,
    status TEXT DEFAULT 'pending',
    scheduled_at TEXT,
    sent_at TEXT,
    error TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    type TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_clients_status ON clients(status);
CREATE INDEX IF NOT EXISTS idx_clients_tier ON clients(tier);
CREATE INDEX IF NOT EXISTS idx_clients_next_contact ON clients(next_contact);
CREATE INDEX IF NOT EXISTS idx_email_queue_status ON email_queue(status);
CREATE INDEX IF NOT EXISTS idx_activities_client ON activities(client_id);

-- Insert 5 demo clients
INSERT INTO clients (name, email, phone, company, business_type, city, state, tier, status, pos_system, replacement_score, last_contact, next_contact, notes) VALUES
('Sarah Chen', 'sarah@goldendragon.test', '626-555-0101', 'Golden Dragon Restaurant', 'Restaurant', 'Pasadena', 'CA', 'Prime', 'active', 'Aloha', 75, '2026-05-10', '2026-05-20', 'High-value prospect. Interested in POS upgrade next quarter.'),
('Mike Torres', 'mike@barriotacos.test', '323-555-0102', 'Barrio Tacos', 'Restaurant', 'Los Angeles', 'CA', 'PPCL', 'prospect', 'Square', 45, NULL, '2026-05-17', 'New lead from LA expo. Follow up on hardware needs.'),
('Lisa Park', 'lisa@seoulkitchen.test', '213-555-0103', 'Seoul Kitchen', 'Restaurant', 'Koreatown', 'CA', 'Stone', 'inactive', 'Toast', 25, '2026-03-15', NULL, 'Long-term client. On supply subscription only.'),
('Dave Kumar', 'dave@spiceroute.test', '310-555-0104', 'Spice Route', 'Restaurant', 'Santa Monica', 'CA', 'PPCL', 'follow-up', 'Clover', 60, '2026-05-12', '2026-05-19', 'Demo scheduled. Sent proposal, awaiting response.'),
('Emma Wilson', 'emma@coastalgrill.test', '949-555-0105', 'Coastal Grill', 'Restaurant', 'Newport Beach', 'CA', 'Prime', 'new', NULL, 85, NULL, '2026-05-16', 'Hot lead - 8yr old POS system, negative reviews about speed.');

-- Demo scheduled emails
INSERT INTO email_queue (client_id, template, subject, status, scheduled_at) VALUES
(1, 'follow_up', 'Quick check-in on your POS upgrade timeline', 'pending', '2026-05-18T09:00:00'),
(4, 'demo_reminder', 'Reminder: Your demo is tomorrow', 'pending', '2026-05-18T14:00:00'),
(5, 'intro', 'Welcome to Performance Supply Depot', 'pending', '2026-05-16T10:00:00');

-- Demo activity log
INSERT INTO activities (client_id, type, description) VALUES
(1, 'email_sent', 'Initial outreach sent - opened 2x'),
(1, 'call', 'Discovery call - interested in Q3 upgrade'),
(2, 'meeting', 'Met at LA Restaurant Expo booth'),
(4, 'demo_scheduled', 'Demo scheduled for May 19, 2pm'),
(5, 'lead_capture', 'Website form submission - POS upgrade inquiry');
