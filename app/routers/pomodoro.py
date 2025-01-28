from fastapi import APIRouter, HTTPException
from app.models.pomodoro import PomodoroCreate
from app.db.tasks_db import tasks
from app.db.pomodoro_db import pomodoro_sessions
from datetime import datetime

router = APIRouter()

@router.post("/pomodoro")
def create_pomodoro(pomodoro: PomodoroCreate):
    for task in tasks:
        if task["id"] == pomodoro.task_id:
            if any(
                session["task_id"] == pomodoro.task_id and session["end_time"] is None
                for session in pomodoro_sessions
            ):
                raise HTTPException(status_code=400, detail="Active timer already exists")
            new_session = {
                "task_id": pomodoro.task_id,
                "start_time": datetime.utcnow(),
                "end_time": None,
                "completed": False,
            }
            pomodoro_sessions.append(new_session)
            return new_session
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/pomodoro/{task_id}/stop")
def stop_pomodoro(task_id: int):
    for session in pomodoro_sessions:
        if session["task_id"] == task_id and session["end_time"] is None:
            session["end_time"] = datetime.utcnow()
            session["completed"] = True
            return session
    raise HTTPException(status_code=400, detail="No active timer found")

@router.get("/pomodoro/stats")
def get_pomodoro_stats():
    stats = {}
    total_time = 0
    for session in pomodoro_sessions:
        if session["completed"]:
            task_id = session["task_id"]
            duration = (session["end_time"] - session["start_time"]).total_seconds() / 60
            total_time += duration
            stats[task_id] = stats.get(task_id, 0) + 1
    return {
        "sessions_per_task": stats,
        "total_time": int(total_time)
    }
