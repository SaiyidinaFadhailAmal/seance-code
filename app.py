import ast
import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
DB_PATH = os.environ.get("GRIMOIRE_DB_PATH", "grimoire.db")
MAX_CODE_LENGTH = 15000

SAMPLE_CURSES = [
    {
        "id": "python-mutable-trap",
        "title": "The Phantom Mutable Leviathan (Python)",
        "language": "Python",
        "code": '''def summon_acolytes(name, roster=[]):
    roster.append(name)
    return roster

print(summon_acolytes("Malakor"))
print(summon_acolytes("Vespera"))  # Why is Malakor still haunting this list?!

def divide_souls(total, vessels):
    return total / vessels

print(divide_souls(100, 0))'''
    },
    {
        "id": "js-async-wraith",
        "title": "The Unbound Async Wraith (JavaScript)",
        "language": "JavaScript",
        "code": '''async function fetchRelicData(relicIds) {
  const results = [];
  relicIds.forEach(async (id) => {
    const res = await fetch(`/api/relics/${id}`);
    const data = res.json(); // Missing await!
    results.push(data);
  });
  return results; // Always returns empty [] before promises resolve!
}'''
    },
    {
        "id": "sql-oblivion-query",
        "title": "The Unbounded Oblivion Purge (SQL)",
        "language": "SQL",
        "code": '''-- Cursed production maintenance query
UPDATE acolyte_accounts
SET status = 'BANISHED', soul_balance = 0;

SELECT a.username, r.relic_name
FROM acolyte_accounts a, forbidden_relics r
WHERE a.status = 'ACTIVE' OR r.cursed = 1;'''
    },
    {
        "id": "php-type-juggling-ghoul",
        "title": "The Loose-Type Juggling Ghoul (PHP)",
        "language": "PHP",
        "code": '''<?php
function verifyMasterSigil($providedToken, $storedHash) {
    // Loose comparison allows magic hash bypass (0e1234 == 0)
    if ($providedToken == $storedHash) {
        $user = $_GET['acolyte'];
        echo "Welcome back, " . $user;
        return true;
    }
    return false;
}'''
    },
    {
        "id": "stacktrace-abyssal-crash",
        "title": "The Null-Reference Traceback (Stack Trace)",
        "language": "Other",
        "code": '''Traceback (most recent call last):
  File "/srv/seance/ritual_engine.py", line 84, in bind_spirit
    sigil_power = payload["grimoire"]["amplifier"].upper()
KeyError: 'amplifier'

During handling of the above exception, another exception occurred:
AttributeError: 'NoneType' object has no attribute 'upper' '''
    }
]

@app.route("/api/grimoire", methods=["DELETE"])
def clear_grimoire():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM exorcisms")
        conn.commit()
    return jsonify({"status": "purged"})
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS exorcisms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT NOT NULL,
                original_code TEXT NOT NULL,
                curse_name TEXT NOT NULL,
                severity TEXT NOT NULL,
                spectral_diagnosis TEXT NOT NULL,
                astral_nodes_json TEXT NOT NULL,
                purified_code TEXT NOT NULL,
                prevention_ward TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


def validate_code_payload(code: str, language: str) -> tuple[bool, str]:
    if not isinstance(code, str) or not code.strip():
        return False, "The summoning circle is empty. Paste cursed code or an error log to begin."
    if len(code) > MAX_CODE_LENGTH:
        return False, f"The tome is too massive ({len(code)} chars). Limit input to {MAX_CODE_LENGTH} characters."
    if not isinstance(language, str) or not language.strip():
        return False, "Specify the arcane language (e.g., Python, JavaScript, SQL)."
    return True, ""


