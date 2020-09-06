import os, json
from exporter import save_to_file
from scrapper import get_all_jobs
from flask import Flask, render_template, request, redirect, send_file


os.system("clear")
app = Flask("SuperPythonJobSrapper")

db = {}


def json_writer(name, datas):
    try:
        with open(f"{name}.json", "w") as json_file:
            json.dump(datas, json_file)
    except:
        pass

    return


@app.after_request
def add_header(rqst):
    rqst.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    rqst.headers["Pragma"] = "no-cache"
    rqst.headers["Expires"] = "0"
    rqst.headers["Cache-Control"] = "public, max-age=0"
    return rqst


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scrap")
def scrap_result():
    try:
        job_name = request.args.get("job")
        existing_db = db.get(job_name)
        job_name = job_name.lower()
        jobs = []
        if existing_db:
            jobs = existing_db
        else:
            so_jobs, ww_jobs, ro_jobs = get_all_jobs(job_name)
            jobs = so_jobs + ww_jobs + ro_jobs
            db[job_name] = jobs
            json_writer(job_name, db)
        return render_template(
            "jobs.html",
            job_name=job_name,
            job_nums=len(jobs),
            jobs=jobs,
        )
    except Exception as e:
        print(str(e))
        return redirect("/")


@app.route("/export")
def export():
    try:
        job = request.args.get("job")
        if not job:
            raise Exception()
        job = job.lower()
        jobs = db.get(job)
        if not jobs:
            print("db 없음")
            print(jobs)
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except Exception as e:
        print(str(e))
        return redirect("/")


app.run(host="0.0.0.0")