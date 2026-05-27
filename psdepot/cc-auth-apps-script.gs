/**
 * Credit Card Authorization Form - Google Apps Script
 * 
 * This script:
 * 1. Triggers on Google Form submission
 * 2. Creates a PDF from the form response
 * 3. Emails the PDF to customer and merchant
 * 4. Saves a copy to Google Drive
 * 
 * Setup Instructions:
 * 1. Open your Google Form → Responses tab → Click the Sheets icon → Create a new spreadsheet
 * 2. In the spreadsheet, go to Extensions → Apps Script
 * 3. Delete the default code and paste this entire file
 * 4. Save (Ctrl+S or ⌘+S)
 * 5. Click the Triggers icon (⏰) on the left
 * 6. Add Trigger: Choose function 'onFormSubmit', choose event source 'From form', choose event type 'On form submit'
 * 7. Authorize permissions when prompted
 */

// CONFIGURATION - Update these values
const CONFIG = {
  // Your merchant email - where YOU receive the PDF
  MERCHANT_EMAIL: 'info@psdepot.com',  // ← CHANGE THIS
  
  // Email subject lines
  EMAIL_SUBJECT_CUSTOMER: 'Your Credit Card Authorization - Performance Supply Depot',
  EMAIL_SUBJECT_MERCHANT: 'NEW: CC Authorization Received - {businessName}',
  
  // Google Drive folder ID where PDFs will be saved (optional)
  // To get folder ID: Open Drive folder, look at URL: .../folders/FOLDER_ID_HERE
  ARCHIVE_FOLDER_ID: '',  // ← Paste folder ID here or leave empty
  
  // CC or BCC additional recipients (optional)
  CC_EMAIL: '',
  BCC_EMAIL: ''
};

/**
 * Main trigger function - runs when form is submitted
 */
function onFormSubmit(e) {
  try {
    // Log the incoming data for debugging
    console.log('Form submitted:', JSON.stringify(e.values));
    
    // Parse form response
    const response = parseFormResponse(e);
    
    // Generate PDF
    const pdfBlob = createAuthorizationPDF(response);
    
    // Send emails
    sendCustomerEmail(response, pdfBlob);
    sendMerchantEmail(response, pdfBlob);
    
    // Save to Drive if configured
    if (CONFIG.ARCHIVE_FOLDER_ID) {
      saveToDrive(response, pdfBlob);
    }
    
    console.log('✅ CC Authorization processed successfully for: ' + response.businessName);
    
  } catch (error) {
    console.error('❌ Error processing form submission:', error);
    // Send error notification to merchant
    sendErrorNotification(error, e);
  }
}

/**
 * Parse Google Form response into structured object
 * Adjust column indices based on your form field order
 */
function parseFormResponse(e) {
  const values = e.values;
  const headers = e.namedValues ? Object.keys(e.namedValues) : [];
  
  // Get timestamp from event or use current time
  const timestamp = e.range ? e.range.getRow() : new Date().toISOString();
  
  // Generate a unique form ID
  const formId = 'PSD-' + Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyyMMdd-HHmmss');
  
  return {
    // Metadata
    timestamp: Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'MMMM dd, yyyy at h:mm a z'),
    submittedAt: new Date().toISOString(),
    formId: formId,
    
    // Section 1: Business Information (adjust indices based on your form)
    businessName: values[1] || '',
    businessAddress: values[2] || '',
    businessCityStateZip: values[3] || '',
    businessPhone: values[4] || '',
    businessEmail: values[5] || '',
    
    // Section 2: Cardholder Information
    cardholderName: values[6] || '',
    billingAddress: values[7] || '',
    billingZip: values[8] || '',
    cardholderPhone: values[9] || '',
    cardholderEmail: values[10] || '',
    
    // Section 3: Credit Card Information
    cardNumber: maskCardNumber(values[11] || ''),
    rawCardNumber: values[11] || '',
    expirationDate: values[12] || '',
    cvv: values[13] || '',
    cardBillingZip: values[14] || '',
    
    // Section 4: Authorization
    authorizationAgreed: values[15] || '',
    signature: values[16] || '',
    date: values[17] || '',
    
    // Section 5: Optional
    notes: values[18] || ''
  };
}

/**
 * Mask card number for security (show only last 4)
 */
function maskCardNumber(cardNumber) {
  if (!cardNumber) return '';
  const clean = cardNumber.toString().replace(/\s/g, '');
  if (clean.length < 4) return clean;
  return '****-****-****-' + clean.slice(-4);
}

/**
 * Create PDF from HTML template
 */
function createAuthorizationPDF(data) {
  // Build HTML content
  const htmlContent = buildHTMLTemplate(data);
  
  // Convert to PDF
  const blob = Utilities.newBlob(htmlContent, 'text/html', 'authorization.html');
  const pdf = blob.getAs('application/pdf');
  
  // Set filename
  const filename = `CC-Authorization-${data.businessName.replace(/[^a-zA-Z0-9]/g, '_')}-${data.formId}.pdf`;
  pdf.setName(filename);
  
  return pdf;
}

