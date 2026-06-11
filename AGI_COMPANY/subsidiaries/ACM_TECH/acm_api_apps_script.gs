/**
 * ACM Technologies SOAP API Client
 * Google Apps Script Version
 * 
 * For use in Google Sheets to automate ACM orders
 * Based on Jon Scarpa's 2026-05-15 email specifications
 * 
 * Customer ID: 71152
 * Company: Performance Supply Depot
 */

// Configuration - Update these with your credentials
const CONFIG = {
  USER_ID: '71152',
  PASSWORD: 'UPP9EvDE9xkEpI', // Update with actual password
  BASE_URL: 'https://api.acmtech.com/DataIntegration.asmx'
};

/**
 * Step 1: Begin Transaction
 * Returns Transaction_ID for use in subsequent steps
 * @returns {string} Transaction ID or null on error
 */
function step1BeginTransaction() {
  const action = 'Step1_BeginTransaction';
  
  const body = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step1_BeginTransaction xmlns="http://microsoft.com/webservices/">
      <UserID>${CONFIG.USER_ID}</UserID>
      <Password>${CONFIG.PASSWORD}</Password>
    </Step1_BeginTransaction>
  </soap:Body>
</soap:Envelope>`;

  const response = makeSOAPRequest(action, body);
  
  if (!response.success) {
    console.error('Step 1 failed:', response.error);
    return null;
  }
  
  // Extract Transaction_ID from response
  const transactionId = extractFromXML(response.content, 'Transaction_ID');
  console.log('Transaction ID:', transactionId);
  return transactionId;
}

/**
 * Step 2: Submit Order Header
 * @param {string} transactionId - From Step 1
 * @param {Object} header - Order header data
 * @returns {boolean} Success status
 */
function step2OrderHeader(transactionId, header) {
  const action = 'Step2_OrderHeaderFulfillment';
  
  const body = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step2_OrderHeaderFulfillment xmlns="http://microsoft.com/webservices/">
      <UserID>${CONFIG.USER_ID}</UserID>
      <Password>${CONFIG.PASSWORD}</Password>
      <Transaction_ID>${transactionId}</Transaction_ID>
      <OrderDate>${header.orderDate}</OrderDate>
      <PO>${header.poNumber}</PO>
      <ItemCnt>${header.itemCount}</ItemCnt>
      <MailingName>${header.mailingName}</MailingName>
      <Address1>${header.address1}</Address1>
      <City>${header.city}</City>
      <State>${header.state}</State>
      <Zip>${header.zip}</Zip>
      <Country>${header.country || 'US'}</Country>
      ${header.address2 ? `<Address2>${header.address2}</Address2>` : ''}
    </Step2_OrderHeaderFulfillment>
  </soap:Body>
</soap:Envelope>`;

  const response = makeSOAPRequest(action, body);
  console.log('Order Header:', response.success ? 'Success' : 'Failed');
  return response.success;
}

/**
 * Step 3: Submit Order Detail Line
 * Called once per line item
 * @param {string} transactionId - From Step 1
 * @param {Object} item - Line item data
 * @returns {boolean} Success status
 */
