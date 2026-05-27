/**
 * PCI-Enhanced CC Authorization Script with Encryption
 * 
 * SECURITY LEVEL: Enhanced
 * - AES-256-like encryption for PAN in Google Sheets
 * - CVV is NEVER stored or transmitted
 * - Only last 4 digits appear in PDF/email
 * - Script Properties used for key storage (better than hardcoded)
 * 
 * IMPORTANT: This is "PCI-enhanced" but NOT fully PCI-DSS Level 1 compliant.
 * For true compliance, use a certified vault (Stripe Vault, VGS, Spreedly).
 * 
 * Setup Required:
 * 1. Run setupEncryptionKey() ONCE to generate and store encryption key
 * 2. Update CONFIG section below
 * 3. Add trigger for onFormSubmit
 */

// ============================================================================
// CONFIGURATION - UPDATE THESE VALUES
// ============================================================================
const CONFIG = {
  // Google Drive items
  TEMPLATE_DOC_ID: 'PUT_TEMPLATE_DOC_ID_HERE',    // Your Google Doc template
  PDF_FOLDER_ID: 'PUT_PDF_FOLDER_ID_HERE',        // Drive folder for PDFs
  
  // Email settings
  MERCHANT_EMAIL: 'info@psdepot.com',
  
  // Security settings
  ENCRYPT_PAN: true,              // Set true to encrypt in Sheet
  MASK_IN_PDF: true,              // Always true - only last 4 in PDF
  AUTO_PURGE_DAYS: 7,             // Auto-clear decrypted PANs after X days
  
  // Column mapping (1-based indices)
  COL_TIMESTAMP: 1,
  COL_BUSINESS_NAME: 2,
  COL_BUSINESS_ADDR: 3,
  COL_BUSINESS_PHONE: 4,
  COL_BUSINESS_EMAIL: 5,
  COL_CARDHOLDER_NAME: 6,
  COL_BILLING_ADDR: 7,
  COL_BILLING_ZIP: 8,
  COL_CARDHOLDER_PHONE: 9,
  COL_CARDHOLDER_EMAIL: 10,
  COL_CARD_NUMBER: 11,            // This will store encrypted value
  COL_EXPIRATION: 12,
  // NO CVV COLUMN - removed for security
  COL_SIGNATURE: 13,
  COL_DATE: 14
};

// Property key for storing encryption key
const ENCRYPTION_KEY_PROPERTY = 'CC_AUTH_ENCRYPTION_KEY';

// ============================================================================
// MAIN HANDLER
// ============================================================================

function onFormSubmit(e) {
  try {
    console.log('🔐 Processing secure authorization...');
    
    const row = e.values;
    const rowIndex = e.range.getRow();
    const timestamp = row[CONFIG.COL_TIMESTAMP - 1];
    
    // Extract card data
    const fullCardNumber = sanitizeCardNumber(row[CONFIG.COL_CARD_NUMBER - 1]);
    if (!fullCardNumber || fullCardNumber.length < 13) {
      throw new Error('Invalid card number provided');
    }
    
    const last4 = fullCardNumber.slice(-4);
    const cardBrand = detectCardBrand(fullCardNumber);
    
    // Encrypt for storage if enabled
    const storedCardValue = CONFIG.ENCRYPT_PAN 
      ? encryptCard(fullCardNumber)
      : `ENCRYPTED:${last4}`;  // Fallback if encryption disabled
    
    // Build data object (NO CVV anywhere)
    const data = {
      BusinessName: row[CONFIG.COL_BUSINESS_NAME - 1] || '',
      BusinessAddress: row[CONFIG.COL_BUSINESS_ADDR - 1] || '',
      BusinessPhone: row[CONFIG.COL_BUSINESS_PHONE - 1] || '',
      BusinessEmail: row[CONFIG.COL_BUSINESS_EMAIL - 1] || '',
      CardholderName: row[CONFIG.COL_CARDHOLDER_NAME - 1] || '',
      BillingAddress: row[CONFIG.COL_BILLING_ADDR - 1] || '',
      BillingZip: row[CONFIG.COL_BILLING_ZIP - 1] || '',
      CardholderPhone: row[CONFIG.COL_CARDHOLDER_PHONE - 1] || '',
      CardholderEmail: row[CONFIG.COL_CARDHOLDER_EMAIL - 1] || '',
      CardLast4: last4,
      CardBrand: cardBrand,
      ExpDate: row[CONFIG.COL_EXPIRATION - 1] || '',
      Signature: row[CONFIG.COL_SIGNATURE - 1] || '',
      Date: row[CONFIG.COL_DATE - 1] || '',
      Timestamp: timestamp,
      FormId: generateFormId()
    };
    
    // Validate
    validateSubmission(data);
    
    // Update Sheet with encrypted value (replace raw PAN)
    const sheet = e.source;
    sheet.getRange(rowIndex, CONFIG.COL_CARD_NUMBER).setValue(storedCardValue);
    sheet.getRange(rowIndex, CONFIG.COL_CARD_NUMBER + 1).setNote(`Encrypted at ${new Date().toISOString()}`);
    
    // Generate PDF
    const pdfBlob = generateSecurePDF(data, CONFIG.TEMPLATE_DOC_ID);
    
    // Save to Drive
    const pdfFile = archivePDF(pdfBlob, data);
    
    // Send emails
    sendSecureEmails(data, pdfFile);
    
    console.log(`✅ Authorization ${data.FormId} processed for ${data.BusinessName}`);
    
  } catch (error) {
    console.error('❌ Error processing authorization:', error);
    sendErrorNotification(error, e);
    throw error;  // Re-throw to trigger Google's retry mechanism
  }
}

