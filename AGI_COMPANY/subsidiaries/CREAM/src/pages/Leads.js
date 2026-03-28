function Leads(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            // Title
            var titleText = app.CreateText("Leads Management", 0.9, 0.1, "Left");
            titleText.SetTextSize(22);
            titleText.SetTextColor("#1E3A8A");
            layout.AddChild(titleText);
            
            // Add Lead Form
            var formLabel = app.CreateText("Add New Lead:", 0.9, 0.06, "Left");
            formLabel.SetTextSize(14);
            layout.AddChild(formLabel);
            
            var formLay = app.CreateLayout("Linear", "Horizontal,FillXY");
            formLay.SetSize(0.9, 0.15);
            
            var nameInput = app.CreateTextEdit("Name", 0.35, 0.1);
            nameInput.SetHint("Lead Name");
            formLay.AddChild(nameInput);
            
            var sourceSpinner = app.CreateSpinner("Source|Website|Referral|Open House|Zillow|Agent", 0.3, 0.1);
            formLay.AddChild(sourceSpinner);
            
            var saveBtn = app.CreateButton("Save", 0.2, 0.1);
            formLay.AddChild(saveBtn);
            layout.AddChild(formLay);
            
            // Leads List
            var listLabel = app.CreateText("Your Leads:", 0.9, 0.06, "Left");
            listLabel.SetTextSize(14);
            layout.AddChild(listLabel);
            
            var leadsList = app.CreateList("", 0.9, 0.5);
            leadsList.AddItem("Lead #45 [Hot] [View]");
            leadsList.AddItem("Lead #46 [Cold] [View]");
            leadsList.AddItem("Lead #47 [Warm] [View]");
            leadsList.AddItem("Lead #48 [Hot] [View]");
            leadsList.SetOnTouch(function(item) {
                app.ShowPopup("Viewing: " + item);
            });
            layout.AddChild(leadsList);
            
            // Stats
            var statsLay = app.CreateLayout("Linear", "Horizontal,FillXY");
            statsLay.SetSize(0.9, 0.1);
            statsLay.AddChild(app.CreateText("Total: 4 | Hot: 2 | Warm: 1 | Cold: 1", 0.9, 0.08));
            layout.AddChild(statsLay);
            
            this.layContent.AddChild(layout);
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
