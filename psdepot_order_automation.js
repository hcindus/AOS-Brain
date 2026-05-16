/********************************************************************************
 * PERFORMANCE SUPPLY DEPOT LLC - ORDER AUTOMATION SYSTEM
 * Unified Google Apps Script for Park Cafe Group Orders
 * 
 * Features:
 * - Form submission trigger
 * - Automatic PO number generation (YYMMDD-XXX format)
 * - Line item calculation with tax
 * - Internal notification email
 * - Domtar purchase order email (paper products)
 * - Customer invoice email with PDF attachment
 * - ACM ribbon orders via API
 * 
 * Setup: Install as "On Form Submit" trigger on the response sheet
 * Version: 2.0 Unified
 * Date: 2026-05-16
 ********************************************************************************/

// ================================================================================
// CONFIGURATION SECTION
// ================================================================================

const CONFIG = {
  // Business Information
  BUSINESS: {
    name: "Performance Supply Depot LLC",
    addressLine1: "1880 Oak Point Court",
    addressLine2: "Fairfield, CA 94534",
    phone: "888-881-6834",
    email: "info@psdepot.com"
  },
  
  // Email Recipients
  EMAILS: {
    internal: "info@psdepot.com",
    domtarTo: "customersupport.pos@domtar.com",
    domtarCc: "arlene.belarde@domtar.com"
  },
  
  // Tax Configuration
  TAX: {
    rate: 0.0875,  // 8.75% for all locations
    applyToAll: true
  },
  
  // Locations
  LOCATIONS: [
    "Dolores Park Cafe",
    "Duboce Park Cafe", 
    "Precita Park Cafe",
    "Paradise Park Cafe",
    "Dolores Park Cafe - SFO"
  ],
  
  // Sheet Configuration
  SHEET: {
    name: "Form Responses 1",
    headerRow: 1
  },
  
  // PDF/Invoice Settings
  INVOICE: {
    title: "Please find a courtesy invoice for your order. Thank you!",
    folderId: null  // Set to Drive folder ID if saving PDFs to Drive
  },
  
  // ACM API Configuration
  ACM: {
    endpoint: "https://api.acm.com/orders",  // Update with actual ACM endpoint
    apiKey: null  // Store in Script Properties for security
  }
};

// ================================================================================
// PRODUCT CATALOG
// ================================================================================

const PRODUCTS = {
  PF230: {
    code: "PF230",
    name: "Thermal Paper",
    descCustomer: "PF-230 Thermal 3⅛" × 230' (50 rolls)",
    descVendor: "9078-2489 3 1/8 X 230 48G NP 50RL/CTN",
    cost: 60.94,
    sell: 124.10,
    vendor: "DOMTAR",
    uom: "case"
  },
  "13305": {
    code: "13305",
    name: "Bond Paper",
    descCustomer: "13-305 Bond 3" × 165' (50 rolls)",
    descVendor: "9074-0243 3 x 165' BOND 50 RL/CTN",
    cost: 35.66,
    sell: 59.00,
    vendor: "DOMTAR",
    uom: "case"
  },
  CC235: {
    code: "CC235",
    name: "Multi-Ply Paper",
    descCustomer: "CC-235 Multi-Ply 3" × 90' (50 rolls)",
    descVendor: "9077-0047 3 X 90 MULTI PLY W/C 50 RLS/CTN",
    cost: 43.51,
    sell: 76.00,
    vendor: "DOMTAR",
    uom: "case"
  },
  "62245": {
    code: "62245",
    name: "Epson Ribbon",
    descCustomer: "62245 Epson Ribbon (per dozen)",
    descVendor: "38619ERC30BR EPSON COMPATIBLE RIBBON (ERC-30/34/38)",
    cost: 8.84,
    sell: 42.00,
    vendor: "ACM",
    uom: "dozen",
    acmSku: "38619ERC30BR"
  },
  "67240": {
    code: "67240",
    name: "Star Ribbon",
    descCustomer: "67240 Star Ribbon (per dozen)",
    descVendor: "51619RC700BR STAR SP700 COMPATIBLE RIBBON",
    cost: 16.64,
    sell: 52.00,
    vendor: "ACM",
    uom: "dozen",
    acmSku: "51619RC700BR"
  }
};

