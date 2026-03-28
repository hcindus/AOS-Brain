function Farming(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            var titleText = app.CreateText("Community Farming", 0.9, 0.1, "Left");
            titleText.SetTextSize(22);
            titleText.SetTextColor("#1E3A8A");
            layout.AddChild(titleText);
            
            // Map View
            var mapLabel = app.CreateText("Farming Zones:", 0.9, 0.06, "Left");
            mapLabel.SetTextSize(14);
            layout.AddChild(mapLabel);
            
            var mapView = app.CreateWeb("https://maps.google.com", 0.9, 0.4);
            layout.AddChild(mapView);
            
            // Campaigns
            var campLabel = app.CreateText("Active Campaigns:", 0.9, 0.06, "Left");
            campLabel.SetTextSize(14);
            layout.AddChild(campLabel);
            
            var campaignList = app.CreateList("", 0.9, 0.35);
            campaignList.AddItem("Modoc County [View]");
            campaignList.AddItem("94117 Geo-Farm [View]");
            campaignList.AddItem("90210 Beverly Hills [View]");
            campaignList.SetOnTouch(function(item) {
                app.ShowPopup("Opening: " + item);
            });
            layout.AddChild(campaignList);
            
            this.layContent.AddChild(layout);
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
