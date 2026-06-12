/**
 * Collections Workflow Engine
 * Simple Temporal-like workflow system for debt collection
 * No external dependencies - runs on Node.js
 */

const { EventEmitter } = require('events');
const fs = require('fs').promises;
const path = require('path');

class CollectionsWorkflow extends EventEmitter {
  constructor(config = {}) {
    super();
    this.workflows = new Map();
    this.running = false;
    this.checkInterval = config.checkInterval || 60000; // Check every minute
    this.dataDir = config.dataDir || '/root/.openclaw/workspace/miles-collections/data';
  }

  /**
   * Start the workflow engine
   */
  async start() {
    if (this.running) return;
    
    console.log('[Workflow] Starting Collections Workflow Engine...');
    this.running = true;
    
    // Load existing workflows
    await this.loadWorkflows();
    
    // Start the scheduler
    this.scheduler = setInterval(() => this.tick(), this.checkInterval);
    
    this.emit('started');
    console.log('[Workflow] Engine running. Checking every', this.checkInterval / 1000, 'seconds');
  }

  /**
   * Stop the workflow engine
   */
  async stop() {
    if (!this.running) return;
    
    console.log('[Workflow] Stopping...');
    this.running = false;
    
    if (this.scheduler) {
      clearInterval(this.scheduler);
    }
    
    this.emit('stopped');
  }

  /**
   * Load existing account workflows
   */
  async loadWorkflows() {
    try {
      const files = await fs.readdir(this.dataDir);
      const accountFiles = files.filter(f => f.endsWith('.json'));
      
      for (const file of accountFiles) {
        const data = await fs.readFile(path.join(this.dataDir, file), 'utf8');
        const account = JSON.parse(data);
        if (account.status === 'active') {
          this.workflows.set(account.id, {
            accountId: account.id,
            stage: account.workflow || 'early_stage',
            lastAction: account.lastActivity,
            nextActionDue: this.calculateNextAction(account),
            actions: []
          });
        }
      }
      
      console.log(`[Workflow] Loaded ${this.workflows.size} active workflows`);
    } catch (err) {
      console.log('[Workflow] No existing workflows found');
    }
  }

  /**
   * Calculate when next action is due
   */
  calculateNextAction(account) {
    const stages = {
      early_stage: [0, 3, 7, 14], // days from creation
      mid_stage: [31, 35, 45, 60],
      late_stage: [61, 75, 90]
    };
    
    const created = new Date(account.createdAt);
    const now = new Date();
    const daysSince = Math.floor((now - created) / (1000 * 60 * 60 * 24));
    
    const workflowDays = stages[account.workflow] || stages.early_stage;
    
    // Find next action day
    for (const day of workflowDays) {
      if (day > daysSince) {
        const nextDue = new Date(created);
        nextDue.setDate(nextDue.getDate() + day);
        return nextDue.toISOString();
      }
    }
    
    return null; // No more actions
  }

  /**
   * Main tick - check and execute due actions
   */
  async tick() {
    const now = new Date();
    const dueActions = [];
    
    for (const [id, workflow] of this.workflows) {
      if (workflow.nextActionDue && new Date(workflow.nextActionDue) <= now) {
        dueActions.push(workflow);
      }
    }
    
    if (dueActions.length > 0) {
      console.log(`[Workflow] ${dueActions.length} actions due`);
      
      for (const action of dueActions) {
        await this.executeAction(action);
      }
    }
  }

  /**
   * Execute a workflow action
   */
  async executeAction(workflow) {
    const actions = {
      early_stage: ['friendly_email', 'follow_up', 'sms_reminder', 'phone_call'],
      mid_stage: ['urgent_notice', 'phone_call', 'demand_letter', 'final_notice'],
      late_stage: ['legal_notice', 'collection_agency', 'litigation_prep']
    };
    
    const stageActions = actions[workflow.stage] || actions.early_stage;
    const actionIndex = workflow.actions.length;
    
    if (actionIndex >= stageActions.length) {
      console.log(`[Workflow] ${workflow.accountId} - stage complete`);
      workflow.nextActionDue = null;
      return;
    }
    
    const actionType = stageActions[actionIndex];
    
    console.log(`[Workflow] ${workflow.accountId} - executing: ${actionType}`);
    
    // Record the action
    const action = {
      type: actionType,
      timestamp: new Date().toISOString(),
      status: 'pending'
    };
    
    workflow.actions.push(action);
    
    // Update account file
    await this.updateAccountAction(workflow.accountId, action);
    
    // Schedule next action
    workflow.nextActionDue = this.calculateNextActionTime();
    
    this.emit('action:executed', { workflow, action });
  }

