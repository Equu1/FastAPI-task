from pydantic import BaseModel

class PomodoroCreate(BaseModel):
    task_id: int