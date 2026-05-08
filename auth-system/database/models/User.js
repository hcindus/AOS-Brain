const db = require('../db');
const { v4: uuidv4 } = require('uuid');

class User {
    static async findByEmail(email) {
        return new Promise((resolve, reject) => {
            db.get(
                'SELECT * FROM users WHERE email = ?',
                [email.toLowerCase().trim()],
                (err, row) => {
                    if (err) reject(err);
                    else resolve(row);
                }
            );
        });
    }

    static async findById(id) {
        return new Promise((resolve, reject) => {
            db.get(
                'SELECT id, email, mfa_enabled, email_verified, created_at, last_login FROM users WHERE id = ?',
                [id],
                (err, row) => {
                    if (err) reject(err);
                    else resolve(row);
                }
            );
        });
    }

    static async create(email, passwordHash) {
        const id = uuidv4();
        return new Promise((resolve, reject) => {
            db.run(
                `INSERT INTO users (id, email, password_hash) VALUES (?, ?, ?)`,
                [id, email.toLowerCase().trim(), passwordHash],
                (err) => {
                    if (err) reject(err);
                    else resolve({ id, email });
                }
            );
        });
    }

    static async updateMFA(userId, secret, enabled = false) {
        return new Promise((resolve, reject) => {
            db.run(
                'UPDATE users SET mfa_secret = ?, mfa_enabled = ?, mfa_verified = ? WHERE id = ?',
                [secret, enabled ? 1 : 0, enabled ? 1 : 0, userId],
                (err) => {
                    if (err) reject(err);
                    else resolve();
                }
            );
        });
    }

    static async incrementFailedAttempts(userId) {
        return new Promise((resolve, reject) => {
            db.run(
                'UPDATE users SET failed_attempts = failed_attempts + 1 WHERE id = ?',
                [userId],
                (err) => {
                    if (err) reject(err);
                    else resolve();
                }
            );
        });
    }

    static async resetFailedAttempts(userId) {
        return new Promise((resolve, reject) => {
            db.run(
                'UPDATE users SET failed_attempts = 0, locked_until = NULL, last_login = CURRENT_TIMESTAMP WHERE id = ?',
                [userId],
                (err) => {
                    if (err) reject(err);
                    else resolve();
                }
            );
        });
    }

    static async lockAccount(userId, durationMinutes = 15) {
        const lockedUntil = new Date(Date.now() + durationMinutes * 60000).toISOString();
        return new Promise((resolve, reject) => {
            db.run(
                'UPDATE users SET locked_until = ? WHERE id = ?',
                [lockedUntil, userId],
                (err) => {
                    if (err) reject(err);
                    else resolve();
                }
            );
        });
    }

    static async updatePassword(userId, passwordHash) {
        return new Promise((resolve, reject) => {
            db.run(
                'UPDATE users SET password_hash = ?, password_changed_at = CURRENT_TIMESTAMP WHERE id = ?',
                [passwordHash, userId],
                (err) => {
                    if (err) reject(err);
                    else resolve();
                }
            );
        });
    }
}

module.exports = User;