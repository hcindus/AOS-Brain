//
//  PSDEPOTAPI.swift
//  DepotChaos
//
//  Copyright © 2026 Performance Supply Depot LLC. All rights reserved.
//

import Foundation
import Combine

protocol PSDEPOTAPIProtocol {
    func authenticate(credentials: Credentials) async throws -> AuthToken
    func fetchProducts() async throws -> [Product]
    func fetchInventory() async throws -> [StockLevel]
    func fetchAlerts() async throws -> [InventoryAlert]
    func placeOrder(_ order: OrderRequest) async throws -> OrderConfirmation
    func acknowledgeAlert(_ alertId: UUID) async throws
    func subscribeToUpdates() -> AsyncStream<InventoryUpdate>
}

struct Credentials: Codable {
    let email: String
    let password: String
    let apiKey: String?
}

struct AuthToken: Codable {
    let token: String
    let expiresAt: Date
    let refreshToken: String
}

struct StockLevel: Codable {
    let productId: UUID
    let quantity: Int
    let lastUpdated: Date
    let warehouseLocation: String?
}

struct OrderRequest: Codable {
    let productId: UUID
    let quantity: Int
    let priority: OrderPriority
    let notes: String?
    
    enum OrderPriority: String, Codable {
        case normal, urgent, critical
    }
}

struct OrderConfirmation: Codable {
    let orderId: UUID
    let status: OrderStatus
    let estimatedDelivery: Date
    let confirmationNumber: String
}

enum InventoryUpdate: Codable {
    case stockChanged(productId: UUID, newQuantity: Int)
    case alertGenerated(alert: InventoryAlert)
    case alertResolved(alertId: UUID)
    case orderStatusChanged(orderId: UUID, status: OrderStatus)
    case priceChanged(productId: UUID, newPrice: Decimal)
}

class PSDEPOTAPI: PSDEPOTAPIProtocol {
    private let baseURL: URL
    private var authToken: AuthToken?
    private let session: URLSession
    
    private var updateContinuation: AsyncStream<InventoryUpdate>.Continuation?
    private var webSocketTask: URLSessionWebSocketTask?
    
    init(baseURL: URL = URL(string: "https://api.psdepot.com/v1")!) {
        self.baseURL = baseURL
        self.session = URLSession(configuration: .default)
    }
    
    func authenticate(credentials: Credentials) async throws -> AuthToken {
        // Placeholder - would connect to actual PSDEPOT auth
        return AuthToken(
            token: "mock_token_\(UUID().uuidString)",
            expiresAt: Date().addingTimeInterval(3600),
            refreshToken: "mock_refresh_\(UUID().uuidString)"
        )
    }
    
    func fetchProducts() async throws -> [Product] {
        // Return mock data for now
        return MockData.products
    }
    
    func fetchInventory() async throws -> [StockLevel] {
        return MockData.stockLevels
    }
    
    func fetchAlerts() async throws -> [InventoryAlert] {
        return MockData.alerts
    }
    
    func placeOrder(_ order: OrderRequest) async throws -> OrderConfirmation {
        return OrderConfirmation(
            orderId: UUID(),
            status: .pending,
            estimatedDelivery: Date().addingTimeInterval(7 * 24 * 3600),
            confirmationNumber: "PS-\(Int.random(in: 10000...99999))"
        )
    }
    
    func acknowledgeAlert(_ alertId: UUID) async throws {
        // Would POST to /alerts/{id}/acknowledge
    }
    
    func subscribeToUpdates() -> AsyncStream<InventoryUpdate> {
        AsyncStream { continuation in
            self.updateContinuation = continuation
            
            // In production, would connect WebSocket here
            // For now, just return empty stream
            
            continuation.onTermination = { [weak self] _ in
                self?.webSocketTask?.cancel()
            }
        }
    }
}

// MARK: - Mock Data

