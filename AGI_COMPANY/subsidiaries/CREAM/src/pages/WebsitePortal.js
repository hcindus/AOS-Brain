function WebsitePortal(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            var titleText = app.CreateText("Website Portal", 0.9, 0.1, "Left");
            titleText.SetTextSize(22);
            titleText.SetTextColor("#1E3A8A");
            layout.AddChild(titleText);
            
            // Portal Options
            var portalLabel = app.CreateText("Your Websites:", 0.9, 0.06, "Left");
            layout.AddChild(portalLabel);
            
            var portalList = app.CreateList("", 0.9, 0.4);
            portalList.AddItem("Agent Landing Page [Design]");
            portalList.AddItem("Property Listings [Manage]");
            portalList.AddItem("Lead Capture Page [Edit]");
            portalList.AddItem("Blog/News [Create]");
            layout.AddChild(portalList);
            
            // Preview
            var previewBtn = app.CreateButton("Preview All", 0.4, 0.1);
            layout.AddChild(previewBtn);
            
            // Publish
            var publishBtn = app.CreateButton("Publish Changes", 0.4, 0.1);
            layout.AddChild(publishBtn);
            
            this.layContent.AddChild(layout);
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
