from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(tags=["User"])


@router.get("/profile")
async def show_all_users(db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
    users = []
    user_id = current_user.user_id
    tmp_users = db.query(models.User.user_id, models.User.name, models.User.status).filter(models.User.user_id != user_id).all()
    if tmp_users is None:
        raise HTTPException(status_code=404, detail="User not found")
    for user in tmp_users:
        titles = db.query(models.Task.title).filter(models.Task.user_id == user.user_id).all()
        tmp_showuser = schemas.ShowUser(user_id=user.user_id, user_name=user.name, status=user.status, tasks=titles)
        users.append(tmp_showuser)
    return users


@router.get("/profile/{id}")
async def get_profile(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User.name, models.User.department_id, models.User.slack_id, models.User.status).filter(models.User.user_id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    skill_set_id = db.query(models.UsersSkill.skill_id).filter(models.UsersSkill.user_id == id).all()
    flat_skill_ids = [item[0] for item in skill_set_id]
    skill_set = db.query(models.Skill.skill_name).filter(models.Skill.skill_id.in_(flat_skill_ids)).all()
    flat_skill_set = [item[0] for item in skill_set]
    department = db.query(models.Department.department_name).filter(models.Department.department_id == user.department_id).first()
   
    temp_tasks = db.query(models.Task.task_id, models.Task.title, models.Task.user_id, models.Task.register_date, models.Task.concern_desc).filter(models.Task.user_id == id).all()
    tasks = []
    for tmp_task in temp_tasks:
        task_skill_ids = list(db.query(models.TasksSkill.skill_id).filter(models.TasksSkill.task_id == tmp_task.task_id).all())
        flat_skill_ids = [item[0] for item in task_skill_ids]
        task_skill = db.query(models.Skill.skill_name).filter(models.Skill.skill_id.in_(flat_skill_ids)).all()
        flat_task_skill = [item[0] for item in task_skill]
        task = schemas.Task(task_id=tmp_task.task_id, title=tmp_task.title, user_name=user.name, skill_set=flat_task_skill, task_date=tmp_task.register_date, concern_desc=tmp_task.concern_desc)
        tasks.append(task)
    return {"name": user.name, "department": str(department), "skill_set": flat_skill_set, "slack_id": user.slack_id, "status": user.status, "tasks": tasks}

@router.put("/profile/{id}")
async def set_profile(id: int, request: schemas.ChangeProfile, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.user_id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = request.user_name
    user.status = request.status
    user.department_id = request.department_id
    user.slack_id = request.slack_id
    db.commit()
    for skill_id in request.skill_set:
        if (None == db.query(models.UsersSkill.user_id).filter(models.UsersSkill.user_id == user.user_id, models.UsersSkill.skill_id == skill_id).first()):
            new_userskill = models.UsersSkill(user_id = user.user_id, skill_id = skill_id)
            db.add(new_userskill)
            db.commit()
            db.refresh(new_userskill)
    return 'ok'

@router.patch("/profile/{id}")
async def update_profile(id: int, request : schemas.UpdateProfile, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.user_id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return 'ok'

@router.post("/profile/myprofile")
async def get_myprofile(db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
    user = db.query(models.User.name, models.User.department_id, models.User.slack_id, models.User.status).filter(models.User.user_id == current_user.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    skill_set_id = db.query(models.UsersSkill.skill_id).filter(models.UsersSkill.user_id == current_user.user_id).all()
    flat_skill_ids = [item[0] for item in skill_set_id]
    skill_set = db.query(models.Skill.skill_name).filter(models.Skill.skill_id.in_(flat_skill_ids)).all()
    flat_skill_set = [item[0] for item in skill_set]
    department_query = db.query(models.Department.department_name).filter(models.Department.department_id == user.department_id).first()
    department = department_query[0]
    temp_tasks = db.query(models.Task.task_id, models.Task.title, models.Task.user_id, models.Task.register_date, models.Task.concern_desc).filter(models.Task.user_id == current_user.user_id).all()
    tasks = []
    for tmp_task in temp_tasks:
        task_skill_ids = list(db.query(models.TasksSkill.skill_id).filter(models.TasksSkill.task_id == tmp_task.task_id).all())
        flat_skill_ids = [item[0] for item in task_skill_ids]
        task_skill = db.query(models.Skill.skill_name).filter(models.Skill.skill_id.in_(flat_skill_ids)).all()
        flat_task_skill = [item[0] for item in task_skill]
        task = schemas.Task(task_id=tmp_task.task_id, title=tmp_task.title, user_name=user.name, skill_set=flat_task_skill, task_date=tmp_task.register_date, concern_desc=tmp_task.concern_desc)
        tasks.append(task)
    return {"name": user.name, "department": str(department), "skill_set": flat_skill_set, "slack_id": user.slack_id, "status": user.status, "tasks": tasks}
