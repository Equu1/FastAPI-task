from fastapi import APIRouter, HTTPException
from app.models.task import TaskCreate, TaskUpdate
from app.db.tasks_db import tasks

router = APIRouter()

@router.post("/tasks")
def create_task(task: TaskCreate):
    if any(t["title"] == task.title for t in tasks):
        raise HTTPException(status_code=400, detail="Title must be unique")
    task_id = len(tasks) + 1
    new_task = task.dict()
    new_task["id"] = task_id
    tasks.append(new_task)
    return new_task

@router.get("/tasks")
def get_tasks(status: str = None):
    if status:
        return [task for task in tasks if task["status"] == status]
    return tasks

@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_id}")
def update_task(task_id: int, updates: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if updates.title and any(t["title"] == updates.title for t in tasks if t["id"] != task_id):
                raise HTTPException(status_code=400, detail="Title must be unique")
            task.update(updates.dict(exclude_unset=True))
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail="Task not found")