  /**
   * Calculate next action time
   */
  calculateNextActionTime() {
    const next = new Date();
    next.setDate(next.getDate() + 3); // 3 days later
    return next.toISOString();
  }

  /**
   * Update account file with action
   */
  async updateAccountAction(accountId, action) {
    try {
      const filepath = path.join(this.dataDir, `${accountId}.json`);
      const data = await fs.readFile(filepath, 'utf8');
      const account = JSON.parse(data);
      
      account.communications = account.communications || [];
      account.communications.push({
        type: action.type,
        timestamp: action.timestamp,
        channel: this.getChannelForAction(action.type),
        status: action.status
      });
      
      account.lastActivity = action.timestamp;
      
      await fs.writeFile(filepath, JSON.stringify(account, null, 2));
    } catch (err) {
      console.error(`[Workflow] Failed to update ${accountId}:`, err);
    }
  }

  /**
   * Get channel for action type
   */
  getChannelForAction(actionType) {
    const channels = {
      friendly_email: 'email',
      follow_up: 'email',
      sms_reminder: 'sms',
      phone_call: 'voice',
      urgent_notice: 'email',
      demand_letter: 'mail',
      final_notice: 'email',
      legal_notice: 'mail'
    };
    
    return channels[actionType] || 'manual';
  }

  /**
   * Get workflow status
   */
  getStatus() {
    const now = new Date();
    let dueCount = 0;
    
    for (const workflow of this.workflows.values()) {
      if (workflow.nextActionDue && new Date(workflow.nextActionDue) <= now) {
        dueCount++;
      }
    }
    
    return {
      running: this.running,
      totalWorkflows: this.workflows.size,
      actionsDue: dueCount,
      checkInterval: this.checkInterval
    };
  }

  /**
   * Manually trigger an action
   */
  async triggerAction(accountId, actionType) {
    const workflow = this.workflows.get(accountId);
    if (!workflow) {
      throw new Error('Workflow not found');
    }
    
    console.log(`[Workflow] Manual trigger: ${accountId} - ${actionType}`);
    
    const action = {
      type: actionType,
      timestamp: new Date().toISOString(),
      status: 'executed'
    };
    
    await this.updateAccountAction(accountId, action);
    
    this.emit('action:manual', { workflow, action });
    
    return action;
  }
}

module.exports = CollectionsWorkflow;

// CLI interface
if (require.main === module) {
  const workflow = new CollectionsWorkflow();
  
  const command = process.argv[2];
  
  switch (command) {
    case 'start':
      workflow.start().catch(console.error);
      
      // Keep running
      process.on('SIGINT', async () => {
        console.log('\n[Workflow] Shutting down...');
        await workflow.stop();
        process.exit(0);
      });
      break;
      
    case 'status':
      workflow.loadWorkflows().then(() => {
        console.log(workflow.getStatus());
        process.exit(0);
      });
      break;
      
    case 'trigger':
      const accountId = process.argv[3];
      const actionType = process.argv[4] || 'phone_call';
      workflow.triggerAction(accountId, actionType)
        .then(() => process.exit(0))
        .catch(err => {
          console.error(err);
          process.exit(1);
        });
      break;
      
    default:
      console.log(`
Collections Workflow Engine

Commands:
  node workflow.js start              - Start the workflow engine
  node workflow.js status           - Show workflow status
  node workflow.js trigger [id] [action] - Manually trigger action

Examples:
  node workflow.js start
  node workflow.js trigger pendo_0001_234 phone_call
      `);
      process.exit(0);
  }
}
