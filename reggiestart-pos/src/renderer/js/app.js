/**
 * ReggieStart POS - Main Application Logic
 * Full-featured standalone point of sale system
 */

// State management
const state = {
  cart: [],
  products: [],
  settings: {
    taxRate: 8.5,
    storeName: 'ReggieStart Demo Store'
  },
  currentInput: '',
  currentMode: 'normal', // normal, qty, void, disc, plu
  transactionsToday: 0
};

// DOM Elements
const elements = {
  productsGrid: document.getElementById('products-grid'),
  cartItems: document.getElementById('cart-items'),
  subtotal: document.getElementById('subtotal'),
  tax: document.getElementById('tax'),
  grandTotal: document.getElementById('grand-total'),
  taxRate: document.getElementById('tax-rate'),
  productSearch: document.getElementById('product-search'),
  transactionCount: document.getElementById('transaction-count'),
  storeName: document.getElementById('store-name'),
  currentTime: document.getElementById('current-time')
};

// Initialize
async function init() {
  await loadSettings();
  await loadProducts();
  setupEventListeners();
  updateTime();
  setInterval(updateTime, 1000);
  updateTransactionCount();
}

// Load settings from database
async function loadSettings() {
  try {
    const taxRate = await window.electronAPI.getSetting('tax_rate');
    const storeName = await window.electronAPI.getSetting('store_name');
    
    if (taxRate) state.settings.taxRate = parseFloat(taxRate);
    if (storeName) state.settings.storeName = storeName;
    
    elements.taxRate.textContent = state.settings.taxRate + '%';
    elements.storeName.textContent = state.settings.storeName;
  } catch (error) {
    console.error('Failed to load settings:', error);
  }
}

// Load products from database
async function loadProducts() {
  try {
    state.products = await window.electronAPI.getProducts();
    renderProducts();
  } catch (error) {
    console.error('Failed to load products:', error);
    showNotification('Failed to load products', 'error');
  }
}

// Render products grid
function renderProducts(category = 'all') {
  const filtered = category === 'all' 
    ? state.products 
    : state.products.filter(p => p.category === category);
  
  elements.productsGrid.innerHTML = filtered.map(product => `
    <div class="product-card" data-plu="${product.plu}" data-id="${product.id}">
      <span class="product-icon">${getProductIcon(product.category)}</span>
      <span class="product-name">${product.name}</span>
      <span class="product-price">$${product.price.toFixed(2)}</span>
      ${product.stock < 10 ? '<span class="product-stock low">Low Stock: ' + product.stock + '</span>' : ''}
    </div>
  `).join('');
  
  // Add click handlers
  document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('click', () => {
      const plu = card.dataset.plu;
      const product = state.products.find(p => p.plu === plu);
      if (product) addToCart(product);
    });
  });
}

// Get icon for category
function getProductIcon(category) {
  const icons = {
    'Food': '🍔',
    'Beverages': '🥤',
    'Desserts': '🍦',
    'default': '📦'
  };
  return icons[category] || icons.default;
}

// Add item to cart
function addToCart(product, quantity = 1) {
  const existing = state.cart.find(item => item.plu === product.plu);
  
  if (existing) {
    existing.quantity += quantity;
  } else {
    state.cart.push({
      plu: product.plu,
      name: product.name,
      price: product.price,
      quantity: quantity
    });
  }
  
  renderCart();
  playSound('add');
}

// Remove item from cart
function removeFromCart(index) {
  state.cart.splice(index, 1);
  renderCart();
}

// Update item quantity
function updateQuantity(index, delta) {
  state.cart[index].quantity += delta;
  if (state.cart[index].quantity <= 0) {
    removeFromCart(index);
  } else {
    renderCart();
  }
}