// ================================================================================
// MAIN ENTRY POINT
// ================================================================================

/**
 * Trigger function - runs on form submit
 * Install this as an "On form submit" trigger on the response sheet
 * 
 * @param {Object} e - The form submit event object
 */
function onFormSubmit(e) {
  try {
    Logger.log("=== ORDER PROCESSING STARTED ===");
    
    // Get sheet and row data
    const sheet = e.range.getSheet();
    const row = e.range.getRow();
    const headers = getHeaders_(sheet);
    
    Logger.log("Processing row: " + row + " from sheet: " + sheet.getName());
    
    // Extract form data into structured object
    const orderData = extractFormData_(e.values, headers);
    
    // Generate PO number
    const poNumber = generatePONumber();
    orderData.poNumber = poNumber;
    
    // Build line items from quantities
    orderData.lineItems = buildLineItems(orderData.quantities);
    
    // Calculate totals
    orderData.totals = calculateTotals(orderData.lineItems);
    
    // Write PO number back to sheet (column Q typically)
    writePOToSheet_(sheet, row, poNumber);
    
    // Send emails
    sendInternalEmail(orderData);
    
    // Send Domtar email if paper products ordered
    if (hasDomtarItems(orderData.lineItems)) {
      sendDomtarEmail(orderData);
    }
    
    // Place ACM order if ribbon products ordered
    if (hasAcmItems(orderData.lineItems)) {
      placeRibbonOrderWithACM(orderData);
    }
    
    // Generate PDF and send to customer
    const pdfBlob = buildInvoicePdf(orderData);
    sendCustomerEmail(orderData, pdfBlob);
    
    // Mark as processed
    sheet.getRange(row, headers["Status"] || getLastColumn_(sheet)).setValue("Processed");
    
    Logger.log("=== ORDER PROCESSING COMPLETED ===");
    Logger.log("PO Number: " + poNumber);
    
  } catch (err) {
    Logger.log("ERROR in onFormSubmit: " + err);
    Logger.log(err.stack);
    
    // Send error notification
    MailApp.sendEmail({
      to: CONFIG.EMAILS.internal,
      subject: "Order Processing Error - Immediate Attention Required",
      body: "An error occurred processing an order.\n\nError: " + err + "\n\nStack: " + (err.stack || "No stack trace")
    });
  }
}

// ================================================================================
// DATA EXTRACTION & LINE ITEM BUILDING
// ================================================================================

/**
 * Extract form data from submission values
 * 
 * @param {Array} values - Row values from form submission
 * @param {Object} headers - Column header mapping
 * @returns {Object} Structured order data
 */
function extractFormData_(values, headers) {
  // Standard Google Form column mapping (adjust if your form differs)
  // A: Timestamp, B: Location, C: Manager Name, D: Manager Email, 
  // E: PF230 Qty, F: 13305 Qty, G: CC235 Qty, H: 62245 Qty, I: 67240 Qty, J: Notes
  
  return {
    timestamp: values[0],
    location: values[1] || "",
    managerName: values[2] || "",
    managerEmail: values[3] || "",
    quantities: {
      PF230: Number(values[4] || 0),
      "13305": Number(values[5] || 0),
      CC235: Number(values[6] || 0),
      "62245": Number(values[7] || 0),
      "67240": Number(values[8] || 0)
    },
    notes: values[9] || "",
    poNumber: null,
    lineItems: [],
    totals: {}
  };
}

/**
 * Build line items array from quantities
 * 
 * @param {Object} quantities - Product quantities
 * @returns {Array} Line items with calculated values
 */
function buildLineItems(quantities) {
  const items = [];
  
  for (const [sku, qty] of Object.entries(quantities)) {
    if (qty > 0 && PRODUCTS[sku]) {
      const product = PRODUCTS[sku];
      items.push({
        sku: product.code,
        name: product.name,
        descCustomer: product.descCustomer,
        descVendor: product.descVendor,
        quantity: qty,
        cost: product.cost,
        sell: product.sell,
        vendor: product.vendor,
        uom: product.uom,
        acmSku: product.acmSku || null,
        lineCost: product.cost * qty,
        lineSell: product.sell * qty,
        lineProfit: (product.sell - product.cost) * qty
      });
    }
  }
  
  return items;
}

