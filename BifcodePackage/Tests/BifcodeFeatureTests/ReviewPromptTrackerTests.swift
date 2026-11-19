//
//  ReviewPromptTrackerTests.swift
//
//  Created on 19.11.2026.
//  Copyright © 2026 Agnidia. All rights reserved.
//

import Foundation
import Testing
@testable import BifcodeFeature

@Suite("ReviewPromptTracker Tests")
@MainActor
struct ReviewPromptTrackerTests {
    private func makeDefaults() -> UserDefaults {
        let name = "ReviewPromptTrackerTests-\(UUID().uuidString)"
        let defaults = UserDefaults(suiteName: name)!
        defaults.removePersistentDomain(forName: name)
        return defaults
    }

    @Test("Fires on the 5th export only")
    func firesOnFifth() {
        let tracker = ReviewPromptTracker(defaults: makeDefaults())
        let results = (1...4).map { _ in tracker.recordSuccessfulExport() }
        #expect(results == [false, false, false, false])
        #expect(tracker.recordSuccessfulExport())
    }

    @Test("Never fires again after the first prompt")
    func firesOnce() {
        let tracker = ReviewPromptTracker(defaults: makeDefaults())
        for _ in 1...5 {
            _ = tracker.recordSuccessfulExport()
        }
        let later = (1...10).map { _ in tracker.recordSuccessfulExport() }
        #expect(!later.contains(true))
    }

    @Test("State persists across tracker instances")
    func persists() {
        let defaults = makeDefaults()
        for _ in 1...4 {
            _ = ReviewPromptTracker(defaults: defaults).recordSuccessfulExport()
        }
        #expect(ReviewPromptTracker(defaults: defaults).recordSuccessfulExport())
        #expect(!ReviewPromptTracker(defaults: defaults).recordSuccessfulExport())
    }

    @Test("Custom threshold is respected")
    func customThreshold() {
        let tracker = ReviewPromptTracker(defaults: makeDefaults(), threshold: 2)
        #expect(!tracker.recordSuccessfulExport())
        #expect(tracker.recordSuccessfulExport())
    }
}
