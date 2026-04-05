// Dusty - Cross-Chain Crypto Wallet Demo
// Version: 1.0
// Global Variables
var dustData = [];
var transactions = [];
var apiKeys = { 
  Binance: process.env.BINANCE_API_KEY || "", 
  Kucoin: process.env.KUCOIN_API_KEY || "" 
};
var walletAssets = { 
  Bitgert: { dust: 10, main: 50 }, 
  Ethereum: { dust: 0.001, main: 1 }, 
  Binance: { dust: 0.5, main: 10 }, 
  Solana: { dust: 0.02, main: 5 },
  Arbitrum: { dust: 0.05, main: 2 },
  Polygon: { dust: 0.1, main: 3 }
};
var firstSweep = true;
var stakedDust = 0;
var mainLay, settingsLay, historyLay, dappLay, portfolio, dustList, historyList, network;

function OnStart() {
  app.SetOrientation("Portrait");
  mainLay = app.CreateLayout("linear", "Vertical,FillXY");
  mainLay.SetBackColor("#1e1e2f");
  
  // Header
  var headerLay = app.CreateLayout("linear", "Horizontal");
  headerLay.SetBackColor("#6200ea");
  var logo = app.CreateText("Dusty", 0.3, 0.08, "Bold");
  logo.SetTextColor("#ffffff");
  logo.SetTextSize(22);
  network = app.CreateSpinner("All,Bitgert,Ethereum,Binance,Solana,Arbitrum,Polygon", 0.4, 0.08);
  network.SetTextColor("#ffffff");
  network.SetBackColor("#3a3a5c");
  var tabBtn = app.CreateButton("Tabs", 0.3, 0.08);
  tabBtn.SetBackColor("#ff5722");
  tabBtn.SetTextColor("#ffffff");
  tabBtn.SetOnTouch(showTabs);
  headerLay.AddChild(logo);
  headerLay.AddChild(network);
  headerLay.AddChild(tabBtn);
  mainLay.AddChild(headerLay);
  
  // Portfolio
  portfolio = app.CreateText("Portfolio: $0.00", 1, 0.1, "Bold");
  portfolio.SetTextColor("#00ffcc");
  portfolio.SetTextSize(18);
  portfolio.SetMargins(0, 0.02, 0, 0.02);
  mainLay.AddChild(portfolio);
  
  // Buttons
  var btnLay = app.CreateLayout("linear", "Horizontal");
  var scanBtn = app.CreateButton("Scan", 0.2, 0.1);
  scanBtn.SetBackColor("#6200ea");
  scanBtn.SetTextColor("#ffffff");
  scanBtn.SetOnTouch(scanForAssets);
  var consolidateBtn = app.CreateButton("Consolidate", 0.2, 0.1);
  consolidateBtn.SetBackColor("#00c853");
  consolidateBtn.SetTextColor("#ffffff");
  consolidateBtn.SetOnTouch(consolidateAssets);
  var bridgeBtn = app.CreateButton("Bridge", 0.2, 0.1);
  bridgeBtn.SetBackColor("#ff9800");
  bridgeBtn.SetTextColor("#ffffff");
  bridgeBtn.SetOnTouch(oneClickBridge);
  var stakeBtn = app.CreateButton("Stake", 0.2, 0.1);
  stakeBtn.SetBackColor("#2196f3");
  stakeBtn.SetTextColor("#ffffff");
  stakeBtn.SetOnTouch(stakeAssets);
  var settingsBtn = app.CreateButton("Settings", 0.2, 0.1);
  settingsBtn.SetBackColor("#ff5722");
  settingsBtn.SetTextColor("#ffffff");
  settingsBtn.SetOnTouch(showSettings);
  btnLay.AddChild(scanBtn);
  btnLay.AddChild(consolidateBtn);
  btnLay.AddChild(bridgeBtn);
  btnLay.AddChild(stakeBtn);
  btnLay.AddChild(settingsBtn);
  mainLay.AddChild(btnLay);
  
  // Asset Results
  dustList = app.CreateText("No assets found yet.", 1, 0.4, "Multiline,Left");
  dustList.SetTextColor("#ffffff");
  dustList.SetBackColor("#2a2a40");
  dustList.SetPadding(0.02, 0.02, 0.02, 0.02);
  mainLay.AddChild(dustList);
  
  // Transaction History Layout
  historyLay = app.CreateLayout("linear", "Vertical,FillXY");
  historyLay.SetBackColor("#1e1e2f");
  historyLay.SetVisibility("Hide");
  var historyTitle = app.CreateText("Transaction History", 1, 0.1, "Bold");
  historyTitle.SetTextColor("#ffffff");
  historyTitle.SetTextSize(22);
  historyLay.AddChild(historyTitle);
  historyList = app.CreateText("No transactions yet.", 1, 0.7, "Multiline,Left");
  historyList.SetTextColor("#ffffff");
  historyList.SetBackColor("#2a2a40");
  historyList.SetPadding(0.02, 0.02, 0.02, 0.02);
  historyLay.AddChild(historyList);
  
  // DApp Browser Layout
  dappLay = app.CreateLayout("linear", "Vertical,FillXY");
  dappLay.SetBackColor("#1e1e2f");
  dappLay.SetVisibility("Hide");
  var dappTitle = app.CreateText("DApp & Gaming Hub", 1, 0.1, "Bold");
  dappTitle.SetTextColor("#ffffff");
  dappTitle.SetTextSize(22);
  dappLay.AddChild(dappTitle);
  var dappUrl = app.CreateTextEdit("https://dusty-game.com", 0.8, 0.1);
  dappUrl.SetTextColor("#ffffff");
  dappLay.AddChild(dappUrl);
  var dappContent = app.CreateText("Connected to Dusty Game.\nEarn NFTs staking dust!", 1, 0.6, "Multiline,Left");
  dappContent.SetTextColor("#ffffff");
  dappContent.SetBackColor("#2a2a40");
  dappContent.SetPadding(0.02, 0.02, 0.02, 0.02);
  dappLay.AddChild(dappContent);
  
  // Settings Layout
  settingsLay = app.CreateLayout("linear", "Vertical,FillXY");
  settingsLay.SetBackColor("#1e1e2f");
  settingsLay.SetVisibility("Hide");
  var settingsTitle = app.CreateText("Settings", 1, 0.1, "Bold");
  settingsTitle.SetTextColor("#ffffff");
  settingsTitle.SetTextSize(22);
  settingsLay.AddChild(settingsTitle);
  var binanceKey = app.CreateTextEdit(apiKeys.Binance, 0.8, 0.1);
  binanceKey.SetHint("Binance API Key");
  binanceKey.SetTextColor("#ffffff");
  settingsLay.AddChild(binanceKey);
  var kucoinKey = app.CreateTextEdit(apiKeys.Kucoin, 0.8, 0.1);
  kucoinKey.SetHint("Kucoin API Key");
  kucoinKey.SetTextColor("#ffffff");
  settingsLay.AddChild(kucoinKey);
  var saveBtn = app.CreateButton("Save", 0.4, 0.1);
  saveBtn.SetBackColor("#6200ea");
  saveBtn.SetTextColor("#ffffff");
  saveBtn.SetOnTouch(function() { saveSettings(binanceKey.GetText(), kucoinKey.GetText()); });
  settingsLay.AddChild(saveBtn);
  
  app.AddLayout(mainLay);
  app.AddLayout(settingsLay);
  app.AddLayout(historyLay);
  app.AddLayout(dappLay);
}

