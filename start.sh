#!/bin/bash
python3 app/database.py
python3 app/fetcher.py
uvicorn app.main:app --host 0.0.0.0 --port 8000