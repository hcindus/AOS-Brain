// CREAM Utility Functions

// Validate file names
function isValidFileName(name) {
    return /^[a-zA-Z0-9-_]+$/.test(name);
}

// Show error popup
function showError(message) {
    app.ShowPopup("Error: " + message);
}

// Format currency
function formatCurrency(amount) {
    return "$" + amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

// Get current date formatted
function getCurrentDate() {
    var d = new Date();
    return d.toLocaleDateString();
}

// Save data to local storage
function saveData(key, value) {
    app.WriteFile(appPath + "/data/" + key + ".txt", JSON.stringify(value));
}

// Load data from local storage
function loadData(key) {
    try {
        var data = app.ReadFile(appPath + "/data/" + key + ".txt");
        return JSON.parse(data);
    } catch (e) {
        return null;
    }
}

// Validate email
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Show toast message
function showToast(message) {
    app.ShowPopup(message);
}

// Get status color
function getStatusColor(status) {
    switch(status.toLowerCase()) {
        case "hot": return "#FF0000";
        case "warm": return "#FFA500";
        case "cold": return "#0000FF";
        case "landed": return "#00FF00";
        case "pending": return "#FFFF00";
        case "lost": return "#FF0000";
        default: return "#000000";
    }
}