enum MockData {
    static let products: [Product] = [
        Product(
            id: UUID(),
            sku: "PAP-001",
            name: "Thermal Paper Rolls - 2.25\"",
            category: .paperProducts,
            currentStock: 150,
            minThreshold: 50,
            reorderPoint: 100,
            leadTimeDays: 3,
            supplier: suppliers[0],
            unitPrice: 39.00,
            lastRestocked: Date().addingTimeInterval(-3 * 24 * 3600)
        ),
        Product(
            id: UUID(),
            sku: "RIB-001",
            name: "ERC-38 Ink Ribbon - Black",
            category: .inkRibbons,
            currentStock: 25,
            minThreshold: 30,
            reorderPoint: 50,
            leadTimeDays: 5,
            supplier: suppliers[1],
            unitPrice: 42.00,
            lastRestocked: Date().addingTimeInterval(-7 * 24 * 3600)
        ),
        Product(
            id: UUID(),
            sku: "POS-001",
            name: "Samsung Kiosk Terminal",
            category: .posSystems,
            currentStock: 8,
            minThreshold: 5,
            reorderPoint: 10,
            leadTimeDays: 14,
            supplier: suppliers[2],
            unitPrice: 1295.00,
            lastRestocked: Date().addingTimeInterval(-30 * 24 * 3600)
        ),
        Product(
            id: UUID(),
            sku: "SCL-001",
            name: "Hobart Quantum Scale",
            category: .scales,
            currentStock: 3,
            minThreshold: 2,
            reorderPoint: 5,
            leadTimeDays: 21,
            supplier: suppliers[3],
            unitPrice: 2995.00,
            lastRestocked: nil
        ),
        Product(
            id: UUID(),
            sku: "CLN-001",
            name: "POS Terminal Cleaner",
            category: .cleaning,
            currentStock: 0,
            minThreshold: 10,
            reorderPoint: 25,
            leadTimeDays: 2,
            supplier: suppliers[4],
            unitPrice: 15.99,
            lastRestocked: Date().addingTimeInterval(-14 * 24 * 3600)
        )
    ]
    
    static let suppliers: [Supplier] = [
        Supplier(id: UUID(), name: "Paper Corp", contactEmail: "sales@papercorp.com", contactPhone: "555-0101", leadTimeDays: 3),
        Supplier(id: UUID(), name: "Ribbons R Us", contactEmail: "orders@ribbonsrus.com", contactPhone: "555-0102", leadTimeDays: 5),
        Supplier(id: UUID(), name: "Samsung B2B", contactEmail: "b2b@samsung.com", contactPhone: "555-0103", leadTimeDays: 14),
        Supplier(id: UUID(), name: "Hobart Commercial", contactEmail: "sales@hobart.com", contactPhone: "555-0104", leadTimeDays: 21),
        Supplier(id: UUID(), name: "Clean Solutions", contactEmail: "orders@cleansolutions.com", contactPhone: "555-0105", leadTimeDays: 2)
    ]
    
    static let stockLevels: [StockLevel] = products.map {
        StockLevel(
            productId: $0.id,
            quantity: $0.currentStock,
            lastUpdated: Date(),
            warehouseLocation: "WH-A-01"
        )
    }
    
    static let alerts: [InventoryAlert] = [
        InventoryAlert(
            id: UUID(),
            product: products[1], // Ribbons - low stock
            severity: .warning,
            type: .stockLow,
            message: "ERC-38 Ink Ribbon stock is below reorder point (25 < 50)",
            triggeredAt: Date().addingTimeInterval(-3600),
            acknowledgedAt: nil,
            resolvedAt: nil
        ),
        InventoryAlert(
            id: UUID(),
            product: products[4], // Cleaner - out of stock
            severity: .critical,
            type: .stockout,
            message: "POS Terminal Cleaner is completely out of stock",
            triggeredAt: Date().addingTimeInterval(-7200),
            acknowledgedAt: nil,
            resolvedAt: nil
        )
    ]
}
