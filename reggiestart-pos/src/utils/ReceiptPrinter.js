const { app } = require('electron');
const path = require('path');
const fs = require('fs');

class ReceiptPrinter {
  static print(receiptData) {
    const { items, subtotal, tax, total, paymentMethod, timestamp, storeName, receiptHeader } = receiptData;
    
    // Generate receipt HTML
    const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Receipt</title>
  <style>
    @media print {
      @page { margin: 0; size: 80mm auto; }
      body { margin: 0; }
    }
    body {
      font-family: 'Courier New', monospace;
      font-size: 12px;
      width: 80mm;
      padding: 10px;
      margin: 0 auto;
      background: white;
    }
    .header {
      text-align: center;
      border-bottom: 1px dashed #000;
      padding-bottom: 10px;
      margin-bottom: 10px;
    }
    .header h1 { font-size: 16px; margin: 0; }
    .header p { margin: 5px 0; font-size: 10px; }
    .items { margin: 10px 0; }
    .item { display: flex; justify-content: space-between; margin: 3px 0; }
    .item-name { flex: 1; }
    .item-qty { width: 30px; text-align: center; }
    .item-price { width: 60px; text-align: right; }
    .totals { 
      border-top: 1px dashed #000; 
      margin-top: 10px; 
      padding-top: 10px;
    }
    .total-row { display: flex; justify-content: space-between; margin: 3px 0; }
    .grand-total { 
      font-weight: bold; 
      font-size: 14px; 
      border-top: 1px solid #000;
      margin-top: 5px;
      padding-top: 5px;
    }
    .footer {
      text-align: center;
      margin-top: 20px;
      font-size: 10px;
    }
    .payment-method {
      text-align: center;
      margin: 10px 0;
      padding: 5px;
      border: 1px solid #000;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>${storeName || 'ReggieStart POS'}</h1>
    <p>${new Date(timestamp).toLocaleString()}</p>
  </div>
  
  <div class="items">
    ${items.map(item => `
      <div class="item">
        <span class="item-name">${item.name}</span>
        <span class="item-qty">x${item.quantity}</span>
        <span class="item-price">$${(item.price * item.quantity).toFixed(2)}</span>
      </div>
    `).join('')}
  </div>
  
  <div class="totals">
    <div class="total-row">
      <span>Subtotal:</span>
      <span>$${subtotal.toFixed(2)}</span>
    </div>
    <div class="total-row">
      <span>Tax:</span>
      <span>$${tax.toFixed(2)}</span>
    </div>
    <div class="total-row grand-total">
      <span>TOTAL:</span>
      <span>$${total.toFixed(2)}</span>
    </div>
  </div>
  
  <div class="payment-method">
    Payment: ${paymentMethod}
  </div>
  
  <div class="footer">
    <p>${receiptHeader || 'Thank you for your business!'}</p>
    <p>--- ReggieStart POS ---</p>
  </div>
</body>
</html>
    `;
    
    // Save to temp file and open for printing
    const tempPath = path.join(app.getPath('temp'), `receipt-${Date.now()}.html`);
    fs.writeFileSync(tempPath, html);
    
    // Open in default browser for printing
    const { shell } = require('electron');
    shell.openExternal(`file://${tempPath}`);
    
    return { success: true, path: tempPath };
  }
}

module.exports = ReceiptPrinter;
