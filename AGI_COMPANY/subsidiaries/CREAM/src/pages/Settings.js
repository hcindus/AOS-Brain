function Settings(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            var titleText = app.CreateText("Settings", 0.9, 0.1, "Left");
            titleText.SetTextSize(22);
            titleText.SetTextColor("#1E3A8A");
            layout.AddChild(titleText);
            
            // Settings List
            var settingsList = app.CreateList("", 0.9, 0.5);
            settingsList.AddItem("Customize Theme [Edit]");
            settingsList.AddItem("Notification Preferences [Edit]");
            settingsList.AddItem("Data Backup [Setup]");
            settingsList.AddItem("Sync Account [Connect]");
            settingsList.AddItem("Privacy Options [Edit]");
            settingsList.AddItem("About CREAM [View]");
            settingsList.SetOnTouch(function(item) {
                app.ShowPopup("Settings: " + item);
            });
            layout.AddChild(settingsList);
            
            // Logout
            var logoutBtn = app.CreateButton("Logout", 0.4, 0.1);
            layout.AddChild(logoutBtn);
            
            this.layContent.AddChild(layout);
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
