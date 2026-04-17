# DepotChaos

**Supply Chain Chaos Prevention for Performance Supply Depot LLC**

A cross-platform macOS/iOS application designed to prevent supply chain chaos through intelligent inventory tracking, automated reorder alerts, and real-time order management.

## Overview

DepotChaos is your command center for depot operations. It connects to your existing Performance Supply Depot infrastructure to provide:

- 📊 **Real-time Inventory Monitoring** - Track stock levels across all product categories
- 🔔 **Intelligent Alerts** - Get notified before stockouts occur
- 📦 **Order Management** - Process and track orders from receipt to fulfillment
- 📈 **Analytics Dashboard** - Visualize supply chain health and trends
- 🔄 **Automated Reordering** - Set thresholds and let the system manage restocking

## Platforms

- **macOS** (14.0+) - Native SwiftUI app with menu bar integration
- **iOS** (17.0+) - iPhone and iPad support with widget support
- **iPadOS** - Optimized for tablet workflows

## Installation

### macOS
Download the `.pkg` installer from the latest release or install via:
```bash
# Coming soon: Homebrew
brew install depotchaos
```

### iOS
Install from the App Store or via TestFlight for beta access.

## Features

### Chaos Prevention Engine
The core intelligence system that predicts potential disruptions:
- Predictive stockout alerts (7, 14, 30 day forecasts)
- Seasonal demand pattern recognition
- Lead time variance tracking
- Critical threshold breach notifications

### Inventory Command Center
- Live stock levels across 6 product categories
- Barcode scanning integration
- Location-based inventory tracking
- Multi-warehouse support

### Order Operations
- Unified order inbox
- Status tracking from PO to delivery
- Supplier communication hub
- Backorder management

### Analytics & Reporting
- Daily digest emails
- Weekly trend reports
- Monthly supply chain health score
- Custom report builder

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details.

## API Integration

DepotChaos connects to your existing PSDEPOT systems:
- REST API for inventory data
- WebSocket for real-time updates
- OAuth2 authentication
- End-to-end encryption

## Development

Built with:
- Swift 5.9+
- SwiftUI for UI
- Combine for reactive programming
- Core Data for local persistence
- CloudKit for sync (optional)

## License

© 2026 Performance Supply Depot LLC. All rights reserved.

## Support

- 📧 Email: support@performancesupplydepot.com
- 📱 Phone: 1-800-PSDEPOT

---

**Version:** 1.0.0  
**Build:** 20260415.1  
**Platform:** Universal (Apple Silicon & Intel)