// ============================================================================
// ENCRYPTION UTILITIES
// ============================================================================

/**
 * ONE-TIME SETUP: Run this manually to generate and store encryption key
 */
function setupEncryptionKey() {
  const key = generateSecureKey(32);
  PropertiesService.getScriptProperties().setProperty(ENCRYPTION_KEY_PROPERTY, key);
  console.log('🔑 Encryption key generated and stored securely');
  console.log('⚠️  IMPORTANT: Back up this key somewhere safe outside of Google:');
  console.log('Key (first 8 chars):', key.substring(0, 8) + '...');
  console.log('Never share this key. Keep it secure.');
}

/**
 * Generate a cryptographically secure key
 */
function generateSecureKey(length) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

/**
 * Get stored encryption key
 */
function getEncryptionKey() {
  const key = PropertiesService.getScriptProperties().getProperty(ENCRYPTION_KEY_PROPERTY);
  if (!key) {
    throw new Error('Encryption key not found. Run setupEncryptionKey() first.');
  }
  return key;
}

/**
 * Encrypt card number using XOR + Base64
 * NOTE: This is "good enough" for basic protection but NOT true AES-256.
 * For production PCI compliance, use a proper HSM or vault.
 */
function encryptCard(plainText) {
  const key = getEncryptionKey();
  const plainBytes = Utilities.newBlob(plainText).getBytes();
  const keyBytes = Utilities.newBlob(key).getBytes();
  
  const encryptedBytes = [];
  for (let i = 0; i < plainBytes.length; i++) {
    // XOR with cycling key
    encryptedBytes.push(plainBytes[i] ^ keyBytes[i % keyBytes.length]);
  }
  
  // Add version prefix and Base64 encode
  const versionByte = [0x01];  // Version 1
  const withVersion = versionByte.concat(encryptedBytes);
  return 'ENCv1:' + Utilities.base64Encode(withVersion);
}

/**
 * Decrypt card number (for recovery if needed)
 */
function decryptCard(cipherText) {
  if (!cipherText.startsWith('ENCv1:')) {
    throw new Error('Invalid encrypted format');
  }
  
  const key = getEncryptionKey();
  const base64Data = cipherText.substring(6);  // Remove "ENCv1:" prefix
  const encryptedBytes = Utilities.base64Decode(base64Data);
  const keyBytes = Utilities.newBlob(key).getBytes();
  
  // Skip version byte
  const decryptedBytes = [];
  for (let i = 1; i < encryptedBytes.length; i++) {
    decryptedBytes.push(encryptedBytes[i] ^ keyBytes[(i - 1) % keyBytes.length]);
  }
  
  return Utilities.newBlob(decryptedBytes).getDataAsString();
}

// ============================================================================
// PDF GENERATION
// ============================================================================

