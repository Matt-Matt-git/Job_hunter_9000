from flask import render_template, request, redirect

def add(Jobs_df, csv_path):
    company = request.form["company"]
    title = request.form["title"]
    status = request.form["status"]
    date = request.form["date"]
    notes = request.form["notes"]
    job = [company, title, status, date, notes]
    Jobs_df.loc[len(Jobs_df)] = job
    Jobs_df.to_csv(csv_path, index=False)
    return Jobs_df, redirect("/")

def delete(Jobs_df, csv_path):
    index = int(request.form["index"])
    Jobs_df = Jobs_df.drop(index)
    Jobs_df = Jobs_df.reset_index(drop=True)
    Jobs_df.to_csv(csv_path, index=False)
    return Jobs_df, redirect("/")

def edit(index, Jobs_df):
    index = int(index)
    job = Jobs_df.iloc[index].to_dict()
    return render_template("edit.html", job=job, index=index)

def update(Jobs_df, csv_path):
    index = int(request.form["index"])
    Jobs_df.loc[index, "Company"] = request.form["company"]
    Jobs_df.loc[index, "Job Title"] = request.form["title"]
    Jobs_df.loc[index, "Status"] = request.form["status"]
    Jobs_df.loc[index, "Application date"] = request.form["date"]
    Jobs_df.loc[index, "Notes"] = request.form["notes"]
    Jobs_df.to_csv(csv_path, index=False)
    return Jobs_df, redirect("/")
  













