from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter(tags=["Task"])

@router.get("/task")
async def get_task_list(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    tmp_tasks = db.query(models.Task.task_id, models.Task.title, models.Task.user_id, models.Task.register_date, models.Task.concern_desc).all()
    tasks = []
    for tmp_task in tmp_tasks:
        user_name = str(db.query(models.User.name).filter(models.User.user_id == tmp_task.user_id).first())
        skill_set_id = db.query(models.UsersSkill.skill_id).filter(models.TasksSkill.task_id == tmp_task.task_id).all()
        skill_set = db.query(models.Skill.skill_name).filter(models.Skill.skill_id.in_(skill_set_id)).all()
        task = schemas.Task(task_id=tmp_task.task_id, title=tmp_task.title, user_name=user_name, skill_set=skill_set, task_date=tmp_task.register_date, concern_desc=tmp_task.concern_desc)
        tasks.append(task)
    return tasks

@router.get("/task/{id}")
async def get_task_detail(id:int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    tmp_task = db.query(models.Task.user_id, models.Task.title, models.Task.register_date, models.Task.concern_desc, models.Task.task_detail, models.Task.ticket_link).filter(models.Task.task_id == id).first()
    if tmp_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tmp_user = db.query(models.User.name, models.User.slack_id).filter(models.User.user_id == tmp_task.user_id).first()
    tmp_skill_ids = db.query(models.TasksSkill.skill_id).filter(models.TasksSkill.task_id == id).all()
    skills = db.query(models.Skill.skill_name).filter(models.Skill.skill_id.in_(tmp_skill_ids)).all()
    task = schemas.TaskDetail(title = tmp_task.title, user_name = tmp_user.name, skill_set = skills, concern_desc = tmp_task.concern_desc, task_detail = tmp_task.task_detail, ticket_link = tmp_task.ticket_link, slack_id = tmp_user.slack_id)
    return task

@router.post("/task")
async def create_task(request: schemas.CreateTask, db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
    user_id = current_user.user_id
    new_task = models.Task(user_id=user_id, title = request.title, task_detail = request.task_detail, end_flag=0, concern_desc = request.concern_desc, ticket_link = request.ticket_link, register_date=request.task_date, end_date=request.task_date)
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    for skill in request.skill_set:
        new_taskskill = models.TasksSkill(task_id = new_task.task_id, skill_id = skill)
        db.add(new_taskskill)
        db.commit()
        db.refresh(new_taskskill)
    return new_task.task_id
  
@router.delete("/task/{id}")
async def delete_task(id:int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.task_id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    db.close()
    return {"message": "Task deleted"}