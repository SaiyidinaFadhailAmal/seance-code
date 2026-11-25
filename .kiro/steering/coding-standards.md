---
inclusion: always
---
# Engineering & Architecture Standards

## Tech Stack
- **Backend:** Python 3.10+ with Flask and SQLite (`grimoire.db`).
- **Frontend:** Single-page HTML5 + Tailwind CSS + Vanilla JavaScript (strictly escape all user-provided code before DOM insertion to prevent XSS).
- **Testing:** `pytest` with `hypothesis` for Property-Based Testing (PBT).

## API & Resilience Rules
- All `/api/exorcise` responses must strictly adhere to the JSON schema containing: `id`, `curse_name`, `severity`, `spectral_diagnosis`, `astral_nodes`, `purified_code`, `prevention_ward`, and `created_at`.
- Implement graceful fallback analysis when external LLM API keys (`GEMINI_API_KEY`) are absent or rate-limited so the live demo never returns an unhandled HTTP 500 error.