from fastapi import FastAPI
from typing import List
from database import Engine, Base
from routers import authentication, task, user

app = FastAPI()
app.include_router(authentication.router)
app.include_router(task.router)
app.include_router(user.router)

Base.metadata.create_all(Engine)

@app.get("/")
def read_root():
    return {"status": "ok"}