function scanForAssets() {
  if (!apiKeys.Binance || !apiKeys.Kucoin) {
    app.ShowPopup("Set API keys in Settings first!");
    return;
  }
  dustList.SetText("Scanning all assets...\n");
  app.ShowProgress("Scanning...");
  setTimeout(function() {
    var selectedNetwork = network.GetText();
    dustData = [
      { asset: "BRISE", amount: walletAssets.Bitgert.dust, network: "Bitgert", source: "Internal", fee: 0.0000001, type: "Dust" },
      { asset: "BRISE", amount: walletAssets.Bitgert.main, network: "Bitgert", source: "Internal", fee: 0.0000001, type: "Main" },
      { asset: "ETH", amount: walletAssets.Ethereum.dust, network: "Ethereum", source: "Binance", fee: 5, type: "Dust" },
      { asset: "ETH", amount: walletAssets.Ethereum.main, network: "Ethereum", source: "Binance", fee: 5, type: "Main" },
      { asset: "BNB", amount: walletAssets.Binance.dust, network: "Binance", source: "Binance", fee: 0.5, type: "Dust" },
      { asset: "BNB", amount: walletAssets.Binance.main, network: "Binance", source: "Binance", fee: 0.5, type: "Main" },
      { asset: "SOL", amount: walletAssets.Solana.dust, network: "Solana", source: "Kucoin", fee: 0.01, type: "Dust" },
      { asset: "SOL", amount: walletAssets.Solana.main, network: "Solana", source: "Kucoin", fee: 0.01, type: "Main" },
      { asset: "ARB", amount: walletAssets.Arbitrum.dust, network: "Arbitrum", source: "Kucoin", fee: 0.05, type: "Dust" },
      { asset: "MATIC", amount: walletAssets.Polygon.dust, network: "Polygon", source: "Binance", fee: 0.1, type: "Dust" }
    ].filter(function(item) { 
      return item.amount > 0 && (selectedNetwork === "All" || selectedNetwork === item.network); 
    });
    
    var resultText = "Assets Found:\n";
    dustData.forEach(function(item) {
      resultText += item.source + " (" + item.network + ") - " + item.asset + ": " + item.amount + " " + item.type + " (Fee: " + item.fee + ")\n";
    });
    dustList.SetText(resultText || "No assets found.");
    
    var total = dustData.reduce(function(sum, item) { 
      return sum + item.amount * (item.type === "Dust" ? 0.01 : 1); 
    }, 0);
    var aiPrediction = total * 1.1;
    portfolio.SetText("Portfolio: $" + total.toFixed(2) + "\nAI Prediction: $" + aiPrediction.toFixed(2) + " (+10%)");
    app.HideProgress();
  }, 1000);
}

