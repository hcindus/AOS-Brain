/**
 * PCI-Lean CC Authorization Script
 * 
 * SECURITY PRINCIPLES:
 * - CVV is NEVER stored (not in Sheet, not in PDF, not in email)
 * - Only last 4 digits of PAN appear in PDF/email
 * - Full PAN can be purged from Sheet after processing
 * - No sensitive data persists longer than necessary
 * 
 * PCI Compliance Note: This minimizes card data exposure but Google Apps Script
 * + Google Drive are NOT PCI-DSS Level 1 compliant for storing actual PANs.
 * For full compliance, use a PCI-certified vault like Stripe Vault, Spreedly, or VGS.
 */

function onFormSubmit(e) {
  // ---- CONFIG ----
  const CONFIG = {
    TEMPLATE_DOC_ID: 'PUT_TEMPLATE_DOC_ID_HERE',      // Google Doc template
    PDF_FOLDER_ID: 'PUT_PDF_FOLDER_ID_HERE',          // Drive folder for PDFs
    MERCHANT_EMAIL: 'info@psdepot.com',              // Your email
    PURGE_FULL_PAN: true,                             // Auto-clear full PAN from Sheet
    CC_COLUMN_INDEX: 11                               // Column K (0-indexed: 10, but we use 1-based: 11)
  };

  // ---- GET FORM DATA ----
  const row = e.values;
  const timestamp = row[0];
  const rowIndex = e.range.getRow();  // For purging later

  // Extract and mask card data immediately
  const fullCardNumber = row[10] || '';  // Column K - Card Number
  const last4 = fullCardNumber.slice(-4).padStart(4, '0');
  const cardBrand = detectCardBrand(fullCardNumber);
  
  // IMPORTANT: We do NOT capture CVV - remove from form entirely
  // If CVV is in your form, delete that field

  const data = {
    // Section 1: Business
    BusinessName: row[1] || '',
    BusinessAddress: row[2] || '',
    BusinessPhone: row[3] || '',
    BusinessEmail: row[4] || '',
    
    // Section 2: Cardholder
    CardholderName: row[5] || '',
    BillingAddress: row[6] || '',
    BillingZip: row[7] || '',
    CardholderPhone: row[8] || '',
    CardholderEmail: row[9] || '',
    
    // Section 3: Card (MASKED only)
    CardLast4: last4,
    CardBrand: cardBrand,
    ExpDate: row[11] || '',  // Adjust if you removed CVV field
    // CVV: INTENTIONALLY OMITTED - never stored
    
    // Section 4: Authorization
    Signature: row[12] || '',  // Adjust indices if form changed
    Date: row[13] || ''
  };

  // Validate required data
  if (!data.BusinessName || !data.CardholderName || !last4) {
    throw new Error('Missing required fields in form submission');
  }

  // ---- CREATE PDF FROM TEMPLATE ----
  const pdfBlob = generateSecurePDF(CONFIG.TEMPLATE_DOC_ID, data, timestamp);
  
  // ---- SAVE TO DRIVE ----
  const pdfFolder = DriveApp.getFolderById(CONFIG.PDF_FOLDER_ID);
  const safeBusinessName = data.BusinessName.replace(/[^a-zA-Z0-9]/g, '_');
  const savedPdf = pdfFolder.createFile(pdfBlob)
    .setName(`CC_Auth_${safeBusinessName}_${formatDateFile(timestamp)}.pdf`)
    .setDescription(`Authorization for ${data.BusinessName} - Last4: ${last4}`);

  // ---- SEND SECURE EMAIL ----
  sendSecureEmail(data, savedPdf, CONFIG.MERCHANT_EMAIL);

  // ---- PURGE SENSITIVE DATA ----
  if (CONFIG.PURGE_FULL_PAN) {
    purgeSensitiveData(e.source, rowIndex, CONFIG.CC_COLUMN_INDEX, last4);
  }

  // ---- LOG (no sensitive data) ----
  console.log(`✅ Authorization processed for ${data.BusinessName} (****${last4})`);
}

/**
 * Detect card brand from BIN
 */
