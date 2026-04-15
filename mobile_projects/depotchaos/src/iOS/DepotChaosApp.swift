//
//  DepotChaosApp.swift
//  DepotChaos (iOS)
//
//  Copyright © 2026 Performance Supply Depot LLC. All rights reserved.
//

import SwiftUI

@main
struct DepotChaosApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(InventoryViewModel())
        }
    }
}

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil) -> Bool {
        // Configure app appearance
        return true
    }
}
