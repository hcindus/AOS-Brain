const http = require('http');
const https = require('https');

// Helper to make HTTP requests with timing
function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const startTime = process.hrtime.bigint();
    const client = url.startsWith('https') ? https : http;
    const req = client.request(url, { method: options.method || 'GET', headers: options.headers }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const endTime = process.hrtime.bigint();
        const durationMs = Number(endTime - startTime) / 1_000_000;
        resolve({ statusCode: res.statusCode, data, durationMs });
      });
    });
    req.on('error', reject);
    if (options.body) req.write(JSON.stringify(options.body));
    req.end();
  });
}

// Mock Telegram message via bridge (POST /webhook)
async function sendMockTelegramMessage(userId, chatId, message) {
  const mockTelegramUpdate = {
    update_id: Date.now(),
    message: {
      message_id: Date.now() + 1,
      from: {
        id: parseInt(userId.replace(/\D/g, '')) || 987654321,
        is_bot: false,
        first_name: 'Test',
        last_name: 'User',
        username: userId
      },
      chat: {
        id: parseInt(chatId.replace(/\D/g, '')) || 987654321,
        type: 'private'
      },
      date: Math.floor(Date.now() / 1000),
      text: message
    }
  };
  
  return httpRequest('http://localhost:3001/webhook', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: mockTelegramUpdate
  });
}

