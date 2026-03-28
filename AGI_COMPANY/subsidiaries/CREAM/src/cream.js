// CREAM - Comprehensive Real Estate Agent Management
// Version: 1.0
// Date: August 15, 2025

var app = app || {};
app.currentPage = "Home";
app.data = {
  tasks: ["Follow up with 3 leads", "Send farming letter"],
  leads: [{id: 45, status: "Hot"}, {id: 46, status: "Cold"}],
  appointments: [{name: "Jane Doe", time: "2 PM"}],
  metrics: {leads: 50, appts: 5, conversion: 18, revenue: 42500},
  offlineMode: false
};

function OnStart() {
  app.layout = app.CreateLayout("linear", "VCenter,FillXY");
  app.layout.SetBackColor("#1E3A8A");
  
  // Top Bar
  app.topBar = app.CreateLayout("linear", "Horizontal");
  app.topBar.SetSize(1, 0.1);
  app.hamburger = app.CreateImage("/sdcard/DroidScript/hamburger.png", 0.05, 0.05);
  app.hamburger.SetOnTouch(MenuToggle);
  app.logo = app.CreateImage("/sdcard/DroidScript/cream_logo.png", 0.2, 0.08);
  app.topBar.AddChild(app.hamburger);
  app.topBar.AddChild(app.logo);
  app.layout.AddChild(app.topBar);
  
  // Content Area
  app.content = app.CreateLayout("linear", "Vertical");
  app.content.SetSize(1, 0.8);
  app.layout.AddChild(app.content);
  
  // Bottom Navigation
  app.bottomNav = app.CreateLayout("linear", "Horizontal");
  app.bottomNav.SetSize(1, 0.1);
  app.navHome = app.CreateImage("/sdcard/DroidScript/home_icon.png", 0.1, 0.1);
  app.navLeads = app.CreateImage("/sdcard/DroidScript/leads_icon.png", 0.1, 0.1);
  app.navFarming = app.CreateImage("/sdcard/DroidScript/farming_icon.png", 0.1, 0.1);
  app.navRevenue = app.CreateImage("/sdcard/DroidScript/revenue_icon.png", 0.1, 0.1);
  app.bottomNav.AddChild(app.navHome);
  app.bottomNav.AddChild(app.navLeads);
  app.bottomNav.AddChild(app.navFarming);
  app.bottomNav.AddChild(app.navRevenue);
  app.layout.AddChild(app.bottomNav);
  
  // Event Listeners
  app.navHome.SetOnTouch(function() { LoadPage("Home"); });
  app.navLeads.SetOnTouch(function() { LoadPage("Leads"); });
  app.navFarming.SetOnTouch(function() { LoadPage("Farming"); });
  app.navRevenue.SetOnTouch(function() { LoadPage("Revenue"); });
  
  LoadPage("Home");
  app.AddLayout(app.layout);
}

function MenuToggle() {
  app.CreateDialog("Menu", "Home|Plan Business|Leads|Appointment Tracker|Farming|Revenue|Transaction|Analyze DB|Premium Tools|Settings|Website Portal|Letter Generator", "Ok", OnMenuSelect);
}

function OnMenuSelect(item) {
  LoadPage(item);
}

function LoadPage(page) {
  app.content.RemoveAllChildren();
  app.currentPage = page;
  try {
    switch(page) {
      case "Home": LoadHome(); break;
      case "Plan Business": LoadPlanBusiness(); break;
      case "Leads": LoadLeads(); break;
      case "Appointment Tracker": LoadAppointmentTracker(); break;
      case "Farming": LoadFarming(); break;
      case "Revenue": LoadRevenue(); break;
      case "Transaction": LoadTransaction(); break;
      case "Analyze DB": LoadAnalyzeDB(); break;
      case "Premium Tools": LoadPremiumTools(); break;
      case "Settings": LoadSettings(); break;
      case "Website Portal": LoadWebsitePortal(); break;
      case "Letter Generator": LoadLetterGenerator(); break;
      default: LoadHome();
    }
  } catch(e) {
    app.ShowPopup("Error loading " + page + ": " + e);
  }
}