// Render cart
function renderCart() {
  if (state.cart.length === 0) {
    elements.cartItems.innerHTML = `
      <div class="empty-cart">
        <p>🛒 Cart is empty</p>
        <p class="sub-text">Select products to begin</p>
      </div>
    `;
  } else {
    elements.cartItems.innerHTML = state.cart.map((item, index) => `
      <div class="cart-item" data-index="${index}">
        <div class="cart-item-info">
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-price">$${item.price.toFixed(2)} each</div>
        </div>
        <div class="cart-item-qty">
          <button class="qty-btn" data-action="decrease" data-index="${index}">−</button>
          <span>${item.quantity}</span>
          <button class="qty-btn" data-action="increase" data-index="${index}">+</button>
        </div>
        <div class="cart-item-total">$${(item.price * item.quantity).toFixed(2)}</div>
      </div>
    `).join('');
    
    // Add quantity button handlers
    document.querySelectorAll('.qty-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const index = parseInt(e.target.dataset.index);
        const action = e.target.dataset.action;
        if (action === 'increase') updateQuantity(index, 1);
        else if (action === 'decrease') updateQuantity(index, -1);
      });
    });
  }
  
  updateTotals();
}

// Calculate and update totals
function updateTotals() {
  const subtotal = state.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const tax = subtotal * (state.settings.taxRate / 100);
  const total = subtotal + tax;
  
  elements.subtotal.textContent = '$' + subtotal.toFixed(2);
  elements.tax.textContent = '$' + tax.toFixed(2);
  elements.grandTotal.textContent = '$' + total.toFixed(2);
  
  return { subtotal, tax, total };
}

// Clear transaction
function clearTransaction() {
  if (state.cart.length === 0) return;
  
  if (confirm('Clear current transaction?')) {
    state.cart = [];
    renderCart();
    playSound('cancel');
  }
}

// Process payment
async function processPayment(method) {
  if (state.cart.length === 0) {
    showNotification('Cart is empty', 'warning');
    return;
  }
  
  const totals = updateTotals();
  
  if (method === 'Cash') {
    showPaymentModal(totals);
  } else {
    // Card payments - process directly
    await completeTransaction(method, totals.total);
  }
}

// Show payment modal
function showPaymentModal(totals) {
  const modal = document.getElementById('payment-modal');
  document.getElementById('modal-total').textContent = '$' + totals.total.toFixed(2);
  document.getElementById('amount-received').value = '';
  document.getElementById('change-amount').textContent = '$0.00';
  
  modal.classList.add('active');
  
  // Focus and calculate change
  const amountInput = document.getElementById('amount-received');
  amountInput.focus();
  
  amountInput.addEventListener('input', () => {
    const received = parseFloat(amountInput.value) || 0;
    const change = Math.max(0, received - totals.total);
    document.getElementById('change-amount').textContent = '$' + change.toFixed(2);
  });
}

// Complete transaction
async function completeTransaction(paymentMethod, amountReceived) {
  try {
    const totals = updateTotals();
    
    const transaction = {
      items: [...state.cart],
      subtotal: totals.subtotal,
      tax: totals.tax,
      total: totals.total,
      paymentMethod: paymentMethod
    };
    
    // Save to database
    const transactionId = await window.electronAPI.saveTransaction(transaction);
    
    // Print receipt
    const receiptData = {
      ...transaction,
      timestamp: new Date().toISOString(),
      storeName: state.settings.storeName,
      receiptHeader: 'Thank you for your business!'
    };
    
    await window.electronAPI.printReceipt(receiptData);
    
    // Show receipt modal
    showReceiptModal(receiptData);
    
    // Clear cart
    state.cart = [];
    renderCart();
    
    // Update transaction count
    state.transactionsToday++;
    updateTransactionCount();
    
    playSound('success');
    showNotification('Transaction completed!', 'success');
    
  } catch (error) {
    console.error('Transaction failed:', error);
    showNotification('Transaction failed: ' + error.message, 'error');
  }
}

