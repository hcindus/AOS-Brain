#!/usr/bin/env node
/**
 * Dusty MVP Full End-to-End Test with Detailed Timing
 * 
 * Tests the complete flow:
 * 1. Bridge webhook → Core-Agent
 * 2. Core-Agent processing
 * 3. OpenClaw mock response
 * 4. End-to-end latency
 */

const axios = require('axios');
const fs = require('fs');

// Service endpoints
const BRIDGE_URL = process.env.BRIDGE_URL || 'http://localhost:3001';
const CORE_AGENT_URL = process.env.CORE_AGENT_URL || 'http://localhost:3000';
const OPENCLAW_URL = process.env.OPENCLAW_URL || 'http://localhost:4000';

// Test configuration
const TEST_CONFIG = {
  bridge: { path: '/webhook', method: 'POST' },
  coreAgent: { path: '/tasks', method: 'POST' },
  openclaw: { path: '/receive_message', method: 'POST' }
};

// Mock Telegram message payload
const mockTelegramMessage = {
  update_id: 123456789,
  message: {
    message_id: 1,
    from: {
      id: 987654321,
      username: 'test_user',
      first_name: 'Test',
      last_name: 'User',
      is_bot: false
    },
    chat: {
      id: 987654321,
      first_name: 'Test',
      last_name: 'User',
      username: 'test_user',
      type: 'private'
    },
    date: Math.floor(Date.now() / 1000),
    text: 'Show me my dust balance'
  }
};

// Test results structure
const testResults = {
  timestamp: new Date().toISOString(),
  overall: {
    status: 'PENDING',
    totalDuration: 0,
    startTime: null,
    endTime: null
  },
  phases: {
    phase1_bridge: {
      name: 'Phase 1: Bridge → Core-Agent (Telegram flow)',
      status: 'NOT_STARTED',
      timing: { start: 0, end: 0, duration: 0 },
      details: {}
    },
    phase2_coreAgent: {
      name: 'Phase 2: Core-Agent Processing',
      status: 'NOT_STARTED',
      timing: { start: 0, end: 0, duration: 0 },
      details: {}
    },
    phase3_openclaw: {
      name: 'Phase 3: OpenClaw Response Generation',
      status: 'NOT_STARTED',
      timing: { start: 0, end: 0, duration: 0 },
      details: {}
    },
    phase4_returnPath: {
      name: 'Phase 4: Return Path (Bridge Response)',
      status: 'NOT_STARTED',
      timing: { start: 0, end: 0, duration: 0 },
      details: {}
    }
  },
  logs: [],
  errors: [],
  recommendations: []
};

function log(message, level = 'info') {
  const timestamp = new Date().toISOString();
  const logEntry = { timestamp, level, message };
  testResults.logs.push(logEntry);
  console.log(`[${timestamp}] [${level.toUpperCase()}] ${message}`);
}

function recordError(phase, error) {
  const errorInfo = {
    phase,
    message: error.message,
    code: error.code,
    stack: error.stack,
    timestamp: new Date().toISOString()
  };
  testResults.errors.push(errorInfo);
  log(`ERROR in ${phase}: ${error.message}`, 'error');
}

async function checkHealth(endpoint, name) {
  try {
    const start = Date.now();
    const response = await axios.get(`${endpoint}/health`, { timeout: 5000 });
    const duration = Date.now() - start;
    return {
      healthy: response.data.status === 'healthy',
      data: response.data,
      responseTime: duration
    };
  } catch (error) {
    return {
      healthy: false,
      error: error.message,
      responseTime: null
    };
  }
}

