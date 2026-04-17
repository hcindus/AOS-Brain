//
//  Product.swift
//  DepotChaos
//
//  Copyright © 2026 Performance Supply Depot LLC. All rights reserved.
//

import Foundation

struct Product: Codable, Identifiable, Hashable {
    let id: UUID
    let sku: String
    let name: String
    let category: Category
    let currentStock: Int
    let minThreshold: Int
    let reorderPoint: Int
    let leadTimeDays: Int
    let supplier: Supplier
    let unitPrice: Decimal
    let lastRestocked: Date?
    
    enum Category: String, Codable, CaseIterable {
        case paperProducts = "Paper Products"
        case inkRibbons = "Ink Ribbons"
        case posSystems = "Samsung POS Systems"
        case scales = "Scales"
        case accessories = "Accessories"
        case cleaning = "Cleaning Supplies"
        
        var icon: String {
            switch self {
            case .paperProducts: return "doc.text"
            case .inkRibbons: return "printer"
            case .posSystems: return "desktopcomputer"
            case .scales: return "scalemass"
            case .accessories: return "cube.box"
            case .cleaning: return "sparkles"
            }
        }
    }
    
    var stockStatus: StockStatus {
        if currentStock == 0 {
            return .outOfStock
        } else if currentStock <= minThreshold {
            return .critical
        } else if currentStock <= reorderPoint {
            return .low
        } else {
            return .healthy
        }
    }
    
    var daysUntilStockout: Int? {
        guard currentStock > 0 else { return 0 }
        // Simplified calculation - would use historical data in production
        let dailyUsage = 1 // Placeholder
        return currentStock / dailyUsage
    }
}

enum StockStatus: String, Codable {
    case healthy = "Healthy"
    case low = "Low"
    case critical = "Critical"
    case outOfStock = "Out of Stock"
    
    var color: String {
        switch self {
        case .healthy: return "green"
        case .low: return "yellow"
        case .critical: return "orange"
        case .outOfStock: return "red"
        }
    }
}

struct Supplier: Codable, Identifiable, Hashable {
    let id: UUID
    let name: String
    let contactEmail: String
    let contactPhone: String
    let leadTimeDays: Int
}
