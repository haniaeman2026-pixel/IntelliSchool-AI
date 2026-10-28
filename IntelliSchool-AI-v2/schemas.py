from pydantic import BaseModel, Field

class AgentRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    role: str = "Admin"
    approved: bool = False

class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    grade: str = Field(min_length=2, max_length=30)
    guardian: str = Field(min_length=2, max_length=100)
    email: str = Field(default="", max_length=150)
    fee_total: float = Field(default=10000, ge=0, le=10000000)
    actor: str = "Admin"

class AttendanceUpdate(BaseModel):
    student_id: int = Field(ge=1)
    status: str
    date: str | None = None
    actor: str = "Admin"

class PaymentCreate(BaseModel):
    student_id: int = Field(ge=1)
    amount: float = Field(gt=0, le=10000000)
    method: str = "Cash"
    reference: str = Field(default="", max_length=120)
    actor: str = "Admin"

class MarksUpdate(BaseModel):
    student_id: int = Field(ge=1)
    subject: str = Field(min_length=2, max_length=60)
    marks: float = Field(ge=0, le=100)
    actor: str = "Teacher"

class NoticeCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    body: str = Field(min_length=2, max_length=3000)
    audience: str = "All"
    actor: str = "Admin"
