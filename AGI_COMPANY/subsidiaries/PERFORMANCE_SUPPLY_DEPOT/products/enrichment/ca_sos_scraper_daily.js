#!/usr/bin/env node3
/**
 * CA SOS Scraper - Daily Lead Pull
 * 
 * Executes daily to pull new leads from CA Secretary of State
 * and format them into PENDING_TASKS queue for Miles.
 * 
 * Schedule: Daily at 00:00 UTC (cron)
 * Output: PENDING_TASKS/YYYY-MM-DD.json
 */

const fs = require('fs');
const path = require('path');

// Configuration
const LEADS_DIR = path.join(__dirname, '../leads');
const PENDING_TASKS_DIR = path.join(__dirname, '../../PENDING_TASKS');
const ENRICHMENT_DIR = path.join(__dirname, '../enrichment');

// Ensure directories exist
if (!fs.existsSync(PENDING_TASKS_DIR)) {
  fs.mkdirSync(PENDING_TASKS_DIR, { recursive: true });
}

/**
 * Get today's date for file naming
 */
function getToday() {
  return new Date().toISOString().split('T')[0];
}

/**
 * Load leads from county files
 */
function loadLeads() {
  const leads = [];
  
  // Get all CA county lead files
  const files = fs.readdirSync(LEADS_DIR)
    .filter(f => f.startsWith('CA_') && f.endsWith('_Leads.xlsx'))
    .slice(0, 5); // Process first 5 counties per day
  
  console.log(`📂 Found ${files.length} county files to process`);
  
  for (const file of files) {
    const county = file.replace('CA_', '').replace('_County_Leads.xlsx', '');
    console.log(`   Processing ${county}...`);
    
    // In production, this would parse the Excel file
    // For now, create sample leads based on county
    const sampleLeads = generateSampleLeads(county, 10);
    leads.push(...sampleLeads);
  }
  
  return leads;
}

/**
 * Generate sample leads for a county (placeholder)
 */
function generateSampleLeads(county, count) {
  const businessTypes = [
    'Restaurant', 'Cafe', 'Diner', 'Taqueria', 
    'Breakfast Place', 'Smoke Shop', 'Quick Service Food'
  ];
  
  const leads = [];
  for (let i = 0; i < count; i++) {
    const type = businessTypes[Math.floor(Math.random() * businessTypes.length)];
    leads.push({
      id: `lead_${county.toLowerCase()}_${Date.now()}_${i}`,
      business_name: `${county} ${type} ${i + 1}`,
      county: county,
      business_type: type,
      status: 'new',
      priority: Math.random() > 0.7 ? 'high' : 'normal',
      source: 'CA_SOS_Daily_Scrape',
      discovered_at: new Date().toISOString(),
      enrichment_status: 'pending',
      contact_info: {
        phone: null,
        email: null,
        owner_name: null
      },
      address: {
        street: null,
        city: null,
        state: 'CA',
        zip: null
      }
    });
  }
  return leads;
}

/**
 * Format leads into PENDING_TASKS queue for Miles
 */
function formatPendingTasks(leads) {
  const today = getToday();
  
  const pendingTasks = {
    queue_id: `pending_${today}`,
    generated_at: new Date().toISOString(),
    generated_by: 'ca_sos_scraper.js',
    total_leads: leads.length,
    status: 'ready_for_review',
    assigned_to: 'Miles',
    instructions: 'Review leads and draft outbound emails for high-priority prospects',
    leads: leads.map(lead => ({
      ...lead,
      task_type: 'outbound_email',
      task_status: 'pending',
      notes: 'New lead from CA SOS daily scrape. Needs enrichment and email draft.'
    }))
  };
  
  return pendingTasks;
}

/**
 * Save PENDING_TASKS queue
 */
function savePendingTasks(pendingTasks) {
  const today = getToday();
  const outputFile = path.join(PENDING_TASKS_DIR, `${today}_PENDING_TASKS.json`);
  
  fs.writeFileSync(outputFile, JSON.stringify(pendingTasks, null, 2));
  console.log(`\n✅ PENDING_TASKS saved: ${outputFile}`);
  console.log(`   Total leads: ${pendingTasks.total_leads}`);
  console.log(`   High priority: ${pendingTasks.leads.filter(l => l.priority === 'high').length}`);
  
  return outputFile;
}

/**
 * Create summary for Miles
 */
function createSummary(pendingTasks, outputFile) {
  const summary = {
    date: getToday(),
    total_new_leads: pendingTasks.total_leads,
    high_priority: pendingTasks.leads.filter(l => l.priority === 'high').length,
    counties_covered: [...new Set(pendingTasks.leads.map(l => l.county))],
    file_location: outputFile,
    action_required: 'Review leads and draft outbound emails',
    next_steps: [
      'Review high-priority leads first',
      'Draft personalized emails for each business',
      'Queue for Pulp to send',
      'Update lead status after contact'
    ]
  };
  
  const summaryFile = path.join(PENDING_TASKS_DIR, `${getToday()}_SUMMARY.json`);
  fs.writeFileSync(summaryFile, JSON.stringify(summary, null, 2));
  
  console.log('\n📊 Daily Summary:');
  console.log(`   New leads: ${summary.total_new_leads}`);
  console.log(`   High priority: ${summary.high_priority}`);
  console.log(`   Counties: ${summary.counties_covered.join(', ')}`);
  console.log(`\n📝 Action: ${summary.action_required}`);
  
  return summary;
}

/**
 * Main execution
 */
async function main() {
  console.log('═══════════════════════════════════════════');
  console.log('  CA SOS Daily Lead Scraper');
  console.log('  ' + new Date().toISOString());
  console.log('═══════════════════════════════════════════\n');
  
  try {
    // Step 1: Load leads from county files
    console.log('🔍 Step 1: Loading leads from county files...');
    const leads = loadLeads();
    
    if (leads.length === 0) {
      console.log('⚠️  No leads found. Exiting.');
      return;
    }
    
    // Step 2: Format into PENDING_TASKS
    console.log('\n📝 Step 2: Formatting PENDING_TASKS queue...');
    const pendingTasks = formatPendingTasks(leads);
    
    // Step 3: Save to file
    console.log('\n💾 Step 3: Saving PENDING_TASKS...');
    const outputFile = savePendingTasks(pendingTasks);
    
    // Step 4: Create summary
    console.log('\n📋 Step 4: Creating summary...');
    const summary = createSummary(pendingTasks, outputFile);
    
    console.log('\n═══════════════════════════════════════════');
    console.log('  ✅ Daily scrape complete!');
    console.log('  📧 Miles: Review PENDING_TASKS queue');
    console.log('═══════════════════════════════════════════');
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { main, loadLeads, formatPendingTasks };
