const { app, BrowserWindow, ipcMain, dialog, Menu } = require('electron');
const path = require('path');
const Database = require('./database/Database');
const ReceiptPrinter = require('./utils/ReceiptPrinter');

let mainWindow;
let db;
let printer;

// Security: Prevent new window creation
app.on('web-contents-created', (event, contents) => {
  contents.on('new-window', (event, navigationUrl) => {
    event.preventDefault();
  });
});

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1024,
    minHeight: 768,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      webSecurity: true
    },
    icon: path.join(__dirname, '../assets/icons/icon.png'),
    title: 'ReggieStart POS v1.0.0',
    show: false
  });

  // Load the app
  mainWindow.loadFile(path.join(__dirname, 'renderer/index.html'));

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Open DevTools in development
    if (process.env.NODE_ENV === 'development') {
      mainWindow.webContents.openDevTools();
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Setup menu
  setupMenu();
}

function setupMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'New Transaction',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow.webContents.send('menu-new-transaction');
          }
        },
        {
          label: 'Daily Report',
          accelerator: 'CmdOrCtrl+R',
          click: () => {
            mainWindow.webContents.send('menu-daily-report');
          }
        },
        { type: 'separator' },
        {
          label: 'Settings',
          accelerator: 'CmdOrCtrl+,',
          click: () => {
            mainWindow.webContents.send('menu-settings');
          }
        },
        { type: 'separator' },
        {
          label: 'Exit',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => {
            app.quit();
          }
        }
      ]
    },
    {
      label: 'Inventory',
      submenu: [
        {
          label: 'Manage Products',
          accelerator: 'CmdOrCtrl+P',
          click: () => {
            mainWindow.webContents.send('menu-products');
          }
        },
        {
          label: 'Categories',
          click: () => {
            mainWindow.webContents.send('menu-categories');
          }
        }
      ]
    },
    {
      label: 'Reports',
      submenu: [
        {
          label: 'Sales Report',
          click: () => {
            mainWindow.webContents.send('menu-sales-report');
          }
        },
        {
          label: 'Inventory Report',
          click: () => {
            mainWindow.webContents.send('menu-inventory-report');
          }
        }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'About ReggieStart POS',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'About',
              message: 'ReggieStart POS v1.0.0',
              detail: 'A full-featured standalone point of sale system.\n\n© 2026 AGI Company'
            });
          }
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// Initialize database
async function initializeDatabase() {
  db = new Database();
  await db.initialize();
  console.log('Database initialized');
  
  // Seed demo data if empty
  const productCount = db.getProductCount();
  if (productCount === 0) {
    console.log('Seeding demo data...');
    seedDemoData();
  }
}

function seedDemoData() {
  const demoProducts = [
    { plu: '1001', name: 'Cheeseburger', price: 8.99, category: 'Food', stock: 50 },
    { plu: '1002', name: 'French Fries', price: 3.49, category: 'Food', stock: 100 },
    { plu: '1003', name: 'Soda (16oz)', price: 2.49, category: 'Beverages', stock: 200 },
    { plu: '1004', name: 'Milkshake', price: 4.99, category: 'Beverages', stock: 30 },
    { plu: '1005', name: 'Chicken Sandwich', price: 9.49, category: 'Food', stock: 40 },
    { plu: '1006', name: 'Onion Rings', price: 3.99, category: 'Food', stock: 60 },
    { plu: '1007', name: 'Salad', price: 6.49, category: 'Food', stock: 25 },
    { plu: '1008', name: 'Coffee', price: 1.99, category: 'Beverages', stock: 150 },
    { plu: '1009', name: 'Bottled Water', price: 1.49, category: 'Beverages', stock: 300 },
    { plu: '1010', name: 'Ice Cream Cone', price: 2.49, category: 'Desserts', stock: 80 }
  ];
  
  demoProducts.forEach(product => {
    db.addProduct(product);
  });
  
  // Add tax rate
  db.setSetting('tax_rate', '8.5');
  db.setSetting('store_name', 'ReggieStart Demo Store');
  db.setSetting('receipt_header', 'Thank you for shopping!');
}

// IPC handlers
ipcMain.handle('db-get-products', () => {
  return db.getAllProducts();
});

ipcMain.handle('db-get-product-by-plu', (event, plu) => {
  return db.getProductByPLU(plu);
});

ipcMain.handle('db-add-product', (event, product) => {
  return db.addProduct(product);
});

ipcMain.handle('db-update-product', (event, product) => {
  return db.updateProduct(product);
});

ipcMain.handle('db-delete-product', (event, id) => {
  return db.deleteProduct(id);
});

ipcMain.handle('db-save-transaction', (event, transaction) => {
  return db.saveTransaction(transaction);
});

ipcMain.handle('db-get-transactions', (event, limit = 100) => {
  return db.getRecentTransactions(limit);
});

ipcMain.handle('db-get-daily-report', (event, date) => {
  return db.getDailyReport(date);
});

ipcMain.handle('db-get-setting', (event, key) => {
  return db.getSetting(key);
});

ipcMain.handle('db-set-setting', (event, key, value) => {
  return db.setSetting(key, value);
});

ipcMain.handle('print-receipt', (event, receiptData) => {
  return ReceiptPrinter.print(receiptData);
});

ipcMain.handle('export-data', async () => {
  const result = await dialog.showSaveDialog(mainWindow, {
    title: 'Export Data',
    defaultPath: `reggiestart-backup-${Date.now()}.json`,
    filters: [
      { name: 'JSON Files', extensions: ['json'] }
    ]
  });
  
  if (!result.canceled) {
    const data = db.exportAll();
    require('fs').writeFileSync(result.filePath, JSON.stringify(data, null, 2));
    return { success: true, path: result.filePath };
  }
  return { success: false };
});

// App lifecycle
app.whenReady().then(async () => {
  await initializeDatabase();
  createWindow();
});

app.on('window-all-closed', () => {
  if (db) {
    db.close();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// Security: Prevent navigation
app.on('web-contents-created', (event, contents) => {
  contents.on('will-navigate', (event, navigationUrl) => {
    event.preventDefault();
  });
});
