# Technical Design — SéanceCode

## Architecture
- `app.py`: Serves the Gothic UI (`/`), sample presets (`/api/samples`), exorcism endpoint (`/api/exorcise`), and Grimoire history (`/api/grimoire`).
- `SQLite (grimoire.db)`: Stores table `exorcisms (id, language, original_code, curse_name, severity, diagnosis, astral_nodes_json, purified_code, prevention_ward, created_at)`.
- `templates/index.html`: Responsive dark-mode UI with animated SVG ritual sigil, tab/split views for Cursed vs. Purified code, and interactive Grimoire history cards.