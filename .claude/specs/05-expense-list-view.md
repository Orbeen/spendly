# Spec: Expense List/View

## Overview
This step adds a dedicated page showing a signed-in user's full expense history. `profile.html`
(Step 4) only ever shows a preview of the 10 most recent expenses as part of the dashboard; this
step gives users a way to see everything they've logged, not just the preview. It is strictly
read-only — no way to create, edit, or delete an expense from this page. Those actions arrive in
Steps 7–9, and this step's route only ever issues `SELECT` queries.

## Depends on
- Step 1 — Database setup (`database/db.py` with `get_db()`, `init_db()`, `expenses` table).
  Already complete.
- Step 3 — Login and Logout (`session["user_id"]` convention; `current_user` context processor).
  Already complete.
- Step 4 — Profile Page (establishes the pattern this step reuses: a logged-in-only route that
  queries `expenses` filtered by `user_id` and renders it with the `.expense-list`/`.expense-row*`
  CSS already defined in `static/css/style.css`). Already complete.

## Routes
- `GET /expenses` — render the signed-in user's full expense list, ordered most recent first —
  logged-in only. If `session["user_id"]` is not set, redirect to `GET /login` instead of
  rendering (same pattern as `profile()`).

## Database changes
No database changes. The existing `expenses` table (`id`, `user_id`, `amount`, `category`, `date`,
`description`, `created_at`) already supports everything this page needs. The route only reads
data — a single `SELECT ... WHERE user_id = ? ORDER BY date DESC, id DESC` query, no `LIMIT`
(unlike profile.html's 10-row preview, this page shows all of the user's expenses).

## Templates
- **Create:** `templates/expenses.html` — new page showing:
  - A page heading (e.g. "Your expenses")
  - The full list of the user's expenses, reusing the existing `.expense-list`/`.expense-row`/
    `.expense-row-date`/`.expense-row-category`/`.expense-row-desc`/`.expense-row-amount` CSS
    classes from `profile.html` so the row layout is visually consistent with the dashboard
    preview
  - An empty state if the user has no expenses yet (reuse the existing `.profile-empty` class
    and "No expenses logged yet." copy from `profile.html` for consistency) — do not assume
    seeded data is always present
- **Modify:** `templates/base.html` — add an "Expenses" link to the logged-in branch of both the
  nav bar (`nav-links`) and the footer's "Product" column, pointing at `url_for('expenses')`,
  alongside the existing "My account"/"Logout" (nav) and "My account"/"Logout" (footer) links.
  This is the first page besides `/profile` that a logged-in user needs to reach, so it needs to
  be discoverable from the nav like every other real page already is.

## Files to change
- `app.py`:
  - Add a new `expenses` route. On `GET`:
    - If `session.get("user_id")` is falsy, `redirect(url_for('login'))`.
    - Otherwise, query all of that user's expenses ordered by `date DESC, id DESC` and
      `render_template("expenses.html", ...)` with that data.
  - Reuse `get_db()` from `database/db.py`, closed in a `finally` block — same pattern as
    `profile()`. No new helper functions needed in `database/db.py`.
- `templates/base.html`: add the "Expenses" nav/footer links described above.

## Files to create
- `templates/expenses.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (not applicable to this step, but do not ever select or render
  `password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `/expenses` must not be reachable without a session — redirect to `/login` rather than erroring
  or exposing another user's data
- Only ever query expenses `WHERE user_id = ?` using the signed-in user's id from the session —
  never trust a client-supplied user id
- Currency values in the template must be displayed with the ₹ prefix, consistent with the rest
  of the UI
- This page is read-only. Do not add "Add expense", "Edit", or "Delete" links/buttons, and do not
  implement `add_expense`, `edit_expense`, or `delete_expense` — those remain placeholders until
  Steps 7–9
- No pagination in this step — render the full list in one page. The seeded/demo dataset sizes in
  this tutorial are small; adding pagination now would be scope creep ahead of what this step
  needs

## Definition of done
- [ ] Visiting `/expenses` while logged out redirects to `/login`
- [ ] Visiting `/expenses` while logged in (e.g. as the seeded `demo@spendly.com` user) renders a
      real page listing that user's expenses
- [ ] The list reflects every row in `expenses` for the signed-in user, not just the 10 most
      recent (verify by seeding more than 10 expenses via `/seed-expense` and confirming they all
      appear)
- [ ] Expenses are ordered most recent first (by `date`, then `id`, descending)
- [ ] A newly registered user with zero expenses sees an empty state, not an error, when visiting
      `/expenses`
- [ ] The nav bar and footer show a working "Expenses" link when logged in, absent when logged out
- [ ] The page uses only CSS variables already defined in `static/css/style.css` (or new ones
      added to `:root`), no hardcoded hex colors
- [ ] No route or link on this page mutates data or implements add/edit/delete functionality
- [ ] App starts and runs without errors after the change
