function AnalyzeDB(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            var titleText = app.CreateText("Database Analysis", 0.9, 0.1, "Left");
            titleText.SetTextSize(22);
            titleText.SetTextColor("#1E3A8A");
            layout.AddChild(titleText);
            
            // Timeline
            var timeLabel = app.CreateText("Recent Activity:", 0.9, 0.06, "Left");
            timeLabel.SetTextSize(14);
            layout.AddChild(timeLabel);
            
            var timeline = app.CreateList("", 0.9, 0.3);
            timeline.AddItem("Email sent [Tap]");
            timeline.AddItem("Offer made [Tap]");
            timeline.AddItem("Follow-up call [Tap]");
            timeline.AddItem("Listing presentation [Tap]");
            layout.AddChild(timeline);
            
            // Insights
            var insightsLabel = app.CreateText("AI Insights:", 0.9, 0.06, "Left");
            insightsLabel.SetTextSize(14);
            insightsLabel.SetTextColor("#FF6B00");
            layout.AddChild(insightsLabel);
            
            var insights = app.CreateText("Focus on 90210: 25% conversion\nModoc County: High engagement\nBest time to call: 2-4 PM", 0.9, 0.2);
            insights.SetTextColor("#333333");
            layout.AddChild(insights);
            
            // Charts placeholder
            var chartLabel = app.CreateText("Performance Charts:", 0.9, 0.06, "Left");
            chartLabel.SetTextSize(14);
            layout.AddChild(chartLabel);
            
            var chart = app.CreateText("[Charts would render here]", 0.9, 0.15);
            layout.AddChild(chart);
            
            this.layContent.AddChild(layout);
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