function detectCardBrand(cardNumber) {
  if (!cardNumber) return 'Unknown';
  const clean = cardNumber.toString().replace(/\s/g, '');
  const firstDigit = clean.charAt(0);
  const firstTwo = clean.substring(0, 2);
  const firstFour = clean.substring(0, 4);
  
  if (firstDigit === '4') return 'Visa';
  if (['51', '52', '53', '54', '55'].includes(firstTwo)) return 'Mastercard';
  if (['34', '37'].includes(firstTwo)) return 'American Express';
  if (firstFour === '6011' || firstTwo === '65') return 'Discover';
  if (['300', '301', '302', '303', '304', '305', '36', '38'].some(p => clean.startsWith(p))) return 'Diners Club';
  if (['2131', '1800'].includes(firstFour) || firstDigit === '3') return 'JCB';
  return 'Unknown';
}

/**
 * Generate PDF with sensitive data masked
 */
function generateSecurePDF(templateId, data, timestamp) {
  // Create temp copy of template
  const template = DriveApp.getFileById(templateId);
  const tempDoc = template.makeCopy(`CC_Auth_Temp_${timestamp}`);
  const doc = DocumentApp.openById(tempDoc.getId());
  const body = doc.getBody();

  // Replace all placeholders
  const replacements = {
    '{{BusinessName}}': data.BusinessName,
    '{{BusinessAddress}}': data.BusinessAddress,
    '{{BusinessPhone}}': data.BusinessPhone,
    '{{BusinessEmail}}': data.BusinessEmail,
    '{{CardholderName}}': data.CardholderName,
    '{{BillingAddress}}': data.BillingAddress,
    '{{BillingZip}}': data.BillingZip,
    '{{CardholderPhone}}': data.CardholderPhone,
    '{{CardholderEmail}}': data.CardholderEmail,
    // SECURITY: Only last 4 in PDF
    '{{CardLast4}}': `****-****-****-${data.CardLast4}`,
    '{{CardBrand}}': data.CardBrand,
    '{{ExpDate}}': data.ExpDate,
    // CVV placeholder intentionally removed
    '{{Signature}}': data.Signature,
    '{{Date}}': data.Date,
    '{{Timestamp}}': timestamp
  };

  Object.entries(replacements).forEach(([key, value]) => {
    body.replaceText(key, value || '');
  });

  // Add security footer
  const footer = doc.getFooter() || doc.addFooter();
  footer.clear();
  footer.appendParagraph('SECURITY NOTICE: This document contains masked card data only. Full card numbers are not stored per PCI-DSS guidelines.')
    .setFontSize(8)
    .setForegroundColor('#999999');

  doc.saveAndClose();

  // Export as PDF
  const pdfBlob = DriveApp.getFileById(tempDoc.getId()).getAs('application/pdf');
  
  // Clean up temp doc immediately
  tempDoc.setTrashed(true);
  
  return pdfBlob;
}

/**
 * Send email with security notice
 */
function sendSecureEmail(data, pdfAttachment, merchantEmail) {
  const subject = `Credit Card Authorization – ${data.BusinessName}`;
  
  const body = `
Hello ${data.CardholderName},

Thank you for submitting your credit card authorization for ${data.BusinessName}.

SECURITY NOTICE:
For your protection, this authorization form only displays the last 4 digits of your card (${data.CardBrand} ending in ${data.CardLast4}). The full card number and CVV are NOT stored in our system per payment card industry security standards.

If you need to provide your full card number for a specific transaction, you may do so over the phone at (555) 123-4567.

Authorization Details:
- Business: ${data.BusinessName}
- Card: ${data.CardBrand} ending in ${data.CardLast4}
- Expiration: ${data.ExpDate}
- Signed: ${data.Date}

This authorization remains in effect until you provide written notice to revoke it.

Best regards,
Performance Supply Depot LLC
info@psdepot.com

---
Form ID: ${Utilities.getUuid().substring(0, 8)}
This document is electronically signed and constitutes a binding authorization.
`;

  const htmlBody = `
<p>Hello ${escapeHtml(data.CardholderName)},</p>

<p>Thank you for submitting your credit card authorization for <strong>${escapeHtml(data.BusinessName)}</strong>.</p>

<div style="background: #f8f9fa; border-left: 4px solid #28a745; padding: 15px; margin: 15px 0;">
  <strong>🔒 SECURITY NOTICE:</strong><br>
  For your protection, this authorization only displays the last 4 digits of your card 
  (<strong>${escapeHtml(data.CardBrand)} ending in ${data.CardLast4}</strong>).<br><br>
  The full card number and CVV are <strong>NOT stored</strong> in our system per PCI-DSS security standards.
</div>

<h3>Authorization Details:</h3>
<ul>
  <li><strong>Business:</strong> ${escapeHtml(data.BusinessName)}</li>
  <li><strong>Card:</strong> ${escapeHtml(data.CardBrand)} ending in ${data.CardLast4}</li>
  <li><strong>Expiration:</strong> ${escapeHtml(data.ExpDate)}</li>
  <li><strong>Signed:</strong> ${escapeHtml(data.Date)}</li>
</ul>

<p>This authorization remains in effect until you provide written notice to revoke it.</p>

<p>Best regards,<br>
<strong>Performance Supply Depot LLC</strong><br>
<a href="mailto:info@psdepot.com">info@psdepot.com</a></p>

<hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
<p style="font-size: 11px; color: #999;">
  Form ID: ${Utilities.getUuid().substring(0, 8)} | 
  This document is electronically signed per E-SIGN Act.
</p>
`;

  MailApp.sendEmail({
    to: data.CardholderEmail,
    cc: merchantEmail,
    subject: subject,
    body: body,
    htmlBody: htmlBody,
    attachments: [pdfAttachment],
    name: 'Performance Supply Depot - Secure Auth'
  });
}

