# Cursor Rules for This Project
- Keep passwords in plain text only because the user requested it; do not hash unless specifically asked later.
- Admin login must remain `admin` / `admin` and use the shared login page with users; redirect admins to `/admin` and users to `/dashboard`.
- Preserve responsive, modern styling; reuse the existing design system (dark theme, pills, cards, buttons).
- Before changing data models, update both `app.py` and `database.sql` to stay aligned.
- Prefer small, readable functions and add brief comments only where logic is non-obvious.
- Run lints or quick tests on touched files when making substantive changes.

