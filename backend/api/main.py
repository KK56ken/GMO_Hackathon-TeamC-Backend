from fastapi import Depends, FastAPI, HTTPException, Security, Body, status, Response
from fastapi.security.api_key import APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from passlib.context import CryptContext
from typing import List
import bcrypt

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

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/signup")
async def signup(request: schemas.User, db: Session = Depends(get_db)):
    hashdPassword = pwd_cxt.hash(request.password)
    new_user = models.User(email=request.email, password=hashdPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return 

@app.get("/profile/{id}")
async def get_profile(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User.name, models.User.department_id, models.User.slack_id, models.User.status).filter(models.User.user_id == id).first()
    skill_set_id = db.query(models.UsersSkill.skill_id).filter(models.UsersSkill.user_id == id).all()
    skill_set = db.query(models.Skill.skill_name).filter(models.Skill.skill_id.in_(skill_set_id)).all()
    department = db.query(models.Department.department_name).filter(models.Department.department_id == user.department_id).first()
   
    temp_tasks = db.query(models.Task.task_id, models.Task.title, models.Task.user_id, models.Task.register_date, models.Task.concern_desc).filter(models.Task.user_id == id).all()
    tasks = []
    for tmp_task in temp_tasks:
        task_skill_ids = db.query(models.TaskSkill.skill_id).filter(models.TaskSkill.task_id.in_(tmp_task.task_id)).all()
        task_skill = db.query(models.Skill.skill_name).filter(models.Skill.skill_id.in_(task_skill_ids)).all()
        task = schemas.Task(task_id=tmp_task.task_id, title=tmp_task.title, user_name=user.name, skill_set=task_skill, task_date=tmp_task.register_date, concern_desc=tmp_task.concern_desc)
        tasks.append(task)
    return {"name": user.name, "department": department, "skill_set": skill_set, "slack_id": user.slack_id, "status": user.status, "tasks": tasks}

@app.get("/profile")
async def show_all_users(db: Session = Depends(get_db)):
    users = []
    tmp_users = db.query(models.User.user_id, models.User.name, models.User.status)
    for user in tmp_users:
        titles = db.query(models.Task.title).filter(models.Task.user_id == user.user_id).all()
        tmp_showuser = schemas.ShowUser(user_id=user.user_id, user_name=user.name, status=user.status, tasks=titles)
        users.append(tmp_showuser)
    return users

@app.get("/task")
async def get_task_list(db: Session = Depends(get_db)):
    tmp_tasks = db.query(models.Task.task_id, models.Task.title, models.Task.user_id, models.Task.register_date, models.Task.concern_desc).all()
    tasks = []
    for tmp_task in tmp_tasks:
        user_name = db.query(models.User.name).filter(user_id = tmp_task.user_id).first()
        skill_set_id = db.query(models.UserSkill.skill_id).filter(models.TaskSkill.task_id == tmp_task.task_id).all()
        skill_set = db.query(models.Skill.skill_name).filter(models.Skill.skill_id.in_(skill_set_id)).all()
        task = schemas.Task(task_id=tmp_task.task_id, title=tmp_task.title, user_name=user_name, skill_set=skill_set, task_date=tmp_task.register_date, concern_desc=tmp_task.concern_desc)
        tasks.append(task)
    return tasks

@app.get("/task/{id}")
async def get_task_detail(id:int, db: Session = Depends(get_db)):
    tmp_task = db.query(models.Task.user_id, models.Task.title, models.Task.register_date, models.Task.concern_desc, models.Task.task_detail, models.Task.ticket_link).filter(models.Task.task_id == id).first()
    tmp_user = db.query(models.User.name, models.User.slack_id).filter(models.User.user_id == task.user_id).first()
    tmp_skill_ids = db.query(models.TasksSkill.skill_id).filter(models.TasksSkill.task_id == id).all()
    skills = db.query(models.Skill.skill_name).filter(models.Skill.skill_id.in_(tmp_skill_ids)).all()
    task = schemas.TaskDetail(title = tmp_task.title, user_name = tmp_user.name, skill_set = skills, concern_desc = tmp_task.concern_desc, task_detail = tmp_task.task_detail, ticket_link = tmp_task.ticket_link, slack_link = tmp_user.slack_link)
    return task

@app.post("/task")
async def signup(request: schemas.CreateTask, db: Session = Depends(get_db)):
    new_task = models.Task(title = request.title, task_detail = request.task_detail, concern_desc = request.concern_desc, ticket_link = request.ticket_link, register_date = request.task_date)
    db.add(new_task)
    db.refresh(new_task)
    for skill in request.skill_set:
        new_taskskill = models.TasksSkill(task_id = new_task.task_id, skill_id = skill)
        db.add(new_taskskill)
        db.commit()
        db.refresh(new_taskskill)
    return new_task.task_id