// ================================================================================
// CALCULATIONS
// ================================================================================

/**
 * Calculate order totals
 * 
 * @param {Array} lineItems - Array of line items
 * @returns {Object} Totals object
 */
function calculateTotals(lineItems) {
  const subtotal = lineItems.reduce((sum, item) => sum + item.lineSell, 0);
  const costTotal = lineItems.reduce((sum, item) => sum + item.lineCost, 0);
  const tax = subtotal * CONFIG.TAX.rate;
  const total = subtotal + tax;
  const profit = subtotal - costTotal;
  const margin = subtotal > 0 ? (profit / subtotal) * 100 : 0;
  
  return {
    subtotal: round(subtotal),
    tax: round(tax),
    taxRate: CONFIG.TAX.rate,
    total: round(total),
    costTotal: round(costTotal),
    profit: round(profit),
    margin: round(margin, 2)
  };
}

/**
 * Round number to 2 decimal places
 * 
 * @param {Number} num - Number to round
 * @param {Number} decimals - Decimal places (default 2)
 * @returns {Number} Rounded number
 */
function round(num, decimals = 2) {
  const factor = Math.pow(10, decimals);
  return Math.round((num + Number.EPSILON) * factor) / factor;
}

/**
 * Format currency for display
 * 
 * @param {Number} amount - Amount to format
 * @returns {String} Formatted currency string
 */
function formatCurrency(amount) {
  return "$" + amount.toFixed(2);
}

// ================================================================================
// PO NUMBER GENERATION
// ================================================================================

/**
 * Generate PO number in YYMMDD-XXX format
 * Sequentially increments based on today's orders
 * 
 * @returns {String} PO number
 */
function generatePONumber() {
  const now = new Date();
  const yy = String(now.getFullYear()).slice(-2);
  const mm = String(now.getMonth() + 1).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');
  const datePrefix = yy + mm + dd;
  
  // Get sequence number for today
  const seq = getNextSequence_(datePrefix);
  
  return datePrefix + "-" + String(seq).padStart(3, '0');
}

/**
 * Get next sequence number for PO generation
 * Uses Script Properties for persistence
 * 
 * @param {String} datePrefix - YYMMDD prefix
 * @returns {Number} Next sequence number
 */
function getNextSequence_(datePrefix) {
  const props = PropertiesService.getScriptProperties();
  const lastPrefix = props.getProperty('LAST_PO_PREFIX') || '';
  let seq = 1;
  
  if (lastPrefix === datePrefix) {
    const lastSeq = parseInt(props.getProperty('LAST_PO_SEQUENCE') || '0', 10);
    seq = lastSeq + 1;
  }
  
  props.setProperty('LAST_PO_PREFIX', datePrefix);
  props.setProperty('LAST_PO_SEQUENCE', String(seq));
  
  return seq;
}

// ================================================================================
// EMAIL FUNCTIONS
// ================================================================================

/**
 * Send internal notification email
 * 
 * @param {Object} orderData - Order data object
 */
function sendInternalEmail(orderData) {
  const subject = `Customer Order - ${orderData.location} - PO ${orderData.poNumber}`;
  
  let body = `New Order Received\n`;
  body += `================\n\n`;
  body += `PO Number: ${orderData.poNumber}\n`;
  body += `Location: ${orderData.location}\n`;
  body += `Manager: ${orderData.managerName}\n`;
  body += `Email: ${orderData.managerEmail}\n`;
  body += `Date: ${new Date(orderData.timestamp).toLocaleString()}\n\n`;
  
  body += `Order Items:\n`;
  body += `-----------\n`;
  orderData.lineItems.forEach(item => {
    body += `${item.descCustomer} x ${item.quantity} = ${formatCurrency(item.lineSell)}\n`;
  });
  
  body += `\nTotals:\n`;
  body += `-------\n`;
  body += `Subtotal: ${formatCurrency(orderData.totals.subtotal)}\n`;
  body += `Tax (${(orderData.totals.taxRate * 100).toFixed(2)}%): ${formatCurrency(orderData.totals.tax)}\n`;
  body += `Total: ${formatCurrency(orderData.totals.total)}\n`;
  body += `Profit: ${formatCurrency(orderData.totals.profit)}\n`;
  body += `Margin: ${orderData.totals.margin.toFixed(2)}%\n\n`;
  
  if (orderData.notes) {
    body += `Notes: ${orderData.notes}\n\n`;
  }
  
  body += `---\n`;
  body += `Performance Supply Depot LLC\n`;
  body += `888-881-6834 | info@psdepot.com`;
  
  MailApp.sendEmail({
    to: CONFIG.EMAILS.internal,
    cc: orderData.managerEmail,
    subject: subject,
    body: body
  });
  
  Logger.log("Internal email sent to: " + CONFIG.EMAILS.internal);
}

