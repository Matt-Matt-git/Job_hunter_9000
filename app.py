from flask import Flask, render_template, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from collections import defaultdict
from flask_migrate import Migrate

GHOSTING_THRESHOLDS = {
    "Pharmaceutical": 28,
    "Biotech": 28,
    "Chemical": 21,
    "Food & Beverage": 21,
    "Finance": 21,
    "Technology": 14,
    "Retail": 7,
    "Hospitality": 7,
    "Healthcare": 21,
    "Academic/Research": 56,
    "Engineering": 21,
    "Legal": 21,
    "Marketing": 14,
    "Other": 21
}

app = Flask(__name__)
app.secret_key = "your_secret_key"

filepath = os.path.dirname(__file__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(filepath, "jobs.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    notes = db.Column(db.String)
    industry = db.Column(db.String, nullable=True)
    source = db.Column(db.String, nullable=True)
    contact_name = db.Column(db.String, nullable=True)
    contact_email = db.Column(db.String, nullable=True)
    salary = db.Column(db.String, nullable=True)
    job_url = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    closing_date = db.Column(db.String, nullable=True)
    ghosted = db.Column(db.Boolean, default = False)
    history = db.relationship('StatusHistory', backref='job', lazy=True, cascade="all, delete-orphan")

class StatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String, nullable=False)
    changed_date = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    notes_at_change = db.Column(db.String, nullable=True)

@app.route("/add", methods=["POST"])
def add_route():
    company = request.form["company"]
    job_title = request.form["title"]
    status = request.form["status"]
    date = request.form["date"]
    notes = request.form["notes"]
    industry = request.form.get("industry", "")
    source = request.form.get("source", "")
    contact_name = request.form.get("contact_name", "")
    contact_email = request.form.get("contact_email", "")
    salary = request.form.get("salary", "")
    job_url = request.form.get("job_url", "")
    location = request.form.get("location", "")
    closing_date = request.form.get("closing_date", "")

    new_job = Job(
        company=company,
        job_title=job_title,
        status=status,
        date=date,
        notes=notes,
        industry=industry,
        source=source,
        contact_name=contact_name,
        contact_email=contact_email,
        salary=salary,
        job_url=job_url,
        location=location,
        closing_date=closing_date
    )
    db.session.add(new_job)

    history = StatusHistory(
        job=new_job,
        status=status,
        changed_date=date,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        notes_at_change=""
    )
    db.session.add(history)
    
    db.session.commit()
    flash("Job added successfully")
    return redirect("/")
""
@app.route("/delete", methods=["POST"])
def delete_route():
    job_id = request.form["index"]
    job = Job.query.get(job_id)
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted successfully")
    return redirect("/")

@app.route("/update", methods=["POST"])
def update_route():
    job_id = request.form["index"]
    job = Job.query.get(job_id)
    
    old_status = job.status
    new_status = request.form["status"]
    
    job.company = request.form["company"]
    job.job_title = request.form["title"]
    job.status = new_status
    job.date = request.form["date"]
    job.notes = request.form["notes"]
    job.industry = request.form.get("industry", "")
    job.source = request.form.get("source", "")
    job.contact_name = request.form.get("contact_name", "")
    job.contact_email = request.form.get("contact_email", "")
    job.salary = request.form.get("salary", "")
    job.job_url = request.form.get("job_url", "")
    job.location = request.form.get("location", "")
    job.closing_date = request.form.get("closing_date", "")
    
    if old_status != new_status:
        history = StatusHistory(
            job=job,
            status=new_status,
            changed_date=datetime.now().strftime("%Y-%m-%d"),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            notes_at_change=request.form.get("status_notes", "")
        )
        db.session.add(history)
    db.session.commit()

    flash("Job updated successfully")
    return redirect("/")

@app.route("/")
def index():
    jobs = Job.query.all()
    jobs_history = StatusHistory.query.all()
    
    num_interview = set()
    for history in jobs_history:
        if history.status == 'Interview':
            num_interview.add(history.job_id)

    num_rejected = set()
    for history in jobs_history:
        if history.status == 'Rejected':
            num_rejected.add(history.job_id)

    num_ghosted = 0
    for job in jobs:
        threshold = GHOSTING_THRESHOLDS.get(job.industry, 21)
        if job.status in ["Applied", "Interview"]:
            date = datetime.strptime(job.date, "%Y-%m-%d")
            days_since = (datetime.now() - date).days
            if days_since >= threshold:
                num_ghosted += 1
                job.ghosted=True
            else:
                job.ghosted=False
    db.session.commit()

    total = len(jobs)
    applied = sum(1 for job in jobs if job.status == "Applied")
    interview = len(num_interview)
    rejected = len(num_rejected)
    rejection_rate = round((rejected / total * 100), 1) if total > 0 else 0
    interview_rate = round((interview / total * 100), 1) if total > 0 else 0
    

    monthly = defaultdict(int)
    weekly = defaultdict(int)
    daily = defaultdict(int)

    for job in jobs:
        date = datetime.strptime(job.date, "%Y-%m-%d")
        monthly[date.strftime("%Y-%m")] += 1
        weekly[date.strftime("%Y-W%W")] += 1
        daily[date.strftime("%Y-%m-%d")] += 1
    
    chart_labels_M = sorted(monthly.keys())
    chart_labels_W = sorted(weekly.keys())
    chart_labels_D = sorted(daily.keys())

    return render_template("index.html",
        jobs=jobs,
        total=total,
        applied=applied,
        interview=interview,
        rejected=rejected,
        rejection_rate=rejection_rate,
        interview_rate=interview_rate,
        ghosted = num_ghosted,

        chart_labels_M=chart_labels_M,
        chart_data_M=[monthly[k] for k in chart_labels_M],
        chart_labels_W=chart_labels_W,
        chart_data_W=[weekly[k] for k in chart_labels_W],
        chart_labels_D=chart_labels_D,
        chart_data_D=[daily[k] for k in chart_labels_D],
    )

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)