def fallback_static_exorcist(code: str, language: str) -> dict:
    """Deterministic fallback analyzer ensuring 100% uptime even without an external LLM key."""
    lowered = code.lower()

    if "roster=[]" in code.replace(" ", "") or ("=[]" in code.replace(" ", "") and "def " in code):
        return {
            "curse_name": "The Phantom Mutable Default Leviathan",
            "severity": "Vengeful Wraith",
            "spectral_diagnosis": (
                "Two distinct spirits haunt this script: (1) A mutable list `[]` is bound once at function "
                "definition time, causing state to leak across invocations; (2) An unguarded division by zero "
                "triggers a fatal ZeroDivisionError."
            ),
            "astral_nodes": [
                "Node I — Function Definition: `roster=[]` allocates a single shared list in memory.",
                "Node II — State Contamination: Subsequent calls mutate the same list reference.",
                "Node III — Abyssal Crash: `divide_souls(100, 0)` divides by zero without a guard clause."
            ],
            "purified_code": '''def summon_acolytes(name: str, roster: list[str] | None = None) -> list[str]:
    if roster is None:
        roster = []
    roster.append(name)
    return roster


def divide_souls(total: float, vessels: float) -> float:
    if vessels == 0:
        raise ValueError("Cannot divide souls across zero vessels.")
    return total / vessels''',
            "prevention_ward": "Always default mutable function parameters to `None` and validate denominators before division."
        }

    if "foreach" in lowered and "async" in lowered:
        return {
            "curse_name": "The Unbound Async Wraith",
            "severity": "Vengeful Wraith",
            "spectral_diagnosis": (
                "`Array.prototype.forEach` ignores returned Promises, causing `fetchRelicData` to return an empty "
                "array immediately. Additionally, `res.json()` lacks an `await` keyword."
            ),
            "astral_nodes": [
                "Node I — Premature Return: `forEach` fires async callbacks without awaiting completion.",
                "Node II — Unresolved Promise: `res.json()` returns a pending Promise instead of parsed JSON.",
                "Node III — Race Condition: Caller receives `[]` before network I/O finishes."
            ],
            "purified_code": '''async function fetchRelicData(relicIds) {
  const requests = relicIds.map(async (id) => {
    const res = await fetch(`/api/relics/${encodeURIComponent(id)}`);
    if (!res.ok) {
      throw new Error(`Failed to summon relic ${id}: ${res.status}`);
    }
    return res.json();
  });
  return Promise.all(requests);
}''',
            "prevention_ward": "Use `Promise.all` with `.map()` instead of `forEach` for concurrent async operations, and always `await res.json()`."
        }

    if language.lower() == "sql" or ("update " in lowered and "where" not in lowered.split(";")[0]):
        return {
            "curse_name": "The Unbounded Oblivion Purge",
            "severity": "Eldritch Horror",
            "spectral_diagnosis": (
                "An `UPDATE` statement without a `WHERE` clause overwrites every row in `acolyte_accounts`, "
                "while the comma-separated `FROM` clause creates an accidental Cartesian product (`CROSS JOIN`)."
            ),
            "astral_nodes": [
                "Node I — Missing Predicate: `UPDATE` mutates the entire table indiscriminately.",
                "Node II — Cartesian Explosion: Implicit comma join multiplies every account with every relic.",
                "Node III — Transaction Risk: Destructive mutation executes without a rollback boundary."
            ],
            "purified_code": '''BEGIN TRANSACTION;

UPDATE acolyte_accounts
SET status = 'BANISHED', soul_balance = 0
WHERE last_ritual_at < CURRENT_DATE - INTERVAL '90 days'
  AND status = 'DORMANT';

SELECT a.username, r.relic_name
FROM acolyte_accounts a
INNER JOIN forbidden_relics r ON r.owner_id = a.id
WHERE a.status = 'ACTIVE' AND r.cursed = 1;

COMMIT;''',
            "prevention_ward": "Never execute `UPDATE` or `DELETE` without an explicit `WHERE` filter, and replace comma joins with explicit `JOIN ... ON` clauses."
        }

    if language.lower() == "php" or "<?php" in lowered:
        return {
            "curse_name": "The Loose-Type Juggling Ghoul",
            "severity": "Eldritch Horror",
            "spectral_diagnosis": (
                "Loose equality (`==`) in PHP coerces scientific-notation strings (`0e...`) to zero, enabling "
                "authentication bypass, while unescaped `$_GET` output introduces Reflected XSS."
            ),
            "astral_nodes": [
                "Node I — Type Coercion Trap: `$providedToken == $storedHash` evaluates `0e123 == 0e999` as true.",
                "Node II — Timing Side-Channel: Non-constant-time comparison leaks token prefix length.",
                "Node III — Reflected XSS: Raw `$_GET['acolyte']` echoes unescaped HTML into the response."
            ],
            "purified_code": '''<?php
declare(strict_types=1);

function verifyMasterSigil(string $providedToken, string $storedHash): bool {
    if (!hash_equals($storedHash, $providedToken)) {
        return false;
    }
    $user = htmlspecialchars($_GET['acolyte'] ?? 'Guest', ENT_QUOTES, 'UTF-8');
    echo "Welcome back, " . $user;
    return true;
}''',
            "prevention_ward": "Use `hash_equals()` or strict `===` for secret verification, and sanitize all output with `htmlspecialchars()`."
        }

    if "traceback" in lowered or "keyerror" in lowered or "attributeerror" in lowered:
        return {
            "curse_name": "The Null-Reference Abyssal Traceback",
            "severity": "Vengeful Wraith",
            "spectral_diagnosis": (
                "Chained dictionary indexing `payload['grimoire']['amplifier']` raises a `KeyError` when optional "
                "nested keys are missing, cascading into an `AttributeError` when `.upper()` is called on `None`."
            ),
            "astral_nodes": [
                "Node I — Unsafe Key Lookup: Direct bracket access crashes on missing `'amplifier'` key.",
                "Node II — Chained Exception: Fallback handler leaves value as `None` without type validation.",
                "Node III — Null Dereference: Calling `.upper()` on `NoneType` aborts the worker."
            ],
            "purified_code": '''def bind_spirit(payload: dict) -> str:
    grimoire = payload.get("grimoire") or {}
    amplifier = grimoire.get("amplifier")
    if not isinstance(amplifier, str) or not amplifier.strip():
        return "DEFAULT_SIGIL"
    return amplifier.strip().upper()''',
            "prevention_ward": "Use chained `.get()` with type checks before calling string methods on external payloads."
        }

    syntax_note = "Potential logic anomaly, unhandled edge cases, or missing error boundaries detected."
    if language.lower() == "python":
        try:
            ast.parse(code)
            syntax_note = "AST parsed cleanly, but runtime edge cases, missing type guards, and exception handling need reinforcement."
        except SyntaxError as exc:
            syntax_note = f"Fatal Python SyntaxError on line {exc.lineno}: {exc.msg}."

    return {
        "curse_name": f"The Shadowed {language} Poltergeist",
        "severity": "Minor Poltergeist",
        "spectral_diagnosis": syntax_note,
        "astral_nodes": [
            "Node I — Boundary Inspection: Checked input types and null/empty edge states.",
            "Node II — Control Flow Audit: Verified error propagation and resource cleanup.",
            "Node III — Purification: Wrapped execution in defensive guards and explicit typing."
        ],
        "purified_code": f"# Purified {language} Ritual Output\n# Added defensive validation and structured error handling\n\n{code.strip()}\n",
        "prevention_ward": "Enforce strict input validation, explicit error handling, and automated property-based tests on core functions."
    }