/**
 * Build HTML template for PDF
 */
function buildHTMLTemplate(data) {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Credit Card Authorization - ${data.businessName}</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: 'Helvetica Neue', Arial, sans-serif;
      font-size: 11pt;
      line-height: 1.5;
      color: #333;
      max-width: 8.5in;
      margin: 0 auto;
      padding: 0.5in;
    }
    .header {
      text-align: center;
      border-bottom: 3px solid #1a5490;
      padding-bottom: 15px;
      margin-bottom: 25px;
    }
    .header h1 {
      color: #1a5490;
      font-size: 20pt;
      margin: 0 0 5px 0;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .header p {
      color: #666;
      margin: 0;
      font-size: 10pt;
    }
    .section {
      margin-bottom: 20px;
    }
    .section-title {
      background: #1a5490;
      color: white;
      padding: 8px 12px;
      font-weight: bold;
      font-size: 11pt;
      margin-bottom: 10px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .field-row {
      display: flex;
      margin-bottom: 8px;
      border-bottom: 1px solid #ddd;
      padding-bottom: 4px;
    }
    .field-label {
      width: 35%;
      font-weight: bold;
      color: #555;
      font-size: 9pt;
      text-transform: uppercase;
    }
    .field-value {
      width: 65%;
      font-family: 'Courier New', monospace;
      font-size: 11pt;
      color: #000;
    }
    .cc-number {
      font-family: 'Courier New', monospace;
      font-size: 13pt;
      letter-spacing: 2px;
      background: #f5f5f5;
      padding: 8px 12px;
      border-radius: 4px;
      display: inline-block;
    }
    .auth-box {
      border: 2px solid #1a5490;
      padding: 15px;
      background: #f8f9fa;
      margin: 15px 0;
    }
    .auth-box ol {
      margin: 0;
      padding-left: 20px;
    }
    .auth-box li {
      margin-bottom: 10px;
      font-size: 10pt;
      line-height: 1.6;
    }
    .signature-block {
      margin-top: 30px;
      border-top: 2px solid #333;
      padding-top: 20px;
    }
    .signature-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 20px;
    }
    .signature-line {
      width: 45%;
    }
    .signature-line .line {
      border-bottom: 1px solid #333;
      height: 30px;
      margin-bottom: 5px;
    }
    .signature-line .label {
      font-size: 9pt;
      color: #666;
      text-transform: uppercase;
    }
    .footer {
      margin-top: 30px;
      padding-top: 15px;
      border-top: 1px solid #ccc;
      font-size: 8pt;
      color: #666;
      text-align: center;
    }
    .timestamp {
      text-align: right;
      font-size: 9pt;
      color: #666;
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <div class="timestamp">
    Form ID: ${data.formId} | Submitted: ${data.timestamp}
  </div>

  <div class="header">
    <h1>Credit Card Authorization Form</h1>
    <p>Performance Supply Depot LLC</p>
  </div>

  <div class="section">
    <div class="section-title">Section 1 — Business Information</div>
    <div class="field-row">
      <div class="field-label">Business Name</div>
      <div class="field-value">${data.businessName}</div>
    </div>
    <div class="field-row">
      <div class="field-label">Business Address</div>
      <div class="field-value">${data.businessAddress}</div>
    </div>
    <div class="field-row">
      <div class="field-label">City, State, ZIP</div>
      <div class="field-value">${data.businessCityStateZip}</div>
    </div>
    <div class="field-row">
      <div class="field-label">Phone Number</div>
      <div class="field-value">${data.businessPhone}</div>
    </div>
    <div class="field-row">
      <div class="field-label">Email Address</div>
      <div class="field-value">${data.businessEmail}</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Section 2 — Authorized Cardholder</div>
    <div class="field-row">
      <div class="field-label">Cardholder Name</div>
      <div class="field-value">${data.cardholderName}</div>
    </div>
    <div class="field-row">
      <div class="field-label">Billing Address</div>
      <div class="field-value">${data.billingAddress}</div>
    </div>
    <div class="field-row">
      <div class="field-label">Billing ZIP</div>
      <div class="field-value">${data.billingZip}</div>
    </div>
    <div class="field-row">
      <div class="field-label">Phone</div>
      <div class="field-value">${data.cardholderPhone}</div>
    </div>
    <div class="field-row">
      <div class="field-label">Email</div>
      <div class="field-value">${data.cardholderEmail}</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Section 3 — Credit Card Details</div>
    <div class="field-row" style="border-bottom: none;">
      <div class="field-label">Card Number</div>
      <div class="field-value">
        <span class="cc-number">${data.cardNumber}</span>
      </div>
    </div>
    <div class="field-row">
      <div class="field-label" style="width: 25%;">Expiration</div>
      <div class="field-value" style="width: 25%;">${data.expirationDate}</div>
      <div class="field-label" style="width: 25%; text-align: center;">CVV</div>
      <div class="field-value" style="width: 25%;">${data.cvv}</div>
    </div>
    <div class="field-row">
      <div class="field-label">Billing ZIP (Card)</div>
      <div class="field-value">${data.cardBillingZip}</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Section 4 — Authorization Agreement</div>
    <div class="auth-box">
      <ol>
        <li><strong>Charge Authorization:</strong> I hereby authorize Performance Supply Depot LLC to charge the credit card listed above for purchases, invoices, or recurring orders made by my business. I confirm that I am an authorized user of this credit card and that I will not dispute charges provided they correspond to the terms indicated on invoices or order confirmations.</li>
        <li><strong>Information Storage:</strong> I authorize Performance Supply Depot LLC to store this credit card information securely on file for future transactions, recurring orders, or replacement orders requested by my business. This authorization will remain in effect until I provide written notice to revoke it.</li>
        <li><strong>Record Keeping:</strong> I understand that a PDF copy of this authorization, including the information I have provided, will be generated and emailed to both myself and Performance Supply Depot LLC for record-keeping purposes.</li>
      </ol>
    </div>
  </div>

  <div class="signature-block">
    <div class="signature-row">
      <div class="signature-line">
        <div class="line">${data.signature}</div>
        <div class="label">Electronic Signature</div>
      </div>
      <div class="signature-line">
        <div class="line">${data.date}</div>
        <div class="label">Date</div>
      </div>
    </div>
  </div>

  ${data.notes ? `
  <div class="section" style="margin-top: 20px; border-top: 1px dashed #ccc; padding-top: 15px;">
    <div class="field-label">Special Instructions</div>
    <div class="field-value" style="font-family: inherit;">${data.notes}</div>
  </div>
  ` : ''}

  <div class="footer">
    <p><strong>Performance Supply Depot LLC</strong></p>
    <p>This document constitutes a binding authorization per the Electronic Signatures in Global and National Commerce Act (E-SIGN, 15 U.S.C. § 7001).</p>
    <p style="margin-top: 10px; font-size: 7pt; color: #999;">
      Form ID: ${data.formId} | Submitted: ${data.timestamp}
    </p>
  </div>
</body>
</html>
  `;
}

/**
 * Send email to customer with PDF attachment
 */
function sendCustomerEmail(data, pdfBlob) {
  const subject = CONFIG.EMAIL_SUBJECT_CUSTOMER;
  
  const body = `
    <p>Hello ${data.cardholderName},</p>
    
    <p>Thank you for submitting your Credit Card Authorization for <strong>${data.businessName}</strong>.</p>
    
    <p>A PDF copy of your authorization is attached to this email for your records. Please retain this document for your files.</p>
    
    <p><strong>Summary:</strong></p>
    <ul>
      <li>Business: ${data.businessName}</li>
      <li>Card on file: ${data.cardNumber}</li>
      <li>Submitted: ${data.timestamp}</li>
      <li>Form ID: ${data.formId}</li>
    </ul>
    
    <p>This authorization will remain in effect until you provide written notice to revoke it. If you have any questions or need to make changes, please contact us at ${CONFIG.MERCHANT_EMAIL}.</p>
    
    <p>Best regards,<br>
    Performance Supply Depot LLC</p>
    
    <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
    <p style="font-size: 11px; color: #999;">
      This is an automated email sent from a secure form submission system. 
      Form ID: ${data.formId}
    </p>
  `;
  
  const options = {
    htmlBody: body,
    attachments: [pdfBlob],
    name: 'Performance Supply Depot'
  };
  
  if (CONFIG.CC_EMAIL) options.cc = CONFIG.CC_EMAIL;
  if (CONFIG.BCC_EMAIL) options.bcc = CONFIG.BCC_EMAIL;
  
  GmailApp.sendEmail(data.cardholderEmail, subject, '', options);
}

/**
 * Send notification email to merchant
 */
function sendMerchantEmail(data, pdfBlob) {
  const subject = CONFIG.EMAIL_SUBJECT_MERCHANT.replace('{businessName}', data.businessName);
  
  const body = `
    <p><strong>NEW CREDIT CARD AUTHORIZATION RECEIVED</strong></p>
    
    <p>A new CC authorization form has been submitted and requires your attention.</p>
    
    <p><strong>Business Information:</strong></p>
    <ul>
      <li><strong>Business:</strong> ${data.businessName}</li>
      <li><strong>Business Email:</strong> ${data.businessEmail}</li>
      <li><strong>Business Phone:</strong> ${data.businessPhone}</li>
      <li><strong>Address:</strong> ${data.businessAddress}, ${data.businessCityStateZip}</li>
    </ul>
    
    <p><strong>Cardholder Information:</strong></p>
    <ul>
      <li><strong>Name:</strong> ${data.cardholderName}</li>
      <li><strong>Email:</strong> ${data.cardholderEmail}</li>
      <li><strong>Phone:</strong> ${data.cardholderPhone}</li>
      <li><strong>Card:</strong> ${data.cardNumber} (Exp: ${data.expirationDate})</li>
    </ul>
    
    <p><strong>Submission Details:</strong></p>
    <ul>
      <li><strong>Submitted:</strong> ${data.timestamp}</li>
      <li><strong>Form ID:</strong> ${data.formId}</li>
      <li><strong>Signed by:</strong> ${data.signature}</li>
    </ul>
    
    ${data.notes ? `<p><strong>Special Instructions:</strong><br>${data.notes}</p>` : ''}
    
    <p>The complete authorization PDF is attached.</p>
    
    <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
    <p style="font-size: 11px; color: #999;">
      Form ID: ${data.formId} | Timestamp: ${data.timestamp}
    </p>
  `;
  
  const options = {
    htmlBody: body,
    attachments: [pdfBlob],
    name: 'CC Authorization System'
  };
  
  GmailApp.sendEmail(CONFIG.MERCHANT_EMAIL, subject, '', options);
}

/**
 * Save PDF to Google Drive folder
 */
function saveToDrive(data, pdfBlob) {
  try {
    const folder = DriveApp.getFolderById(CONFIG.ARCHIVE_FOLDER_ID);
    const file = folder.createFile(pdfBlob);
    file.setDescription(`CC Authorization for ${data.businessName} - ${data.formId}`);
    console.log('📁 Saved to Drive: ' + file.getName());
    return file;
  } catch (error) {
    console.error('⚠️ Could not save to Drive:', error);
    return null;
  }
}

/**
 * Send error notification to merchant
 */
function sendErrorNotification(error, eventData) {
  const subject = '⚠️ CC Form Processing Error';
  const body = `
    <p><strong>An error occurred processing a CC authorization form:</strong></p>
    <pre style="background: #f5f5f5; padding: 10px; overflow-x: auto;">${error.toString()}</pre>
    
    <p><strong>Event Data:</strong></p>
    <pre style="background: #f5f5f5; padding: 10px; overflow-x: auto;">${JSON.stringify(eventData, null, 2)}</pre>
    
    <p>Please check the form submission manually.</p>
  `;
  
  GmailApp.sendEmail(CONFIG.MERCHANT_EMAIL, subject, '', {
    htmlBody: body,
    name: 'CC Authorization System Error'
  });
}

/**
 * Manual test function - run this to verify setup
 * In Apps Script editor: Select function 'testFormProcessing' → Run
 */
function testFormProcessing() {
  // Simulate a form submission
  const mockEvent = {
    values: [
      '2024-01-15 10:30:00',  // Timestamp
      'Test Business LLC',     // Business Name
      '123 Commerce St',       // Business Address
      'Tampa, FL 33601',       // City, State, ZIP
      '(555) 123-4567',        // Business Phone
      'business@test.com',     // Business Email
      'John Doe',              // Cardholder Name
      '456 Billing Ave',       // Billing Address
      '33602',                 // Billing ZIP
      '(555) 987-6543',        // Cardholder Phone
      'john@email.com',        // Cardholder Email
      '4111111111111111',      // Card Number
      '12/25',                 // Expiration
      '123',                   // CVV
      '33602',                 // Card Billing ZIP
      '["Authorized"]',        // Authorization checkboxes
      'John Doe',              // Signature
      '2024-01-15',            // Date
      'Please ship via FedEx'  // Notes
    ]
  };
  
  onFormSubmit(mockEvent);
  console.log('✅ Test completed. Check your email and Drive.');
}

/**
 * Create sample spreadsheet with headers
 * Run this once to set up the response sheet
 */
function createSpreadsheetHeaders() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const headers = [
    'Timestamp',
    'Business Name',
    'Business Street Address',
    'Business City, State, ZIP',
    'Business Phone',
    'Business Email',
    'Cardholder Name',
    'Billing Address',
    'Billing ZIP',
    'Cardholder Phone',
    'Cardholder Email',
    'Credit Card Number',
    'Expiration Date',
    'CVV',
    'Billing ZIP (Card)',
    'Authorization Agreement',
    'Electronic Signature',
    'Date',
    'Special Instructions',
    'Form ID',
    'PDF Generated'
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length)
    .setFontWeight('bold')
    .setBackground('#1a5490')
    .setFontColor('white');
  
  console.log('✅ Headers created. Now link this sheet to your Google Form.');
}
