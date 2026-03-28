function PlanBusiness(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            var titleText = app.CreateText("Plan Your Business", 0.9, 0.1, "Left");
            titleText.SetTextSize(22);
            titleText.SetTextColor("#1E3A8A");
            layout.AddChild(titleText);
            
            // Goals
            var goalsLabel = app.CreateText("Quarterly Goals:", 0.9, 0.06, "Left");
            goalsLabel.SetTextSize(14);
            layout.AddChild(goalsLabel);
            
            var goalsList = app.CreateList("", 0.9, 0.3);
            goalsList.AddItem("Add 50 leads [67%]");
            goalsList.AddItem("Close 10 deals [75%]");
            goalsList.AddItem("Launch 3 campaigns [33%]");
            goalsList.AddItem("Generate $100K revenue [45%]");
            layout.AddChild(goalsList);
            
            // Coach's Corner
            var coachLabel = app.CreateText("Coach's Corner:", 0.9, 0.06, "Left");
            coachLabel.SetTextSize(14);
            coachLabel.SetTextColor("#FF6B00");
            layout.AddChild(coachLabel);
            
            var coachTip = app.CreateText("Focus on 94117 geo-farming - high conversion area!", 0.9, 0.1);
            coachTip.SetTextColor("#333333");
            layout.AddChild(coachTip);
            
            // Add Goal
            var addGoalBtn = app.CreateButton("Add New Goal", 0.4, 0.1);
            layout.AddChild(addGoalBtn);
            
            this.layContent.AddChild(layout);
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