function LoadHome() {
  var welcome = app.CreateText("Welcome, Agent A!", 0.3, 0.1, "left");
  welcome.SetTextSize(20);
Size(20);
  app.content.AddChild(welcome);
  
  var tasksList = app.CreateList("", 0.9, 0.3);
  tasksList.AddItem("Follow up with 3 leads [View]");
  tasksList.AddItem("Send farming letter [Generate]");
  tasksList.SetOnTouch(TaskAction);
  app.content.AddChild(tasksList);
  
  var quickActions = app.CreateHBox(0.9, 0.1);
  quickActions.AddChild(app.CreateButton("Add Lead", 0.2, 0.1, "AddLead"));
  quickActions.AddChild(app.CreateButton("Generate Letter", 0.2, 0.1, "GenerateLetter"));
  quickActions.AddChild(app.CreateButton("View Revenue", 0.2, 0.1, "ViewRevenue"));
  quickActions.AddChild(app.CreateButton("Schedule Appt", 0.2, 0.1, "ScheduleAppt"));
  app.content.AddChild(quickActions);
  
  var metrics = app.CreateLayout("linear", "Vertical");
  metrics.AddChild(app.CreateText("Leads Added: 50 [Detail]", 0.9, 0.1));
  metrics.AddChild(app.CreateText("Appts: 5 [Detail]", 0.9, 0.1));
  metrics.AddChild(app.CreateText("Conversion: 18% [Detail]", 0.9, 0.1));
  metrics.AddChild(app.CreateText("Q3 Revenue: $42,500 [Detail]", 0.9, 0.1));
  app.content.AddChild(metrics);
}

function LoadPlanBusiness() {
  var planner = app.CreateLayout("linear", "Vertical");
  planner.AddChild(app.CreateText("Add 50 leads [67%]", 0.9, 0.1));
  planner.AddChild(app.CreateText("Close 10 deals [75%]", 0.9, 0.1));
  planner.AddChild(app.CreateText("Launch 3 campaigns [33%]", 0.9, 0.1));
  app.content.AddChild(planner);
  var coachTip = app.CreateText("Coach's Corner: Focus on 94117 geo-farming", 0.9, 0.1);
  app.content.AddChild(coachTip);
}

function LoadLeads() {
  var addForm = app.CreateLayout("linear", "Horizontal");
  addForm.AddChild(app.CreateTextEdit("Name", 0.4, 0.1));
  addForm.AddChild(app.CreateSpinner(["Source1", "Source2"], 0.4, 0.1));
  addForm.AddChild(app.CreateButton("Save", 0.1, 0.1));
  app.content.AddChild(addForm);
  
  var leadsList = app.CreateList("", 0.9, 0.3);
  leadsList.AddItem("Lead #45 [Hot] [View]");
  leadsList.AddItem("Lead #46 [Cold] [View]");
  leadsList.SetOnTouch(LeadAction);
  app.content.AddChild(leadsList);
}

function LoadAppointmentTracker() {
  var apptList = app.CreateList("", 0.9, 0.3);
  apptList.AddItem("Jane Doe, 2 PM [View]");
  apptList.SetOnTouch(AppointmentAction);
  app.content.AddChild(apptList);
  
  var logForm = app.CreateLayout("linear", "Horizontal");
  logForm.AddChild(app.CreateSpinner(["Landed", "Pending", "Lost"], 0.4, 0.1));
  logForm.AddChild(app.CreateDatePicker(0.4, 0.1));
  logForm.AddChild(app.CreateButton("Save", 0.1, 0.1));
  app.content.AddChild(logForm);
}

