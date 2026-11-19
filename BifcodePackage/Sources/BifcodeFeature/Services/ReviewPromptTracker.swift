//
//  ReviewPromptTracker.swift
//
//  Created on 19.11.2026.
//  Copyright © 2026 Agnidia. All rights reserved.
//

import Foundation

/// Counts successful exports and signals once when the App Store rating prompt is due.
@MainActor
public struct ReviewPromptTracker {
    static let countKey = "successfulExportCount"
    static let requestedKey = "hasRequestedReview"

    private let defaults: UserDefaults
    private let threshold: Int

    public init(defaults: UserDefaults = .standard, threshold: Int = 5) {
        self.defaults = defaults
        self.threshold = threshold
    }

    /// Returns `true` exactly once, when the count first reaches the threshold.
    /// The flag is set before the dialog shows, so a suppressed dialog is never retried.
    public func recordSuccessfulExport() -> Bool {
        let count = defaults.integer(forKey: Self.countKey) + 1
        defaults.set(count, forKey: Self.countKey)

        guard count >= threshold, !defaults.bool(forKey: Self.requestedKey) else {
            return false
        }
        defaults.set(true, forKey: Self.requestedKey)
        return true
    }
}
