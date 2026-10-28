
<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:101828,50:23395B,100:101828&height=180&section=header&text=INTELLISCHOOL%20AI&fontSize=38&fontColor=FFFFFF&fontAlignY=42&desc=SMART%20SCHOOL%20MANAGEMENT%20SYSTEM&descSize=14&descAlignY=65&animation=fadeIn" width="100%" alt="IntelliSchool AI Header" />

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=17&duration=3000&pause=900&color=3B82F6&center=true&vCenter=true&width=650&lines=Intelligent+School+Management;Student+Records+%7C+Attendance+%7C+Fees;Results+%7C+Notices+%7C+AI+Agent;Powered+by+FastAPI+%26+LangGraph" alt="Typing Animation" />

<br/>

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langchain&logoColor=white" alt="LangGraph" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript" />
</p>

**A smarter way to manage school operations.**

</div>

---

## 📌 Overview

**IntelliSchool AI** is an AI-assisted school management system designed to organize essential academic and administrative operations through a unified web interface.

It combines a FastAPI backend, SQLite database, and a LangGraph-based agent workflow to support school data management and approval-based actions.

## ✨ Key Features

- **Dashboard** — Overview of student records and school statistics.
- **Student Management** — Add and manage student information.
- **Attendance Tracking** — Record and review daily attendance.
- **Fees & Payments** — Track fee balances and record payments.
- **Results Management** — Save and retrieve student marks.
- **Notice Board** — Create and manage school announcements.
- **AI Agent** — Process requests through classification, permission checks, decision-making, and actions.
- **Input Validation** — Validate incoming data using Pydantic schemas.

## ⚙️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API and application server |
| SQLite | Local database storage |
| Pydantic | Request validation and data schemas |
| LangGraph | Agent workflow orchestration |
| HTML, CSS & JavaScript | Web interface |

## 🔄 System Workflow

<div align="center">

`User Interface` → `FastAPI Backend` → `Validation & Agent Logic` → `SQLite Database` → `Response`

</div>

### AI Agent Workflow

`User Request` → `Classify` → `Check Permissions` → `Retrieve Data` → `Decide` → `Act / Request Approval` → `Final Response`

The current agent uses rule-based intent classification within a LangGraph workflow. It is a prototype and does not represent a fully autonomous or production-secured AI system.

## 📁 Project Structure

```text
IntelliSchool-AI-v2/
├── static/
│   └── index.html
├── tests/
│   └── test_workflow.py
├── agent.py
├── database.py
├── main.py
├── schemas.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/haniaeman2026-pixel/IntelliSchool-AI.git
cd IntelliSchool-AI/IntelliSchool-AI-v2
```

### 2. Create a Virtual Environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file using `.env.example` as a template. Add your own API key only if required by your configuration.

**Never commit `.env` or expose API keys publicly.**

### 5. Run the Application

```bash
python -m uvicorn main:app --reload
```

Open the application at:

- **Web Interface:** http://127.0.0.1:8000
- **API Documentation:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/api/health

## 🧪 Testing

Run the available tests with:

```bash
python -m pytest -q
```

## 🔐 Security Notes

- Keep API keys in your local `.env` file.
- Commit `.env.example` with placeholder values only.
- Keep `.env`, virtual environments, Python cache files, and local database files out of public Git history.
- Treat role-based permissions in this academic prototype as demonstration logic, not production-grade authentication.

## 🎯 Project Objective

To demonstrate how a web-based school management application can combine structured data management with a workflow-driven AI agent for administrative assistance.

## 👩‍💻 Developer

<div align="center">

**Developed by Hania Eman**

*AI & Data Science Student | Python Developer*

<br/>

<a href="https://github.com/haniaeman2026-pixel">
  <img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github" alt="GitHub Profile" />
</a>

<br/><br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:101828,50:23395B,100:101828&height=70&section=footer" width="100%" alt="Footer" />

</div>
