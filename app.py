from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from function import add, delete, edit, update 
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

filepath = os.path.dirname(__file__)
csv_path = os.path.join(filepath, "info.csv")
Jobs_df = pd.read_csv(csv_path)

filepath = os.path.dirname(__file__)
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
    history = db.relationship('StatusHistory', backref='job', lazy=True)

class StatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String, nullable=False)
    changed_date = db.Column(db.String, nullable=False)

@app.route("/add", methods=["POST"])
def add_route():
    global Jobs_df
    Jobs_df, response = add(Jobs_df, csv_path)
    flash("Job added successfully")
    return response

@app.route("/delete", methods=["POST"])
def delete_route():
    global Jobs_df
    Jobs_df, response = delete(Jobs_df, csv_path)
    flash("Job deleted successfully")
    return response

@app.route("/update", methods=["POST"])
def update_route():
    global Jobs_df
    Jobs_df, response = update(Jobs_df, csv_path)
    flash("Job editted successfully")
    return response

@app.route("/")
def index():
    total = len(Jobs_df)
    applied = len(Jobs_df[Jobs_df["Status"] == "Applied"])
    interview = len(Jobs_df[Jobs_df["Status"] == "Interview"])
    rejected = len(Jobs_df[Jobs_df["Status"] == "Rejected"])
    rejection_rate = round((rejected / total * 100), 1) if total > 0 else 0
    interview_rate = round((interview / total * 100), 1) if total > 0 else 0

    temp_df = Jobs_df.copy()
    temp_df["Application date"] = pd.to_datetime(temp_df["Application date"])
    monthly = temp_df.groupby(temp_df["Application date"].dt.to_period("M")).size()
    weekly = temp_df.groupby(temp_df["Application date"].dt.to_period("W")).size()
    daily = temp_df.groupby(temp_df["Application date"].dt.to_period("D")).size()
    
    chart_labels_M = [str(p) for p in monthly.index]
    chart_data_M = monthly.tolist()
    chart_labels_W = [str(p) for p in weekly.index]
    chart_data_W = weekly.tolist()
    chart_labels_D = [str(p) for p in daily.index]
    chart_data_D = daily.tolist()

    return render_template("index.html", 
        jobs=Jobs_df.to_dict("records"),
        total=total,
        applied=applied,
        interview=interview,
        rejected=rejected,
        rejection_rate=rejection_rate,
        interview_rate=interview_rate,
        chart_labels_M=chart_labels_M,
        chart_data_M=chart_data_M,
        chart_labels_W=chart_labels_W,
        chart_data_W=chart_data_W,
        chart_labels_D=chart_labels_D,  # ← add these
        chart_data_D=chart_data_D,
    )

if __name__ == "__main__":
    app.run(debug=True)