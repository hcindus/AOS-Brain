function Transaction(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            var titleText = app.CreateText("Transaction Pipeline", 0.9, 0.1, "Left");
            titleText.SetTextSize(22);
            titleText.SetTextColor("#1E3A8A");
            layout.AddChild(titleText);
            
            // Pipeline Stages
            var stagesLabel = app.CreateText("Active Transactions:", 0.9, 0.06, "Left");
            stagesLabel.SetTextSize(14);
            layout.AddChild(stagesLabel);
            
            var pipeline = app.CreateList("", 0.9, 0.5);
            pipeline.AddItem("Coach [In Progress]");
            pipeline.AddItem("Pre-Approval [Done]");
            pipeline.AddItem("Showing [In Progress]");
            pipeline.AddItem("Offer Submitted [Pending]");
            pipeline.AddItem("Under Contract [Active]");
            pipeline.AddItem("Closing [Scheduled]");
            pipeline.SetOnTouch(function(item) {
                app.ShowPopup("Transaction: " + item);
            });
            layout.AddChild(pipeline);
            
            // Stats
            var statsText = app.CreateText("Active: 6 | This Month: 2 | Closed: 15", 0.9, 0.08);
            layout.AddChild(statsText);
            
            this.layContent.AddChild(layout);
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