/**
 * Send purchase order email to Domtar
 * Only for DOMTAR vendor items
 * 
 * @param {Object} orderData - Order data object
 */
function sendDomtarEmail(orderData) {
  const domtarItems = orderData.lineItems.filter(item => item.vendor === "DOMTAR");
  
  if (domtarItems.length === 0) return;
  
  const subject = `Blind Drop PO ${orderData.poNumber} - ${orderData.location}`;
  
  let body = `Please process the following blind drop order:\n\n`;
  body += `PO Number: ${orderData.poNumber}\n`;
  body += `Ship To: ${orderData.location}\n`;
  body += `Attention: ${orderData.managerName}\n\n`;
  
  body += `Items:\n`;
  body += `------\n`;
  domtarItems.forEach(item => {
    body += `${item.descVendor}\n`;
    body += `Qty: ${item.quantity} ${item.uom}\n\n`;
  });
  
  body += `\nSpecial Instructions: ${orderData.notes || "None"}\n\n`;
  body += `Thank you,\n`;
  body += `Performance Supply Depot LLC`;
  
  MailApp.sendEmail({
    to: CONFIG.EMAILS.domtarTo,
    cc: CONFIG.EMAILS.domtarCc,
    subject: subject,
    body: body
  });
  
  Logger.log("Domtar PO email sent");
}

/**
 * Send customer invoice email with PDF attachment
 * 
 * @param {Object} orderData - Order data object
 * @param {Blob} pdfBlob - PDF invoice blob
 */
function sendCustomerEmail(orderData, pdfBlob) {
  const subject = `Courtesy Invoice for Your Order - PO ${orderData.poNumber}`;
  
  let body = `Dear ${orderData.managerName},\n\n`;
  body += `Thank you for your order from Performance Supply Depot LLC.\n\n`;
  body += `Your order has been received and is being processed.\n`;
  body += `Please find your courtesy invoice attached.\n\n`;
  body += `PO Number: ${orderData.poNumber}\n`;
  body += `Location: ${orderData.location}\n`;
  body += `Total Amount: ${formatCurrency(orderData.totals.total)}\n\n`;
  body += `If you have any questions, please contact us at:\n`;
  body += `Phone: ${CONFIG.BUSINESS.phone}\n`;
  body += `Email: ${CONFIG.BUSINESS.email}\n\n`;
  body += `Best regards,\n`;
  body += `Performance Supply Depot LLC Team`;
  
  MailApp.sendEmail({
    to: orderData.managerEmail,
    cc: CONFIG.EMAILS.internal,
    subject: subject,
    body: body,
    attachments: [pdfBlob]
  });
  
  Logger.log("Customer invoice email sent to: " + orderData.managerEmail);
}

// ================================================================================
// ACM RIBBON ORDERS
// ================================================================================

/**
 * Place order with ACM for ribbon products
 * 
 * @param {Object} orderData - Order data object
 * @returns {String|null} Tracking number or null
 */
