from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN

import models
from util import util

import schemas
from database import Engine, Base, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

Base.metadata.create_all(Engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/users")
async def create_user(user: schemas.Users, db: Session = Depends(get_db)):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        token=user.token,
        status=user.status,
        department_id=user.department_id,
        slack_id=user.slack_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user