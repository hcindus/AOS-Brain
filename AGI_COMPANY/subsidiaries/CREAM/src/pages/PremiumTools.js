function PremiumTools(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            var titleText = app.CreateText("Premium Tools", 0.9, 0.1, "Left");
            titleText.SetTextSize(22);
            titleText.SetTextColor("#1E3A8A");
            layout.AddChild(titleText);
            
            var descText = app.CreateText("Unlock advanced features:", 0.9, 0.06, "Left");
            layout.AddChild(descText);
            
            // Tools List
            var toolsList = app.CreateList("", 0.9, 0.45);
            toolsList.AddItem("AI Lead Scoring [$99] [Upgrade]");
            toolsList.AddItem("Tax Export Pro [$49] [Upgrade]");
            toolsList.AddItem("Voice-to-Text Letters [$29] [Upgrade]");
            toolsList.AddItem("Advanced Analytics [$79] [Upgrade]");
            toolsList.AddItem("Custom Branding [$39] [Upgrade]");
            toolsList.SetOnTouch(function(item) {
                app.ShowPopup("Upgrade: " + item);
            });
            layout.AddChild(toolsList);
            
            // Current Plan
            var planText = app.CreateText("Current Plan: Free Tier", 0.9, 0.08);
            planText.SetTextColor("#666666");
            layout.AddChild(planText);
            
            this.layContent.AddChild(layout);
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
