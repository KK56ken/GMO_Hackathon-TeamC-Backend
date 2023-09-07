from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import Engine, Base
from routers import authentication, task, user, departments, skills

app = FastAPI()

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(authentication.router)
app.include_router(task.router)
app.include_router(user.router)
app.include_router(departments.router)
app.include_router(skills.router)

Base.metadata.create_all(Engine)

@app.get("/")
def read_root():
    return {"status": "ok"}