# ⚡ Axiom AI — Job Market Analyzer

> Analyzes real-time job market data using FastAPI and SQLite

## 🚀 What It Does
- Fetches 100+ real job listings from live API
- Stores data in SQLite database
- Exposes REST API endpoints via FastAPI
- Interactive API documentation

## 🛠 Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root — API info |
| GET | `/jobs` | Get all jobs |
| GET | `/jobs/count` | Total job count |
| GET | `/jobs/locations` | Jobs by location |

## ⚙️ How to Run
```bash
# Clone the repo
git clone https://github.com/mostafa-raihan/axiom_ai.git
cd axiom_ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python3 app/database.py

# Fetch jobs
python3 app/fetcher.py

# Run the API
uvicorn app.main:app --reload
```

## 📖 API Docs
Visit `http://127.0.0.1:8000/docs` for interactive API documentation

## 👨‍💻 Author
**Mostafa Raihan** — AI & Data Engineering Student @ SAMK