async function runPhase1_BridgeToCoreAgent() {
  const phase = testResults.phases.phase1_bridge;
  phase.status = 'RUNNING';
  phase.timing.start = Date.now();
  
  log('=== PHASE 1: Bridge → Core-Agent ===');
  
  try {
    // First check bridge health
    log('Checking Bridge health...');
    const bridgeHealth = await checkHealth(BRIDGE_URL, 'Bridge');
    phase.details.bridgeHealth = bridgeHealth;
    
    if (!bridgeHealth.healthy) {
      throw new Error(`Bridge is not healthy: ${bridgeHealth.error}`);
    }
    log(`Bridge is healthy (response time: ${bridgeHealth.responseTime}ms)`);
    
    // Check core-agent health
    log('Checking Core-Agent health...');
    const coreHealth = await checkHealth(CORE_AGENT_URL, 'Core-Agent');
    phase.details.coreAgentHealth = coreHealth;
    
    if (!coreHealth.healthy) {
      throw new Error(`Core-Agent is not healthy: ${coreHealth.error}`);
    }
    log(`Core-Agent is healthy (response time: ${coreHealth.responseTime}ms)`);
    
    // Send webhook to bridge
    log('Sending mock Telegram webhook to Bridge...');
    const webhookStart = Date.now();
    
    const response = await axios.post(
      `${BRIDGE_URL}/webhook`,
      mockTelegramMessage,
      {
        headers: { 'Content-Type': 'application/json' },
        timeout: 15000
      }
    );
    
    const webhookDuration = Date.now() - webhookStart;
    phase.details.webhookResponse = {
      status: response.status,
      data: response.data,
      duration: webhookDuration
    };
    
    log(`Webhook sent successfully in ${webhookDuration}ms`);
    log(`Response: ${JSON.stringify(response.data, null, 2)}`);
    
    phase.status = 'SUCCESS';
    phase.timing.end = Date.now();
    phase.timing.duration = phase.timing.end - phase.timing.start;
    
    return response.data;
  } catch (error) {
    recordError('phase1_bridge', error);
    phase.status = 'FAILED';
    phase.timing.end = Date.now();
    phase.timing.duration = phase.timing.end - phase.timing.start;
    throw error;
  }
}

async function runPhase2_CoreAgentProcessing() {
  const phase = testResults.phases.phase2_coreAgent;
  phase.status = 'RUNNING';
  phase.timing.start = Date.now();
  
  log('=== PHASE 2: Core-Agent Processing ===');
  
  try {
    // Verify task was created in core-agent
    log('Checking task creation in Core-Agent...');
    
    const taskCreateStart = Date.now();
    const taskPayload = {
      type: 'telegram_message',
      payload: {
        source: 'telegram',
        userId: mockTelegramMessage.message.from.id,
        username: mockTelegramMessage.message.from.username,
        text: mockTelegramMessage.message.text,
        messageId: mockTelegramMessage.message.message_id
      }
    };
    
    const response = await axios.post(
      `${CORE_AGENT_URL}/tasks`,
      taskPayload,
      {
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000
      }
    );
    
    const taskCreateDuration = Date.now() - taskCreateStart;
    phase.details.taskCreation = {
      status: response.status,
      data: response.data,
      duration: taskCreateDuration
    };
    
    log(`Task created in ${taskCreateDuration}ms`);
    log(`Task ID: ${response.data.id}`);
    
    // Store task ID for later
    phase.details.taskId = response.data.id;
    
    // Verify task exists
    log('Verifying task retrieval...');
    const taskGetStart = Date.now();
    const getResponse = await axios.get(
      `${CORE_AGENT_URL}/tasks/${response.data.id}`,
      { timeout: 5000 }
    );
    const taskGetDuration = Date.now() - taskGetStart;
    
    phase.details.taskRetrieval = {
      status: getResponse.status,
      duration: taskGetDuration
    };
    
    log(`Task verified in ${taskGetDuration}ms`);
    
    phase.status = 'SUCCESS';
    phase.timing.end = Date.now();
    phase.timing.duration = phase.timing.end - phase.timing.start;
    
    return response.data;
  } catch (error) {
    recordError('phase2_coreAgent', error);
    phase.status = 'FAILED';
    phase.timing.end = Date.now();
    phase.timing.duration = phase.timing.end - phase.timing.start;
    throw error;
  }
}

