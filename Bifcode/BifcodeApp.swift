//
//  BifcodeApp.swift
//
//  Created on 17.12.2025.
//  Copyright © 2026 IGR Soft. All rights reserved.
//

import BifcodeFeature
import SwiftUI

@main
struct BifcodeApp: App {
    @Environment(\.openWindow) private var openWindow
    
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .windowStyle(.hiddenTitleBar)
        .defaultSize(width: 800, height: 600)
        .commands {
            CommandGroup(replacing: .appInfo) {
                Button("About Bifcode") {
                    openWindow(id: "about")
                }
            }
        }
        
        AboutView.window
    }
}
