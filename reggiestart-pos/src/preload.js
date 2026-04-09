const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods to renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  // Database operations
  getProducts: () => ipcRenderer.invoke('db-get-products'),
  getProductByPLU: (plu) => ipcRenderer.invoke('db-get-product-by-plu', plu),
  addProduct: (product) => ipcRenderer.invoke('db-add-product', product),
  updateProduct: (product) => ipcRenderer.invoke('db-update-product', product),
  deleteProduct: (id) => ipcRenderer.invoke('db-delete-product', id),
  saveTransaction: (transaction) => ipcRenderer.invoke('db-save-transaction', transaction),
  getTransactions: (limit) => ipcRenderer.invoke('db-get-transactions', limit),
  getDailyReport: (date) => ipcRenderer.invoke('db-get-daily-report', date),
  getSetting: (key) => ipcRenderer.invoke('db-get-setting', key),
  setSetting: (key, value) => ipcRenderer.invoke('db-set-setting', key, value),
  
  // Printing
  printReceipt: (receiptData) => ipcRenderer.invoke('print-receipt', receiptData),
  
  // Data export
  exportData: () => ipcRenderer.invoke('export-data'),
  
  // Menu events
  onMenuNewTransaction: (callback) => ipcRenderer.on('menu-new-transaction', callback),
  onMenuDailyReport: (callback) => ipcRenderer.on('menu-daily-report', callback),
  onMenuSettings: (callback) => ipcRenderer.on('menu-settings', callback),
  onMenuProducts: (callback) => ipcRenderer.on('menu-products', callback),
  onMenuCategories: (callback) => ipcRenderer.on('menu-categories', callback),
  onMenuSalesReport: (callback) => ipcRenderer.on('menu-sales-report', callback),
  onMenuInventoryReport: (callback) => ipcRenderer.on('menu-inventory-report', callback)
});

// Security: Remove listeners when not needed
window.addEventListener('beforeunload', () => {
  ipcRenderer.removeAllListeners();
});