function step3OrderDetail(transactionId, item) {
  const action = 'Step3_OrderDetailFulfillment';
  
  const body = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step3_OrderDetailFulfillment xmlns="http://microsoft.com/webservices/">
      <UserID>${CONFIG.USER_ID}</UserID>
      <Password>${CONFIG.PASSWORD}</Password>
      <Transaction_ID>${transactionId}</Transaction_ID>
      <ACM_ItemNo>${item.sku}</ACM_ItemNo>
      <Qty>${item.quantity}</Qty>
      <Price>${item.price.toFixed(2)}</Price>
    </Step3_OrderDetailFulfillment>
  </soap:Body>
</soap:Envelope>`;

  const response = makeSOAPRequest(action, body);
  console.log(`Line Item ${item.sku}:`, response.success ? 'Success' : 'Failed');
  return response.success;
}

/**
 * Step 4: Check Availability (Optional)
 * Real-time inventory check before finalizing
 * @param {string} transactionId - From Step 1
 * @returns {Object} Availability status
 */
function step4CheckAvailability(transactionId) {
  const action = 'Step4_CheckAvailability';
  
  const body = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step4_CheckAvailability xmlns="http://microsoft.com/webservices/">
      <UserID>${CONFIG.USER_ID}</UserID>
      <Password>${CONFIG.PASSWORD}</Password>
      <Transaction_ID>${transactionId}</Transaction_ID>
    </Step4_CheckAvailability>
  </soap:Body>
</soap:Envelope>`;

  const response = makeSOAPRequest(action, body);
  
  return {
    available: response.success,
    details: response.content
  };
}

/**
 * Step 5: End Transaction
 * Finalizes order and returns confirmation
 * @param {string} transactionId - From Step 1
 * @returns {string} Order ID or null on error
 */
function step5EndTransaction(transactionId) {
  const action = 'Step5_EndTransaction';
  
  const body = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Step5_EndTransaction xmlns="http://microsoft.com/webservices/">
      <UserID>${CONFIG.USER_ID}</UserID>
      <Password>${CONFIG.PASSWORD}</Password>
      <Transaction_ID>${transactionId}</Transaction_ID>
    </Step5_EndTransaction>
  </soap:Body>
</soap:Envelope>`;

  const response = makeSOAPRequest(action, body);
  
  if (!response.success) {
    console.error('Step 5 failed:', response.error);
    return null;
  }
  
  const orderId = extractFromXML(response.content, 'OrderID');
  console.log('Order ID:', orderId);
  return orderId;
}

/**
 * Complete Order Submission Workflow
 * Steps: 1 → 2 → 3 → 4 → 5
 * @param {Object} header - Order header
 * @param {Array} items - Array of line items
 * @returns {Object} Result with success flag and order ID
 */
function submitFullOrder(header, items) {
  const result = {
    success: false,
    transactionId: null,
    orderId: null,
    error: null,
    stepsCompleted: []
  };
  
  // Step 1: Begin Transaction
  const transactionId = step1BeginTransaction();
  if (!transactionId) {
    result.error = 'Failed to begin transaction (Step 1)';
    return result;
  }
  result.transactionId = transactionId;
  result.stepsCompleted.push(1);
  
  // Step 2: Order Header
  if (!step2OrderHeader(transactionId, header)) {
    result.error = 'Failed to submit order header (Step 2)';
    return result;
  }
  result.stepsCompleted.push(2);
  
  // Step 3: Order Detail (for each item)
  for (let item of items) {
    if (!step3OrderDetail(transactionId, item)) {
      result.error = `Failed to submit line item: ${item.sku}`;
      return result;
    }
  }
  result.stepsCompleted.push(3);
  
  // Step 4: Check Availability
  const availability = step4CheckAvailability(transactionId);
  if (!availability.available) {
    result.error = 'Items not available';
    return result;
  }
  result.stepsCompleted.push(4);
  
  // Step 5: End Transaction
  const orderId = step5EndTransaction(transactionId);
  if (!orderId) {
    result.error = 'Failed to finalize transaction (Step 5)';
    return result;
  }
  
  result.orderId = orderId;
  result.stepsCompleted.push(5);
  result.success = true;
  
  return result;
}

/**
 * Get Product List (Page 24)
 * Returns daily pricing, inventory, and image links
 * @returns {Array} Product list
 */
function getProductList() {
  const action = 'GetProductList';
  
  const body = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetProductList xmlns="http://microsoft.com/webservices/">
      <UserID>${CONFIG.USER_ID}</UserID>
      <Password>${CONFIG.PASSWORD}</Password>
    </GetProductList>
  </soap:Body>
</soap:Envelope>`;

  const response = makeSOAPRequest(action, body);
  
  if (!response.success) {
    console.error('Failed to get product list:', response.error);
    return [];
  }
  
  return parseProductList(response.content);
}

