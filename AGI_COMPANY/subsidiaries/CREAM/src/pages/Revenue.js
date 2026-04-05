function Revenue(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            var titleText = app.CreateText("Revenue & Profit", 0.9, 0.1, "Left");
            titleText.SetTextSize(22);
            titleText.SetTextColor("#1E3A8A");
            layout.AddChild(titleText);
            
            // Revenue List
            var revLabel = app.CreateText("Income Sources:", 0.9, 0.06, "Left");
            revLabel.SetTextSize(14);
            layout.AddChild(revLabel);
            
            var revenueList = app.CreateList("", 0.9, 0.35);
            revenueList.AddItem("Commissions: $42,500 [Detail]");
            revenueList.AddItem("Referrals: $5,000 [Detail]");
            revenueList.AddItem("Rental Income: $1,200 [Detail]");
            revenueList.AddItem("Other: $800 [Detail]");
            layout.AddChild(revenueList);
            
            // Summary
            var summaryLay = app.CreateLayout("Linear", "Vertical,FillXY");
            summaryLay.SetSize(0.9, 0.25);
            summaryLay.AddChild(app.CreateText("Gross Revenue: $49,500", 0.9, 0.08));
            summaryLay.AddChild(app.CreateText("Expenses: $14,500", 0.9, 0.08));
            summaryLay.AddChild(app.CreateText("Net Profit: $35,000", 0.9, 0.08));
            summaryLay.AddChild(app.CreateText("Q3 2025", 0.9, 0.08));
            layout.AddChild(summaryLay);
            
            // Export Button
            var exportBtn = app.CreateButton("Export PDF", 0.4, 0.1);
            layout.AddChild(exportBtn);
            
            this.layContent.AddChild(layout);
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