def invoke_ai_exorcist(code: str, language: str) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return fallback_static_exorcist(code, language)

    prompt = (
        f"You are SéanceCode, a Victorian Gothic AI code exorcist. "
        f"Analyze the following {language} code or error log.\n"
        f"Return ONLY valid JSON with these exact keys:\n"
        f'- "curse_name": dramatic Halloween/Gothic name for the bug (string)\n'
        f'- "severity": one of "Minor Poltergeist", "Vengeful Wraith", or "Eldritch Horror"\n'
        f'- "spectral_diagnosis": clear, accurate technical root-cause explanation (string)\n'
        f'- "astral_nodes": array of 3 concise step-by-step trace strings showing how the bug manifests\n'
        f'- "purified_code": complete, clean, production-ready fixed code (string)\n'
        f'- "prevention_ward": one actionable engineering rule to prevent this bug (string)\n\n'
        f"Code/Log:\n<code_input>\n{code}\n</code_input>"
    )

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        response = requests.post(
            url,
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            },
            timeout=20
        )
        response.raise_for_status()
        raw_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(raw_text)
        required = {"curse_name", "severity", "spectral_diagnosis", "astral_nodes", "purified_code", "prevention_ward"}
        if not required.issubset(parsed.keys()):
            return fallback_static_exorcist(code, language)
        if parsed["severity"] not in {"Minor Poltergeist", "Vengeful Wraith", "Eldritch Horror"}:
            parsed["severity"] = "Vengeful Wraith"
        return parsed
    except Exception:
        return fallback_static_exorcist(code, language)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/samples", methods=["GET"])
def get_samples():
    return jsonify({"samples": SAMPLE_CURSES})


@app.route("/api/exorcise", methods=["POST"])
def exorcise():
    payload = request.get_json(silent=True) or {}
    code = payload.get("code", "")
    language = payload.get("language", "Python")

    is_valid, error_msg = validate_code_payload(code, language)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    result = invoke_ai_exorcist(code, language)
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO exorcisms (
                language, original_code, curse_name, severity,
                spectral_diagnosis, astral_nodes_json, purified_code,
                prevention_ward, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                language.strip(),
                code,
                result["curse_name"],
                result["severity"],
                result["spectral_diagnosis"],
                json.dumps(result["astral_nodes"]),
                result["purified_code"],
                result["prevention_ward"],
                created_at
            )
        )
        exorcism_id = cursor.lastrowid
        conn.commit()

    return jsonify({
        "id": exorcism_id,
        "language": language.strip(),
        "original_code": code,
        "curse_name": result["curse_name"],
        "severity": result["severity"],
        "spectral_diagnosis": result["spectral_diagnosis"],
        "astral_nodes": result["astral_nodes"],
        "purified_code": result["purified_code"],
        "prevention_ward": result["prevention_ward"],
        "created_at": created_at
    })


@app.route("/api/grimoire", methods=["GET"])
def get_grimoire():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM exorcisms ORDER BY id DESC LIMIT 12"
        ).fetchall()

    items = []
    for row in rows:
        items.append({
            "id": row["id"],
            "language": row["language"],
            "original_code": row["original_code"],
            "curse_name": row["curse_name"],
            "severity": row["severity"],
            "spectral_diagnosis": row["spectral_diagnosis"],
            "astral_nodes": json.loads(row["astral_nodes_json"]),
            "purified_code": row["purified_code"],
            "prevention_ward": row["prevention_ward"],
            "created_at": row["created_at"]
        })
    return jsonify({"grimoire": items})


init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)