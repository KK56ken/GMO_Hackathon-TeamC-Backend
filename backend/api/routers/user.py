from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter(tags=["User"])


@router.get("/profile")
async def show_all_users(db: Session = Depends(database.get_db)):
    users = []
    tmp_users = db.query(models.User.user_id, models.User.name, models.User.status)
    for user in tmp_users:
        titles = db.query(models.Task.title).filter(models.Task.user_id == user.user_id).all()
        tmp_showuser = schemas.ShowUser(user_id=user.user_id, user_name=user.name, status=user.status, tasks=titles)
        users.append(tmp_showuser)
    return users


@router.get("/profile/{id}")
async def get_profile(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User.name, models.User.department_id, models.User.slack_id, models.User.status).filter(models.User.user_id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
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