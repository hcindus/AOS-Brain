# ReggieStart POS - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Download Pre-built Package

1. Download the latest release from [Releases](https://github.com/agi-company/reggiestart-pos/releases)
2. Choose your platform:
   - **Linux**: `.AppImage` or `.deb`
   - **Windows**: `.exe`
   - **macOS**: `.dmg`

### Option 2: Build from Source

```bash
# Clone repository
git clone https://github.com/agi-company/reggiestart-pos.git
cd reggiestart-pos

# Install dependencies
npm install

# Run in development mode
npm start

# Build for production
npm run build
```

---

## 📋 First-Time Setup

### 1. Launch the Application

```bash
# Linux (AppImage)
./ReggieStart-POS-linux.AppImage

# Linux (installed)
reggiestart

# Windows
ReggieStart POS.exe

# macOS
Open from Applications folder
```

### 2. Initial Configuration

On first launch, the system will:
- ✅ Create local database (`~/.config/ReggieStart POS/`)
- ✅ Seed demo products (10 items)
- ✅ Set default tax rate (8.5%)

### 3. Customize Settings

Click **⚙️ Settings** in the status bar to customize:
- Store name
- Tax rate
- Receipt header/footer
- Currency symbol

---

## 💳 Making a Sale

### Step-by-Step Transaction

1. **Select Products**
   - Click product cards in the grid
   - Or type PLU code and press PLU button
   - Or use search bar to find products

2. **Adjust Quantities**
   - Click +/- buttons on cart items
   - Or select item and enter quantity on numpad

3. **Process Payment**
   - Click **Cash**, **Credit**, or **Debit**
   - For cash: enter amount received
   - System calculates change automatically

4. **Print Receipt**
   - Receipt prints automatically
   - Or click **Print Receipt** button

---

## 🧮 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+N` | New transaction |
| `Ctrl+R` | Daily report |
| `Ctrl+P` | Manage products |
| `Ctrl+,` | Settings |
| `Esc` | Cancel current operation |
| `Enter` | Confirm input |

---

## 📊 Reports

Access reports via **📊 Reports** button:

- **Daily Summary**: Today's sales totals
- **Transactions**: List of all transactions
- **Top Products**: Best-selling items

---

## 🛠️ Troubleshooting

### App Won't Launch

```bash
# Check logs
~/.config/ReggieStart POS/logs/main.log

# Reset database (WARNING: Deletes all data)
rm ~/.config/ReggieStart POS/reggiestart.db
```

### Database Issues

```bash
# Export data for backup
# (Available via Settings > Export Data)

# Import data
# (Available via Settings > Import Data)
```

### Receipt Not Printing

- Ensure printer is connected
- Check printer settings in OS
- Try printing to PDF first

---

## 📞 Support

- **GitHub Issues**: [github.com/agi-company/reggiestart-pos/issues](https://github.com/agi-company/reggiestart-pos/issues)
- **Email**: support@agi-company.ai
- **Documentation**: [docs.agi-company.ai/reggiestart](https://docs.agi-company.ai/reggiestart)

---

*Built with ❤️ by AGI Company*
