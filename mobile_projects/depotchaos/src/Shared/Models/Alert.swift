//
//  Alert.swift
//  DepotChaos
//
//  Copyright © 2026 Performance Supply Depot LLC. All rights reserved.
//

import Foundation

enum AlertSeverity: String, Codable, Comparable {
    case critical = "Critical"
    case warning = "Warning"
    case info = "Info"
    
    var priority: Int {
        switch self {
        case .critical: return 3
        case .warning: return 2
        case .info: return 1
        }
    }
    
    static func < (lhs: AlertSeverity, rhs: AlertSeverity) -> Bool {
        lhs.priority < rhs.priority
    }
}

struct InventoryAlert: Codable, Identifiable {
    let id: UUID
    let product: Product
    let severity: AlertSeverity
    let type: AlertType
    let message: String
    let triggeredAt: Date
    var acknowledgedAt: Date?
    var resolvedAt: Date?
    
    var isAcknowledged: Bool {
        acknowledgedAt != nil
    }
    
    var isResolved: Bool {
        resolvedAt != nil
    }
    
    var requiresAction: Bool {
        !isAcknowledged && !isResolved
    }
    
    enum AlertType: String, Codable {
        case stockLow = "Low Stock"
        case stockCritical = "Critical Stock"
        case stockout = "Stockout"
        case reorderPending = "Reorder Pending"
        case deliveryOverdue = "Delivery Overdue"
        case priceIncrease = "Price Increase"
        case qualityIssue = "Quality Issue"
        case demandSpike = "Demand Spike Detected"
    }
}

struct AlertCount: Codable {
    let critical: Int
    let warning: Int
    let info: Int
    
    var total: Int {
        critical + warning + info
    }
    
    var hasCritical: Bool {
        critical > 0
    }
}
