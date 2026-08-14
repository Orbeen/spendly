# Spec: Profile Page

## Overview
This step replaces the `/profile` placeholder (`"Profile page — coming in
Step 4"`) with the real landing page a user sees after logging in or
registering. It shows the signed-in user's account details (name, email,
member-since date) and a read-only summary of their spending so far, using
whatever expenses already exist in the database. It does not add any way to
create, edit, or delete expenses — that arrives in Steps 7–9. This is the
first logged-in-only page in the app, so it also establishes the pattern for
guarding a route behind `session["user_id"]`.

## Depends on
- Step 1 — Database setup (`database/db.py` with `get_db()`, `init_db()`,
  `users` and `expenses` tables). Already complete.
- Step 2 — Registration (`POST /register`, `session["user_id"]` convention).
  Already complete.
- Step 3 — Login and Logout (`POST /login` sets `session["user_id"]`,
  `GET /logout` clears it; `current_user` context processor injects the
  signed-in user into every template). Already complete.

## Routes
- `GET /profile` — render the signed-in user's profile and expense summary
  — logged-in only. If `session["user_id"]` is not set, redirect to
  `GET /login` instead of rendering.

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`,
`created_at`) and `expenses` table (`id`, `user_id`, `amount`, `category`,
`date`, `description`, `created_at`) already support everything this page
needs. The route only reads data — it issues `SELECT` queries against both
tables filtered by `user_id`; no schema changes required.

## Templates
- **Create:** `templates/profile.html` — new page showing:
  - Account details: name, email, member-since date (`users.created_at`)
  - Total spend across all of the user's expenses
  - A simple breakdown by category (sum of `amount` grouped by `category`)
  - A list (or table) of the user's most recent expenses (e.g. last 10,
    ordered by `date` descending)
  - An empty state if the user has no expenses yet (e.g. "No expenses
    logged yet.") — do not assume seeded data is always present
- **Modify:** none. The nav bar's logged-in state (`base.html`) already
  links relevant auth actions via the existing `current_user` context
  processor from Step 3; no nav changes needed for this step.

## Files to change
- `app.py`:
  - Replace the placeholder `profile` route. On `GET`:
    - If `session.get("user_id")` is falsy, `redirect(url_for('login'))`.
    - Otherwise, look up the user by id, query their expenses (total sum,
      per-category sums, recent list), and `render_template("profile.html",
      ...)` with that data.
  - Reuse `get_db()` from `database/db.py`; no new helper functions needed
    in `database/db.py` for this step — plain parameterised SQL in the
    route is consistent with `register`/`login`.

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (not applicable to this step, but do not
  ever select or render `password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `/profile` must not be reachable without a session — redirect to
  `/login` rather than erroring or exposing another user's data
- Only ever query expenses `WHERE user_id = ?` using the signed-in user's
  id from the session — never trust a client-supplied user id
- Currency values in the template must be displayed with the ₹ prefix,
  consistent with the rest of the UI
- Do not implement add/edit/delete expense functionality or their routes
  in this step — `add_expense`, `edit_expense`, `delete_expense` remain
  placeholders until Steps 7–9

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Visiting `/profile` while logged in (e.g. as the seeded
      `demo@spendly.com` user) renders a real page, not the placeholder
      string
- [ ] The profile page shows the signed-in user's name and email
- [ ] The profile page shows a total spend figure that matches the sum of
      that user's rows in `expenses`
- [ ] The profile page shows a per-category breakdown that matches the
      seeded categories/amounts for that user
- [ ] The profile page shows a recent-expenses list reflecting that user's
      `expenses` rows
- [ ] A newly registered user with zero expenses sees an empty state, not
      an error, when visiting `/profile`
- [ ] The page uses only CSS variables already defined in
      `static/css/style.css` (or new ones added to `:root`), no hardcoded
      hex colors
- [ ] App starts and runs without errors after the change
