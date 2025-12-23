import os
import re
from datetime import datetime

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "nlp-recruitment-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///nlp_recruitment.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # plain text by request
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resumes = db.relationship("Resume", backref="user", lazy=True)
    applications = db.relationship("Application", backref="user", lazy=True)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship("Application", backref="job", lazy=True)


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship("Application", backref="resume", lazy=True)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), nullable=True)
    status = db.Column(db.String(40), default="Under Review")
    match_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def tokenize(text: str) -> set:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def score_resume_against_job(resume_text: str, job_description: str) -> float:
    """
    Light-weight overlap score to mimic NLP matching without heavy deps.
    """
    resume_tokens = tokenize(resume_text)
    job_tokens = tokenize(job_description)
    if not resume_tokens or not job_tokens:
        return 0.0
    overlap = resume_tokens.intersection(job_tokens)
    return round(len(overlap) / len(job_tokens) * 100, 2)


def ensure_admin_user():
    admin = User.query.filter_by(email="admin@system.local").first()
    if not admin:
        admin = User(
            name="Admin",
            email="admin@system.local",
            password="admin",
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()


def current_user():
    if "user_id" not in session:
        return None
    return User.query.get(session["user_id"])


def login_required(role=None):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("login"))
            if role and user.role != role:
                flash("You are not authorized to access this area.", "danger")
                return redirect(url_for("home"))
            return fn(*args, **kwargs)

        wrapper.__name__ = fn.__name__
        return wrapper

    return decorator


@app.before_first_request
def setup():
    db.create_all()
    ensure_admin_user()


@app.route("/")
def home():
    jobs = Job.query.order_by(Job.created_at.desc()).limit(3).all()
    return render_template("home.html", jobs=jobs, user=current_user())


@app.route("/about")
def about():
    return render_template("about.html", user=current_user())


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not all([name, email, password]):
            flash("All fields are required.", "warning")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "danger")
            return redirect(url_for("register"))

        user = User(name=name, email=email, password=password, role="user")
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        session["role"] = user.role
        flash("Welcome! You are registered and logged in.", "success")
        return redirect(url_for("user_dashboard"))

    return render_template("register.html", user=current_user())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip().lower()
        password = request.form.get("password", "")

        if identifier == "admin" and password == "admin":
            admin_user = User.query.filter_by(role="admin").first()
            if admin_user:
                session["user_id"] = admin_user.id
                session["role"] = "admin"
                flash("Logged in as admin.", "success")
                return redirect(url_for("admin_dashboard"))

        user = User.query.filter(
            or_(User.email == identifier, User.name.ilike(identifier))
        ).first()
        if not user or user.password != password:
            flash("Invalid credentials. Try again.", "danger")
            return redirect(url_for("login"))

        session["user_id"] = user.id
        session["role"] = user.role
        flash("Welcome back!", "success")
        if user.role == "admin":
            return redirect(url_for("admin_dashboard"))
        return redirect(url_for("user_dashboard"))

    return render_template("login.html", user=current_user())


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required(role="user")
def user_dashboard():
    user = current_user()
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    applications = (
        Application.query.filter_by(user_id=user.id)
        .order_by(Application.created_at.desc())
        .all()
    )
    latest_resume = (
        Resume.query.filter_by(user_id=user.id)
        .order_by(Resume.created_at.desc())
        .first()
    )
    return render_template(
        "dashboard_user.html",
        user=user,
        jobs=jobs,
        applications=applications,
        latest_resume=latest_resume,
    )


@app.route("/upload_resume", methods=["POST"])
@login_required(role="user")
def upload_resume():
    user = current_user()
    content = request.form.get("resume_text", "").strip()
    if not content:
        flash("Please paste your resume text.", "warning")
        return redirect(url_for("user_dashboard"))
    resume = Resume(user_id=user.id, content=content)
    db.session.add(resume)
    db.session.commit()
    flash("Resume saved.", "success")
    return redirect(url_for("user_dashboard"))


@app.route("/apply/<int:job_id>", methods=["POST"])
@login_required(role="user")
def apply(job_id):
    user = current_user()
    job = Job.query.get_or_404(job_id)
    resume_text = request.form.get("resume_text", "").strip()

    latest_resume = (
        Resume.query.filter_by(user_id=user.id)
        .order_by(Resume.created_at.desc())
        .first()
    )

    if not resume_text and not latest_resume:
        flash("Upload a resume before applying.", "warning")
        return redirect(url_for("user_dashboard"))

    if resume_text:
        resume = Resume(user_id=user.id, content=resume_text)
        db.session.add(resume)
        db.session.flush()
    else:
        resume = latest_resume

    score = score_resume_against_job(resume.content, job.description)
    application = Application(
        user_id=user.id,
        job_id=job.id,
        resume_id=resume.id,
        status="Under Review",
        match_score=score,
    )
    db.session.add(application)
    db.session.commit()
    flash(f"Applied to {job.title}. Match score: {score}%", "success")
    return redirect(url_for("user_dashboard"))


@app.route("/admin")
@login_required(role="admin")
def admin_dashboard():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    applications = (
        Application.query.order_by(Application.match_score.desc()).all()
    )
    total_users = User.query.filter(User.role == "user").count()
    total_jobs = Job.query.count()
    total_apps = Application.query.count()
    return render_template(
        "dashboard_admin.html",
        user=current_user(),
        jobs=jobs,
        applications=applications,
        total_users=total_users,
        total_jobs=total_jobs,
        total_apps=total_apps,
    )


@app.route("/admin/jobs", methods=["POST"])
@login_required(role="admin")
def create_job():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    location = request.form.get("location", "").strip()
    if not title or not description:
        flash("Title and description are required.", "warning")
        return redirect(url_for("admin_dashboard"))

    job = Job(title=title, description=description, location=location)
    db.session.add(job)
    db.session.commit()
    flash("Job posted.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/applications/<int:application_id>/status", methods=["POST"])
@login_required(role="admin")
def update_application_status(application_id):
    status = request.form.get("status", "Under Review")
    application = Application.query.get_or_404(application_id)
    application.status = status
    db.session.commit()
    flash(f"Application {application.id} marked as {status}.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/reports")
@login_required(role="admin")
def reports():
    job_stats = (
        db.session.query(Job.title, db.func.count(Application.id))
        .outerjoin(Application)
        .group_by(Job.id)
        .all()
    )
    status_stats = (
        db.session.query(Application.status, db.func.count(Application.id))
        .group_by(Application.status)
        .all()
    )
    return render_template(
        "reports.html",
        user=current_user(),
        job_stats=job_stats,
        status_stats=status_stats,
    )


if __name__ == "__main__":
    app.run(debug=True)