/**
 * Get Tracking Information (Page 16)
 * @param {string} orderId - Order ID
 * @returns {Array} Tracking details
 */
function getTracking(orderId) {
  const action = 'GetTracking';
  
  const body = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetTracking xmlns="http://microsoft.com/webservices/">
      <UserID>${CONFIG.USER_ID}</UserID>
      <Password>${CONFIG.PASSWORD}</Password>
      <Order_ID>${orderId}</Order_ID>
    </GetTracking>
  </soap:Body>
</soap:Envelope>`;

  const response = makeSOAPRequest(action, body);
  return response.success ? parseTracking(response.content) : [];
}

/**
 * Get Invoice Summary (Pages 19-20)
 * @param {string} startDate - Format: YYYY/MM/DD
 * @param {string} endDate - Format: YYYY/MM/DD
 * @returns {Array} Invoice list
 */
function getInvoiceSummary(startDate, endDate) {
  const action = 'GetInvoiceSummary';
  
  const body = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetInvoiceSummary xmlns="http://microsoft.com/webservices/">
      <UserID>${CONFIG.USER_ID}</UserID>
      <Password>${CONFIG.PASSWORD}</Password>
      <Start_Date>${startDate}</Start_Date>
      <End_Date>${endDate}</End_Date>
    </GetInvoiceSummary>
  </soap:Body>
</soap:Envelope>`;

  const response = makeSOAPRequest(action, body);
  return response.success ? parseInvoices(response.content) : [];
}

/**
 * Get Invoice Detail (Page 20)
 * @param {string} invoiceId - Invoice ID
 * @returns {Object} Invoice detail
 */
function getInvoiceDetail(invoiceId) {
  const action = 'GetInvoiceDetail';
  
  const body = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetInvoiceDetail xmlns="http://microsoft.com/webservices/">
      <UserID>${CONFIG.USER_ID}</UserID>
      <Password>${CONFIG.PASSWORD}</Password>
      <Invoice_ID>${invoiceId}</Invoice_ID>
    </GetInvoiceDetail>
  </soap:Body>
</soap:Envelope>`;

  const response = makeSOAPRequest(action, body);
  return response.success ? parseInvoiceDetail(response.content) : null;
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Make SOAP request to ACM API
 * @param {string} action - SOAP action
 * @param {string} body - SOAP body XML
 * @returns {Object} Response with success flag and content
 */
function makeSOAPRequest(action, body) {
  const url = CONFIG.BASE_URL;
  
  const options = {
    method: 'post',
    contentType: 'text/xml; charset=utf-8',
    headers: {
      'SOAPAction': `http://microsoft.com/webservices/${action}`
    },
    payload: body,
    muteHttpExceptions: true
  };
  
  try {
    const response = UrlFetchApp.fetch(url, options);
    const responseCode = response.getResponseCode();
    const responseText = response.getContentText();
    
    if (responseCode === 200) {
      return {
        success: true,
        content: responseText,
        code: responseCode
      };
    } else {
      return {
        success: false,
        error: `HTTP ${responseCode}: ${responseText.substring(0, 200)}`,
        code: responseCode
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.toString()
    };
  }
}

/**
 * Extract value from XML by tag name
 * @param {string} xml - XML string
 * @param {string} tagName - Tag to find
 * @returns {string|null} Extracted value
 */
function extractFromXML(xml, tagName) {
  const regex = new RegExp(`<${tagName}[^>]*>([^<]+)</${tagName}>`, 'i');
  const match = xml.match(regex);
  return match ? match[1] : null;
}

/**
 * Parse product list from XML
 * @param {string} xml - XML response
 * @returns {Array} Product objects
 */
