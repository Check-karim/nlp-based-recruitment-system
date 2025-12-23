# NLP Recruitment System (Flask)

Lightweight, modern web app for recruitment workflows with simple NLP-based resume-to-job matching. Built with Flask, SQLAlchemy, and a responsive UI.

## Features
- Single login page for admin and users; role-based redirects.
- Admin (predefined `admin` / `admin`): post jobs, rank applications, change statuses, view reports.
- Candidates: register, upload/paste resume, browse jobs, apply, and track application status.
- Simple NLP overlap scorer to highlight best-fit candidates.
- Responsive, dark-themed UI.

## Quick start (SQLite default)
1) Python 3.11+ recommended.  
2) Install deps:
```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
3) Run the app:
```
flask --app app run
```
4) Open http://127.0.0.1:5000 and log in as:
```
admin / admin
```
or register a new candidate.

## Using MySQL
1) Create the schema and seed data:
```
mysql -u <user> -p < database.sql
```
2) Point the app to MySQL (example):
```
set DATABASE_URL=mysql+pymysql://root:password@localhost:3306/nlp_recruitment
flask --app app run
```

## Project structure
- `app.py` — Flask app, routes, models, NLP scoring, role guards.
- `templates/` — HTML templates (shared base, dashboards, reports).
- `static/css/styles.css` — Modern responsive styling.
- `database.sql` — MySQL schema + seed data (admin/user, jobs).
- `requirements.txt` — Python dependencies.
- `CursorRules.md` — Collaboration guidelines.

## Notes
- Passwords are stored as plain text per request; do not use in production.
- The scoring uses token overlap for transparency and zero extra downloads; swap in a richer model as needed.
- If you change the admin credentials, update both the DB row and the login check.

## Next steps
- Add email notifications for decisions.
- Attach real resume file uploads with virus scanning.
- Expand NLP to TF-IDF or embeddings for better ranking.

