# NLP-Based Recruitment Management Information System

Modern web application for recruitment workflows powered by Natural Language Processing. Built with Flask, SQLAlchemy, scikit-learn, and a responsive dark-themed UI.

## Objectives

- **User-friendly interface** for candidates and admins to interact with the system
- **NLP techniques** for resume parsing (PDF, DOCX, TXT) and candidate screening via TF-IDF + cosine similarity
- **Analytics and reports** with skill frequency, score distributions, and pipeline insights

## Features

### Candidate
- Register with validated credentials (name, username, email, password)
- Upload resumes as **PDF, DOCX, or TXT** files, or paste text directly
- Automatic **NLP skill extraction** from resume content
- Browse and apply to jobs with **TF-IDF match scoring**
- Track application status in real time

### Admin
- **Full job CRUD** — add, edit, and delete jobs (predefined login: `admin` / `admin`)
- View NLP-ranked applicants with extracted skills and match scores
- Update application statuses (Under Review / Selected / Rejected)
- **Analytics dashboard** with bar charts, skill clouds, top candidates, and timeline

### Validation
- **Name:** letters and spaces only (no numbers or special characters)
- **Username:** no spaces, cannot start with a number, letters/numbers/underscores only
- **Email:** standard email format validation
- **Password:** minimum 6 characters
- Both client-side (real-time) and server-side validation

### NLP Pipeline
1. **Text extraction** — pdfplumber (PDF), python-docx (DOCX), plain text
2. **Skill extraction** — pattern matching against a curated taxonomy of 60+ technical and soft skills
3. **TF-IDF vectorization** — converts resume and job description into weighted feature vectors
4. **Cosine similarity** — computes semantic closeness to produce a match score

## Quick start (MySQL)
1) Python 3.11+ recommended. MySQL server must be running.
2) Create the database and seed data:
```
mysql -u root -p < database.sql
```
3) Install deps:
```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
4) Configure the connection (defaults to `root` with no password on `localhost:3306`):
```
set DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/nlp_recruitment
```
5) Run the app:
```
flask --app app run
```
6) Open http://127.0.0.1:5000 and log in as:
```
admin / admin
```
or register a new candidate.

## Project structure
- `app.py` — Flask app, routes, models, NLP scoring, resume parsing, validation.
- `templates/` — HTML templates (shared base, dashboards, reports).
- `static/css/styles.css` — Modern responsive dark-themed styling.
- `database.sql` — MySQL schema + seed data (admin/user, jobs).
- `requirements.txt` — Python dependencies.
- `uploads/` — Temporary storage for uploaded resume files (auto-created).

## Notes
- Passwords are stored as plain text per request; do not use in production.
- The NLP scoring uses TF-IDF with cosine similarity from scikit-learn.
- Resume files are parsed in memory and not permanently stored on disk.
- If you change the admin credentials, update both the DB row and the login check.
