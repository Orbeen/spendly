# Spec: Registration

## Overview
This step implements real user registration, replacing the current GET-only
`register.html` form (which renders but has no POST handler behind it). Users
submit their name, email, and password; the app validates the input, hashes
the password with werkzeug, inserts a new row into `users`, and starts a
logged-in session. This is the first authentication step in the Spendly
roadmap — it unblocks login, logout, and profile, all of which need real
user accounts to work against.

## Depends on
- Step 1 — Database setup (`database/db.py` with `get_db()`, `init_db()`,
  `users` table). Already complete.

## Routes
- `GET /register` — render the registration form — public (already exists,
  unchanged)
- `POST /register` — validate input, create the user, log them in, redirect
  to profile — public

## Database changes
No database changes. The existing `users` table
(`id`, `name`, `email`, `password_hash`, `created_at`) already supports
registration as-is. No new columns or tables needed.

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — surface validation/error messages
  via the existing `{% if error %}` block (already wired to accept an
  `error` variable; no structural change needed unless field-specific
  messages are required)

## Files to change
- `app.py` — change `register` route to accept `GET` and `POST`; on POST,
  validate fields, check for duplicate email, hash password, insert user,
  set session, redirect

## Files to create
None.

## New dependencies
No new dependencies. Flask's built-in `session` (via `app.secret_key`) and
`werkzeug.security.generate_password_hash` (already used in `database/db.py`)
cover this step. Note: `app.py` does not currently set `app.secret_key` —
this must be added for sessions to work, using a hardcoded dev value
consistent with this tutorial stage (no `.env`/config system exists yet).

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate on the server even though HTML5 `required`/`type=email` attributes
  exist on the form — client-side validation is not a substitute
- Reject registration if the email already exists in `users` (case-insensitive
  comparison is out of scope for this step — match existing schema's plain
  `UNIQUE` constraint behavior)
- On success, store the new user's id in `session` (e.g. `session["user_id"]`)
  so later steps (profile, logout) have a logged-in user to work with
- Do not implement `/logout` or `/profile` in this step — leave their
  placeholder responses as-is

## Definition of done
- [ ] Visiting `/register` still renders the form (GET unchanged)
- [ ] Submitting the form with valid name/email/password creates a new row
      in the `users` table with a hashed password (verify it is not stored
      in plaintext)
- [ ] Submitting with an email that already exists shows an error on the
      page and does not create a duplicate row
- [ ] Submitting with a missing required field shows an error and does not
      create a row
- [ ] After successful registration, the browser session contains the new
      user's id (inspect via a temporary debug route or the Flask session
      cookie) and the user is redirected away from `/register`
- [ ] App starts and runs without errors after the change
