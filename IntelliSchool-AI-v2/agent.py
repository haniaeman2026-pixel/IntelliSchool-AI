from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import database

PERMISSIONS = {
    "Admin": {"student","attendance","fees","results","notice","update_attendance"},
    "Teacher": {"student","attendance","results","update_attendance"},
    "Student": {"own_record"},
    "Parent": {"own_record"},
}

class AgentState(TypedDict, total=False):
    message: str
    role: str
    intent: str
    allowed: bool
    data: object
    needs_approval: bool
    approved: bool
    action_done: bool
    answer: str
    student_id: int
    student_name: str
    target_status: str

def classify(state):
    text=state["message"].lower()
    if any(x in text for x in ["mark present","mark absent","update attendance","change attendance"]): intent="update_attendance"
    elif any(x in text for x in ["attendance","present today","absent today"]): intent="attendance"
    elif any(x in text for x in ["fee","fees","dues","payment"]): intent="fees"
    elif any(x in text for x in ["result","marks","score","exam"]): intent="results"
    elif any(x in text for x in ["student","record","profile","list students"]): intent="student"
    elif any(x in text for x in ["notice","announcement","circular"]): intent="notice"
    else: intent="help"
    return {"intent":intent}

def check_permissions(state):
    role=state.get("role","Admin")
    intent=state.get("intent","help")
    return {"allowed": intent=="help" or intent in PERMISSIONS.get(role,set())}

def retrieve(state):
    intent=state.get("intent")
    text=state.get("message","").lower()
    if intent=="student": data=database.students()
    elif intent=="attendance": data=database.attendance()
    elif intent=="fees": data=database.fees()
    elif intent=="results": data=database.results()
    elif intent=="update_attendance":
        match=next((s for s in database.students() if s["name"].lower() in text),None)
        return {"data":match,"student_id":match["id"] if match else 0,
                "student_name":match["name"] if match else "",
                "target_status":"Absent" if "absent" in text else "Present","needs_approval":True}
    else: data=None
    return {"data":data}

def decide(state):
    if not state.get("allowed",False):
        return {"answer":f"Access denied: the {state.get('role','user')} demo role cannot perform this request."}
    intent=state.get("intent")
    if intent=="help":
        return {"answer":"I can summarize attendance, fee dues, student records and exam results. I can also request an attendance update, which needs approval before changing the database."}
    if intent=="notice":
        return {"answer":"Use the Notices module to create a school notice. Official communications should be checked by authorized staff before publication."}
    if intent=="update_attendance":
        if not state.get("data"): return {"answer":"Student not identified. Try the exact sample name, such as Sara Ahmed."}
        return {"answer":f"Requested change: {state['student_name']} (ID {state['student_id']}) → {state['target_status']}. Please approve before the record changes.","needs_approval":True}
    data=state.get("data") or []
    if intent=="attendance":
        present=sum(x["status"]=="Present" for x in data); absent=sum(x["status"]=="Absent" for x in data); late=sum(x["status"]=="Late" for x in data)
        answer=f"Today's attendance: {present} present, {absent} absent, {late} late across {len(data)} recorded entries."
    elif intent=="fees":
        due=[x for x in data if x["balance"]>0]
        answer=f"Fee summary: {len(due)} students have outstanding balances totalling Rs. {sum(x['balance'] for x in due):,.0f}."
    elif intent=="results":
        avg=sum(x["marks"] for x in data)/len(data) if data else 0
        answer=f"There are {len(data)} recorded subject results. Average recorded mark: {avg:.1f}/100."
    else: answer=f"The school database currently contains {len(data)} student records."
    return {"answer":answer}

def act(state):
    if state.get("intent")!="update_attendance" or not state.get("allowed"): return {}
    if not state.get("approved"): return {"action_done":False}
    sid=state.get("student_id")
    if not sid: return {"answer":"No student matched; no change was made.","action_done":False,"needs_approval":False}
    result=database.update_attendance(sid,state["target_status"],actor=state.get("role","Admin"))
    return {"answer":result["message"],"action_done":True,"needs_approval":False}

def build_graph():
    graph=StateGraph(AgentState)
    graph.add_node("classify",classify)
    graph.add_node("permissions",check_permissions)
    graph.add_node("retrieve",retrieve)
    graph.add_node("decide",decide)
    graph.add_node("act",act)
    graph.add_edge(START,"classify")
    graph.add_edge("classify","permissions")
    graph.add_edge("permissions","retrieve")
    graph.add_edge("retrieve","decide")
    graph.add_edge("decide","act")
    graph.add_edge("act",END)
    return graph.compile()

def run_agent(message,role="Admin",approved=False):
    state=build_graph().invoke({"message":message,"role":role,"approved":approved})
    return {"answer":state.get("answer","Request completed."),
            "intent":state.get("intent","help"),
            "needs_approval":state.get("needs_approval",False),
            "action_done":state.get("action_done",False),
            "role":role,"workflow":["classify","permissions","retrieve","decide","act"],
            "note":"Sample data only. The role selector is a demonstration, not secure login."}
