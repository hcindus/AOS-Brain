const Database = require('better-sqlite3');
const path = require('path');
const { app } = require('electron');
const { v4: uuidv4 } = require('uuid');

class POSDatabase {
  constructor() {
    // Store database in user data directory
    const dbPath = path.join(app.getPath('userData'), 'reggiestart.db');
    this.db = new Database(dbPath);
    this.db.pragma('journal_mode = WAL');
  }

  initialize() {
    // Create products table
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        plu TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT,
        stock INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Create transactions table
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS transactions (
        id TEXT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        items TEXT NOT NULL,
        subtotal REAL NOT NULL,
        tax REAL NOT NULL,
        total REAL NOT NULL,
        payment_method TEXT NOT NULL,
        status TEXT DEFAULT 'completed'
      )
    `);

    // Create settings table
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
      )
    `);

    // Create indexes
    this.db.exec(`CREATE INDEX IF NOT EXISTS idx_products_plu ON products(plu)`);
    this.db.exec(`CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)`);
    this.db.exec(`CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp)`);
  }

  // Product operations
  getAllProducts() {
    return this.db.prepare('SELECT * FROM products ORDER BY name').all();
  }

  getProductByPLU(plu) {
    return this.db.prepare('SELECT * FROM products WHERE plu = ?').get(plu);
  }

  getProductById(id) {
    return this.db.prepare('SELECT * FROM products WHERE id = ?').get(id);
  }

  addProduct(product) {
    const id = uuidv4();
    const stmt = this.db.prepare(`
      INSERT INTO products (id, plu, name, price, category, stock)
      VALUES (?, ?, ?, ?, ?, ?)
    `);
    stmt.run(id, product.plu, product.name, product.price, product.category, product.stock || 0);
    return id;
  }

  updateProduct(product) {
    const stmt = this.db.prepare(`
      UPDATE products 
      SET plu = ?, name = ?, price = ?, category = ?, stock = ?, updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `);
    stmt.run(product.plu, product.name, product.price, product.category, product.stock, product.id);
    return true;
  }

  deleteProduct(id) {
    const stmt = this.db.prepare('DELETE FROM products WHERE id = ?');
    stmt.run(id);
    return true;
  }

  getProductCount() {
    const result = this.db.prepare('SELECT COUNT(*) as count FROM products').get();
    return result.count;
  }

  // Transaction operations
  saveTransaction(transaction) {
    const id = uuidv4();
    const stmt = this.db.prepare(`
      INSERT INTO transactions (id, items, subtotal, tax, total, payment_method)
      VALUES (?, ?, ?, ?, ?, ?)
    `);
    stmt.run(
      id,
      JSON.stringify(transaction.items),
      transaction.subtotal,
      transaction.tax,
      transaction.total,
      transaction.paymentMethod
    );
    
    // Update stock for each item
    transaction.items.forEach(item => {
      if (item.plu) {
        this.db.prepare(`
          UPDATE products SET stock = stock - ?, updated_at = CURRENT_TIMESTAMP
          WHERE plu = ?
        `).run(item.quantity, item.plu);
      }
    });
    
    return id;
  }

  getRecentTransactions(limit = 100) {
    return this.db.prepare(`
      SELECT * FROM transactions 
      ORDER BY timestamp DESC 
      LIMIT ?
    `).all(limit);
  }

  getDailyReport(date) {
    const startOfDay = date + ' 00:00:00';
    const endOfDay = date + ' 23:59:59';
    
    const transactions = this.db.prepare(`
      SELECT * FROM transactions 
      WHERE timestamp BETWEEN ? AND ?
      ORDER BY timestamp DESC
    `).all(startOfDay, endOfDay);
    
    const summary = this.db.prepare(`
      SELECT 
        COUNT(*) as transaction_count,
        SUM(total) as total_sales,
        SUM(tax) as total_tax,
        SUM(subtotal) as total_subtotal,
        payment_method,
        COUNT(*) as method_count
      FROM transactions 
      WHERE timestamp BETWEEN ? AND ?
      GROUP BY payment_method
    `).all(startOfDay, endOfDay);
    
    return { transactions, summary };
  }

  // Settings operations
  getSetting(key) {
    const result = this.db.prepare('SELECT value FROM settings WHERE key = ?').get(key);
    return result ? result.value : null;
  }

  setSetting(key, value) {
    const stmt = this.db.prepare(`
      INSERT INTO settings (key, value) VALUES (?, ?)
      ON CONFLICT(key) DO UPDATE SET value = excluded.value
    `);
    stmt.run(key, value);
    return true;
  }

  // Export all data
  exportAll() {
    return {
      products: this.getAllProducts(),
      transactions: this.getRecentTransactions(10000),
      settings: this.db.prepare('SELECT * FROM settings').all(),
      exportedAt: new Date().toISOString()
    };
n  }

  close() {
    this.db.close();
  }
}

module.exports = POSDatabase;
