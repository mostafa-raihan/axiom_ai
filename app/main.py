from fastapi import FastAPI
import sqlite3
import os
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))


app = FastAPI(
    title="Axiom AI",
    description="AI Job Market Analyzer",
    version="1.0.0"
)

DATABASE = os.path.join(os.path.dirname(__file__), "..", "axiom.db")

def get_jobs_from_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jobs

# Root endpoint
@app.get("/")
def root():
    return {
        "name": "Axiom AI",
        "description": "AI Job Market Analyzer",
        "endpoints": ["/jobs", "/jobs/count", "/jobs/locations"]
    }

# Get all jobs
@app.get("/jobs")
def get_jobs():
    jobs = get_jobs_from_db()
    return {"total": len(jobs), "jobs": jobs}

# Get total count
@app.get("/jobs/count")
def get_count():
    jobs = get_jobs_from_db()
    return {"total_jobs": len(jobs)}

# Get all locations
@app.get("/jobs/locations")
def get_locations():
    jobs = get_jobs_from_db()
    locations = {}
    for job in jobs:
        loc = job["location"] or "Unknown"
        locations[loc] = locations.get(loc, 0) + 1
    sorted_locations = dict(sorted(locations.items(), key=lambda x: x[1], reverse=True))
    return {"locations": sorted_locations}

# Search jobs by keyword
@app.get("/jobs/search/{keyword}")
def search_jobs(keyword: str):
    jobs = get_jobs_from_db()
    results = [
        job for job in jobs
        if keyword.lower() in job["title"].lower()
        or keyword.lower() in job["description"].lower()
    ]
    return {"keyword": keyword, "total": len(results), "jobs": results}

# Top skills in demand
@app.get("/jobs/skills")
def get_skills():
    jobs = get_jobs_from_db()
    skills = [
        "python", "sql", "java", "javascript", "react", "docker",
        "kubernetes", "aws", "azure", "machine learning", "ai",
        "fastapi", "django", "pytorch", "tensorflow", "git",
        "linux", "typescript", "nodejs", "mongodb"
    ]
    skill_count = {}
    for job in jobs:
        description = (job["description"] or "").lower()
        title = (job["title"] or "").lower()
        for skill in skills:
            if skill in description or skill in title:
                skill_count[skill] = skill_count.get(skill, 0) + 1

    sorted_skills = dict(sorted(skill_count.items(), key=lambda x: x[1], reverse=True))
    return {"total_jobs_analyzed": len(jobs), "skills_in_demand": sorted_skills}

# Top companies hiring
@app.get("/jobs/companies")
def get_companies():
    jobs = get_jobs_from_db()
    companies = {}
    for job in jobs:
        company = job["company"] or "Unknown"
        companies[company] = companies.get(company, 0) + 1
    sorted_companies = dict(sorted(companies.items(), key=lambda x: x[1], reverse=True)[:20])
    return {"top_companies": sorted_companies}

# Job titles in demand
@app.get("/jobs/titles")
def get_titles():
    jobs = get_jobs_from_db()
    titles = {}
    for job in jobs:
        title = job["title"] or "Unknown"
        titles[title] = titles.get(title, 0) + 1
    sorted_titles = dict(sorted(titles.items(), key=lambda x: x[1], reverse=True)[:20])
    return {"top_titles": sorted_titles}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open(os.path.join(os.path.dirname(__file__), "..", "templates", "index.html")) as f:
        return HTMLResponse(content=f.read())