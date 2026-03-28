#!/usr/bin/env node
/**
 * TEST MYL0NR0S.CLOUD
 * Browser automation test using Playwright
 */

const { chromium } = require('playwright');
const fs = require('fs').promises;
const path = require('path');

async function testWebsite() {
  console.log('='.repeat(70));
  console.log('🌐 TESTING MYL0NR0S.CLOUD');
  console.log('='.repeat(70));
  console.log();

  const browser = await chromium.launch({
    headless: true,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
  });

  const page = await context.newPage();
  const results = [];
  const screenshotsDir = '/root/.openclaw/workspace/test_screenshots';
  await fs.mkdir(screenshotsDir, { recursive: true });

  try {
    // Test 1: Homepage Load
    console.log('Test 1: Loading homepage...');
    const startTime = Date.now();
    const response = await page.goto('http://myl0nr0s.cloud', {
      waitUntil: 'networkidle',
      timeout: 60000
    });
    const loadTime = Date.now() - startTime;

    results.push({
      test: 'Homepage Load',
      status: response.ok() ? 'PASS' : 'FAIL',
      statusCode: response.status(),
      loadTime: `${loadTime}ms`,
      url: page.url()
    });

    console.log(`  ✅ Status: ${response.status()} (${loadTime}ms)`);

    // Test 2: Page Title
    const title = await page.title();
    results.push({
      test: 'Page Title',
      status: title ? 'PASS' : 'FAIL',
      value: title
    });
    console.log(`  ✅ Title: ${title}`);

    // Test 3: Check for key elements
    const elements = await page.evaluate(() => {
      return {
        hasHeader: !!document.querySelector('header'),
        hasNavigation: !!document.querySelector('nav'),
        hasFooter: !!document.querySelector('footer'),
        hasProducts: document.querySelectorAll('.product').length,
        hasCheckout: !!document.querySelector('[data-testid="checkout"]') ||
                     !!document.querySelector('#checkout'),
        totalLinks: document.querySelectorAll('a').length,
        totalImages: document.querySelectorAll('img').length
      };
    });

    results.push({
      test: 'Page Elements',
      status: 'INFO',
      elements: elements
    });

    console.log('  ✅ Page elements found:');
    console.log(`     - Header: ${elements.hasHeader}`);
    console.log(`     - Navigation: ${elements.hasNavigation}`);
    console.log(`     - Footer: ${elements.hasFooter}`);
    console.log(`     - Products: ${elements.hasProducts}`);
    console.log(`     - Links: ${elements.totalLinks}`);
    console.log(`     - Images: ${elements.totalImages}`);

    // Test 4: Screenshot
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const screenshotPath = path.join(screenshotsDir, `myl0nr0s_home_${timestamp}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    results.push({
      test: 'Screenshot',
      status: 'PASS',
      path: screenshotPath
    });
    console.log(`  ✅ Screenshot saved: ${path.basename(screenshotPath)}`);

    // Test 5: Check checkout page if exists
    try {
      console.log('\nTest 2: Testing checkout page...');
      await page.goto('http://myl0nr0s.cloud/checkout.html', {
        waitUntil: 'networkidle',
        timeout: 30000
      });

      const checkoutElements = await page.evaluate(() => {
        return {
          hasStripe: !!document.querySelector('[data-stripe]') ||
                     document.body.innerHTML.includes('stripe'),
          hasForm: !!document.querySelector('form'),
          hasPayment: !!document.querySelector('[data-payment]') ||
                      !!document.querySelector('#payment-form')
        };
      });

      results.push({
        test: 'Checkout Page',
        status: 'PASS',
        elements: checkoutElements
      });

      console.log(`  ✅ Checkout elements:`);
      console.log(`     - Stripe integration: ${checkoutElements.hasStripe}`);
      console.log(`     - Form present: ${checkoutElements.hasForm}`);
      console.log(`     - Payment section: ${checkoutElements.hasPayment}`);

    } catch (e) {
      results.push({
        test: 'Checkout Page',
        status: 'FAIL',
        error: e.message
      });
      console.log(`  ⚠️  Checkout test: ${e.message}`);
    }

    // Test 6: SSL/HTTPS check
    console.log('\nTest 3: Security check...');
    const securityInfo = await page.evaluate(() => {
      return {
        protocol: window.location.protocol,
        secure: window.location.protocol === 'https:'
      };
    });

    results.push({
      test: 'SSL/HTTPS',
      status: securityInfo.secure ? 'PASS' : 'WARN',
      protocol: securityInfo.protocol
    });
    console.log(`  ℹ️  Protocol: ${securityInfo.protocol}`);
    console.log(`  ℹ️  Secure: ${securityInfo.secure}`);

    // Final screenshot of checkout
    const checkoutScreenshot = path.join(screenshotsDir, `myl0nr0s_checkout_${timestamp}.png`);
    await page.screenshot({ path: checkoutScreenshot, fullPage: true });
    console.log(`  ✅ Checkout screenshot saved`);

  } catch (error) {
    console.error(`\n❌ Test error: ${error.message}`);
    results.push({
      test: 'Overall',
      status: 'FAIL',
      error: error.message
    });

    // Error screenshot
    const errorScreenshot = path.join(screenshotsDir, `myl0nr0s_error_${Date.now()}.png`);
    await page.screenshot({ path: errorScreenshot, fullPage: true });
    console.log(`  📸 Error screenshot saved: ${errorScreenshot}`);
  }

  await context.close();
  await browser.close();

  // Save results
  const resultsPath = path.join(screenshotsDir, `test_results_${Date.now()}.json`);
  await fs.writeFile(resultsPath, JSON.stringify(results, null, 2));

  // Summary
  console.log('\n' + '='.repeat(70));
  console.log('📊 TEST SUMMARY');
  console.log('='.repeat(70));

  const passed = results.filter(r => r.status === 'PASS').length;
  const failed = results.filter(r => r.status === 'FAIL').length;
  const total = results.length;

  console.log(`Total tests: ${total}`);
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`ℹ️  Info: ${total - passed - failed}`);
  console.log();
  console.log(`💾 Results saved to: ${resultsPath}`);
  console.log(`📸 Screenshots saved to: ${screenshotsDir}`);
  console.log('='.repeat(70));

  return results;
}

testWebsite().catch(console.error);