function parseProductList(xml) {
  const products = [];
  // Parse logic would go here based on actual ACM response format
  return products;
}

/**
 * Parse tracking info from XML
 * @param {string} xml - XML response
 * @returns {Array} Tracking objects
 */
function parseTracking(xml) {
  const tracking = [];
  // Parse logic would go here based on actual ACM response format
  return tracking;
}

/**
 * Parse invoices from XML
 * @param {string} xml - XML response
 * @returns {Array} Invoice objects
 */
function parseInvoices(xml) {
  const invoices = [];
  // Parse logic would go here based on actual ACM response format
  return invoices;
}

/**
 * Parse invoice detail from XML
 * @param {string} xml - XML response
 * @returns {Object} Invoice detail
 */
function parseInvoiceDetail(xml) {
  const detail = { lines: [], totals: {} };
  // Parse logic would go here based on actual ACM response format
  return detail;
}

// ============================================================================
// GOOGLE SHEETS INTEGRATION
// ============================================================================

/**
 * Test connection to ACM API
 * Run this first to verify connectivity
 */
function testConnection() {
  console.log('Testing ACM API connection...');
  const transactionId = step1BeginTransaction();
  
  if (transactionId) {
    console.log('✅ Connection successful! Transaction ID:', transactionId);
    return true;
  } else {
    console.log('❌ Connection failed');
    return false;
  }
}

/**
 * Submit order from Google Sheets
 * Assumes sheet has columns: PO, Date, Name, Address1, City, State, Zip, SKU1, Qty1, Price1, SKU2, Qty2, Price2...
 */
function submitOrderFromSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  
  // Assuming first row is headers, data starts from row 2
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    
    const header = {
      orderDate: Utilities.formatDate(new Date(row[1]), Session.getScriptTimeZone(), 'yyyy/MM/dd'),
      poNumber: row[0].toString(),
      itemCount: 1, // Calculate based on SKU columns
      mailingName: row[2],
      address1: row[3],
      city: row[5],
      state: row[6],
      zip: row[7].toString()
    };
    
    const items = [{
      sku: row[8],
      quantity: parseInt(row[9]),
      price: parseFloat(row[10])
    }];
    
    const result = submitFullOrder(header, items);
    
    // Write result back to sheet
    if (result.success) {
      sheet.getRange(i + 1, 12).setValue(`✅ Order ${result.orderId}`);
    } else {
      sheet.getRange(i + 1, 12).setValue(`❌ ${result.error}`);
    }
  }
}

/**
 * Create menu in Google Sheets
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('ACM Orders')
    .addItem('Test Connection', 'testConnection')
    .addItem('Submit Orders', 'submitOrderFromSheet')
    .addItem('Get Products', 'showProductList')
    .addToUi();
}

/**
 * Show product list in dialog
 */
function showProductList() {
  const products = getProductList();
  
  const html = HtmlService.createHtmlOutput(
    '<pre>' + JSON.stringify(products, null, 2) + '</pre>'
  ).setWidth(600).setHeight(400);
  
  SpreadsheetApp.getUi().showModalDialog(html, 'ACM Product List');
}

/**
 * Example usage in Apps Script
 */
function exampleUsage() {
  // Test connection first
  if (!testConnection()) {
    console.log('Cannot connect to ACM API');
    return;
  }
  
  // Create order
  const header = {
    orderDate: Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy/MM/dd'),
    poNumber: 'PO-2026-001',
    itemCount: 1,
    mailingName: 'David Johnson',
    address1: '1234 Gale Ave',
    city: 'Eureka',
    state: 'CA',
    zip: '90165',
    country: 'US'
  };
  
  const items = [{
    sku: '652334560T',
    quantity: 5,
    price: 23.99
  }];
  
  const result = submitFullOrder(header, items);
  
  if (result.success) {
    console.log(`✅ Order submitted: ${result.orderId}`);
  } else {
    console.log(`❌ Error: ${result.error}`);
  }
}