const http = require('http');
const https = require('https');
const fs = require('fs');

function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const startTime = process.hrtime.bigint();
    const client = url.startsWith('https') ? https : http;
    const reqUrl = new URL(url);
    const reqOptions = {
      hostname: reqUrl.hostname,
      port: reqUrl.port,
      path: reqUrl.pathname + reqUrl.search,
      method: options.method || 'GET',
      headers: options.headers || {}
    };
    const req = client.request(reqOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const endTime = process.hrtime.bigint();
        const durationMs = Number(endTime - startTime) / 1_000_000;
        resolve({ statusCode: res.statusCode, data, durationMs, headers: res.headers });
      });
    });
    req.on('error', reject);
    if (options.body) {
      req.write(JSON.stringify(options.body));
    }
    req.end();
  });
}

async function sendWebhookMessage(userId, chatId, text, username = 'testuser') {
  const telegramPayload = {
    update_id: Math.floor(Math.random() * 1000000000),
    message: {
      message_id: Math.floor(Math.random() * 10000),
      from: { id: userId, is_bot: false, first_name: 'Test', last_name: 'User', username: username, language_code: 'en' },
      chat: { id: chatId, first_name: 'Test', last_name: 'User', username: username, type: 'private' },
      date: Math.floor(Date.now() / 1000),
      text: text
    }
  };
  return httpRequest('http://localhost:3001/webhook', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: telegramPayload
  });
}

