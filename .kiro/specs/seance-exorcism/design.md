# Technical Design — SéanceCode

## Overview

SéanceCode is a Flask-based web application that performs static AST/heuristic analysis and AI-assisted code refactoring presented through a Victorian Gothic séance interface, persisting every diagnostic result in a local SQLite grimoire.

## Architecture

- `app.py`: Serves the Gothic UI (`/`), sample presets (`/api/samples`), exorcism endpoint (`/api/exorcise`), and Grimoire history/purge endpoints (`/api/grimoire`).
- `templates/index.html`: Responsive dark-mode UI with animated SVG ritual astrolabe, tab/split views for Cursed vs. Purified code, Markdown scroll export, and interactive Grimoire history cards.

## Components and Interfaces

- **Summoning Altar (`templates/index.html`)**: Accepts source code input up to 15,000 characters across Python, JavaScript, SQL, PHP, and general stack traces.
- **Diagnostic Engine (`app.py`)**: Processes `POST /api/exorcise` payloads, executes deterministic AST/pattern analysis or LLM synthesis, and returns structured JSON diagnostics.
- **Grimoire Ledger API (`app.py`)**: Exposes `GET /api/grimoire` to retrieve archived folios and `DELETE /api/grimoire` to purge stored records.

## Data Models

- **SQLite Table `exorcisms` (`grimoire.db`)**:
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT): Sequential folio identifier.
  - `language` (TEXT): Programming language or trace category.
  - `original_code` (TEXT): Submitted afflicted code snippet.
  - `curse_name` (TEXT): Generated occult entity title.
  - `severity` (TEXT): Threat tier (`Minor Poltergeist`, `Vengeful Wraith`, or `Eldritch Horror`).
  - `diagnosis` (TEXT): Root-cause explanation.
  - `astral_nodes_json` (TEXT): JSON array of 3 sequential execution fault trace steps.
  - `purified_code` (TEXT): Refactored, safe code output.
  - `prevention_ward` (TEXT): Defensive coding recommendation.
  - `created_at` (TEXT): UTC timestamp of the ritual.

## Correctness Properties

### Property 1: Input Validation Boundary

Empty or whitespace-only code submissions and payloads exceeding 15,000 characters must always be rejected with HTTP `400`.

**Validates: Requirements 1.1**

### Property 2: Structural Diagnostic Completeness

Every valid exorcism response must contain a non-empty `curse_name`, valid `severity`, `spectral_diagnosis`, 3-step `astral_nodes`, `purified_code`, and `prevention_ward`.

**Validates: Requirements 2.1**

### Property 3: Ledger Persistence and Purge Round-Trip

Each successful ritual persists a retrievable record in `grimoire.db`, and invoking `DELETE /api/grimoire` clears all stored folios.

**Validates: Requirements 3.1**

## Error Handling

- Returns JSON error payloads with HTTP `400` for empty input, oversized payloads, or unsupported parameters.
- Falls back deterministically to built-in AST and heuristic static analyzers if external AI API keys are absent or unreachable.

## Testing Strategy

- **Property-Based Testing (`tests/test_properties.py`)**: Uses `pytest` and `Hypothesis` to fuzz code inputs, verify boundary rejections, validate schema invariants, and test SQLite persistence.
- **Automated Agent Hook (`.kiro/hooks/test-on-save.kiro.hook`)**: Automatically executes `pytest` whenever backend Python files are saved.