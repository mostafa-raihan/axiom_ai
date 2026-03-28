import requests
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), "..", "axiom.db")

def fetch_jobs():
    print("Fetching jobs from API...")
    url = "https://arbeitnow.com/api/job-board-api"
    response = requests.get(url)
    data = response.json()
    jobs = data["data"]
    print(f"Found {len(jobs)} jobs!")
    return jobs

def save_jobs(jobs):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs")  # Clear old data
    for job in jobs:
        cursor.execute("""
            INSERT INTO jobs (title, company, location, description)
            VALUES (?, ?, ?, ?)
        """, (
            job.get("title"),
            job.get("company_name"),
            job.get("location"),
            job.get("description")
        ))
    conn.commit()
    conn.close()
    print(f"Saved {len(jobs)} jobs to database!")

if __name__ == "__main__":
    jobs = fetch_jobs()
    save_jobs(jobs)