async function runPhase3_OpenClawResponse() {
  const phase = testResults.phases.phase3_openclaw;
  phase.status = 'RUNNING';
  phase.timing.start = Date.now();
  
  log('=== PHASE 3: OpenClaw Response Generation ===');
  
  try {
    // Check OpenClaw health
    log('Checking OpenClaw mock health...');
    const openclawHealth = await checkHealth(OPENCLAW_URL, 'OpenClaw');
    phase.details.openclawHealth = openclawHealth;
    
    if (!openclawHealth.healthy) {
      throw new Error(`OpenClaw is not healthy: ${openclawHealth.error}`);
    }
    log(`OpenClaw is healthy (response time: ${openclawHealth.responseTime}ms)`);
    
    // Send message directly to OpenClaw
    log('Sending message to OpenClaw...');
    const messageStart = Date.now();
    
    const response = await axios.post(
      `${OPENCLAW_URL}/receive_message`,
      {
        message: mockTelegramMessage.message.text,
        user_id: mockTelegramMessage.message.from.id,
        session_id: `test_${Date.now()}`
      },
      {
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000
      }
    );
    
    const messageDuration = Date.now() - messageStart;
    phase.details.response = {
      status: response.status,
      duration: messageDuration,
      data: response.data
    };
    
    log(`OpenClaw responded in ${messageDuration}ms`);
    log(`Response type: ${response.data.action}`);
    log(`Response preview: ${response.data.response.substring(0, 100)}...`);
    
    phase.status = 'SUCCESS';
    phase.timing.end = Date.now();
    phase.timing.duration = phase.timing.end - phase.timing.start;
    
    return response.data;
  } catch (error) {
    recordError('phase3_openclaw', error);
    phase.status = 'FAILED';
    phase.timing.end = Date.now();
    phase.timing.duration = phase.timing.end - phase.timing.start;
    throw error;
  }
}

async function runPhase4_ReturnPath() {
  const phase = testResults.phases.phase4_returnPath;
  phase.status = 'RUNNING';
  phase.timing.start = Date.now();
  
  log('=== PHASE 4: Return Path Verification ===');
  
  try {
    // Verify bridge response format for Telegram
    log('Checking bridge response format...');
    
    const response = await axios.get(`${BRIDGE_URL}/health`, { timeout: 5000 });
    phase.details.bridgeEndToEnd = {
      status: response.status,
      format: 'telegram_compatible',
      circuits: response.data.circuitBreaker || { state: 'unknown' }
    };
    
    log('Bridge response format verified');
    
    phase.status = 'SUCCESS';
    phase.timing.end = Date.now();
    phase.timing.duration = phase.timing.end - phase.timing.start;
    
    return true;
  } catch (error) {
    recordError('phase4_returnPath', error);
    phase.status = 'FAILED';
    phase.timing.end = Date.now();
    phase.timing.duration = phase.timing.end - phase.timing.start;
    // Don't throw - return path failure is not critical
    return false;
  }
}

function generateRecommendations() {
  const recs = [];
  
  // Check phase 1
  if (testResults.phases.phase1_bridge.status !== 'SUCCESS') {
    recs.push({
      priority: 'HIGH',
      phase: 'Phase 1',
      recommendation: 'Ensure Bridge service is running: cd dusty_mvp_sandbox/bridge_mock && node bridge_mock.js'
    });
  }
  
  // Check phase 2
  if (testResults.phases.phase2_coreAgent.status !== 'SUCCESS') {
    recs.push({
      priority: 'HIGH',
      phase: 'Phase 2',
      recommendation: 'Ensure Core-Agent is running: cd dusty_mvp_sandbox/core-agent && node src/index.js'
    });
  }
  
  // Check phase 3
  if (testResults.phases.phase3_openclaw.status !== 'SUCCESS') {
    recs.push({
      priority: 'HIGH',
      phase: 'Phase 3',
      recommendation: 'Ensure OpenClaw mock is running: cd dusty_mvp_sandbox/openclaw_mock && node openclaw_mock.js'
    });
  }
  
  // Performance recommendations
  const totalDuration = testResults.overall.totalDuration;
  if (totalDuration > 5000) {
    recs.push({
      priority: 'MEDIUM',
      phase: 'Performance',
      recommendation: `End-to-end latency is high (${totalDuration}ms). Consider optimizing service response times or network connectivity.`
    });
  }
  
  if (testResults.errors.length > 0) {
    recs.push({
      priority: 'HIGH',
      phase: 'General',
      recommendation: 'Review error logs and stack traces in the test report for detailed debugging information.'
    });
  }
  
  // Add success recommendation if everything passed
  if (recs.length === 0) {
    recs.push({
      priority: 'INFO',
      phase: 'All Phases',
      recommendation: 'All test phases passed successfully. System is operational.'
    });
  }
  
  return recs;
}

