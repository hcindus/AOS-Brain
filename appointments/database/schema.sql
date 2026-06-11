-- PSD Appointments Database Schema
-- Separate from DepotChaos unified.db

-- Core appointments table
CREATE TABLE IF NOT EXISTS appointments (
    id TEXT PRIMARY KEY,
    lead_id INTEGER,                    -- FK to DepotChaos leads (logical)
    customer_name TEXT NOT NULL,
    customer_email TEXT,
    customer_phone TEXT,
    service_type TEXT DEFAULT 'consultation',  -- consultation, demo, callback, install
    scheduled_at TIMESTAMP NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    status TEXT DEFAULT 'confirmed',   -- confirmed, completed, cancelled, no_show
    notes TEXT,
    created_by TEXT,                   -- User ID from auth system
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    google_event_id TEXT,              -- Google Calendar event ID
    reminder_sent BOOLEAN DEFAULT 0,
    FOREIGN KEY (lead_id) REFERENCES leads(id) DEFERRABLE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(date(scheduled_at));
CREATE INDEX IF NOT EXISTS idx_appointments_status ON appointments(status);
CREATE INDEX IF NOT EXISTS idx_appointments_lead ON appointments(lead_id);

-- Availability slots table
CREATE TABLE IF NOT EXISTS availability_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot_date DATE NOT NULL,
    slot_time TIME NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    is_available BOOLEAN DEFAULT 1,
    appointment_id TEXT,
    buffer_before INTEGER DEFAULT 15,   -- Buffer time before slot
    buffer_after INTEGER DEFAULT 15,    -- Buffer time after slot
    recurring_pattern TEXT,              -- For recurring slots: daily, weekly, etc
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_slots_date ON availability_slots(slot_date);
CREATE INDEX IF NOT EXISTS idx_slots_available ON availability_slots(is_available);

-- Google Calendar sync tokens
CREATE TABLE IF NOT EXISTS google_sync_tokens (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    credential_json TEXT,              -- Encrypted OAuth credentials
    refresh_token TEXT,
    calendar_id TEXT DEFAULT 'primary',
    last_sync_at TIMESTAMP,
    next_sync_token TEXT,                -- For incremental sync
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sync queue for async operations
CREATE TABLE IF NOT EXISTS sync_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation TEXT NOT NULL,             -- create, update, delete
    appointment_id TEXT,
    google_event_id TEXT,
    status TEXT DEFAULT 'pending',       -- pending, synced, failed
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sync_status ON sync_queue(status);

-- Mobile app sessions
CREATE TABLE IF NOT EXISTS mobile_sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    device_fingerprint TEXT,
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP,
    device_type TEXT,                    -- android, ios, web
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sessions_user ON mobile_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON mobile_sessions(access_token);

-- Notifications log
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id TEXT,
    type TEXT,                           -- reminder, confirmation, cancellation
    channel TEXT,                        -- email, sms, push
    status TEXT DEFAULT 'pending',       -- pending, sent, failed
    sent_at TIMESTAMP,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE
);

-- Service types configuration
CREATE TABLE IF NOT EXISTS service_types (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    color TEXT,                          -- Hex color for calendar display
    description TEXT,
    requires_lead BOOLEAN DEFAULT 1,      -- Whether this service requires a lead
    active BOOLEAN DEFAULT 1
);

-- Insert default service types
INSERT OR IGNORE INTO service_types (id, name, duration_minutes, color, description) VALUES
('consultation', 'Initial Consultation', 60, '#4CAF50', 'First meeting to discuss needs'),
('demo', 'Product Demo', 90, '#2196F3', 'Full POS system demonstration'),
('callback', 'Follow-up Call', 30, '#FF9800', 'Scheduled follow-up conversation'),
('install', 'Installation', 180, '#9C27B0', 'POS system installation and training'),
('training', 'Training Session', 120, '#00BCD4', 'Staff training on POS system'),
('support', 'Technical Support', 60, '#795548', 'Technical support appointment');

-- User preferences (for mobile app)
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id TEXT PRIMARY KEY,
    notification_email BOOLEAN DEFAULT 1,
    notification_sms BOOLEAN DEFAULT 0,
    notification_push BOOLEAN DEFAULT 1,
    default_calendar_view TEXT DEFAULT 'week', -- day, week, month
    working_hours_start TIME DEFAULT '09:00',
    working_hours_end TIME DEFAULT '17:00',
    timezone TEXT DEFAULT 'UTC',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log for compliance
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    record_id TEXT NOT NULL,
    action TEXT NOT NULL,                -- INSERT, UPDATE, DELETE
    old_values TEXT,                     -- JSON
    new_values TEXT,                     -- JSON
    user_id TEXT,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_record ON audit_log(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at);
