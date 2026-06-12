/**
 * Miles Collections Module
 * Real implementation for Performance Supply Depot
 * 
 * Production-ready debt collection system
 * @version 1.0.0
 */

const fs = require('fs').promises;
const path = require('path');
const { EventEmitter } = require('events');

class MilesCollections extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = {
      dataDir: config.dataDir || '/root/.openclaw/workspace/miles-collections/data',
      templatesDir: config.templatesDir || '/root/.openclaw/workspace/miles-collections/templates',
      tier: config.tier || 'starter',
      ...config
    };
    
    this.workflows = new Map();
    this.initialized = false;
    
    // Ensure data directory exists
    this.initDataDir();
  }
  
  async initDataDir() {
    try {
      await fs.mkdir(this.config.dataDir, { recursive: true });
    } catch (err) {
      console.error('Failed to create data directory:', err);
    }
  }
  
  /**
   * Initialize the service
   */
  async init() {
    console.log(`[MilesCollections] Initializing (${this.config.tier} tier)...`);
    
    // Load existing accounts
    await this.loadAccounts();
    
    // Load workflows
    this.loadWorkflows();
    
    this.initialized = true;
    this.emit('ready');
    console.log(`[MilesCollections] Ready - ${this.config.tier} tier active`);
    
    return this;
  }
  
  /**
   * Load accounts from storage
   */
  async loadAccounts() {
    try {
      const files = await fs.readdir(this.config.dataDir);
      const accountFiles = files.filter(f => f.endsWith('.json'));
      
      for (const file of accountFiles) {
        const data = await fs.readFile(path.join(this.config.dataDir, file), 'utf8');
        const account = JSON.parse(data);
        this.workflows.set(account.id, account);
      }
      
      console.log(`[MilesCollections] Loaded ${this.workflows.size} accounts`);
    } catch (err) {
      console.log('[MilesCollections] No existing accounts found');
    }
  }
  
  /**
   * Save account to storage
   */
  async saveAccount(account) {
    const filepath = path.join(this.config.dataDir, `${account.id}.json`);
    await fs.writeFile(filepath, JSON.stringify(account, null, 2));
  }
  
  /**
   * Load collection workflows
   */
  loadWorkflows() {
    this.workflowDefinitions = {
      early_stage: {
        name: 'Early Stage (0-30 days)',
        stages: [
          { day: 0, action: 'friendly_email', channel: 'email' },
          { day: 3, action: 'follow_up', channel: 'email' },
          { day: 7, action: 'sms_reminder', channel: 'sms' },
          { day: 14, action: 'phone_call', channel: 'voice' }
        ]
      },
      mid_stage: {
        name: 'Mid Stage (31-60 days)',
        stages: [
          { day: 31, action: 'urgent_notice', channel: 'email' },
          { day: 35, action: 'phone_call', channel: 'voice' },
          { day: 45, action: 'demand_letter', channel: 'mail' },
          { day: 60, action: 'final_notice', channel: 'email' }
        ]
      },
      late_stage: {
        name: 'Late Stage (60+ days)',
        stages: [
          { day: 61, action: 'legal_notice', channel: 'mail' },
          { day: 75, action: 'collection_agency', channel: 'external' },
          { day: 90, action: 'litigation_prep', channel: 'legal' }
        ]
      },
      payment_plan: {
        name: 'Payment Plan',
        stages: [
          { day: 0, action: 'plan_confirmation', channel: 'email' },
          { day: -3, action: 'payment_reminder', channel: 'sms', beforePayment: true },
          { day: 0, action: 'payment_due', channel: 'email' },
          { day: 1, action: 'payment_missed', channel: 'email' }
        ]
      }
    };
  }
  
  /**
   * Add a new collection account
   */
  async addAccount(accountData) {
    const account = {
      id: accountData.id || `acc_${Date.now()}`,
      debtor: {
        name: accountData.debtorName,
        email: accountData.debtorEmail,
        phone: accountData.debtorPhone,
        address: accountData.debtorAddress
      },
      originalBalance: parseFloat(accountData.balance),
      currentBalance: parseFloat(accountData.balance),
      daysDelinquent: parseInt(accountData.daysDelinquent) || 0,
      invoiceRefs: accountData.invoiceRefs || [],
      status: 'active',
      workflow: this.assignWorkflow(accountData.daysDelinquent),
      priority: this.calculatePriority(accountData.balance, accountData.daysDelinquent),
      createdAt: new Date().toISOString(),
      lastActivity: new Date().toISOString(),
      communications: [],
      payments: [],
      notes: accountData.notes || []
    };
    
    // Save to storage
    await this.saveAccount(account);
    this.workflows.set(account.id, account);
    
    this.emit('account:added', account);
    console.log(`[MilesCollections] Account added: ${account.id} (${account.priority} priority)`);
    
    return account;
  }
  
  /**
   * Calculate priority based on balance and delinquency
   */
  calculatePriority(balance, days) {
    const score = (balance * 0.6) + (days * 10);
    
    if (score >= 5000) return 'critical';
    if (score >= 2000) return 'high';
    if (score >= 500) return 'medium';
    return 'low';
  }
  
  /**
   * Assign workflow based on delinquency
   */
  assignWorkflow(days) {
    if (days >= 60) return 'late_stage';
    if (days >= 30) return 'mid_stage';
    return 'early_stage';
  }
  
  /**
   * Get account by ID
   */
  getAccount(id) {
    return this.workflows.get(id);
  }
  
  /**
   * List all accounts
   */
  getAccounts(filter = {}) {
    let accounts = Array.from(this.workflows.values());
    
    if (filter.status) {
      accounts = accounts.filter(a => a.status === filter.status);
    }
    if (filter.priority) {
      accounts = accounts.filter(a => a.priority === filter.priority);
    }
    if (filter.workflow) {
      accounts = accounts.filter(a => a.workflow === filter.workflow);
    }
    
    return accounts;
  }
  
  /**
   * Process a payment
   */
  async processPayment(accountId, amount, method = 'manual') {
    const account = this.workflows.get(accountId);
    if (!account) throw new Error('Account not found');
    
    const payment = {
      id: `pay_${Date.now()}`,
      amount: parseFloat(amount),
      method,
      timestamp: new Date().toISOString()
    };
    
    account.payments.push(payment);
    account.currentBalance -= payment.amount;
    account.lastActivity = new Date().toISOString();
    
    if (account.currentBalance <= 0) {
      account.currentBalance = 0;
      account.status = 'paid';
      this.emit('account:paid', account);
    }
    
    await this.saveAccount(account);
    this.emit('payment:received', { accountId, payment });
    
    console.log(`[MilesCollections] Payment: $${payment.amount.toFixed(2)} on ${accountId}`);
    
    return payment;
  }
  
  /**
   * Create payment plan
   */
  async createPaymentPlan(accountId, numPayments = 3) {
    const account = this.workflows.get(accountId);
    if (!account) throw new Error('Account not found');
    
    const paymentAmount = account.currentBalance / numPayments;
    
    account.paymentPlan = {
      id: `plan_${Date.now()}`,
      numPayments,
      paymentAmount: parseFloat(paymentAmount.toFixed(2)),
      totalAmount: account.currentBalance,
      paymentsMade: 0,
      status: 'active',
      createdAt: new Date().toISOString()
    };
    
    account.workflow = 'payment_plan';
    await this.saveAccount(account);
    
    this.emit('paymentplan:created', account.paymentPlan);
    console.log(`[MilesCollections] Payment plan: ${numPayments}x $${paymentAmount.toFixed(2)}`);
    
    return account.paymentPlan;
  }
  
  /**
   * Add communication note
   */
  async addCommunication(accountId, type, message, channel = 'manual') {
    const account = this.workflows.get(accountId);
    if (!account) throw new Error('Account not found');
    
    const communication = {
      id: `comm_${Date.now()}`,
      type,
      message,
      channel,
      timestamp: new Date().toISOString()
    };
    
    account.communications.push(communication);
    account.lastActivity = new Date().toISOString();
    
    await this.saveAccount(account);
    
    return communication;
  }
  
  /**
   * Get metrics
   */
  getMetrics() {
    const accounts = Array.from(this.workflows.values());
    const paidAccounts = accounts.filter(a => a.status === 'paid');
    const activeAccounts = accounts.filter(a => a.status === 'active');
    
    const totalRecovered = accounts.reduce((sum, a) => 
      sum + a.payments.reduce((p, pay) => p + pay.amount, 0), 0
    );
    
    const totalDebt = accounts.reduce((sum, a) => sum + a.originalBalance, 0);
    
    return {
      totalAccounts: accounts.length,
      activeAccounts: activeAccounts.length,
      paidAccounts: paidAccounts.length,
      recoveryRate: accounts.length > 0 ? (paidAccounts.length / accounts.length * 100).toFixed(1) : 0,
      totalDebt: totalDebt.toFixed(2),
      totalRecovered: totalRecovered.toFixed(2),
      outstandingBalance: (totalDebt - totalRecovered).toFixed(2),
      byPriority: {
        critical: accounts.filter(a => a.priority === 'critical').length,
        high: accounts.filter(a => a.priority === 'high').length,
        medium: accounts.filter(a => a.priority === 'medium').length,
        low: accounts.filter(a => a.priority === 'low').length
      }
    };
  }
  
  /**
   * Export to CSV
   */
  exportToCSV() {
    const accounts = Array.from(this.workflows.values());
    const headers = ['ID', 'Name', 'Email', 'Phone', 'Original Balance', 'Current Balance', 'Days Delinquent', 'Priority', 'Status', 'Created'];
    
    const rows = accounts.map(a => [
      a.id,
      a.debtor.name,
      a.debtor.email,
      a.debtor.phone,
      a.originalBalance.toFixed(2),
      a.currentBalance.toFixed(2),
      a.daysDelinquent,
      a.priority,
      a.status,
      a.createdAt
    ]);
    
    return [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  }
  
  /**
   * Get next actions for an account
   */
  getNextActions(accountId) {
    const account = this.workflows.get(accountId);
    if (!account) return null;
    
    const workflow = this.workflowDefinitions[account.workflow];
    if (!workflow) return null;
    
    const daysSinceCreation = Math.floor(
      (Date.now() - new Date(account.createdAt).getTime()) / (1000 * 60 * 60 * 24)
    );
    
    return workflow.stages
      .filter(s => s.day <= daysSinceCreation && !account.communications.some(c => c.type === s.action))
      .map(s => ({
        ...s,
        daysOverdue: daysSinceCreation - s.day
      }));
  }
}

