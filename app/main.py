from fastapi import FastAPI
import sqlite3
import os

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