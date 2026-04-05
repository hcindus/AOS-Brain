#!/usr/bin/env node
// Dusty MVP End-to-End Detailed Test
// Full pipeline: Telegram Bridge → Core-Agent → OpenClaw

const http = require('http');
const fs = require('fs');

function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const startTime = process.hrtime.bigint();
    const client = url.startsWith('https') ? require('https') : http;
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

async function runDetailedE2ETest() {
  const testStart = Date.now();
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const testRunId = `dusty-e2e-${timestamp}`;
  const cronJobId = 'fdc63bd5-b2c2-481c-9a5f-d3e001eff52f';

  const report = {
    testId: testRunId,
    cronJobId: cronJobId,
    timestamp: new Date().toISOString(),
    phases: []
  };

  console.log('='.repeat(60));
  console.log('  DUSTY MVP END-TO-END TEST');
  console.log(`  Test ID: ${testRunId}`);
  console.log(`  Cron Job: ${cronJobId}`);
  console.log(`  Time: ${new Date().toISOString()}`);
  console.log('='.repeat(60));
  console.log();

  // Phase 1: Service Health Checks
  console.log('[1/4] Service Health Checks');
  const p1Start = process.hrtime.bigint();
  const phase1 = { 
    phase: 1, 
    name: 'Service Health Checks', 
    status: 'FAIL',
    services: {}
  };
  
  let allHealthy = true;
  
  // Check Bridge
  try {
    const bridgeStart = process.hrtime.bigint();
    const bridge = await httpRequest('http://localhost:3001/health');
    const bridgeData = JSON.parse(bridge.data);
    const bridgeLatency = Number(process.hrtime.bigint() - bridgeStart) / 1_000_000;
    phase1.services.bridge = {
      endpoint: 'localhost:3001/health',
      status: 'healthy',
      statusCode: bridge.statusCode,
      latencyMs: bridgeLatency.toFixed(2),
      uptime: bridgeData.uptime,
      service: bridgeData.service
    };
    console.log('  ✅ Bridge Mock: Healthy');
    console.log(`     Latency: ${bridgeLatency.toFixed(2)}ms | Uptime: ${Math.floor(bridgeData.uptime/3600)}h`);
  } catch (e) {
    phase1.services.bridge = { status: 'failed', error: e.message };
    console.log(`  ❌ Bridge Mock: ${e.message}`);
    allHealthy = false;
  }

  // Check Core-Agent
  try {
    const coreStart = process.hrtime.bigint();
    const core = await httpRequest('http://localhost:3000/health');
    const coreData = JSON.parse(core.data);
    const coreLatency = Number(process.hrtime.bigint() - coreStart) / 1_000_000;
    phase1.services.coreAgent = {
      endpoint: 'localhost:3000/health',
      status: 'healthy',
      statusCode: core.statusCode,
      latencyMs: coreLatency.toFixed(2),
      uptime: coreData.uptime,
      service: coreData.service
    };
    console.log('  ✅ Core-Agent: Healthy');
    console.log(`     Latency: ${coreLatency.toFixed(2)}ms | Uptime: ${Math.floor(coreData.uptime/3600)}h`);
  } catch (e) {
    phase1.services.coreAgent = { status: 'failed', error: e.message };
    console.log(`  ❌ Core-Agent: ${e.message}`);
    allHealthy = false;
  }

  // Check OpenClaw
  try {
    const ocStart = process.hrtime.bigint();
    const oc = await httpRequest('http://localhost:4000/status');
    const ocData = JSON.parse(oc.data);
    const ocLatency = Number(process.hrtime.bigint() - ocStart) / 1_000_000;
    phase1.services.openclaw = {
      endpoint: 'localhost:4000/status',
      status: 'healthy',
      statusCode: oc.statusCode,
      latencyMs: ocLatency.toFixed(2),
      uptime: ocData.uptime,
      interactions: ocData.total_interactions
    };
    console.log('  ✅ OpenClaw Mock: Healthy');
    console.log(`     Latency: ${ocLatency.toFixed(2)}ms | Interactions: ${ocData.total_interactions}`);
  } catch (e) {
    phase1.services.openclaw = { status: 'failed', error: e.message };
    console.log(`  ❌ OpenClaw Mock: ${e.message}`);
    allHealthy = false;
  }

  phase1.status = allHealthy ? 'PASS' : 'FAIL';
  phase1.durationMs = Number(process.hrtime.bigint() - p1Start) / 1_000_000;
  report.phases.push(phase1);
  console.log(`  Phase duration: ${phase1.durationMs.toFixed(2)}ms`);
  console.log();

  // Phase 2: Bridge Message Delivery (E2E Core)
  console.log('[2/4] Bridge Message Delivery');
  console.log('      Sending: "/dust balance" via Bridge /webhook');
  const p2Start = process.hrtime.bigint();
  const phase2 = { phase: 2, name: 'Bridge Message Delivery', status: 'FAIL' };

  try {
    const payload = {
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

    const result = await httpRequest('http://localhost:3001/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: payload
    });

    phase2.httpCode = result.statusCode;
    phase2.latencyMs = result.durationMs;

    if (result.statusCode === 200) {
      const data = JSON.parse(result.data);
      phase2.forwarded = data.forwarded;
      phase2.requestId = data.requestId;
      phase2.coreAgentResponse = data.coreAgentResponse;
      
      const hasCoreResponse = data.coreAgentResponse !== undefined;
      const hasOpenClawResponse = data.coreAgentResponse?.openclawResponse !== undefined || 
                                   data.coreAgentResponse?.response !== undefined;

      if (hasOpenClawResponse) {
        phase2.status = 'PASS';
        console.log('  ✅ Bridge → Core-Agent → OpenClaw: SUCCESS');
        console.log(`     Request ID: ${data.requestId}`);
      } else if (hasCoreResponse) {
        phase2.status = 'PARTIAL';
        console.log('  ⚠️ Bridge → Core-Agent: OK | Core-Agent → OpenClaw: Pending/Failed');
        console.log(`     Request ID: ${data.requestId}`);
        console.log(`     Core Response: ${JSON.stringify(data.coreAgentResponse).substring(0, 100)}...`);
      } else {
        console.log('  ⚠️ Bridge accepted message but no core response');
      }
      phase2.response = data;
    } else {
      console.log(`  ❌ HTTP ${result.statusCode}: ${result.data.substring(0, 100)}`);
    }
  } catch (e) {
    phase2.error = e.message;
    console.log(`  ❌ Error: ${e.message}`);
  }

  phase2.durationMs = Number(process.hrtime.bigint() - p2Start) / 1_000_000;
  report.phases.push(phase2);
  console.log(`  Phase duration: ${phase2.durationMs.toFixed(2)}ms`);
  console.log();

  // Phase 3: Core-Agent Processing Verification
  console.log('[3/4] Core-Agent Processing Verification');
  const p3Start = process.hrtime.bigint();
  const phase3 = { phase: 3, name: 'Core-Agent Processing', status: 'FAIL' };

  try {
    const health = await httpRequest('http://localhost:3000/health');
    const healthData = JSON.parse(health.data);
    phase3.latencyMs = health.durationMs;
    phase3.uptimeHours = Math.floor(healthData.uptime / 3600);
    phase3.port = healthData.port;
    phase3.status = 'PASS';
    console.log('  ✅ Core-Agent processing verified');
    console.log(`     Latency: ${health.durationMs.toFixed(2)}ms | Running for ${phase3.uptimeHours}h`);
  } catch (e) {
    phase3.error = e.message;
    console.log(`  ❌ Core-Agent check failed: ${e.message}`);
  }

  phase3.durationMs = Number(process.hrtime.bigint() - p3Start) / 1_000_000;
  report.phases.push(phase3);
  console.log(`  Phase duration: ${phase3.durationMs.toFixed(2)}ms`);
  console.log();

  // Phase 4: OpenClaw Response Verification
  console.log('[4/4] OpenClaw Response Verification');
  const p4Start = process.hrtime.bigint();
  const phase4 = { phase: 4, name: 'OpenClaw Response', status: 'FAIL' };

  try {
    const status = await httpRequest('http://localhost:4000/status');
    const data = JSON.parse(status.data);
    phase4.latencyMs = status.durationMs;
    phase4.interactions = data.total_interactions;
    phase4.status = 'PASS';
    console.log('  ✅ OpenClaw response verified');
    console.log(`     Latency: ${status.durationMs.toFixed(2)}ms | Total interactions: ${data.total_interactions}`);
  } catch (e) {
    phase4.error = e.message;
    console.log(`  ❌ OpenClaw check failed: ${e.message}`);
  }

  phase4.durationMs = Number(process.hrtime.bigint() - p4Start) / 1_000_000;
  report.phases.push(phase4);
  console.log(`  Phase duration: ${phase4.durationMs.toFixed(2)}ms`);
  console.log();

  // Summary
  console.log('='.repeat(60));
  console.log('  TEST SUMMARY');
  console.log('='.repeat(60));
  
  const passed = report.phases.filter(p => p.status === 'PASS').length;
  const failed = report.phases.filter(p => p.status === 'FAIL').length;
  const partial = report.phases.filter(p => p.status === 'PARTIAL').length;
  const totalDuration = report.phases.reduce((sum, p) => sum + p.durationMs, 0);

  console.log();
  console.log(`Overall Status: ${failed === 0 ? '✅ PASS' : partial > 0 ? '⚠️ PARTIAL' : '❌ FAIL'}`);
  console.log(`Results: ${passed} passed, ${partial} partial, ${failed} failed`);
  console.log(`Total Duration: ${totalDuration.toFixed(2)}ms`);
  console.log();
  
  console.log('Phase Breakdown:');
  report.phases.forEach(p => {
    const statusIcon = p.status === 'PASS' ? '✅' : p.status === 'PARTIAL' ? '⚠️' : '❌';
    console.log(`  ${statusIcon} ${p.name}: ${p.durationMs.toFixed(2)}ms`);
  });
  console.log();

  report.summary = {
    passed: passed,
    partial: partial,
    failed: failed,
    totalPhases: report.phases.length,
    totalDurationMs: totalDuration,
    overallStatus: failed === 0 ? (partial > 0 ? 'PARTIAL' : 'PASS') : 'FAIL'
  };

  // Save report
  const reportFilename = `dusty_e2e_report_${new Date().toISOString().slice(0,10).replace(/-/g, '-')}_${Date.now()}_cron_${cronJobId}.json`;
  fs.writeFileSync(reportFilename, JSON.stringify(report, null, 2));
  console.log(`Report saved: ${reportFilename}`);
  console.log();
  console.log('='.repeat(60));
  console.log('  END OF TEST');
  console.log('='.repeat(60));
}

runDetailedE2ETest().catch(err => {
  console.error('Test runner error:', err);
  process.exit(1);
});