function placeRibbonOrderWithACM(orderData) {
  const acmItems = orderData.lineItems.filter(item => item.vendor === "ACM");
  
  if (acmItems.length === 0) return null;
  
  Logger.log("Placing ACM order for PO: " + orderData.poNumber);
  
  // Prepare order payload
  const orderPayload = {
    poNumber: orderData.poNumber,
    shipTo: {
      name: orderData.location,
      attention: orderData.managerName,
      address: orderData.location  // You may need to expand this with actual address
    },
    items: acmItems.map(item => ({
      sku: item.acmSku,
      quantity: item.quantity,
      description: item.descVendor
    })),
    notes: orderData.notes || ""
  };
  
  // TODO: Implement actual ACM API call
  // This is a placeholder - replace with actual API endpoint and authentication
  try {
    const apiKey = getAcmApiKey_();
    
    if (!apiKey || CONFIG.ACM.endpoint.includes("api.acm.com")) {
      // Demo mode - log the order instead
      Logger.log("ACM Order Payload (Demo Mode):");
      Logger.log(JSON.stringify(orderPayload, null, 2));
      return "DEMO-" + orderData.poNumber;
    }
    
    const response = UrlFetchApp.fetch(CONFIG.ACM.endpoint, {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json"
      },
      payload: JSON.stringify(orderPayload)
    });
    
    const result = JSON.parse(response.getContentText());
    Logger.log("ACM Order Response: " + JSON.stringify(result));
    
    return result.trackingNumber || result.orderId || null;
    
  } catch (err) {
    Logger.log("ACM Order Error: " + err);
    return null;
  }
}

/**
 * Get ACM API key from Script Properties
 * 
 * @returns {String|null} API key
 */
function getAcmApiKey_() {
  const props = PropertiesService.getScriptProperties();
  return props.getProperty("ACM_API_KEY");
}

// ================================================================================
// PDF INVOICE GENERATION
// ================================================================================

/**
 * Build PDF invoice
 * 
 * @param {Object} orderData - Order data object
 * @returns {Blob} PDF blob
 */
function buildInvoicePdf(orderData) {
  // Create HTML content for PDF
  const html = generateInvoiceHtml_(orderData);
  
  // Convert to PDF
  const blob = Utilities.newBlob(html, MimeType.HTML);
  const pdf = blob.getAs(MimeType.PDF);
  pdf.setName(`Invoice_${orderData.poNumber}.pdf`);
  
  return pdf;
}

/**
 * Generate HTML for invoice PDF
 * 
 * @param {Object} orderData - Order data object
 * @returns {String} HTML string
 */
