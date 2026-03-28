// CREAM - Comprehensive Real Estate Agent Management
// Main Application File
// Version: 2.0 (Modular)

var appPath = "/sdcard/MyApp";
var curMenu = "Home";
var curPage = null;

// Load external page scripts
try {
    app.Script(appPath + "/pages/Utils.js");
    app.Script(appPath + "/pages/Home.js");
    app.Script(appPath + "/pages/PlanBusiness.js");
    app.Script(appPath + "/pages/Leads.js");
    app.Script(appPath + "/pages/AppointmentTracker.js");
    app.Script(appPath + "/pages/Farming.js");
    app.Script(appPath + "/pages/Revenue.js");
    app.Script(appPath + "/pages/Transaction.js");
    app.Script(appPath + "/pages/AnalyzeDB.js");
    app.Script(appPath + "/pages/PremiumTools.js");
    app.Script(appPath + "/pages/Settings.js");
    app.Script(appPath + "/pages/WebsitePortal.js");
    app.Script(appPath + "/pages/LetterGenerator.js");
} catch(e) {
    app.ShowPopup("Error loading scripts: " + e);
}

// App data
app.data = {
    tasks: ["Follow up with 3 leads", "Send farming letter"],
    leads: [{id: 45, status: "Hot"}, {id: 46, status: "Cold"}],
    appointments: [{name: "Jane Doe", time: "2 PM"}],
    metrics: {leads: 50, appts: 5, conversion: 18, revenue: 42500},
    offlineMode: false
};

var drawerWidth = 0.75;
var layMain, layContent, drawerScroll;

// Main entry point
function OnStart() {
    try {
        app.SetOrientation("Portrait");
        CreateTheme();
        
        // Create app folder
        if (!app.MakeFolder(appPath)) {
            throw new Error("Failed to create app folder");
        }
        if (!app.MakeFolder(appPath + "/data")) {
            throw new Error("Failed to create data folder");
        }
        
        // Create layouts
        layMain = app.CreateLayout("Linear", "FillXY");
        layMain.SetBackColor("#ffffff");
        
        CreateActionBar();
        CreatePageContainer();
        CreateDrawer();
        
        // Initialize pages
        home = curPage = new Home(appPath, layContent);
        planBusiness = new PlanBusiness(appPath, layContent);
        leads = new Leads(appPath, layContent);
        appointmentTracker = new AppointmentTracker(appPath, layContent);
        farming = new Farming(appPath, layContent);
        revenue = new Revenue(appPath, layContent);
        transaction = new Transaction(appPath, layContent);
        analyzeDB = new AnalyzeDB(appPath, layContent);
        premiumTools = new PremiumTools(appPath, layContent);
        settings = new Settings(appPath, layContent);
        websitePortal = new WebsitePortal(appPath, layContent);
        letterGenerator = new LetterGenerator(appPath, layContent);
        
        // Add layouts
        app.AddLayout(layMain);
        app.AddDrawer(drawerScroll, "Left", drawerWidth);
        
    } catch(e) {
        app.ShowPopup("Startup Error: " + e);
    }
}

function CreateTheme() {
    // Material-style theme
    app.SetTheme("Material");
}

function CreateActionBar() {
    var actionBar = app.CreateLayout("Linear", "Horizontal,FillXY");
    actionBar.SetSize(1, 0.1);
    actionBar.SetBackColor("#1E3A8A");
    
    var menuBtn = app.CreateImage("/sdcard/DroidScript/menu.png", 0.1, 0.08);
    menuBtn.SetOnTouch(function() {
        app.OpenDrawer();
    });
    actionBar.AddChild(menuBtn);
    
    var title = app.CreateText("CREAM", 0.8, 0.1, "Center");
    title.SetTextColor("#FFFFFF");
    title.SetTextSize(22);
    actionBar.AddChild(title);
    
    layMain.AddChild(actionBar);
}

function CreatePageContainer() {
    layContent = app.CreateLayout("Linear", "FillXY");
    layContent.SetSize(1, 0.9);
    layMain.AddChild(layContent);
}

function CreateDrawer() {
    drawerScroll = app.CreateLayout("ScrollView", "FillXY");
    drawerScroll.SetBackColor("#F5F5F5");
    
    var drawerLayout = app.CreateLayout("Linear", "Vertical");
    
    // Header
    var drawerHeader = app.CreateText("CREAM Menu", 0.9, 0.1);
    drawerHeader.SetTextSize(20);
    drawerHeader.SetTextColor("#1E3A8A");
    drawerLayout.AddChild(drawerHeader);
    
    // Menu items
    var menuItems = [
        "Home",
        "Plan Business",
        "Leads",
        "Appointment Tracker",
        "Farming",
        "Revenue",
        "Transaction",
        "Analyze DB",
        "Premium Tools",
        "Website Portal",
        "Letter Generator",
        "Settings"
    ];
    
    for (var i = 0; i < menuItems.length; i++) {
        var item = app.CreateText(menuItems[i], 0.9, 0.08);
        item.SetTextSize(16);
        item.SetPadding(0.02, 0.02, 0.02, 0.02);
        item.SetOnTouch(eval("function() { NavigateTo('" + menuItems[i] + "'); }"));
        drawerLayout.AddChild(item);
    }
    
    drawerScroll.AddChild(drawerLayout);
}

function NavigateTo(page) {
    app.CloseDrawer();
    
    // Hide all pages
    if (home) home.Show(false);
    if (planBusiness) planBusiness.Show(false);
    if (leads) leads.Show(false);
    if (appointmentTracker) appointmentTracker.Show(false);
    if (farming) farming.Show(false);
    if (revenue) revenue.Show(false);
    if (transaction) transaction.Show(false);
    if (analyzeDB) analyzeDB.Show(false);
    if (premiumTools) premiumTools.Show(false);
    if (settings) settings.Show(false);
    if (websitePortal) websitePortal.Show(false);
    if (letterGenerator) letterGenerator.Show(false);
    
    // Show selected page
    switch(page) {
        case "Home": if (home) home.Show(true, page); break;
        case "Plan Business": if (planBusiness) planBusiness.Show(true, page); break;
        case "Leads": if (leads) leads.Show(true, page); break;
        case "Appointment Tracker": if (appointmentTracker) appointmentTracker.Show(true, page); break;
        case "Farming": if (farming) farming.Show(true, page); break;
        case "Revenue": if (revenue) revenue.Show(true, page); break;
        case "Transaction": if (transaction) transaction.Show(true, page); break;
        case "Analyze DB": if (analyzeDB) analyzeDB.Show(true, page); break;
        case "Premium Tools": if (premiumTools) premiumTools.Show(true, page); break;
        case "Settings": if (settings) settings.Show(true, page); break;
        case "Website Portal": if (websitePortal) websitePortal.Show(true, page); break;
        case "Letter Generator": if (letterGenerator) letterGenerator.Show(true, page); break;
    }
    
    curMenu = page;
}