module.exports = MilesCollections;

// CLI interface
if (require.main === module) {
  const collections = new MilesCollections({ tier: 'professional' });
  
  async function run() {
    await collections.init();
    
    const command = process.argv[2];
    
    switch (command) {
      case 'add':
        const account = await collections.addAccount({
          debtorName: process.argv[3] || 'Test Customer',
          debtorEmail: process.argv[4] || 'test@test.com',
          debtorPhone: process.argv[5] || '555-1234',
          balance: process.argv[6] || 1000,
          daysDelinquent: process.argv[7] || 30
        });
        console.log('Account created:', account.id);
        break;
        
      case 'list':
        const accounts = collections.getAccounts();
        console.table(accounts.map(a => ({
          ID: a.id,
          Name: a.debtor.name,
          Balance: a.currentBalance.toFixed(2),
          Days: a.daysDelinquent,
          Priority: a.priority,
          Status: a.status
        })));
        break;
        
      case 'metrics':
        console.log(collections.getMetrics());
        break;
        
      case 'export':
        console.log(collections.exportToCSV());
        break;
        
      default:
        console.log(`
Miles Collections Module

Commands:
  node miles-collections.js add [name] [email] [phone] [balance] [days]
  node miles-collections.js list
  node miles-collections.js metrics
  node miles-collections.js export
        `);
    }
    
    process.exit(0);
  }
  
  run().catch(console.error);
}
