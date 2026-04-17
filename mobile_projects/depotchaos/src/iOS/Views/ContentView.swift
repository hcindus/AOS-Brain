//
//  ContentView.swift
//  DepotChaos (iOS)
//
//  Copyright © 2026 Performance Supply Depot LLC. All rights reserved.
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var viewModel: InventoryViewModel
    
    var body: some View {
        TabView {
            DashboardView()
                .tabItem {
                    Label("Dashboard", systemImage: "gauge.with.dots.needle.67percent")
                }
            
            InventoryListView()
                .tabItem {
                    Label("Inventory", systemImage: "cube.box.fill")
                }
            
            AlertsView()
                .tabItem {
                    Label("Alerts", systemImage: "bell.fill")
                }
                .badge(viewModel.alertCount.total)
            
            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
        }
        .task {
            await viewModel.loadInventory()
        }
    }
}

// MARK: - Dashboard View
struct DashboardView: View {
    @EnvironmentObject var viewModel: InventoryViewModel
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Status Card
                    StatusCardView()
                    
                    // Critical Alerts
                    if !viewModel.criticalAlerts.isEmpty {
                        CriticalAlertsSection()
                    }
                    
                    // Quick Actions
                    QuickActionsView()
                    
                    // Inventory Summary
                    InventorySummaryView()
                }
                .padding()
            }
            .navigationTitle("DepotChaos")
            .refreshable {
                await viewModel.refresh()
            }
        }
    }
}

struct StatusCardView: View {
    @EnvironmentObject var viewModel: InventoryViewModel
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: "shield.checkered")
                    .font(.largeTitle)
                    .foregroundColor(statusColor)
                
                VStack(alignment: .leading) {
                    Text("Supply Chain Status")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Text(statusText)
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(statusColor)
                }
                
                Spacer()
            }
            
            if viewModel.alertCount.hasCritical {
                Text("\(viewModel.criticalAlerts.count) critical issues require immediate attention")
                    .font(.subheadline)
                    .foregroundColor(.red)
            } else if viewModel.alertCount.total > 0 {
                Text("\(viewModel.alertCount.total) items need attention")
                    .font(.subheadline)
                    .foregroundColor(.orange)
            } else {
                Text("All systems nominal")
                    .font(.subheadline)
                    .foregroundColor(.green)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(radius: 2)
    }
    
    var statusText: String {
        if viewModel.alertCount.hasCritical {
            return "CRITICAL"
        } else if viewModel.alertCount.total > 0 {
            return "WARNING"
        } else {
            return "HEALTHY"
        }
    }
    
    var statusColor: Color {
        if viewModel.alertCount.hasCritical {
            return .red
        } else if viewModel.alertCount.total > 0 {
            return .orange
        } else {
            return .green
        }
    }
}

struct CriticalAlertsSection: View {
    @EnvironmentObject var viewModel: InventoryViewModel
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Critical Alerts")
                .font(.headline)
            
            ForEach(viewModel.criticalAlerts.prefix(3)) { alert in
                AlertRowView(alert: alert)
            }
        }
    }
}

struct AlertRowView: View {
    let alert: InventoryAlert
    
    var body: some View {
        HStack {
            Image(systemName: iconName)
                .foregroundColor(severityColor)
            
            VStack(alignment: .leading) {
                Text(alert.product.name)
                    .font(.subheadline)
                    .fontWeight(.semibold)
                Text(alert.message)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }
            
            Spacer()
            
            Text(alert.severity.rawValue)
                .font(.caption2)
                .fontWeight(.bold)
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(severityColor.opacity(0.2))
                .foregroundColor(severityColor)
                .cornerRadius(4)
        }
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(8)
    }
    
    var iconName: String {
        switch alert.type {
        case .stockLow: return "exclamationmark.triangle"
        case .stockCritical: return "exclamationmark.triangle.fill"
        case .stockout: return "xmark.circle.fill"
        case .reorderPending: return "clock"
        case .deliveryOverdue: return "truck.box.badge.clock"
        case .priceIncrease: return "arrow.up.circle"
        case .qualityIssue: return "exclamationmark.shield"
        case .demandSpike: return "chart.line.uptrend.xyaxis"
        }
    }
    
    var severityColor: Color {
        switch alert.severity {
        case .critical: return .red
        case .warning: return .orange
        case .info: return .blue
        }
    }
}

struct QuickActionsView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Quick Actions")
                .font(.headline)
            
            HStack(spacing: 16) {
                QuickActionButton(icon: "plus.circle.fill", title: "New Order", color: .blue)
                QuickActionButton(icon: "barcode.viewfinder", title: "Scan", color: .green)
                QuickActionButton(icon: "arrow.clockwise", title: "Sync", color: .purple)
                QuickActionButton(icon: "doc.text", title: "Report", color: .orange)
            }
        }
    }
}