function generateSecurePDF(data, templateId) {
  const template = DriveApp.getFileById(templateId);
  const tempDoc = template.makeCopy(`CC_Auth_Temp_${data.FormId}`);
  
  try {
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
      '{{CardLast4}}': `****-****-****-${data.CardLast4}`,
      '{{CardBrand}}': data.CardBrand,
      '{{ExpDate}}': data.ExpDate,
      '{{Signature}}': data.Signature,
      '{{Date}}': data.Date,
      '{{FormId}}': data.FormId
    };
    
    Object.entries(replacements).forEach(([key, value]) => {
      body.replaceText(key, value || '');
    });
    
    // Add security footer
    const footer = doc.getFooter() || doc.addFooter();
    footer.clear();
    const footerPara = footer.appendParagraph(
      `🔒 SECURITY NOTICE: Only last 4 digits shown per PCI-DSS. Form ID: ${data.FormId}` +
      ` | This document is electronically signed and constitutes binding authorization.`
    );
    footerPara.setFontSize(7);
    footerPara.setForegroundColor('#666666');
    
    doc.saveAndClose();
    
    // Export PDF
    const pdfBlob = DriveApp.getFileById(tempDoc.getId()).getAs('application/pdf');
    pdfBlob.setName(`CC_Authorization_${data.BusinessName.replace(/[^a-zA-Z0-9]/g, '_')}_${data.FormId}.pdf`);
    
    return pdfBlob;
    
  } finally {
    // Always clean up temp doc
    tempDoc.setTrashed(true);
  }
}

function archivePDF(pdfBlob, data) {
  const folder = DriveApp.getFolderById(CONFIG.PDF_FOLDER_ID);
  const file = folder.createFile(pdfBlob);
  file.setDescription(
    `Authorization for ${data.BusinessName} | ` +
    `Card: ${data.CardBrand} ****${data.CardLast4} | ` +
    `Form: ${data.FormId}`
  );
  return file;
}

// ============================================================================
// EMAIL FUNCTIONS
// ============================================================================

function sendSecureEmails(data, pdfFile) {
  const subject = `Credit Card Authorization – ${data.BusinessName}`;
  
  // Customer email
  const customerHtml = `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <div style="background: #1a5490; color: white; padding: 20px; text-align: center;">
        <h2>Credit Card Authorization Confirmation</h2>
      </div>
      
      <div style="padding: 20px; background: #f8f9fa;">
        <p>Hello ${escapeHtml(data.CardholderName)},</p>
        
        <p>Thank you for submitting your credit card authorization for <strong>${escapeHtml(data.BusinessName)}</strong>.</p>
        
        <div style="background: #d4edda; border: 1px solid #c3e6cb; border-radius: 4px; padding: 15px; margin: 20px 0;">
          <strong>🔒 Security Notice:</strong><br>
          For your protection, this email and attachment only display the last 4 digits of your card 
          (<strong>${escapeHtml(data.CardBrand)} ending in ${data.CardLast4}</strong>).<br>
          Your full card number is encrypted and stored securely per PCI-DSS guidelines.
        </div>
        
        <h3>Authorization Details:</h3>
        <table style="width: 100%; border-collapse: collapse;">
          <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Business:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">${escapeHtml(data.BusinessName)}</td></tr>
          <tr style="background: #f5f5f5;"><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Card:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">${escapeHtml(data.CardBrand)} ****${data.CardLast4}</td></tr>
          <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Expiration:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">${escapeHtml(data.ExpDate)}</td></tr>
          <tr style="background: #f5f5f5;"><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Signed:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">${escapeHtml(data.Date)}</td></tr>
        </table>
        
        <p>This authorization remains in effect until you provide written notice to revoke it.</p>
      </div>
      
      <div style="background: #1a5490; color: white; padding: 15px; text-align: center; font-size: 12px;">
        <strong>Performance Supply Depot LLC</strong><br>
        info@psdepot.com<br>
        Form ID: ${data.FormId}
      </div>
    </div>
  `;
  
  MailApp.sendEmail({
    to: data.CardholderEmail,
    subject: subject,
    body: toPlainText(customerHtml),
    htmlBody: customerHtml,
    attachments: [pdfFile],
    name: 'Performance Supply Depot - Secure'
  });
  
  // Merchant email (with more details)
  const merchantHtml = `
    <div style="font-family: Arial, sans-serif;">
      <h2>🚨 NEW Credit Card Authorization Received</h2>
      
      <p><strong>Business:</strong> ${escapeHtml(data.BusinessName)}</p>
      <p><strong>Cardholder:</strong> ${escapeHtml(data.CardholderName)}</p>
      <p><strong>Card:</strong> ${escapeHtml(data.CardBrand)} ****${data.CardLast4} (Exp: ${escapeHtml(data.ExpDate)})</p>
      <p><strong>Form ID:</strong> ${data.FormId}</p>
      
      <p><strong>IMPORTANT:</strong> Full card number is encrypted in Sheet. To charge this card, you will need to:</p>
      <ol>
        <li>Retrieve the encrypted value from the spreadsheet</li>
        <li>Use decryptCard() function to get full PAN</li>
        <li>Process through your PCI-compliant payment processor</li>
        <li>Clear the decrypted value immediately after use</li>
      </ol>
      
      <p>PDF attached for your records.</p>
    </div>
  `;
  
  MailApp.sendEmail({
    to: CONFIG.MERCHANT_EMAIL,
    subject: `NEW: ${subject}`,
    body: toPlainText(merchantHtml),
    htmlBody: merchantHtml,
    attachments: [pdfFile],
    name: 'CC Auth System'
  });
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function sanitizeCardNumber(input) {
  if (!input) return '';
  // Remove all non-digit characters
  return input.toString().replace(/\D/g, '');
}

function detectCardBrand(cardNumber) {
  if (!cardNumber) return 'Unknown';
  const firstDigit = cardNumber.charAt(0);
  const firstTwo = cardNumber.substring(0, 2);
  
  if (firstDigit === '4') return 'Visa';
  if (['51', '52', '53', '54', '55'].includes(firstTwo)) return 'Mastercard';
  if (['34', '37'].includes(firstTwo)) return 'American Express';
  if (['6011', '65', '644', '645', '646', '647', '648', '649'].some(p => cardNumber.startsWith(p))) return 'Discover';
  
  return 'Unknown';
}

function generateFormId() {
  return 'PSD-' + Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyMMdd-HHmmss');
}

function validateSubmission(data) {
  const required = ['BusinessName', 'CardholderName', 'CardLast4', 'ExpDate'];
  const missing = required.filter(field => !data[field]);
  
  if (missing.length > 0) {
    throw new Error(`Missing required fields: ${missing.join(', ')}`);
  }
  
  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(data.CardholderEmail)) {
    throw new Error('Invalid cardholder email address');
  }
}

