from fastapi import Depends, FastAPI, HTTPException, Security, Body
from fastapi.security.api_key import APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from passlib.context import CryptContext
from typing import List

import models
from routers import test
from util import util

import schemas
from database import Engine, Base, SessionLocal
from sqlalchemy.orm import Session

correct_key: str = util.get_apikey()
api_key_header = APIKeyHeader(name='Authorization', auto_error=False)

async def get_api_key(
    api_key_header: str = Security(api_key_header),
    ):
    if api_key_header == correct_key:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

app = FastAPI()
app.include_router(test.router, dependencies=[Depends(get_api_key)], tags=["Test"])

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

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/auth")
async def authorization(request: schemas.User, db: Session = Depends(get_db)):
    hashdPasswoed = pwd_cxt.hash(request.password)
    new_user = models.User(email=request.email, password=hashdPasswoed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return 

@app.get("/profile")
def showAllUsers(db: Session = Depends(get_db)):
    users = List[schemas.ShowUser]
    tmp_users = db.query(models.User.id, models.User.name, models.User.status)
    for user in tmp_users:
        titles = db.query(models.Task.title).filter(user_id = user.id).all
        tmp_showuser = schemas.ShowUser
        tmp_showuser.user_id = user.user_id
        tmp_showuser.user_name = user.name
        tmp_showuser.status = user.status
        tmp_showuser.tasks = titles
        users.append(tmp_showuser)
    return users