// Show receipt modal
function showReceiptModal(receiptData) {
  const modal = document.getElementById('receipt-modal');
  const preview = document.getElementById('receipt-preview');
  
  preview.innerHTML = `
    <div style="text-align: center; margin-bottom: 15px;">
      <strong>${receiptData.storeName}</strong><br>
      ${new Date(receiptData.timestamp).toLocaleString()}
    </div>
    <div style="margin: 15px 0; border-top: 1px dashed #000; border-bottom: 1px dashed #000; padding: 10px 0;">
      ${receiptData.items.map(item => `
        <div style="display: flex; justify-content: space-between; margin: 3px 0;">
          <span>${item.name} x${item.quantity}</span>
          <span>$${(item.price * item.quantity).toFixed(2)}</span>
        </div>
      `).join('')}
    </div>
    <div style="text-align: right;">
      <div>Subtotal: $${receiptData.subtotal.toFixed(2)}</div>
      <div>Tax: $${receiptData.tax.toFixed(2)}</div>
      <div style="font-weight: bold; margin-top: 5px;">Total: $${receiptData.total.toFixed(2)}</div>
      <div style="margin-top: 5px;">Payment: ${receiptData.paymentMethod}</div>
    </div>
    <div style="text-align: center; margin-top: 15px; font-size: 11px;">
      ${receiptData.receiptHeader}
    </div>
  `;
  
  modal.classList.add('active');
}

// Update transaction count display
function updateTransactionCount() {
  elements.transactionCount.textContent = `Transactions Today: ${state.transactionsToday}`;
}

// Update clock
function updateTime() {
  const now = new Date();
  elements.currentTime.textContent = now.toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit',
    second: '2-digit'
  });
}

// Setup event listeners
function setupEventListeners() {
  // Category tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderProducts(btn.dataset.category);
    });
  });
  
  // Product search
  elements.productSearch.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    if (query.length === 0) {
      renderProducts();
      return;
    }
    
    // Check if it's a PLU
    const pluMatch = state.products.find(p => p.plu === query);
    if (pluMatch) {
      addToCart(pluMatch);
      elements.productSearch.value = '';
      renderProducts();
      return;
    }
    
    // Filter by name
    const filtered = state.products.filter(p => 
      p.name.toLowerCase().includes(query) || 
      p.plu.includes(query)
    );
    
    elements.productsGrid.innerHTML = filtered.map(product => `
      <div class="product-card" data-plu="${product.plu}">
        <span class="product-icon">${getProductIcon(product.category)}</span>
        <span class="product-name">${product.name}</span>
        <span class="product-price">$${product.price.toFixed(2)}</span>
      </div>
    `).join('');
    
    document.querySelectorAll('.product-card').forEach(card => {
      card.addEventListener('click', () => {
        const plu = card.dataset.plu;
        const product = state.products.find(p => p.plu === plu);
        if (product) addToCart(product);
      });
    });
  });
  
  // Clear transaction
  document.getElementById('clear-transaction').addEventListener('click', clearTransaction);
  
  // Payment buttons
  document.querySelectorAll('.payment-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      processPayment(btn.dataset.method);
    });
  });
  
  // Numpad
  document.querySelectorAll('.num-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      state.currentInput += btn.dataset.num;
      // Could show input somewhere
    });
  });
  
  document.querySelectorAll('.func-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const func = btn.dataset.func;
      handleFunctionKey(func);
    });
  });
  
  // Modal buttons
  document.querySelector('.btn-cancel').addEventListener('click', () => {
    document.getElementById('payment-modal').classList.remove('active');
  });
  
  document.querySelector('.btn-complete').addEventListener('click', async () => {
    const received = parseFloat(document.getElementById('amount-received').value) || 0;
    const total = parseFloat(document.getElementById('modal-total').textContent.replace('$', ''));
    
    if (received < total) {
      showNotification('Amount received is less than total', 'error');
      return;
    }
    
    document.getElementById('payment-modal').classList.remove('active');
    await completeTransaction('Cash', received);
  });
  
  // Receipt modal buttons
  document.querySelector('.btn-print').addEventListener('click', () => {
    window.print();
  });
  
  document.querySelector('.btn-skip').addEventListener('click', () => {
    document.getElementById('receipt-modal').classList.remove('active');
  });
  
  // Close modals on X
  document.querySelectorAll('.modal-close').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.target.closest('.modal').classList.remove('active');
    });
  });
  
  // Status bar buttons
  document.getElementById('btn-settings').addEventListener('click', () => {
    showNotification('Settings - Coming soon!', 'info');
  });
  
  document.getElementById('btn-help').addEventListener('click', () => {
    showNotification('Help - Coming soon!', 'info');
  });
  
  document.getElementById('btn-reports').addEventListener('click', async () => {
    await showReportsModal();
  });
  
  // Menu event handlers (from Electron)
  if (window.electronAPI) {
    window.electronAPI.onMenuNewTransaction(() => clearTransaction());
    window.electronAPI.onMenuProducts(() => showNotification('Products - Coming soon!', 'info'));
    window.electronAPI.onMenuDailyReport(() => showReportsModal());
  }
}