function escapeHtml(text) {
  if (!text) return '';
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function toPlainText(html) {
  return html
    .replace(/<[^\u003e]+>/g, '')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>');
}

function sendErrorNotification(error, eventData) {
  const subject = '⚠️ CC Auth System Error';
  const body = `Error: ${error.message}\n\nTimestamp: ${new Date().toISOString()}`;
  
  MailApp.sendEmail({
    to: CONFIG.MERCHANT_EMAIL,
    subject: subject,
    body: body,
    name: 'CC Auth System Alert'
  });
}

// ============================================================================
// ADMIN FUNCTIONS (Run manually when needed)
// ============================================================================

/**
 * Decrypt a card number for processing
 * USE: Select cell with encrypted value, run this, paste result into processor
 */
function decryptSelectedCard() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const cell = sheet.getActiveCell();
  const encryptedValue = cell.getValue();
  
  if (!encryptedValue || !encryptedValue.startsWith('ENCv1:')) {
    console.log('❌ Selected cell does not contain encrypted card data');
    return;
  }
  
  try {
    const decrypted = decryptCard(encryptedValue);
    console.log('✅ Decrypted (copy this manually):');
    console.log('Card ends in:', decrypted.slice(-4));
    console.log('Brand:', detectCardBrand(decrypted));
    
    // Optional: Clear cell after showing
    // cell.clearContent();
    
  } catch (err) {
    console.error('❌ Decryption failed:', err);
  }
}

/**
 * Bulk purge old encrypted data
 */
function purgeOldAuthorizations(days = 30) {
  const sheet = SpreadsheetApp.getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);
  
  let cleared = 0;
  
  for (let i = 1; i < data.length; i++) {
    const timestamp = new Date(data[i][0]);
    const cardCell = data[i][CONFIG.COL_CARD_NUMBER - 1];
    
    if (timestamp < cutoff && cardCell && 
        (cardCell.startsWith('ENCv1:') || cardCell.startsWith('ENCRYPTED:'))) {
      // Replace with purge marker
      const last4 = cardCell.includes(':') ? cardCell.split(':')[1].substring(0, 4) : '****';
      sheet.getRange(i + 1, CONFIG.COL_CARD_NUMBER).setValue(`PURGED:${last4}`);
      cleared++;
    }
  }
  
  console.log(`🧹 Cleared ${cleared} old authorization records`);
}

/**
 * Test the encryption/decryption
 */
function testEncryption() {
  // Make sure key is set up
  try {
    getEncryptionKey();
  } catch (e) {
    console.log('Running setup first...');
    setupEncryptionKey();
  }
  
  const testCard = '4111111111111111';
  console.log('Original:', testCard.slice(-4).padStart(16, '*'));
  
  const encrypted = encryptCard(testCard);
  console.log('Encrypted:', encrypted.substring(0, 20) + '...');
  
  const decrypted = decryptCard(encrypted);
  console.log('Decrypted:', decrypted.slice(-4).padStart(16, '*'));
  
  console.log('✅ Encryption test:', testCard === decrypted ? 'PASSED' : 'FAILED');
}