function consolidateAssets() {
  if (dustData.length === 0) {
    dustList.SetText("No assets to consolidate.");
    return;
  }
  app.ShowPopupMenu(["To BRISE", "To USDC"], function(choice) {
    var target = choice === "To USDC" ? "USDC" : "BRISE";
    app.ShowConfirm("Consolidate to " + target + " with zero fees (Bitgert subsidized)?", function() {
      dustList.SetText("Consolidating...\n");
      app.ShowProgress("Consolidating...");
      setTimeout(function() {
        var total = dustData.reduce(function(sum, item) { return sum + item.amount; }, 0);
        var feeSaved = dustData.reduce(function(sum, item) { return sum + item.fee * item.amount; }, 0);
        dustList.SetText("Consolidated " + total.toFixed(4) + " to " + total.toFixed(4) + " " + target + ".\nFee: $0 (Bitgert + partners)\nSaved: $" + feeSaved.toFixed(2) + " vs. other chains");
        
        transactions.push({
          date: new Date().toLocaleString(),
          amount: total.toFixed(4),
          type: "Consolidation to " + target + " (Zero-Fee)",
          status: "Completed"
        });
        updateHistory();
        dustData = [];
        portfolio.SetText("Portfolio: $0.00");
        app.HideProgress();
        app.ShowPopup("Consolidated to " + target + "!");
      }, 1000);
    });
  });
}

