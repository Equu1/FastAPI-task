from fastapi import FastAPI
from app.routers import tasks, pomodoro

app = FastAPI()

app.include_router(tasks.router, tags=["Tasks"])
app.include_router(pomodoro.router, tags=["Pomodoro"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