// Handle function keys
function handleFunctionKey(func) {
  switch(func) {
    case 'qty':
      state.currentMode = 'qty';
      showNotification('Enter quantity...', 'info');
      break;
    case 'void':
      if (state.cart.length > 0) {
        removeFromCart(state.cart.length - 1);
        playSound('remove');
      }
      break;
    case 'disc':
      showNotification('Discount - Coming soon!', 'info');
      break;
    case 'plu':
      const plu = state.currentInput;
      const product = state.products.find(p => p.plu === plu);
      if (product) {
        addToCart(product);
        state.currentInput = '';
      } else {
        showNotification('Product not found: ' + plu, 'error');
      }
      break;
    case 'enter':
      // Confirm current operation
      state.currentMode = 'normal';
      state.currentInput = '';
      break;
  }
}

// Show reports modal
async function showReportsModal() {
  const modal = document.getElementById('reports-modal');
  const content = document.getElementById('report-content');
  
  // Load daily report
  const today = new Date().toISOString().split('T')[0];
  
  try {
    const report = await window.electronAPI.getDailyReport(today);
    
    content.innerHTML = `
      <h3>Daily Summary - ${today}</h3>
      <div style="margin: 20px 0; padding: 20px; background: #f8fafc; border-radius: 8px;">
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; text-align: center;">
          <div>
            <div style="font-size: 24px; font-weight: bold; color: var(--primary-color);">
              ${report.summary.reduce((sum, s) => sum + s.transaction_count, 0)}
            </div>
            <div style="color: var(--text-light);">Transactions</div>
          </div>
          <div>
            <div style="font-size: 24px; font-weight: bold; color: var(--success-color);">
              $${report.summary.reduce((sum, s) => sum + s.total_sales, 0).toFixed(2)}
            </div>
            <div style="color: var(--text-light);">Total Sales</div>
          </div>
          <div>
            <div style="font-size: 24px; font-weight: bold; color: var(--warning-color);">
              $${report.summary.reduce((sum, s) => sum + s.total_tax, 0).toFixed(2)}
            </div>
            <div style="color: var(--text-light);">Tax Collected</div>
          </div>
        </div>
      </div>
      
      <h4>Payment Methods</h4>
      <table style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr style="border-bottom: 2px solid var(--border-color);">
            <th style="text-align: left; padding: 10px;">Method</th>
            <th style="text-align: right; padding: 10px;">Transactions</th>
            <th style="text-align: right; padding: 10px;">Amount</th>
          </tr>
        </thead>
        <tbody>
          ${report.summary.map(s => `
            <tr style="border-bottom: 1px solid var(--border-color);">
              <td style="padding: 10px;">${s.payment_method}</td>
              <td style="text-align: right; padding: 10px;">${s.method_count}</td>
              <td style="text-align: right; padding: 10px;">$${s.total_sales.toFixed(2)}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  } catch (error) {
    content.innerHTML = `<p>Error loading report: ${error.message}</p>`;
  }
  
  modal.classList.add('active');
}

// Notification system
function showNotification(message, type = 'info') {
  // Simple console log for now, could be expanded
  console.log(`[${type.toUpperCase()}] ${message}`);
  
  // Could add toast notifications here
}

// Sound effects (placeholder)
function playSound(type) {
  // Placeholder - could use Web Audio API
  console.log(`Sound: ${type}`);
}

// Start the app
document.addEventListener('DOMContentLoaded', init);
