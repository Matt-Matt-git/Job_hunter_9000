from flask import Flask, render_template, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

filepath = os.path.dirname(__file__)
csv_path = os.path.join(filepath, "info.csv")
Jobs_df = pd.read_csv(csv_path)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(filepath, "jobs.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    notes = db.Column(db.String)
    history = db.relationship('StatusHistory', backref='job', lazy=True, cascade="all, delete-orphan")

class StatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String, nullable=False)
    changed_date = db.Column(db.String, nullable=False)

@app.route("/add", methods=["POST"])
def add_route():
    company = request.form["company"]
    job_title = request.form["title"]
    status = request.form["status"]
    date = request.form["date"]
    notes = request.form["notes"]

    new_job = Job(
        company=company,
        job_title=job_title,
        status=status,
        date=date,
        notes=notes
    )
    db.session.add(new_job)

    history = StatusHistory(
        job=new_job,
        status=status,
        changed_date=date
    )
    db.session.add(history)
    
    db.session.commit()
    flash("Job added successfully")
    return redirect("/")

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
    
    if old_status != new_status:
        history = StatusHistory(
            job=job,
            status=new_status,
            changed_date=datetime.now().strftime("%Y-%m-%d")
        )
        db.session.add(history)
    db.session.commit()

    flash("Job updated successfully")
    return redirect("/")

@app.route("/")
def index():
    jobs = Job.query.all()
    
    total = len(jobs)
    applied = sum(1 for job in jobs if job.status == "Applied")
    interview = sum(1 for job in jobs if job.status == "Interview")
    rejected = sum(1 for job in jobs if job.status == "Rejected")
    rejection_rate = round((rejected / total * 100), 1) if total > 0 else 0
    interview_rate = round((interview / total * 100), 1) if total > 0 else 0

    return render_template("index.html",
        jobs=jobs,
        total=total,
        applied=applied,
        interview=interview,
        rejected=rejected,
        rejection_rate=rejection_rate,
        interview_rate=interview_rate,
        chart_labels_M=[],
        chart_data_M=[],
        chart_labels_W=[],
        chart_data_W=[],
        chart_labels_D=[],
        chart_data_D=[],
    )

with app.app_context():
    db.create_all()
     # only migrate if database is empty
    if Job.query.count() == 0:
        for _, row in Jobs_df.iterrows():
            job = Job(
                company=row["Company"],
                job_title=row["Job Title"],
                status=row["Status"],
                date=str(row["Application date"]),
                notes=row["Notes"] if pd.notna(row["Notes"]) else ""
            )
            db.session.add(job)
            
            # add initial status to history
            history = StatusHistory(
                job=job,
                status=row["Status"],
                changed_date=str(row["Application date"])
            )
            db.session.add(history)
        
        db.session.commit()
        print("Migration complete!")

if __name__ == "__main__":
    app.run(debug=True)