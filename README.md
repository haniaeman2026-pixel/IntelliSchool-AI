# IntelliSchool AI — Intelligent School Management System

A professional, responsive school management dashboard prototype with light/dark themes. The existing FastAPI + SQLite + LangGraph workflow is retained.

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` and API docs at `http://127.0.0.1:8000/docs`.

## Connected modules
- Student records and add-student form
- Attendance register and status updates
- Fee balances and payment recording
- Exams/results and marks entry
- School notices
- LangGraph agent workspace with approval flow
- Light/dark theme with saved preference

## UI notes
Teacher directory and Classes & Timetable are clearly marked as preview modules because there are no connected backend endpoints for those areas in this prototype. The weekly line chart is illustrative; dashboard counts and fee figures are read from the local database.

## Prototype limitations
The role selector is for demonstration only, not secure authentication. Do not use this prototype with real student data or for production school operations without authentication, authorization, privacy controls, validation, backups, and security review.