struct QuickActionButton: View {
    let icon: String
    let title: String
    let color: Color
    
    var body: some View {
        Button(action: {}) {
            VStack {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                Text(title)
                    .font(.caption)
                    .foregroundColor(.primary)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 16)
            .background(Color(.secondarySystemBackground))
            .cornerRadius(8)
        }
    }
}

struct InventorySummaryView: View {
    @EnvironmentObject var viewModel: InventoryViewModel
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Inventory Summary")
                .font(.headline)
            
            HStack(spacing: 16) {
                SummaryCard(
                    title: "Total Items",
                    value: "\(viewModel.products.count)",
                    icon: "cube.box.fill",
                    color: .blue
                )
                
                SummaryCard(
                    title: "Low Stock",
                    value: "\(viewModel.lowStockProducts.count)",
                    icon: "exclamationmark.triangle.fill",
                    color: .orange
                )
                
                SummaryCard(
                    title: "Out of Stock",
                    value: "\(viewModel.outOfStockProducts.count)",
                    icon: "xmark.circle.fill",
                    color: .red
                )
            }
        }
    }
}

struct SummaryCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)
            
            Text(value)
                .font(.title)
                .fontWeight(.bold)
            
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(8)
    }
}

// MARK: - Inventory List View
struct InventoryListView: View {
    @EnvironmentObject var viewModel: InventoryViewModel
    @State private var selectedCategory: Product.Category?
    @State private var searchText = ""
    
    var filteredProducts: [Product] {
        var products = viewModel.products
        
        if let category = selectedCategory {
            products = products.filter { $0.category == category }
        }
        
        if !searchText.isEmpty {
            products = products.filter {
                $0.name.localizedCaseInsensitiveContains(searchText) ||
                $0.sku.localizedCaseInsensitiveContains(searchText)
            }
        }
        
        return products
    }
    
    var body: some View {
        NavigationView {
            List {
                // Category Filter
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 12) {
                        CategoryFilterButton(title: "All", isSelected: selectedCategory == nil) {
                            selectedCategory = nil
                        }
                        
                        ForEach(Product.Category.allCases, id: \.self) { category in
                            CategoryFilterButton(
                                title: category.rawValue,
                                isSelected: selectedCategory == category
                            ) {
                                selectedCategory = category
                            }
                        }
                    }
                    .padding(.horizontal)
                }
                .listRowInsets(EdgeInsets())
                .listRowSeparator(.hidden)
                .padding(.vertical, 8)
                
                // Product List
                ForEach(filteredProducts) { product in
                    ProductRowView(product: product)
                }
            }
            .listStyle(.plain)
            .searchable(text: $searchText, prompt: "Search products...")
            .navigationTitle("Inventory")
        }
    }
}

struct CategoryFilterButton: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .fontWeight(isSelected ? .bold : .regular)
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(isSelected ? Color.blue : Color(.secondarySystemBackground))
                .foregroundColor(isSelected ? .white : .primary)
                .cornerRadius(20)
        }
    }
}

struct ProductRowView: View {
    let product: Product
    