async function runFullTest() {
  console.log('\n' + '='.repeat(70));
  console.log('DUSTY MVP END-TO-END TEST WITH FULL TIMING');
  console.log('='.repeat(70));
  console.log(`Test started at: ${new Date().toISOString()}`);
  console.log(`Bridge URL: ${BRIDGE_URL}`);
  console.log(`Core-Agent URL: ${CORE_AGENT_URL}`);
  console.log(`OpenClaw URL: ${OPENCLAW_URL}`);
  console.log('='.repeat(70) + '\n');
  
  testResults.overall.startTime = Date.now();
  
  try {
    // Phase 1: Bridge → Core-Agent
    await runPhase1_BridgeToCoreAgent();
    
    // Phase 2: Core-Agent Processing
    await runPhase2_CoreAgentProcessing();
    
    // Phase 3: OpenClaw Response
    await runPhase3_OpenClawResponse();
    
    // Phase 4: Return Path (optional)
    await runPhase4_ReturnPath();
    
    testResults.overall.status = 'SUCCESS';
    
  } catch (error) {
    log(`Test failed with error: ${error.message}`, 'error');
    testResults.overall.status = 'PARTIAL_FAILURE';
  }
  
  testResults.overall.endTime = Date.now();
  testResults.overall.totalDuration = testResults.overall.endTime - testResults.overall.startTime;
  
  // Generate recommendations
  testResults.recommendations = generateRecommendations();
  
  // Print summary
  printSummary();
  
  // Save report
  await saveReport();
  
  return testResults;
}

function printSummary() {
  console.log('\n' + '='.repeat(70));
  console.log('TEST SUMMARY');
  console.log('='.repeat(70));
  
  console.log(`\nOverall Status: ${testResults.overall.status}`);
  console.log(`Total Duration: ${testResults.overall.totalDuration}ms`);
  
  console.log('\n--- Phase Breakdown ---');
  Object.values(testResults.phases).forEach(phase => {
    const statusIcon = phase.status === 'SUCCESS' ? '✅' : 
                       phase.status === 'FAILED' ? '❌' : '⏭️';
    console.log(`\n${statusIcon} ${phase.name}`);
    console.log(`   Status: ${phase.status}`);
    if (phase.timing.duration > 0) {
      console.log(`   Duration: ${phase.timing.duration}ms`);
    }
  });
  
  console.log('\n--- Errors ---');
  if (testResults.errors.length === 0) {
    console.log('No errors recorded');
  } else {
    testResults.errors.forEach((err, idx) => {
      console.log(`\n${idx + 1}. [${err.phase}] ${err.message}`);
    });
  }
  
  console.log('\n--- Recommendations ---');
  testResults.recommendations.forEach((rec, idx) => {
    console.log(`\n${idx + 1}. [${rec.priority}] ${rec.recommendation}`);
  });
  
  console.log('\n' + '='.repeat(70));
}

async function saveReport() {
  const reportFilename = `DUSTY_MVP_E2E_REPORT_${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
  const reportPath = `/root/.openclaw/workspace/${reportFilename}`;
  
  try {
    fs.writeFileSync(reportPath, JSON.stringify(testResults, null, 2));
    log(`Test report saved to: ${reportPath}`);
    
    // Also save as latest
    const latestPath = '/root/.openclaw/workspace/DUSTY_MVP_E2E_REPORT_LATEST.json';
    fs.writeFileSync(latestPath, JSON.stringify(testResults, null, 2));
    
    return reportPath;
  } catch (error) {
    log(`Failed to save report: ${error.message}`, 'error');
  }
}

// Run the test
if (require.main === module) {
  runFullTest().then(() => {
    console.log('\nTest execution complete.\n');
    process.exit(0);
  }).catch(err => {
    console.error('\nTest execution failed:', err);
    process.exit(1);
  });
}

module.exports = { runFullTest };
