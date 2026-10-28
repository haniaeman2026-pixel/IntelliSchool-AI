from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import database
from schemas import AgentRequest, StudentCreate, AttendanceUpdate, PaymentCreate, MarksUpdate, NoticeCreate
from agent import run_agent

BASE=Path(__file__).resolve().parent
load_dotenv(BASE/".env")
app=FastAPI(title="IntelliSchool AI",version="2.0.0")
app.mount("/static",StaticFiles(directory=BASE/"static"),name="static")

@app.on_event("startup")
def startup(): database.init_db()

@app.get("/",response_class=HTMLResponse)
def home(): return (BASE/"static"/"index.html").read_text(encoding="utf-8")

@app.get("/api/health")
def health(): return {"status":"ok","service":"IntelliSchool AI"}

@app.get("/api/dashboard")
def get_dashboard(): return database.dashboard()

@app.get("/api/students")
def get_students(): return database.students()

@app.post("/api/students")
def create_student(payload:StudentCreate):
    try: return database.add_student(payload.model_dump())
    except ValueError as e: raise HTTPException(status_code=400,detail=str(e))

@app.get("/api/attendance")
def get_attendance(day:str|None=None): return database.attendance(day)

@app.post("/api/attendance")
def post_attendance(payload:AttendanceUpdate):
    try: return database.update_attendance(payload.student_id,payload.status,payload.date,payload.actor)
    except ValueError as e: raise HTTPException(status_code=400,detail=str(e))

@app.get("/api/fees")
def get_fees(): return database.fees()

@app.get("/api/payments")
def get_payments(): return database.payment_records()

@app.post("/api/payments")
def post_payment(payload:PaymentCreate):
    try: return database.payment(payload.student_id,payload.amount,payload.method,payload.actor,payload.reference)
    except ValueError as e: raise HTTPException(status_code=400,detail=str(e))

@app.get("/api/results")
def get_results(): return database.results()

@app.post("/api/results")
def post_results(payload:MarksUpdate):
    try: return database.save_marks(payload.student_id,payload.subject,payload.marks,payload.actor)
    except ValueError as e: raise HTTPException(status_code=400,detail=str(e))

@app.get("/api/notices")
def get_notices(): return database.notices()

@app.post("/api/notices")
def post_notice(payload:NoticeCreate):
    try: return database.add_notice(payload.title,payload.body,payload.audience,payload.actor)
    except ValueError as e: raise HTTPException(status_code=400,detail=str(e))

@app.post("/api/agent")
def post_agent(payload:AgentRequest): return run_agent(payload.message,payload.role,payload.approved)