async function runTest() {
  const testId = `dusty-e2e-fdc63bd5-b2c2-481c-9a5f-d3e001eff52f-${Date.now()}`;
  const timestamp = new Date().toISOString();
  const results = {
    testId,
    timestamp,
    overallStatus: 'UNKNOWN',
    summary: { totalSteps: 4, passed: 0, failed: 0, passRate: 0, totalDurationMs: 0 },
    steps: []
  };
  const totalStart = Date.now();

  console.log('🧪 Dusty MVP End-to-End Test');
  console.log(`   Test ID: ${testId}`);
  console.log(`   Time: ${timestamp}`);
  console.log('');

  // Step 1: Health Checks
  const step1Start = Date.now();
  let step1 = { name: 'Service Health Checks', status: 'PASS', durationMs: 0, details: {} };
  try {
    const bridge = await httpRequest('http://localhost:3001/health');
    const core = await httpRequest('http://localhost:3000/health');
    const claw = await httpRequest('http://localhost:4000/status');
    
    const bridgeOk = bridge.statusCode === 200;
    const coreOk = core.statusCode === 200;
    const clawOk = claw.statusCode === 200;
    
    step1.status = (bridgeOk && coreOk && clawOk) ? 'PASS' : 'FAIL';
    step1.details = {
      bridge: bridgeOk,
      core_agent: coreOk,
      openclaw: clawOk,
      bridgeUptime: bridgeOk ? JSON.parse(bridge.data).uptime : null,
      coreUptime: coreOk ? JSON.parse(core.data).uptime : null,
      openclawInteractions: clawOk ? JSON.parse(claw.data).total_interactions : null
    };
    step1.durationMs = Date.now() - step1Start;
    
    console.log('✅ Service Health Checks');
    console.log(`   Bridge: ${bridgeOk ? 'healthy' : 'DOWN'}`);
    console.log(`   Core-Agent: ${coreOk ? 'healthy' : 'DOWN'}`);
    console.log(`   OpenClaw: ${clawOk ? 'healthy' : 'DOWN'}`);
  } catch (e) {
    step1.status = 'FAIL';
    step1.error = e.message;
    step1.durationMs = Date.now() - step1Start;
    console.log('❌ Service Health Checks Failed:', e.message);
  }
  results.steps.push(step1);

  // Step 2: Bridge Message Delivery
  const step2Start = Date.now();
  let step2 = { name: 'Bridge Message Delivery', status: 'PASS', durationMs: 0, details: {} };
  try {
    const webhook = await sendWebhookMessage(999999, 999999, '/dust balance', 'e2e_tester');
    const parsed = JSON.parse(webhook.data);
    
    step2.status = (webhook.statusCode === 200 && parsed.ok && parsed.forwarded) ? 'PASS' : 'FAIL';
    step2.details = {
      status_code: webhook.statusCode,
      forwarded: parsed.forwarded,
      requestId: parsed.requestId,
      has_openclaw_response: parsed.coreAgentResponse?.openclawResponse !== undefined
    };
    step2.durationMs = Date.now() - step2Start;
    
    console.log('');
    console.log('✅ Bridge Message Delivery');
    console.log(`   Request ID: ${parsed.requestId}`);
    console.log(`   Forwarded to Core-Agent: ${parsed.forwarded}`);
    console.log(`   OpenClaw Response: ${parsed.coreAgentResponse?.openclawResponse ? 'YES' : 'NO'}`);
  } catch (e) {
    step2.status = 'FAIL';
    step2.error = e.message;
    step2.durationMs = Date.now() - step2Start;
    console.log('❌ Bridge Message Delivery Failed:', e.message);
  }
  results.steps.push(step2);

  // Step 3: Core-Agent Processing
  const step3Start = Date.now();
  let step3 = { name: 'Core-Agent Processing', status: 'PASS', durationMs: 0, details: {} };
  try {
    const webhook = await sendWebhookMessage(888888, 888888, 'What is my dust balance?', 'tester2');
    const parsed = JSON.parse(webhook.data);
    
    const hasCoreResponse = parsed.coreAgentResponse !== undefined;
    const hasProcessing = parsed.coreAgentResponse?.id && parsed.coreAgentResponse?.status;
    
    step3.status = (hasCoreResponse && hasProcessing) ? 'PASS' : 'FAIL';
    step3.details = {
      has_core_response: hasCoreResponse,
      task_id: parsed.coreAgentResponse?.id,
      status: parsed.coreAgentResponse?.status
    };
    step3.durationMs = Date.now() - step3Start;
    
    console.log('');
    console.log('✅ Core-Agent Processing');
    console.log(`   Task ID: ${parsed.coreAgentResponse?.id}`);
    console.log(`   Status: ${parsed.coreAgentResponse?.status}`);
  } catch (e) {
    step3.status = 'FAIL';
    step3.error = e.message;
    step3.durationMs = Date.now() - step3Start;
    console.log('❌ Core-Agent Processing Failed:', e.message);
  }
  results.steps.push(step3);

  // Step 4: OpenClaw Response
  const step4Start = Date.now();
  let step4 = { name: 'OpenClaw Response', status: 'PASS', durationMs: 0, details: {} };
  try {
    const webhook = await sendWebhookMessage(777777, 777777, '/dust holdings', 'tester3');
    const parsed = JSON.parse(webhook.data);
    
    const ocResponse = parsed.coreAgentResponse?.openclawResponse;
    const hasBot = ocResponse?.bot === 'dusty';
    const hasContent = ocResponse?.response !== undefined;
    const hasData = ocResponse?.data !== undefined;
    
    step4.status = (hasBot && hasContent && hasData) ? 'PASS' : 'FAIL';
    step4.details = {
      bot_name: ocResponse?.bot,
      has_response: hasContent,
      has_data: hasData,
      action: ocResponse?.action,
      response_preview: ocResponse?.response?.substring(0, 50)+
'...'
    };
    step4.durationMs = Date.now() - step4Start;
    
    console.log('');
    console.log('✅ OpenClaw Response');
    console.log(`   Bot: ${ocResponse?.bot}`);
    console.log(`   Action: ${ocResponse?.action}`);
    console.log(`   Preview: "${ocResponse?.response?.substring(0, 60)}..."`);
  } catch (e) {
    step4.status = 'FAIL';
    step4.error = e.message;
    step4.durationMs = Date.now() - step4Start;
    console.log('❌ OpenClaw Response Failed:', e.message);
  }
  results.steps.push(step4);

  // Final Summary
  const totalDuration = Date.now() - totalStart;
  const passed = results.steps.filter(s => s.status === 'PASS').length;
  const failed = results.steps.filter(s => s.status === 'FAIL').length;
  
  results.summary.passed = passed;
  results.summary.failed = failed;
  results.summary.passRate = Math.round((passed / results.summary.totalSteps) * 100);
  results.summary.totalDurationMs = totalDuration;
  results.overallStatus = (failed === 0) ? '✅ PASS' : '❌ FAIL';

  // Save reports
  const dateStr = timestamp.split('T')[0];
  const jsonPath = `/root/.openclaw/workspace/dusty_e2e_report_${dateStr}_${Date.now()}_cron_fdc63bd5.json`;
  const mdPath = `/root/.openclaw/workspace/dusty_e2e_test_report_${dateStr}_${Date.now()}_cron_fdc63bd5.md`;
  
  // JSON
  fs.writeFileSync(jsonPath, JSON.stringify(results, null, 2));
  
  // Markdown
  let md = `# Dusty E2E Test Report

**Test ID:** ${testId}

**Timestamp:** ${timestamp}

**Overall Status:** ${results.overallStatus}

## Summary

- **Total Steps:** ${results.summary.totalSteps}
- **Passed:** ${results.summary.passed}
- **Failed:** ${results.summary.failed}
- **Pass Rate:** ${results.summary.passRate}%
- **Total Duration:** ${results.summary.totalDurationMs.toFixed(2)}ms

## Step Details

`;
  results.steps.forEach(step => {
    md += `### ${step.status === 'PASS' ? '✅' : '❌'} ${step.name}

- **Status:** ${step.status}
- **Duration:** ${step.durationMs}ms
- **Details:** 
\`\`\`json
${JSON.stringify(step.details, null, 2)}
\`\`\`

`;
  });
  
  fs.writeFileSync(mdPath, md);

  console.log('');
  console.log('='.repeat(50));
  console.log(`📊 TEST SUMMARY: ${results.overallStatus}`);
  console.log('='.repeat(50));
  console.log(`Total Steps: ${results.summary.totalSteps}`);
  console.log(`Passed: ${results.summary.passed} | Failed: ${results.summary.failed}`);
  console.log(`Pass Rate: ${results.summary.passRate}%`);
  console.log(`Duration: ${results.summary.totalDurationMs}ms`);
  console.log('');
  console.log(`📁 Reports saved:`);
  console.log(`   JSON: ${jsonPath}`);
  console.log(`   MD: ${mdPath}`);

  return results;
}

runTest();