function LoadFarming() {
  var mapView = app.CreateWeb("https://maps.google.com", 0.9, 0.4);
  app.content.AddChild(mapView);
  
  var campaignList = app.CreateList("", 0.9, 0.3);
  campaignList.AddItem("Modoc County [View]");
  app.content.AddChild(campaignList);
}

function LoadRevenue() {
  var revenueList = app.CreateList("", 0.9, 0.4);
  revenueList.AddItem("Commissions: $42,500 [Detail]");
  revenueList.AddItem("Referrals: $5,000 [Detail]");
  revenueList.AddItem("Net Profit: $35,000 [Detail]");
  app.content.AddChild(revenueList);
  app.content.AddChild(app.CreateButton("Export PDF", 0.3, 0.1, "ExportPDF"));
}

function LoadTransaction() {
  var stagesList = app.CreateList("", 0.9, 0.4);
  stagesList.AddItem("Coach [] [Next]");
  stagesList.AddItem("Transact [] [Edit]");
  stagesList.AddItem("Close [] [View]");
  app.content.AddChild(stagesList);
}

function LoadAnalyzeDB() {
  var timelineList = app.CreateList("", 0.9, 0.3);
  timelineList.AddItem("Email sent [Tap]");
  timelineList.AddItem("Offer made [Tap]");
  app.content.AddChild(timelineList);
  
  var insights = app.CreateText("Insights: Focus on 90210: 25% conversion", 0.9, 0.1);
  app.content.AddChild(insights);
}

function LoadPremiumTools() {
  var toolsList = app.CreateList("", 0.9, 0.4);
  toolsList.AddItem("AI Lead Scoring [$99] [Upgrade]");
  toolsList.AddItem("Tax Export [$49] [Upgrade]");
  app.content.AddChild(toolsList);
}

function LoadSettings() {
  var settingsList = app.CreateList("", 0.9, 0.4);
  settingsList.AddItem("Customize Theme [Edit]");
  settingsList.AddItem("Logout [Exit]");
  app.content.AddChild(settingsList);
}

function LoadWebsitePortal() {
  var portalList = app.CreateList("", 0.9, 0.4);
  portalList.AddItem("Landing Page [Design]");
  portalList.AddItem("Portal [Edit]");
  app.content.AddChild(portalList);
  app.content.AddChild(app.CreateButton("Preview", 0.3, 0.1, "PreviewSite"));
}

function LoadLetterGenerator() {
  var templateList = app.CreateList("", 0.9, 0.4);
  templateList.AddItem("Open House [Select]");
  templateList.AddItem("Farming [Select]");
  app.content.AddChild(templateList);
  
  var editor = app.CreateTextEdit("Dear [Name]", 0.9, 0.2);
  app.content.AddChild(editor);
  app.content.AddChild(app.CreateButton("Send", 0.3, 0.1, "SendLetter"));
}

function TaskAction(item) {
  if (item.includes("Did you land it?"))
    app.CreateDialog("Outcome", "Yes|No|Reschedule", "Ok", OnTaskOutcome);
}

function LeadAction(item) {
  app.ShowPopup("Viewing Lead " + item);
}

function AppointmentAction(item) {
  app.CreateDialog("Outcome", "Yes|No|Reschedule", "Ok", OnApptOutcome);
}

function ExportPDF() {
  app.SaveText("profit_loss.pdf", "P&L Data");
}

function PreviewSite() {
  app.ShowPopup("Previewing Website");
}

function SendLetter() {
  app.ShowPopup("Letter Sent");
}

function OnTaskOutcome(result) {
  app.ShowPopup("Task Outcome: " + result);
}

function OnApptOutcome(result) {
  app.ShowPopup("Appointment Outcome: " + result);
}

function CheckOffline() {
  app.offlineMode = !app.IsOnline();
  if (app.offlineMode) app.ShowPopup("Offline Mode Active");
}

app.SetOnOnline(CheckOffline);
app.SetOnOffline(CheckOffline);

OnStart();
