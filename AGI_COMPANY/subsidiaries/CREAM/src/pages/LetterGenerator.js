function LetterGenerator(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            this.layContent.RemoveAllChildren();
            var layout = app.CreateLayout("Linear", "VCenter,FillXY");
            
            var titleText = app.CreateText("Letter Generator", 0.9, 0.1, "Left");
            titleText.SetTextSize(22);
            titleText.SetTextColor("#1E3A8A");
            layout.AddChild(titleText);
            
            // Templates
            var templateLabel = app.CreateText("Choose Template:", 0.9, 0.06, "Left");
            layout.AddChild(templateLabel);
            
            var templateList = app.CreateList("", 0.9, 0.3);
            templateList.AddItem("Open House [Select]");
            templateList.AddItem("Farming Letter [Select]");
            templateList.AddItem("Thank You [Select]");
            templateList.AddItem("Follow-Up [Select]");
            templateList.AddItem("Just Sold [Select]");
            layout.AddChild(templateList);
            
            // Editor
            var editorLabel = app.CreateText("Letter Content:", 0.9, 0.06, "Left");
            layout.AddChild(editorLabel);
            
            var editor = app.CreateTextEdit("Dear [Name],", 0.9, 0.25);
            editor.SetHint("Write your letter here...");
            layout.AddChild(editor);
            
            // Actions
            var btnLay = app.CreateLayout("Linear", "Horizontal,FillXY");
            btnLay.SetSize(0.9, 0.12);
            btnLay.AddChild(app.CreateButton("Preview", 0.3, 0.1));
            btnLay.AddChild(app.CreateButton("Save", 0.3, 0.1));
            btnLay.AddChild(app.CreateButton("Send", 0.3, 0.1));
            layout.AddChild(btnLay);
            
            this.layContent.AddChild(layout);
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
