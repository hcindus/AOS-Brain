//
//  InventoryViewModel.swift
//  DepotChaos
//
//  Copyright © 2026 Performance Supply Depot LLC. All rights reserved.
//

import Foundation
import Combine

@MainActor
class InventoryViewModel: ObservableObject {
    @Published var products: [Product] = []
    @Published var alerts: [InventoryAlert] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let api: PSDEPOTAPIProtocol
    private var cancellables = Set<AnyCancellable>()
    
    init(api: PSDEPOTAPIProtocol = PSDEPOTAPI()) {
        self.api = api
    }
    
    func loadInventory() async {
        isLoading = true
        errorMessage = nil
        
        do {
            async let productsTask = api.fetchProducts()
            async let alertsTask = api.fetchAlerts()
            
            self.products = try await productsTask
            self.alerts = try await alertsTask
        } catch {
            errorMessage = "Failed to load inventory: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
    
    func refresh() async {
        await loadInventory()
    }
    
    var criticalAlerts: [InventoryAlert] {
        alerts.filter { $0.severity == .critical && $0.requiresAction }
    }
    
    var warningAlerts: [InventoryAlert] {
        alerts.filter { $0.severity == .warning && $0.requiresAction }
    }
    
    var alertCount: AlertCount {
        AlertCount(
            critical: criticalAlerts.count,
            warning: warningAlerts.count,
            info: alerts.filter { $0.severity == .info && $0.requiresAction }.count
        )
    }
    
    func acknowledgeAlert(_ alert: InventoryAlert) async {
        do {
            try await api.acknowledgeAlert(alert.id)
            if let index = alerts.firstIndex(where: { $0.id == alert.id }) {
                alerts[index].acknowledgedAt = Date()
            }
        } catch {
            errorMessage = "Failed to acknowledge alert: \(error.localizedDescription)"
        }
    }
    
    var lowStockProducts: [Product] {
        products.filter { $0.stockStatus == .low || $0.stockStatus == .critical }
    }
    
    var outOfStockProducts: [Product] {
        products.filter { $0.stockStatus == .outOfStock }
    }
    
    func productsByCategory(_ category: Product.Category) -> [Product] {
        products.filter { $0.category == category }
    }
}
