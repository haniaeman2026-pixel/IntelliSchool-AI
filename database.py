import sqlite3
from pathlib import Path
from datetime import date, datetime

DB_PATH = Path(__file__).resolve().parent / "school.db"

def connect():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db

def query(sql, params=()):
    with connect() as db:
        return [dict(r) for r in db.execute(sql, params).fetchall()]

def audit(actor, action, detail):
    with connect() as db:
        db.execute("INSERT INTO audit_log(actor,action,detail,created_at) VALUES(?,?,?,?)",
                   (actor, action, detail, datetime.now().isoformat(timespec="seconds")))

def init_db():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS students(
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, grade TEXT NOT NULL,
          guardian TEXT NOT NULL, email TEXT NOT NULL DEFAULT '', fee_total REAL NOT NULL DEFAULT 10000,
          fee_paid REAL NOT NULL DEFAULT 0, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS attendance(
          id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL REFERENCES students(id),
          day TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('Present','Absent','Late')),
          actor TEXT NOT NULL, UNIQUE(student_id,day));
        CREATE TABLE IF NOT EXISTS payments(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          student_id INTEGER NOT NULL REFERENCES students(id),
          amount REAL NOT NULL CHECK(amount > 0),
          method TEXT NOT NULL DEFAULT 'Cash',
          actor TEXT NOT NULL DEFAULT 'Admin',
          reference TEXT NOT NULL DEFAULT '',
          paid_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS results(
          id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL REFERENCES students(id),
          subject TEXT NOT NULL, marks REAL NOT NULL CHECK(marks>=0 AND marks<=100),
          updated_at TEXT NOT NULL, UNIQUE(student_id,subject));
        CREATE TABLE IF NOT EXISTS notices(
          id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, body TEXT NOT NULL,
          audience TEXT NOT NULL, created_by TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS audit_log(
          id INTEGER PRIMARY KEY AUTOINCREMENT, actor TEXT NOT NULL, action TEXT NOT NULL,
          detail TEXT NOT NULL, created_at TEXT NOT NULL);
        """)
        if db.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
            now=datetime.now().isoformat(timespec="minutes")
            people=[
              ("Ayesha Khan","Grade 8","Mrs. Khan","ayesha.parent@example.com",12000,12000),
              ("Sara Ahmed","Grade 7","Mr. Ahmed","sara.parent@example.com",12000,6000),
              ("Mariam Ali","Grade 9","Mrs. Ali","mariam.parent@example.com",15000,15000),
              ("Zoya Malik","Grade 8","Mr. Malik","zoya.parent@example.com",12000,3000),
              ("Hiba Noor","Grade 6","Mrs. Noor","hiba.parent@example.com",10000,10000)]
            db.executemany("INSERT INTO students(name,grade,guardian,email,fee_total,fee_paid,created_at) VALUES(?,?,?,?,?,?,?)",
                           [(*p,now) for p in people])
            db.executemany("INSERT INTO attendance(student_id,day,status,actor) VALUES(?,?,?,?)",
                           [(1,date.today().isoformat(),"Present","Admin"),(2,date.today().isoformat(),"Absent","Admin"),
                            (3,date.today().isoformat(),"Present","Admin"),(4,date.today().isoformat(),"Present","Admin"),
                            (5,date.today().isoformat(),"Late","Admin")])
            db.executemany("INSERT INTO results(student_id,subject,marks,updated_at) VALUES(?,?,?,?)",
                           [(1,"Science",88,now),(1,"Mathematics",91,now),(2,"Science",72,now),
                            (3,"English",94,now),(4,"Mathematics",79,now),(5,"Science",85,now)])
            db.execute("INSERT INTO notices(title,body,audience,created_by,created_at) VALUES(?,?,?,?,?)",
                       ("Welcome to IntelliSchool","This is a sample notice for the demo portal.","All","Admin",now))

def dashboard():
    with connect() as db:
        total=db.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        present=db.execute("SELECT COUNT(*) FROM attendance WHERE day=? AND status='Present'",(date.today().isoformat(),)).fetchone()[0]
        absent=db.execute("SELECT COUNT(*) FROM attendance WHERE day=? AND status='Absent'",(date.today().isoformat(),)).fetchone()[0]
        due=db.execute("SELECT COUNT(*) FROM students WHERE fee_paid<fee_total").fetchone()[0]
        amount=db.execute("SELECT COALESCE(SUM(fee_total-fee_paid),0) FROM students").fetchone()[0]
    return {"students":total,"present_today":present,"absent_today":absent,"students_with_dues":due,"total_dues":amount}

def students():
    return query("SELECT id,name,grade,guardian,email,fee_total,fee_paid,(fee_total-fee_paid) balance FROM students ORDER BY grade,name")

def student(student_id):
    found=query("SELECT * FROM students WHERE id=?",(student_id,))
    return found[0] if found else None

def add_student(d):
    with connect() as db:
        cur=db.execute("INSERT INTO students(name,grade,guardian,email,fee_total,fee_paid,created_at) VALUES(?,?,?,?,?,?,?)",
            (d["name"].strip(),d["grade"].strip(),d["guardian"].strip(),d.get("email","").strip(),d.get("fee_total",10000),0,datetime.now().isoformat(timespec="minutes")))
        sid=cur.lastrowid
    audit(d.get("actor","Admin"),"student_created",f"Student ID {sid}: {d['name']}")
    return {"ok":True,"id":sid,"message":"Student record created."}

def attendance(day=None):
    day=day or date.today().isoformat()
    return query("""SELECT a.student_id,s.name,s.grade,a.day,a.status,a.actor FROM attendance a
                    JOIN students s ON s.id=a.student_id WHERE a.day=? ORDER BY s.grade,s.name""",(day,))

def update_attendance(student_id,status,day=None,actor="Admin"):
    if status not in {"Present","Absent","Late"}: raise ValueError("Choose Present, Absent, or Late.")
    if not student(student_id): raise ValueError("Student not found.")
    day=day or date.today().isoformat()
    with connect() as db:
        db.execute("""INSERT INTO attendance(student_id,day,status,actor) VALUES(?,?,?,?)
        ON CONFLICT(student_id,day) DO UPDATE SET status=excluded.status,actor=excluded.actor""",(student_id,day,status,actor))
    audit(actor,"attendance_updated",f"Student ID {student_id}: {status} on {day}")
    return {"ok":True,"message":f"Attendance saved as {status}.","date":day}

def fees():
    return query("""SELECT id student_id,name,grade,fee_total,fee_paid,(fee_total-fee_paid) balance,
       CASE WHEN fee_paid>=fee_total THEN 'Paid' ELSE 'Due' END status FROM students ORDER BY balance DESC,name""")

def payment(student_id, amount, method="Cash", actor="Admin", reference=""):
    if amount <= 0:
        raise ValueError("Payment must be greater than zero.")
    method = (method or "Cash").strip()[:40]
    reference = (reference or "").strip()[:120]
    with connect() as db:
        row = db.execute("SELECT id, fee_total, fee_paid FROM students WHERE id=?", (student_id,)).fetchone()
        if not row:
            raise ValueError("Student not found.")
        balance = float(row["fee_total"]) - float(row["fee_paid"])
        if amount > balance:
            raise ValueError("Payment cannot exceed remaining balance.")
        now = datetime.now().isoformat(timespec="seconds")
        db.execute("UPDATE students SET fee_paid=fee_paid+? WHERE id=?", (amount, student_id))
        cur = db.execute(
            "INSERT INTO payments(student_id,amount,method,actor,reference,paid_at) VALUES(?,?,?,?,?,?)",
            (student_id, amount, method, actor, reference, now))
        payment_id = cur.lastrowid
    audit(actor, "fee_payment_recorded", f"Payment ID {payment_id}; Student ID {student_id}: {amount:.2f} via {method}")
    return {"ok": True, "payment_id": payment_id,
            "message": f"Payment of Rs. {amount:,.2f} recorded.",
            "remaining_balance": round(balance - amount, 2)}

def payment_records():
    return query("""SELECT p.id, p.student_id, s.name, s.grade, p.amount, p.method,
                         p.reference, p.actor, p.paid_at
                  FROM payments p JOIN students s ON s.id=p.student_id
                  ORDER BY p.id DESC LIMIT 500""")

def results():
    return query("""SELECT r.student_id,s.name,s.grade,r.subject,r.marks,r.updated_at FROM results r
                    JOIN students s ON s.id=r.student_id ORDER BY s.grade,s.name,r.subject""")

def save_marks(student_id,subject,marks,actor="Teacher"):
    if not student(student_id): raise ValueError("Student not found.")
    if not 0<=marks<=100: raise ValueError("Marks must be between 0 and 100.")
    with connect() as db:
        db.execute("""INSERT INTO results(student_id,subject,marks,updated_at) VALUES(?,?,?,?)
        ON CONFLICT(student_id,subject) DO UPDATE SET marks=excluded.marks,updated_at=excluded.updated_at""",
        (student_id,subject.strip(),marks,datetime.now().isoformat(timespec="minutes")))
    audit(actor,"marks_updated",f"Student ID {student_id}: {subject} = {marks}")
    return {"ok":True,"message":"Marks saved successfully."}

def notices():
    return query("SELECT id,title,body,audience,created_by,created_at FROM notices ORDER BY id DESC")

def add_notice(title,body,audience="All",actor="Admin"):
    if not title.strip() or not body.strip(): raise ValueError("Notice title and body are required.")
    with connect() as db:
        cur=db.execute("INSERT INTO notices(title,body,audience,created_by,created_at) VALUES(?,?,?,?,?)",
            (title.strip(),body.strip(),audience,actor,datetime.now().isoformat(timespec="minutes")))
    audit(actor,"notice_created",f"Notice ID {cur.lastrowid}: {title}")
    return {"ok":True,"id":cur.lastrowid,"message":"Notice published in the prototype portal."}
