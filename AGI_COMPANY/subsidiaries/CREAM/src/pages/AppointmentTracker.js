function AppointmentTracker(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            // Title
            var titleText = app.CreateText("Appointment Tracker", 0.9, 0.1, "Left");
            titleText.SetTextSize(22);
            titleText.SetTextColor("#1E3A8A");
            layout.AddChild(titleText);
            
            // Upcoming Appointments
            var apptLabel = app.CreateText("Upcoming Appointments:", 0.9, 0.06, "Left");
            apptLabel.SetTextSize(14);
            layout.AddChild(apptLabel);
            
            var apptList = app.CreateList("", 0.9, 0.35);
            apptList.AddItem("Jane Doe - 2:00 PM [View]");
            apptList.AddItem("John Smith - 4:30 PM [View]");
            apptList.AddItem("Open House - 10:00 AM [View]");
            apptList.SetOnTouch(function(item) {
                app.CreateYesNoDialog("Did you land it?", function(ret) {
                    app.ShowPopup("Appointment " + ret);
                });
            });
            layout.AddChild(apptList);
            
            // Log Outcome
            var logLabel = app.CreateText("Log Outcome:", 0.9, 0.06, "Left");
            logLabel.SetTextSize(14);
            layout.AddChild(logLabel);
            
            var logLay = app.CreateLayout("Linear", "Horizontal,FillXY");
            logLay.SetSize(0.9, 0.15);
            
            var outcomeSpinner = app.CreateSpinner("Landed|Pending|Lost|No Show", 0.4, 0.1);
            logLay.AddChild(outcomeSpinner);
            
            var datePicker = app.CreateDatePicker(0.3, 0.1);
            logLay.AddChild(datePicker);
            
            var logBtn = app.CreateButton("Save", 0.2, 0.1);
            logLay.AddChild(logBtn);
            layout.AddChild(logLay);
            
            // Stats
            var statsText = app.CreateText("This Week: 5 appts | Landed: 3 | Pending: 1 | Lost: 1", 0.9, 0.08);
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