function oneClickBridge() {
  if (dustData.length === 0) {
    app.ShowPopup("No assets to bridge.");
    return;
  }
  app.ShowPopupMenu(["Bitgert", "Ethereum", "Binance", "Solana", "Fiat"], function(targetNetwork) {
    var target = targetNetwork === "Fiat" ? "USD" : targetNetwork;
    dustList.SetText("Bridging...\n");
    app.ShowProgress("Bridging...");
    setTimeout(function() {
      var total = dustData.reduce(function(sum, item) { return sum + item.amount; }, 0);
      dustList.SetText("Bridged " + total.toFixed(4) + " to " + target + " (optimized via Bitgert).\nFee: $0 (subsidized)");
      transactions.push({
        date: new Date().toLocaleString(),
        amount: total.toFixed(4),
        type: "Auto-Bridge to " + target,
        status: "Completed"
      });
      updateHistory();
      dustData = [];
      portfolio.SetText("Portfolio: $0.00");
      app.HideProgress();
      app.ShowPopup("Bridged to " + target + "!");
    }, 1000);
  });
}

function stakeAssets() {
  if (dustData.length === 0) {
    app.ShowPopup("No assets to stake.");
    return;
  }
  app.ShowConfirm("Stake assets for 10% APY + NFT rewards?", function() {
    dustList.SetText("Staking...\n");
    app.ShowProgress("Staking...");
    setTimeout(function() {
      var total = dustData.reduce(function(sum, item) { return sum + item.amount; }, 0);
      var yieldEstimate = total * 0.10;
      stakedDust += total;
      var nftReward = stakedDust >= 10 ? "Dusty Hero NFT" : "Dusty Minion NFT";
      dustList.SetText("Staked " + total.toFixed(4) + " BRISE.\nYield: " + yieldEstimate.toFixed(4) + " BRISE/year (10% APY)\nReward: " + nftReward);
      transactions.push({
        date: new Date().toLocaleString(),
        amount: total.toFixed(4),
        type: "Stake (10% APY + " + nftReward + ")",
        status: "Completed"
      });
      updateHistory();
      dustData = [];
      portfolio.SetText("Portfolio: $0.00");
      app.HideProgress();
      app.ShowPopup("Staked with NFT reward!");
    }, 1000);
  });
}

function updateHistory() {
  var historyText = "Transaction History:\n";
  transactions.forEach(function(tx) {
    historyText += tx.date + " - " + tx.type + ": " + tx.amount + " (" + tx.status + ")\n";
  });
  historyList.SetText(historyText);
}

function showSettings() {
  mainLay.SetVisibility("Hide");
  settingsLay.SetVisibility("Show");
}

function saveSettings(binanceKey, kucoinKey) {
  apiKeys.Binance = binanceKey;
  apiKeys.Kucoin = kucoinKey;
  settingsLay.SetVisibility("Hide");
  mainLay.SetVisibility("Show");
  app.ShowPopup("API keys saved!");
}

function showTabs() {
  var tabs = ["Wallet", "History", "DApp & Gaming"];
  app.ShowPopupMenu(tabs, function(choice) {
    mainLay.SetVisibility(choice === "Wallet" ? "Show" : "Hide");
    historyLay.SetVisibility(choice === "History" ? "Show" : "Hide");
    dappLay.SetVisibility(choice === "DApp & Gaming" ? "Show" : "Hide");
    settingsLay.SetVisibility("Hide");
  });
}

function resetDemo() {
  walletAssets = { 
    Bitgert: { dust: 10, main: 50 }, 
    Ethereum: { dust: 0.001, main: 1 }, 
    Binance: { dust: 0.5, main: 10 }, 
    Solana: { dust: 0.02, main: 5 },
    Arbitrum: { dust: 0.05, main: 2 },
    Polygon: { dust: 0.1, main: 3 }
  };
  dustData = [];
  transactions = [];
  firstSweep = true;
  stakedDust = 0;
  dustList.SetText("No assets found yet.");
  historyList.SetText("No transactions yet.");
  portfolio.SetText("Portfolio: $0.00");
}
