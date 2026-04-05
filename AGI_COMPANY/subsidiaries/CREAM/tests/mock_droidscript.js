// Mock DroidScript API for testing
const app = {
    // Layout
    CreateLayout: (type) => new MockLayout(type),
    AddLayout: (layout) => console.log('Layout added'),
    
    // Controls
    CreateText: (text, w, h, align) => new MockText(text),
    CreateButton: (text, w, h) => new MockButton(text),
    CreateList: (items, w, h) => new MockList(),
    CreateTextEdit: (hint, w, h) => new MockTextEdit(hint),
    CreateSpinner: (items, w, h) => new MockSpinner(items),
    CreateImage: (path, w, h) => new MockImage(path),
    CreateWeb: (url, w, h) => new MockWeb(url),
    CreateDatePicker: (w, h) => new MockDatePicker(),
    CreateDialog: (title, items, buttons, callback) => {
        console.log(`Dialog: ${title}`);
        if (callback) callback('OK');
    },
    CreateYesNoDialog: (title, callback) => {
        console.log(`YesNoDialog: ${title}`);
        if (callback) callback('Yes');
    },
    
    // System
    ShowPopup: (msg) => console.log(`[POPUP] ${msg}`),
    CreateLayout: (type) => new MockLayout(type),
    SetOrientation: (orient) => console.log(`Orientation: ${orient}`),
    SetTheme: (theme) => console.log(`Theme: ${theme}`),
    MakeFolder: (path) => { console.log(`MakeFolder: ${path}`); return true; },
    AddDrawer: (layout, side, width) => console.log(`Drawer added`),
    Script: (path) => { console.log(`Loading script: ${path}`); return true; },
    
    // File operations
    WriteFile: (path, content) => { console.log(`WriteFile: ${path}`); return true; },
    ReadFile: (path) => { console.log(`ReadFile: ${path}`); return '{}'; },
    
    // Events
    SetOnOnline: (fn) => {},
    SetOnOffline: (fn) => {},
    
    // Data
    data: {}
};

class MockLayout {
    constructor(type) {
        this.type = type;
        this.children = [];
    }
    SetBackColor(color) { console.log(`Layout bg: ${color}`); }
    SetSize(w, h) { console.log(`Layout size: ${w}x${h}`); }
    AddChild(child) { this.children.push(child); }
    RemoveAllChildren() { this.children = []; }
}

class MockText {
    constructor(text) {
        this.text = text;
    }
    SetTextSize(size) { this.size = size; }
    SetTextColor(color) { this.color = color; }
    SetPadding(a,b,c,d) {}
}

class MockButton {
    constructor(text) {
        this.text = text;
    }
    SetOnTouch(fn) { this.onClick = fn; }
}

class MockList {
    constructor() {
        this.items = [];
    }
    AddItem(item) { this.items.push(item); }
    SetOnTouch(fn) { this.onTouch = fn; }
}

class MockTextEdit {
    constructor(hint) {
        this.hint = hint;
    }
    SetHint(h) {}
}

class MockSpinner {
    constructor(items) {
        this.items = items.split('|');
    }
}

class MockImage {
    constructor(path) {
        this.path = path;
    }
    SetOnTouch(fn) {}
}

class MockWeb {
    constructor(url) {
        this.url = url;
    }
}

class MockDatePicker {
    constructor() {}
}

module.exports = app;
