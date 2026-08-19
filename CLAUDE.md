# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a Flask-based personal expense tracker, built as a step-by-step learning project. Each step has
a spec file in `.claude/specs/<NN>-<slug>.md` (generated via the `/create-spec` command) describing what
that step must implement. Steps 1–4 are complete: database setup, registration, login/logout, and the
profile page. Steps 7–9 (add/edit/delete expense) are still placeholders in `app.py` that return a plain
string (e.g. `"Add expense — coming in Step 7"`). When asked to implement one of these steps, follow the
pattern already established by the surrounding code (see `.claude/agents/spendly-reviewer.md` for the
exact conventions a change is expected to follow) rather than jumping ahead to build unrelated future
steps.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dev server (debug mode, auto-reload) — http://127.0.0.1:5001
python app.py
```

On Windows, if `python` resolves to the Microsoft Store alias instead of a real interpreter, use `py`
instead (`py app.py`).

There is no configured test runner script yet, but `pytest` and `pytest-flask` are in `requirements.txt`
for when tests are added — run with `pytest`.

This repo also has project-specific slash commands under `.claude/commands/`:
- `/create-spec <step> <feature>` — creates the next `.claude/specs/` file and a matching `feature/<slug>`
  branch off `main` (requires a clean working tree).
- `/git-push [message]` — stages, commits (excluding anything that looks like a secret), and pushes the
  current branch.
- `/seed-user` — inserts one realistic dummy user into the database.
- `/seed-expense <user_id> <count> <months>` — inserts realistic dummy expenses for a given user, spread
  across the given number of past months.

## Architecture

- **`app.py`** — single-file Flask app; all routes are defined directly on the module-level `app` object
  (no blueprints). `init_db()`/`seed_db()` run once at import time inside `with app.app_context():`, before
  any route is registered. Two `@app.context_processor` functions inject `current_user` (looked up from
  `session["user_id"]` on every request, `None` if logged out) and `current_year` into every template's
  context — this is why templates can reference `current_user` without any route passing it explicitly.
  `app.secret_key` is a hardcoded dev placeholder (needed for `session` to work) and is intentionally left
  as-is; don't "fix" it unless asked to productionize the app.
- **`database/db.py`** — `get_db()` opens a new SQLite connection per call (`row_factory = sqlite3.Row`,
  `PRAGMA foreign_keys = ON`); there is no connection pooling or `flask.g` caching, so every caller is
  responsible for closing what it opens (`try/finally: conn.close()` — see any route in `app.py` for the
  pattern). `init_db()` creates `users` and `expenses` (`CREATE TABLE IF NOT EXISTS`), and `seed_db()`
  inserts one demo user + 8 sample expenses, guarded so it never duplicates data on repeated runs. The
  resulting SQLite file (`expense_tracker.db`) is gitignored and created at runtime — it does not exist in
  source control.
- **`templates/`** — Jinja2 templates, all extending `base.html` (nav, footer, flash-free shared `<head>`).
  Pages use `{% block title %}`, `{% block content %}`, and `{% block scripts %}`. Static assets are
  referenced via `url_for('static', filename=...)`, never hardcoded paths. `profile.html` is the first
  logged-in-only page and establishes the pattern for a dashboard view driven entirely by SQL aggregate
  queries in its route (total spend, this-month spend, category breakdown, recent transactions) rather
  than any client-side computation.
- **`static/css/style.css`** — single global stylesheet for the whole app (no per-page CSS files); uses CSS
  custom properties for colors/spacing — new styling should reuse existing variables rather than
  hardcoding hex values.
- **`static/js/main.js`** — currently an empty placeholder; add page behavior here as features are built.
- **`.claude/agents/spendly-reviewer.md`** — a subagent meant to be used proactively after any change to
  `app.py`, `database/db.py`, or `templates/`; it encodes this project's established conventions in detail
  (route/endpoint naming, the `get_db()`/`finally: close()` pattern, auth-gating via
  `session.get("user_id")`, no ORM/parameterized-queries-only, template block structure) and is a good
  source of truth if this file and the code ever disagree.

## Conventions

- Currency is displayed in ₹ (Indian Rupees) throughout the UI copy.
- Route URLs and Flask endpoint function names correspond directly (e.g. `register` → `/register`,
  `login` → `/login`); link to them with `url_for(...)` rather than hardcoded strings.
- Placeholder routes for not-yet-built features return a plain string describing which step will implement
  them (currently `add_expense`, `edit_expense`, `delete_expense`) — replace these with real
  implementations (templates, DB access) rather than leaving the string response in place once a step is
  implemented, and never leave a placeholder string alongside partially-added real logic.
- No ORM (no SQLAlchemy) — raw `sqlite3` only, and every query is parameterized (`?` placeholders); never
  build SQL with string formatting or f-strings.
- Passwords are always handled via `werkzeug.security.generate_password_hash` /
  `check_password_hash` — never stored or compared in plain text.
- A route that requires login checks `session.get("user_id")` and redirects to `login` when absent — see
  `profile()` in `app.py` for the reference pattern.
