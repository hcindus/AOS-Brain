# CREAM File Structure (Modular)

## Directory Structure
```
/sdcard/MyApp/
├── Home.js
├── PlanBusiness.js
├── Leads.js
├── AppointmentTracker.js
├── Farming.js
├── Revenue.js
├── Transaction.js
├── AnalyzeDB.js
├── PremiumTools.js
├── Settings.js
├── WebsitePortal.js
├── LetterGenerator.js
├── Utils.js
└── CREAM.js (main file)
```

## Page Template

Each .js file defines a constructor function with Show, IsChanged, and IsVisible methods:

```javascript
// Example: Home.js
function Home(appPath, layContent) {
    this.appPath = appPath;
    this.layContent = layContent;
    this.isVisible = false;
    
    this.Show = function(show, title) {
        if (show) {
            // Create UI elements
            this.isVisible = true;
        } else {
            this.isVisible = false;
        }
    };
    
    this.IsChanged = function() { return false; };
    this.IsVisible = function() { return this.isVisible; };
}
```

## Utils.js Functions
```javascript
function isValidFileName(name) {
    return /^[a-zA-Z0-9-_]+$/.test(name);
}

function showError(message) {
    app.ShowPopup(message);
}
```

## Page Adaptations

| Page | Key Features |
|------|--------------|
| Home.js | Welcome, tasks, quick actions, metrics |
| PlanBusiness.js | Goal planner, coach tips |
| Leads.js | Add form, leads list |
| AppointmentTracker.js | Appointments list, log form |
| Farming.js | Map view (app.CreateWeb), campaigns |
| Revenue.js | Revenue list, export button |
| Transaction.js | Pipeline stages |
| AnalyzeDB.js | Timeline, insights, charts |
| PremiumTools.js | Upgrade options |
| Settings.js | Settings toggles |
| WebsitePortal.js | Templates, preview |
| LetterGenerator.js | Templates, text editor |

## Implementation Notes
- Error handling: Include try-catch blocks for UI creation
- Assets: Store images in /sdcard/MyApp/Img/
- Testing: Load main file in DroidScript, verify navigation

## Status
- ✅ Template structure documented
- 🔄 Page scripts to be created
