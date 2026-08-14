# Spec: Login and Logout

## Overview
This step implements real authentication for existing users, completing the
Spendly auth flow started by registration. Users submit their email and
password on the existing GET-only `login.html` form; the app verifies the
credentials against the `users` table and starts a logged-in session on
success. It also implements `/logout`, which currently returns the
placeholder string `"Logout — coming in Step 3"`, so that a logged-in user
can end their session and return to a signed-out state. Together these
close the loop opened by registration: a user can now register, log out,
and log back in.

## Depends on
- Step 1 — Database setup (`database/db.py` with `get_db()`, `init_db()`,
  `users` table). Already complete.
- Step 2 — Registration (`POST /register`, password hashing with werkzeug,
  `session["user_id"]` convention). Already complete.

## Routes
- `GET /login` — render the login form — public (already exists, unchanged)
- `POST /login` — validate credentials, start session, redirect to profile — public
- `GET /logout` — clear the session, redirect to landing page — logged-in

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`,
`password_hash`, `created_at`) already supports login as-is.

## Templates
- **Create:** none
- **Modify:** `templates/login.html` — surface a login error via an
  `{% if error %}` block (matching the existing pattern in
  `register.html`); no structural change otherwise

## Files to change
- `app.py`:
  - Change `login` route to accept `GET` and `POST`. On POST, look up the
    user by email, verify the password with
    `werkzeug.security.check_password_hash`, and on success set
    `session["user_id"]` and redirect to profile. On failure, re-render
    `login.html` with a generic error (do not reveal whether the email
    exists).
  - Replace the placeholder `logout` route body: clear `session["user_id"]`
    (e.g. `session.pop("user_id", None)` or `session.clear()`) and redirect
    to `landing`.
- `templates/login.html` — add the `{% if error %}` block above the form,
  matching `register.html`.

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` ships with the
`werkzeug` package already in `requirements.txt` (used via Flask, and
`generate_password_hash` is already imported in `app.py`).

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`check_password_hash` against the stored
  `password_hash`, never compare plaintext)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use a single generic error message for both "no such email" and "wrong
  password" cases (e.g. "Invalid email or password.") to avoid leaking
  which emails are registered
- Do not implement `/profile` in this step — it may still return its
  placeholder response; `/login` and `/register` should redirect to
  `url_for('profile')` on success as they already do (or will), even
  though `profile` itself remains a placeholder
- Do not modify `/register` or the `users` table beyond what already exists

## Definition of done
- [ ] Visiting `/login` still renders the form (GET unchanged)
- [ ] Submitting `/login` with a valid registered email and correct password
      sets `session["user_id"]` and redirects away from `/login`
- [ ] Submitting `/login` with a correct email and wrong password shows an
      "Invalid email or password." error and does not set the session
- [ ] Submitting `/login` with an email that doesn't exist shows the same
      "Invalid email or password." error (no distinct message)
- [ ] Visiting `/logout` while logged in clears the session and redirects to
      the landing page
- [ ] After `/logout`, the session no longer contains `user_id` (verify via
      the Flask session cookie or a temporary debug check)
- [ ] App starts and runs without errors after the change
