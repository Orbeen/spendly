# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a Flask-based personal expense tracker, built as a step-by-step learning project (comments in
the codebase say things like "Students will write this file in Step 1"). Expect the codebase to be
intentionally incomplete in places — routes and modules exist as placeholders (e.g. `"Logout — coming in
Step 3"`) that get filled in as the tutorial progresses. When asked to implement one of these steps, follow
the pattern already established by the surrounding code rather than jumping ahead to build unrelated
future steps.

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

## Architecture

- **`app.py`** — single-file Flask app; all routes are currently defined directly on the module-level
  `app` object (no blueprints yet). Routes render Jinja templates from `templates/`.
- **`database/db.py`** — intended to hold `get_db()` (SQLite connection with `row_factory` and foreign
  keys enabled), `init_db()` (creates tables with `CREATE TABLE IF NOT EXISTS`), and `seed_db()` (sample
  data for development). The resulting SQLite file (`expense_tracker.db`) is gitignored and created at
  runtime — it does not exist in source control.
- **`templates/`** — Jinja2 templates, all extending `base.html` (nav, footer, shared `<head>`). Pages use
  `{% block title %}`, `{% block content %}`, and `{% block scripts %}`. Static assets are referenced via
  `url_for('static', filename=...)`, never hardcoded paths.
- **`static/css/style.css`** — single global stylesheet for the whole app (no per-page CSS files).
- **`static/js/main.js`** — currently an empty placeholder; add page behavior here as features are built.

## Conventions

- Currency is displayed in ₹ (Indian Rupees) throughout the UI copy.
- Route URLs and Flask endpoint function names correspond directly (e.g. `register` → `/register`,
  `login` → `/login`); link to them with `url_for(...)` rather than hardcoded strings.
- Placeholder routes for not-yet-built features return a plain string describing which step will implement
  them (e.g. `add_expense`, `edit_expense`, `delete_expense`, `logout`, `profile`) — replace these with real
  implementations (templates, DB access) rather than leaving the string response in place once a step is
  implemented.
