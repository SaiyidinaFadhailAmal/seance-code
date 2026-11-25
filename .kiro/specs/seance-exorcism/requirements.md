# Requirements Document — SéanceCode Exorcism Engine

## Introduction
SéanceCode transforms debugging and legacy code refactoring into an interactive Victorian Gothic séance ritual while delivering accurate root-cause analysis and refactored code.

## Requirements

### Requirement 1: Cursed Code Submission
**User Story:** As a developer, I want to submit broken code or error logs into the summoning circle, so that I can receive an automated diagnosis and fix.
- **1.1:** WHEN a user submits non-empty code or error logs (up to 15,000 characters), THE SYSTEM SHALL validate the payload and initiate the exorcism analysis.
- **1.2:** WHEN a user submits empty or whitespace-only input, THE SYSTEM SHALL reject the request with HTTP 400 and a thematic error message.
- **1.3:** WHEN a user clicks a sample curse preset, THE SYSTEM SHALL populate the editor with realistic buggy Python, JavaScript, or SQL code.

### Requirement 2: Spectral Diagnosis & Code Purification
**User Story:** As a developer, I want structured root-cause insights and purified code, so that I can fix bugs quickly and prevent regressions.
- **2.1:** WHEN analysis completes, THE SYSTEM SHALL assign a thematic `curse_name` and a severity classification (`Minor Poltergeist`, `Vengeful Wraith`, or `Eldritch Horror`).
- **2.2:** THE SYSTEM SHALL output step-by-step `astral_nodes` tracing the execution flaw, `purified_code`, and a `prevention_ward` best-practice rule.
- **2.3:** IF external AI provider credentials are unavailable, THE SYSTEM SHALL execute a deterministic AST/heuristic static exorcist so functionality remains uninterrupted.

### Requirement 3: Grimoire Persistence & Export
**User Story:** As a developer, I want past exorcisms archived and exportable, so that I can reference resolved bugs later.
- **3.1:** WHEN an exorcism succeeds, THE SYSTEM SHALL persist the record into SQLite and display it in the Grimoire archive.
- **3.2:** WHEN a user clicks export, THE SYSTEM SHALL generate a downloadable Markdown (`.md`) Exorcism Scroll.