    var body: some View {
        HStack(spacing: 12) {
            // Status Indicator
            Circle()
                .fill(statusColor)
                .frame(width: 12, height: 12)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(product.name)
                    .font(.subheadline)
                    .fontWeight(.semibold)
                
                HStack {
                    Text(product.sku)
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    Text("•")
                        .foregroundColor(.secondary)
                    
                    Text(product.category.rawValue)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            Spacer()
            
            VStack(alignment: .trailing) {
                Text("\(product.currentStock)")
                    .font(.headline)
                    .foregroundColor(stockTextColor)
                
                Text("in stock")
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
    
    var statusColor: Color {
        switch product.stockStatus {
        case .healthy: return .green
        case .low: return .yellow
        case .critical: return .orange
        case .outOfStock: return .red
        }
    }
    
    var stockTextColor: Color {
        switch product.stockStatus {
        case .healthy: return .primary
        case .low: return .orange
        case .critical: return .orange
        case .outOfStock: return .red
        }
    }
}

// MARK: - Alerts View
struct AlertsView: View {
    @EnvironmentObject var viewModel: InventoryViewModel
    
    var body: some View {
        NavigationView {
            List {
                if viewModel.alerts.isEmpty {
                    Section {
                        VStack(spacing: 16) {
                            Image(systemName: "checkmark.shield")
                                .font(.system(size: 60))
                                .foregroundColor(.green)
                            
                            Text("No Active Alerts")
                                .font(.headline)
                            
                            Text("Your supply chain is running smoothly")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 60)
                    }
                } else {
                    // Critical Section
                    if !viewModel.criticalAlerts.isEmpty {
                        Section(header: Text("Critical").foregroundColor(.red)) {
                            ForEach(viewModel.criticalAlerts) { alert in
                                AlertDetailRow(alert: alert)
                            }
                        }
                    }
                    
                    // Warnings Section
                    if !viewModel.warningAlerts.isEmpty {
                        Section(header: Text("Warnings").foregroundColor(.orange)) {
                            ForEach(viewModel.warningAlerts) { alert in
                                AlertDetailRow(alert: alert)
                            }
                        }
                    }
                }
            }
            .listStyle(.insetGrouped)
            .navigationTitle("Alerts")
            .refreshable {
                await viewModel.refresh()
            }
        }
    }
}

struct AlertDetailRow: View {
    let alert: InventoryAlert
    @EnvironmentObject var viewModel: InventoryViewModel
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: alertIcon)
                    .foregroundColor(alertColor)
                
                Text(alert.type.rawValue)
                    .font(.caption)
                    .fontWeight(.bold)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 2)
                    .background(alertColor.opacity(0.2))
                    .foregroundColor(alertColor)
                    .cornerRadius(4)
                
                Spacer()
                
                Text(relativeTime)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Text(alert.product.name)
                .font(.subheadline)
                .fontWeight(.semibold)
            
            Text(alert.message)
                .font(.caption)
                .foregroundColor(.secondary)
            
            if alert.requiresAction {
                HStack {
                    Button("Acknowledge") {
                        Task {
                            await viewModel.acknowledgeAlert(alert)
                        }
                    }
                    .buttonStyle(.bordered)
                    .controlSize(.small)
                    
                    Button("Create Order") {
                        // Create order action
                    }
                    .buttonStyle(.borderedProminent)
                    .controlSize(.small)
                }
                .padding(.top, 4)
            }
        }
        .padding(.vertical, 4)
    }
    
    var alertIcon: String {
        switch alert.type {
        case .stockLow: return "exclamationmark.triangle"
        case .stockCritical: return "exclamationmark.triangle.fill"
        case .stockout: return "xmark.circle.fill"
        case .reorderPending: return "clock"
        case .deliveryOverdue: return "truck.box.badge.clock"
        case .priceIncrease: return "arrow.up.circle"
        case .qualityIssue: return "exclamationmark.shield"
        case .demandSpike: return "chart.line.uptrend.xyaxis"
        }
    }
    
    var alertColor: Color {
        switch alert.severity {
        case .critical: return .red
        case .warning: return .orange
        case .info: return .blue
        }
    }
    
    var relativeTime: String {
        let formatter = RelativeDateTimeFormatter()
        return formatter.localizedString(for: alert.triggeredAt, relativeTo: Date())
    }
}

// MARK: - Settings View
struct SettingsView: View {
    var body: some View {
        NavigationView {
            List {
                Section(header: Text("Account")) {
                    HStack {
                        Image(systemName: "person.circle.fill")
                            .font(.largeTitle)
                            .foregroundColor(.blue)
                        
                        VStack(alignment: .leading) {
                            Text("Depot Manager")
                                .font(.headline)
                            Text("manager@psdepot.com")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                    .padding(.vertical, 4)
                }
                
                Section(header: Text("Notifications")) {
                    Toggle("Critical Alerts", isOn: .constant(true))
                    Toggle("Daily Summary", isOn: .constant(true))
                    Toggle("Order Updates", isOn: .constant(true))
                }
                
                Section(header: Text("Preferences")) {
                    NavigationLink("Warehouse Settings") {
                        Text("Warehouse Settings")
                    }
                    NavigationLink("Threshold Configuration") {
                        Text("Thresholds")
                    }
                    NavigationLink("Supplier Management") {
                        Text("Suppliers")
                    }
                }
                
                Section(header: Text("About")) {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0 (20260415)")
                            .foregroundColor(.secondary)
                    }
                    HStack {
                        Text("Build")
                        Spacer()
                        Text("Universal")
                            .foregroundColor(.secondary)
                    }
                }
                
                Section {
                    Button("Sign Out") {
                        // Sign out action
                    }
                    .foregroundColor(.red)
                }
            }
            .navigationTitle("Settings")
        }
    }
}

// MARK: - Preview
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .environmentObject(InventoryViewModel())
    }
}