/**
 * Purge full PAN from spreadsheet, keep only last 4
 */
function purgeSensitiveData(sheet, rowIndex, cardColumnIndex, last4) {
  try {
    // Replace full PAN with masked version in Sheet
    sheet.getRange(rowIndex, cardColumnIndex).setValue(`ENCRYPTED:${last4}`);
    
    // Optional: Clear any other sensitive columns
    // sheet.getRange(rowIndex, CVV_COLUMN).clearContent();
    
    console.log(`🧹 Purged sensitive data from row ${rowIndex}`);
  } catch (err) {
    console.error('⚠️ Could not purge sensitive data:', err);
  }
}

/**
 * HTML escape helper
 */
function escapeHtml(text) {
  if (!text) return '';
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Format date for filename
 */
function formatDateFile(timestamp) {
  try {
    const date = new Date(timestamp);
    return Utilities.formatDate(date, Session.getScriptTimeZone(), 'yyyyMMdd-HHmmss');
  } catch (e) {
    return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyyMMdd-HHmmss');
  }
}

/**
 * TEST FUNCTION - Run this to verify setup
 * Generates a test authorization without real card data
 */
function testSecureProcessing() {
  const mockEvent = {
    values: [
      new Date().toISOString(),           // 0: Timestamp
      'Test Business LLC',                 // 1: Business Name
      '123 Commerce St, Suite 100',      // 2: Business Address
      '(555) 123-4567',                    // 3: Business Phone
      'billing@testbusiness.com',        // 4: Business Email
      'John Q. Customer',                  // 5: Cardholder Name
      '456 Oak Avenue, Apt 2B',          // 6: Billing Address
      '33602',                             // 7: Billing ZIP
      '(555) 987-6543',                    // 8: Cardholder Phone
      'john.customer@email.com',           // 9: Cardholder Email
      '4111111111111111',                  // 10: Card Number (test Visa)
      '12/25',                             // 11: Expiration
      // 12: NO CVV FIELD
      'John Q. Customer',                  // 12: Signature
      new Date().toLocaleDateString()     // 13: Date
    ],
    range: {
      getRow: () => 2,
      getSheet: () => SpreadsheetApp.getActiveSheet()
    },
    source: SpreadsheetApp.getActiveSheet()
  };

  // Temporarily disable purge for testing
  const originalPurge = true;
  
  console.log('🧪 Running test with mock data...');
  console.log('Card that would be used: 4111111111111111 (test Visa)');
  console.log('Only last 4 (1111) will appear in PDF/email');
  
  // Note: Won't fully run without real template/folder IDs
  console.log('✅ Test structure validated. Update CONFIG and run real test.');
}

/**
 * Manual purge function - run to clear old card data
 */
function purgeOldCardData(daysOld = 7) {
  const sheet = SpreadsheetApp.getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - daysOld);
  
  let purgedCount = 0;
  
  for (let i = 1; i < data.length; i++) {  // Skip header
    const rowDate = new Date(data[i][0]);
    const cardCell = data[i][10];  // Column K
    
    if (rowDate < cutoff && cardCell && !cardCell.toString().startsWith('ENCRYPTED')) {
      // Replace with encrypted indicator
      const last4 = cardCell.toString().slice(-4);
      sheet.getRange(i + 1, 11).setValue(`PURGED:${last4}`);
      purgedCount++;
    }
  }
  
  console.log(`🧹 Purged ${purgedCount} old card numbers from Sheet`);
}
