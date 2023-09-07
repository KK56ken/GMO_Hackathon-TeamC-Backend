from fastapi import FastAPI
from typing import List
from database import Engine, Base
import routers

app = FastAPI()
app.include_router(routers.authentication.router)
app.include_router(routers.task.router)
app.include_router(routers.user.router)

Base.metadata.create_all(Engine)

@app.get("/")
def read_root():
    return {"status": "ok"}