async function runTest() {
  console.log('=== Dusty MVP End-to-End Test ===');
  console.log(`Timestamp: ${new Date().toISOString()}`);
  console.log('');

  const results = {
    passed: 0,
    failed: 0,
    tests: []
  };

  // Test 1: Bridge health check
  console.log('1. Service Health Checks');
  try {
    const startTime = process.hrtime.bigint();
    const bridgeHealth = await httpRequest('http://localhost:3001/health');
    const durationMs = Number(process.hrtime.bigint() - startTime) / 1_000_000;

    const status = bridgeHealth.statusCode === 200 ? '✅ PASS' : '❌ FAIL';
    const parsed = JSON.parse(bridgeHealth.data);
    console.log(`   Telegram Bridge Mock: ${status}`);
    console.log(`     - Endpoint: localhost:3001/health`);
    console.log(`     - Status: ${bridgeHealth.statusCode} ${parsed.status}`);
    console.log(`     - Uptime: ${Math.floor(parsed.uptime / 3600)}h ${Math.floor((parsed.uptime % 3600) / 60)}m`);
    console.log(`     - Response Time: ${durationMs.toFixed(2)}ms`);
    results.tests.push({ name: 'Bridge Health', status: 'PASS', durationMs });
    results.passed++;
  } catch (error) {
    console.log(`   Telegram Bridge Mock: ❌ FAIL`);
    console.log(`     - Error: ${error.message}`);
    results.tests.push({ name: 'Bridge Health', status: 'FAIL', error: error.message });
    results.failed++;
  }

  // Test 2: Core-Agent health check
  try {
    const startTime = process.hrtime.bigint();
    const coreHealth = await httpRequest('http://localhost:3000/health');
    const durationMs = Number(process.hrtime.bigint() - startTime) / 1_000_000;

    const status = coreHealth.statusCode === 200 ? '✅ PASS' : '❌ FAIL';
    const parsed = JSON.parse(coreHealth.data);
    console.log(`   Core-Agent: ${status}`);
    console.log(`     - Endpoint: localhost:3000/health`);
    console.log(`     - Status: ${coreHealth.statusCode} ${parsed.status}`);
    console.log(`     - Uptime: ${Math.floor(parsed.uptime / 3600)}h ${Math.floor((parsed.uptime % 3600) / 60)}m`);
    console.log(`     - Response Time: ${durationMs.toFixed(2)}ms`);
    results.tests.push({ name: 'Core-Agent Health', status: 'PASS', durationMs });
    results.passed++;
  } catch (error) {
    console.log(`   Core-Agent: ❌ FAIL`);
    console.log(`     - Error: ${error.message}`);
    results.tests.push({ name: 'Core-Agent Health', status: 'FAIL', error: error.message });
    results.failed++;
  }

  // Test 3: OpenClaw mock health check
  try {
    const startTime = process.hrtime.bigint();
    const openclawHealth = await httpRequest('http://localhost:4000/status');
    const durationMs = Number(process.hrtime.bigint() - startTime) / 1_000_000;

    const status = openclawHealth.statusCode === 200 ? '✅ PASS' : '❌ FAIL';
    const parsed = JSON.parse(openclawHealth.data);
    console.log(`   OpenClaw Mock: ${status}`);
    console.log(`     - Endpoint: localhost:4000/status`);
    console.log(`     - Status: ${openclawHealth.statusCode} ${parsed.status}`);
    console.log(`     - Total Interactions: ${parsed.total_interactions}`);
    console.log(`     - Uptime: ${Math.floor(parsed.uptime / 3600)}h ${Math.floor((parsed.uptime % 3600) / 60)}m`);
    console.log(`     - Response Time: ${durationMs.toFixed(2)}ms`);
    results.tests.push({ name: 'OpenClaw Health', status: 'PASS', durationMs });
    results.passed++;
  } catch (error) {
    console.log(`   OpenClaw Mock: ❌ FAIL`);
    console.log(`     - Error: ${error.message}`);
    results.tests.push({ name: 'OpenClaw Health', status: 'FAIL', error: error.message });
    results.failed++;
  }

  // Test 4: End-to-end flow test - Mock Telegram message via bridge
  console.log('');
  console.log('2. End-to-End Flow Test');
  console.log('   Sending: "/dust balance" via Bridge Mock...');
  try {
    const testStartTime = process.hrtime.bigint();
    const e2eResult = await sendMockTelegramMessage('test_user_e2e', 'test_chat_e2e', '/dust balance');
    const e2eDuration = Number(process.hrtime.bigint() - testStartTime) / 1_000_000;

    const success = e2eResult.statusCode === 200;
    let taskId = 'N/A';
    let openclawResponse = null;
    let forwarded = false;
    try {
      const parsed = JSON.parse(e2eResult.data);
      // Bridge returns: { forwarded: true, coreAgentResponse: { id: ..., openclawResponse: ... } }
      forwarded = parsed.forwarded || false;
      if (parsed.coreAgentResponse) {
        taskId = parsed.coreAgentResponse.id || 'N/A';
        openclawResponse = parsed.coreAgentResponse.openclawResponse;
      }
    } catch (e) {}

    if (success && forwarded && taskId !== 'N/A') {
      console.log(`   Result: ✅ PASS`);
      console.log(`     - Status: ${e2eResult.statusCode}`);
      console.log(`     - Task ID: ${taskId}`);
      if (openclawResponse && openclawResponse.response) {
        const summary = typeof openclawResponse.response === 'string' 
          ? openclawResponse.response.substring(0, 80) + '...' 
          : 'Received';
        console.log(`     - OpenClaw Response: ${summary}`);
      }
      console.log(`     - Total Round-Trip: ${e2eDuration.toFixed(2)}ms`);
      results.tests.push({ name: 'End-to-End Flow', status: 'PASS', durationMs: e2eDuration });
      results.passed++;
    } else {
      console.log(`   Result: ❌ FAIL`);
      console.log(`     - Status: ${e2eResult.statusCode}`);
      console.log(`     - Response: ${e2eResult.data.substring(0, 200)}`);
      results.tests.push({ name: 'End-to-End Flow', status: 'FAIL', durationMs: e2eDuration });
      results.failed++;
    }
  } catch (error) {
    console.log(`   Result: ❌ FAIL`);
    console.log(`     - Error: ${error.message}`);
    results.tests.push({ name: 'End-to-End Flow', status: 'FAIL', error: error.message });
    results.failed++;
  }

  // Test 5: Dust-specific query
  console.log('');
  console.log('3. Dust-Specific Query Test');
  console.log('   Query: "What is my dust balance?"');
  try {
    const testStartTime = process.hrtime.bigint();
    const dustResult = await sendMockTelegramMessage('dusty_user', 'dusty_chat', 'What is my dust balance?');
    const dustDuration = Number(process.hrtime.bigint() - testStartTime) / 1_000_000;

    const success = dustResult.statusCode === 200;
    let taskId = 'N/A';
    let hasBalanceInfo = false;
    try {
      const parsed = JSON.parse(dustResult.data);
      if (parsed.coreAgentResponse) {
        taskId = parsed.coreAgentResponse.id || 'N/A';
        const resp = parsed.coreAgentResponse.openclawResponse;
        if (resp && resp.response && 
            (resp.response.includes('Balance') || resp.response.includes('ETH') || resp.response.includes('USD'))) {
          hasBalanceInfo = true;
        }
      }
    } catch (e) {}

    if (success && taskId !== 'N/A' && hasBalanceInfo) {
      console.log(`   Result: ✅ PASS`);
      console.log(`     - Status: ${dustResult.statusCode}`);
      console.log(`     - Task ID: ${taskId}`);
      console.log(`     - Balance Response: ✅ Contains balance data`);
      console.log(`     - Response Time: ${dustDuration.toFixed(2)}ms`);
      results.tests.push({ name: 'Dust-Specific Query', status: 'PASS', durationMs: dustDuration });
      results.passed++;
    } else {
      console.log(`   Result: ❌ FAIL`);
      console.log(`     - Status: ${dustResult.statusCode}`);
      console.log(`     - Response: ${dustResult.data.substring(0, 200)}`);
      results.tests.push({ name: 'Dust-Specific Query', status: 'FAIL', durationMs: dustDuration });
      results.failed++;
    }
  } catch (error) {
    console.log(`   Result: ❌ FAIL`);
    console.log(`     - Error: ${error.message}`);
    results.tests.push({ name: 'Dust-Specific Query', status: 'FAIL', error: error.message });
    results.failed++;
  }

  // Summary
  console.log('');
  console.log('=== Test Summary ===');
  console.log(`Total Tests: ${results.passed + results.failed}`);
  console.log(`Passed: ${results.passed} ✅`);
  console.log(`Failed: ${results.failed} ${results.failed > 0 ? '❌' : ''}`);
  console.log('');
  console.log('Timing Breakdown:');
  let totalDuration = 0;
  results.tests.forEach(test => {
    if (test.durationMs) {
      console.log(`  ${test.name}: ${test.durationMs.toFixed(2)}ms`);
      totalDuration += test.durationMs;
    }
  });
  console.log(`  Total Test Duration: ${totalDuration.toFixed(2)}ms`);
  console.log('');
  console.log(`Overall Status: ${results.failed === 0 ? '✅ ALL TESTS PASSED' : '❌ SOME TESTS FAILED'}`);
  console.log(`Timestamp: ${new Date().toISOString()}`);

  return results.failed === 0;
}

runTest().then(success => {
  process.exit(success ? 0 : 1);
}).catch(error => {
  console.error('Test runner error:', error);
  process.exit(1);
});
