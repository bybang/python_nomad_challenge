from flask import Flask, render_template, request, redirect, send_file
from extractors.rmok import extract_rmok_jobs
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app = Flask("JobScrapper", static_folder="static")

db = {}

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/search')
def search():
  search_term = request.args.get('term')
  if search_term == None:
    return redirect("/")
  if search_term in db:
    jobs = db[search_term]
  else:
    rmok = extract_rmok_jobs(search_term)
    wwr = extract_wwr_jobs(search_term)
    indeed = extract_indeed_jobs(search_term)
    
    jobs = rmok + wwr + indeed
    db[search_term] = jobs

  return render_template("search.html", term=search_term, jobs=jobs)

@app.route('/export')
def export():
  search_term = request.args.get('term')
  if search_term == None:
    return redirect("/")
  if search_term not in db:
    return redirect(f"/search?term={search_term}")
  save_to_file(search_term, db[search_term])
  return send_file(f"{search_term}.csv", as_attachment=True)

app.run("0.0.0.0")