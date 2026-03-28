function Home(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            // Welcome
            var welcome = app.CreateText("Welcome, Agent A!", 0.9, 0.1, "Left");
            welcome.SetTextSize(22);
            welcome.SetTextColor("#1E3A8A");
            layout.AddChild(welcome);
            
            // Tasks
            var tasksLabel = app.CreateText("Today's Tasks:", 0.9, 0.08, "Left");
            tasksLabel.SetTextSize(16);
            tasksLabel.SetTextColor("#333333");
            layout.AddChild(tasksLabel);
            
            var tasks = app.CreateList("", 0.9, 0.25);
            tasks.AddItem("Follow up with 3 leads [View]");
            tasks.AddItem("Send farming letter [Generate]");
            tasks.SetOnTouch(function(item) {
                if (item.includes("Did you land it?")) {
                    app.CreateYesNoDialog("Did you land it?", function(ret) {
                        app.ShowPopup("Outcome: " + ret);
                    });
                }
            });
            layout.AddChild(tasks);
            
            // Quick Actions
            var actionsLabel = app.CreateText("Quick Actions:", 0.9, 0.08, "Left");
            actionsLabel.SetTextSize(16);
            actionsLabel.SetTextColor("#333333");
            layout.AddChild(actionsLabel);
            
            var btnLay = app.CreateLayout("Linear", "Horizontal,FillXY");
            btnLay.SetSize(0.9, 0.12);
            btnLay.AddChild(app.CreateButton("Add Lead", 0.22, 0.1));
            btnLay.AddChild(app.CreateButton("Gen Letter", 0.22, 0.1));
            btnLay.AddChild(app.CreateButton("Revenue", 0.22, 0.1));
            btnLay.AddChild(app.CreateButton("Schedule", 0.22, 0.1));
            layout.AddChild(btnLay);
            
            // Metrics
            var metricsLabel = app.CreateText("Key Metrics:", 0.9, 0.08, "Left");
            metricsLabel.SetTextSize(16);
            metricsLabel.SetTextColor("#333333");
            layout.AddChild(metricsLabel);
            
            var metrics = app.CreateLayout("Linear", "Vertical,FillXY");
            metrics.SetSize(0.9, 0.3);
            metrics.AddChild(app.CreateText("Leads Added: 50", 0.9, 0.08));
            metrics.AddChild(app.CreateText("Appts: 5", 0.9, 0.08));
            metrics.AddChild(app.CreateText("Conversion: 18%", 0.9, 0.08));
            metrics.AddChild(app.CreateText("Q3 Revenue: $42,500", 0.9, 0.08));
            layout.AddChild(metrics);
            
            this.layContent.AddChild(layout);
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