function generateInvoiceHtml_(orderData) {
  const dateStr = new Date(orderData.timestamp).toLocaleDateString();
  
  let itemsHtml = '';
  orderData.lineItems.forEach(item => {
    itemsHtml += `
      <tr>
        <td>${item.descCustomer}</td>
        <td style="text-align:center">${item.quantity}</td>
        <td style="text-align:right">${formatCurrency(item.sell)}</td>
        <td style="text-align:right">${formatCurrency(item.lineSell)}</td>
      </tr>
    `;
  });
  
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
        .company { font-size: 24px; font-weight: bold; }
        .address { font-size: 12px; color: #666; }
        .invoice-title { font-size: 20px; margin: 20px 0; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background-color: #f5f5f5; font-weight: bold; }
        .totals { margin-top: 20px; text-align: right; }
        .total-row { font-weight: bold; }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }
      </style>
    </head>
    <body>
      <div class="header">
        <div class="company">${CONFIG.BUSINESS.name}</div>
        <div class="address">
          ${CONFIG.BUSINESS.addressLine1}<br>
          ${CONFIG.BUSINESS.addressLine2}<br>
          Phone: ${CONFIG.BUSINESS.phone} | Email: ${CONFIG.BUSINESS.email}
        </div>
      </div>
      
      <div class="invoice-title">COURTESY INVOICE</div>
      
      <table>
        <tr>
          <td><strong>Bill To:</strong><br>${orderData.location}<br>Attn: ${orderData.managerName}</td>
          <td style="text-align:right">
            <strong>Invoice #:</strong> ${orderData.poNumber}<br>
            <strong>Date:</strong> ${dateStr}<br>
            <strong>PO Number:</strong> ${orderData.poNumber}
          </td>
        </tr>
      </table>
      
      <table>
        <thead>
          <tr>
            <th>Description</th>
            <th style="text-align:center">Qty</th>
            <th style="text-align:right">Unit Price</th>
            <th style="text-align:right">Amount</th>
          </tr>
        </thead>
        <tbody>
          ${itemsHtml}
        </tbody>
      </table>
      
      <div class="totals">
        <table style="width: 300px; margin-left: auto;">
          <tr>
            <td>Subtotal:</td>
            <td style="text-align:right">${formatCurrency(orderData.totals.subtotal)}</td>
          </tr>
          <tr>
            <td>Tax (${(orderData.totals.taxRate * 100).toFixed(2)}%):</td>
            <td style="text-align:right">${formatCurrency(orderData.totals.tax)}</td>
          </tr>
          <tr class="total-row">
            <td>Total:</td>
            <td style="text-align:right">${formatCurrency(orderData.totals.total)}</td>
          </tr>
        </table>
      </div>
      
      <div class="footer">
        <p>${CONFIG.INVOICE.title}</p>
        <p>Thank you for your business!</p>
      </div>
    </body>
    </html>
  `;
}

// ================================================================================
// HELPER FUNCTIONS
// ================================================================================

/**
 * Check if order has Domtar items
 * 
 * @param {Array} lineItems - Line items array
 * @returns {Boolean} True if Domtar items exist
 */
function hasDomtarItems(lineItems) {
  return lineItems.some(item => item.vendor === "DOMTAR");
}

/**
 * Check if order has ACM items
 * 
 * @param {Array} lineItems - Line items array
 * @returns {Boolean} True if ACM items exist
 */
function hasAcmItems(lineItems) {
  return lineItems.some(item => item.vendor === "ACM");
}

/**
 * Get headers from sheet
 * 
 * @param {Sheet} sheet - Google Sheet
 * @returns {Object} Header name to column index mapping
 */
function getHeaders_(sheet) {
  const lastCol = sheet.getLastColumn();
  const headerRow = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
  const headers = {};
  
  headerRow.forEach((header, index) => {
    if (header && typeof header === 'string') {
      headers[header.trim()] = index + 1;
    }
  });
  
  return headers;
}

/**
 * Write PO number to sheet
 * 
 * @param {Sheet} sheet - Google Sheet
 * @param {Number} row - Row number
 * @param {String} poNumber - PO number
 */
function writePOToSheet_(sheet, row, poNumber) {
  try {
    // Try to write to column Q (17) first, or find "PO Number" header
    const headers = getHeaders_(sheet);
    let col = headers["PO Number"] || 17;
    
    sheet.getRange(row, col).setValue(poNumber);
    Logger.log("PO Number written to column " + col);
  } catch (err) {
    Logger.log("Could not write PO to sheet: " + err);
  }
}

/**
 * Get last column number
 * 
 * @param {Sheet} sheet - Google Sheet
 * @returns {Number} Last column number
 */
function getLastColumn_(sheet) {
  return sheet.getLastColumn();
}

// ================================================================================
// UTILITY FUNCTIONS
// ================================================================================

/**
 * Set ACM API key (run once to store securely)
 */
function setAcmApiKey() {
  // Run this function and enter your ACM API key when prompted
  const ui = SpreadsheetApp.getUi();
  const response = ui.prompt('Enter ACM API Key:');
  
  if (response.getSelectedButton() == ui.Button.OK) {
    const apiKey = response.getResponseText();
    PropertiesService.getScriptProperties().setProperty('ACM_API_KEY', apiKey);
    ui.alert('API Key stored successfully');
  }
}

/**
 * Test the script with sample data
 * Run this from the Apps Script editor to verify setup
 */
function testOrderProcessing() {
  const mockEvent = {
    values: [
      new Date(),                    // A: Timestamp
      "Dolores Park Cafe",           // B: Location
      "John Doe",                    // C: Manager Name
      "john@example.com",            // D: Manager Email
      2,                             // E: PF230 Qty
      1,                             // F: 13305 Qty
      0,                             // G: CC235 Qty
      3,                             // H: 62245 Qty (Epson Ribbon)
      2,                             // I: 67240 Qty (Star Ribbon)
      "Test order - please ignore"   // J: Notes
    ],
    range: {
      getSheet: function() {
        return SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
      },
      getRow: function() {
        return 2;  // Test row
      }
    }
  };
  
  onFormSubmit(mockEvent);
}

// ================================================================================
// END OF SCRIPT
// ================================================================================
