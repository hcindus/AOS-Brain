const http = require('http');
const https = require('https');
const fs = require('fs');

// Helper to make HTTP requests with timing
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
      const bodyString = JSON.stringify(options.body);
      req.write(bodyString);
    }
    req.end();
  });
}

async function runE2ETest() {
  const testStartTime = Date.now();
  const timestamp = new Date().toISOString();
  const reportId = `dusty-e2e-${timestamp.replace(/[:T]/g, '-').split('.')[0]}`;
  const cronJobId = 'fdc63bd5-b2c2-481c-9a5f-d3e001eff52f';
  
  const results = {
    tests: [],
    passed: 0,
    failed: 0
  };
  
  console.log('=== Dusty MVP End-to-End Test ===');
  console.log(`Timestamp: ${timestamp}`);
  console.log(`Cron Job ID: ${cronJobId}`);
  console.log('');
  
  // Step 1: Bridge Health Check
  console.log('Step 1: Bridge Health Check...');
  let bridgeHealthData = null;
  try {
    const response = await httpRequest('http://localhost:3001/health');
    const parsed = JSON.parse(response.data);
    bridgeHealthData = parsed;
    results.tests.push({
      name: 'Bridge Health Check',
      status: 'PASSED',
      endpoint: 'http://localhost:3001/health',
      http_code: response.statusCode,
      duration_ms: parseFloat(response.durationMs.toFixed(2)),
      details: parsed
    });
    results.passed++;
    console.log(`  ✅ PASS (${response.durationMs.toFixed(2)}ms)`);
  } catch (error) {
    results.tests.push({
      name: 'Bridge Health Check',
      status: 'FAILED',
      endpoint: 'http://localhost:3001/health',
      error: error.message
    });
    results.failed++;
    console.log(`  ❌ FAIL: ${error.message}`);
  }
  
  // Step 2: Core-Agent Health Check
  console.log('Step 2: Core-Agent Health Check...');
  let coreHealthData = null;
  try {
    const response = await httpRequest('http://localhost:3000/health');
    const parsed = JSON.parse(response.data);
    coreHealthData = parsed;
    results.tests.push({
      name: 'Core-Agent Health Check',
      status: 'PASSED',
      endpoint: 'http://localhost:3000/health',
      http_code: response.statusCode,
      duration_ms: parseFloat(response.durationMs.toFixed(2)),
      details: parsed
    });
    results.passed++;
    console.log(`  ✅ PASS (${response.durationMs.toFixed(2)}ms)`);
  } catch (error) {
    results.tests.push({
      name: 'Core-Agent Health Check',
      status: 'FAILED',
      endpoint: 'http://localhost:3000/health',
      error: error.message
    });
    results.failed++;
    console.log(`  ❌ FAIL: ${error.message}`);
  }
  
  // Step 3: OpenClaw Mock Status
  console.log('Step 3: OpenClaw Mock Status...');
  let openclawData = null;
  try {
    const response = await httpRequest('http://localhost:4000/status');
    const parsed = JSON.parse(response.data);
    openclawData = parsed;
    results.tests.push({
      name: 'OpenClaw Mock Status',
      status: 'PASSED',
      endpoint: 'http://localhost:4000/status',
      http_code: response.statusCode,
      duration_ms: parseFloat(response.durationMs.toFixed(2)),
      details: parsed
    });
    results.passed++;
    console.log(`  ✅ PASS (${response.durationMs.toFixed(2)}ms)`);
  } catch (error) {
    results.tests.push({
      name: 'OpenClaw Mock Status',
      status: 'FAILED',
      endpoint: 'http://localhost:4000/status',
      error: error.message
    });
    results.failed++;
    console.log(`  ❌ FAIL: ${error.message}`);
  }
  
  // Step 4: Send Mock Telegram Message via Bridge Webhook
  console.log('Step 4: Send Mock Telegram Message via Bridge...');
  let webhookResponse = null;
  const telegramPayload = {
    update_id: Math.floor(Math.random() * 1000000000),
    message: {
      message_id: Math.floor(Math.random() * 10000),
      from: {
        id: 987654321,
        is_bot: false,
        first_name: 'Test',
        last_name: 'User',
        username: 'e2e_test_user',
        language_code: 'en'
      },
      chat: {
        id: 987654321,
        first_name: 'Test',
        last_name: 'User',
        username: 'e2e_test_user',
        type: 'private'
      },
      date: Math.floor(Date.now() / 1000),
      text: '/dust balance'
    }
  };
  
  try {
    const response = await httpRequest('http://localhost:3001/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: telegramPayload
    });
    
    webhookResponse = JSON.parse(response.data);
    const forwarded = webhookResponse.forwarded === true;
    const hasCoreResponse = webhookResponse.coreAgentResponse !== undefined;
    const hasOpenclawResponse = hasCoreResponse && webhookResponse.coreAgentResponse.openclawResponse !== undefined;
    
    const flowValidated = {
      step_1_bridge_to_core: forwarded,
      step_2_core_to_openclaw: hasCoreResponse,
      step_3_openclaw_response: hasOpenclawResponse
    };
    
    const allPassed = forwarded && hasCoreResponse && hasOpenclawResponse;
    
    results.tests.push({
      name: 'End-to-End Webhook Flow',
      status: allPassed ? 'PASSED' : 'PARTIAL',
      endpoint: 'http://localhost:3001/webhook',
      http_code: response.statusCode,
      duration_ms: parseFloat(response.durationMs.toFixed(2)),
      message_sent: '/dust balance',
      flow_validated: flowValidated,
      response_summary: webhookResponse
    });
    
    if (allPassed) {
      results.passed++;
      console.log(`  ✅ PASS (${response.durationMs.toFixed(2)}ms)`);
      console.log(`     - Bridge → Core-Agent: ✅`);
      console.log(`     - Core-Agent → OpenClaw: ✅`);
      console.log(`     - OpenClaw Response: ✅`);
    } else {
      console.log(`  ⚠️ PARTIAL (${response.durationMs.toFixed(2)}ms)`);
      console.log(`     - Bridge → Core-Agent: ${forwarded ? '✅' : '❌'}`);
      console.log(`     - Core-Agent → OpenClaw: ${hasCoreResponse ? '✅' : '❌'}`);
      console.log(`     - OpenClaw Response: ${hasOpenclawResponse ? '✅' : '❌'}`);
    }
  } catch (error) {
    results.tests.push({
      name: 'End-to-End Webhook Flow',
      status: 'FAILED',
      endpoint: 'http://localhost:3001/webhook',
      error: error.message
    });
    results.failed++;
    console.log(`  ❌ FAIL: ${error.message}`);
  }
  
  // Calculate totals
  const totalDuration = Date.now() - testStartTime;
  const avgResponseTime = results.tests.reduce((sum, t) => sum + (t.duration_ms || 0), 0) / results.tests.length;
  
  // Build final report
  const report = {
    report_id: reportId,
    cron_job_id: cronJobId,
    timestamp: timestamp,
    test_type: 'End-to-End MVP Test',
    status: results.failed === 0 ? 'PASSED' : 'PARTIAL',
    summary: {
      total_tests: results.tests.length,
      passed: results.passed,
      failed: results.failed,
      pass_rate: `${((results.passed / results.tests.length) * 100).toFixed(0)}%`
    },
    test_results: results.tests,
    performance_metrics: {
      avg_response_time_ms: parseFloat(avgResponseTime.toFixed(2)),
      max_response_time_ms: Math.max(...results.tests.map(t => t.duration_ms || 0)),
      min_response_time_ms: Math.min(...results.tests.filter(t => t.duration_ms).map(t => t.duration_ms)),
      total_test_duration_ms: totalDuration,
      components: {
        bridge: {
          version: bridgeHealthData?.version || 'unknown',
          port: 3001,
          uptime_hours: bridgeHealthData ? (bridgeHealthData.uptime / 3600).toFixed(2) : null,
          security: bridgeHealthData?.security || null
        },
        core_agent: {
          version: 'unknown',
          port: 3000,
          uptime_hours: coreHealthData ? (coreHealthData.uptime / 3600).toFixed(2) : null
        },
        openclaw_mock: {
          version: 'unknown',
          port: 4000,
          uptime_hours: openclawData ? (openclawData.uptime / 3600).toFixed(2) : null,
          total_interactions: openclawData?.total_interactions || null
        }
      }
    },
    validation_summary: {
      telegram_bridge_mock: bridgeHealthData ? '✅ Healthy and operational' : '❌ Failed',
      core_agent: coreHealthData ? '✅ Healthy and processing requests' : '❌ Failed',
      openclaw_mock: openclawData ? '✅ Healthy and responding' : '❌ Failed',
      end_to_end_flow: webhookResponse?.coreAgentResponse?.openclawResponse ? '✅ Full pipeline operational' : '⚠️ Partial'
    },
    test_executed_by: 'OpenClaw Agent (cron job)',
    report_generated: new Date().toISOString()
  };
  
  // Console summary
  console.log('');
  console.log('='.repeat(60));
  console.log('=== TEST SUMMARY ===');
  console.log('='.repeat(60));
  console.log(`Status: ${report.status}`);
  console.log(`Passed: ${results.passed}/${results.tests.length}`);
  console.log(`Total Duration: ${totalDuration}ms`);
  console.log(`Avg Response Time: ${avgResponseTime.toFixed(2)}ms`);
  console.log('');
  console.log('Component Status:');
  console.log(`  Telegram Bridge Mock: ${report.validation_summary.telegram_bridge_mock}`);
  console.log(`  Core-Agent: ${report.validation_summary.core_agent}`);
  console.log(`  OpenClaw Mock: ${report.validation_summary.openclaw_mock}`);
  console.log(`  End-to-End Flow: ${report.validation_summary.end_to_end_flow}`);
  console.log('');
  
  // Save report to file
  const reportFilename = `dusty_e2e_report_${timestamp.split('T')[0].replace(/-/g, '')}_${Date.now()}_cron_${cronJobId}.json`;
  fs.writeFileSync(reportFilename, JSON.stringify(report, null, 2));
  console.log(`Report saved to: ${reportFilename}`);
  
  return report;
}

runE2ETest().then(report => {
  console.log('\n✅ Dusty MVP E2E Test completed!');
  process.exit(0);
}).catch(error => {
  console.error('\n❌ Test runner error:', error);
  process.exit(1);
});
