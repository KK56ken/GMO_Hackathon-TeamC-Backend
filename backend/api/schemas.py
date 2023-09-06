from pydantic import BaseModel
from datetime import datetime
from typing import List

class User(BaseModel):
    email:str
    password:str

class Task(BaseModel):
    task_id: int
    title: str
    user_name: str
    skill_set: List[str]
    task_date: datetime
    concern_desc: str
      
class ShowUser(BaseModel):
    user_id:int
    user_name:str
    status:int
    tasks:str

    class Config():
        orm_mode = True

# class Users(BaseModel):
#     user_id: int
#     name: str
#     email: str
#     password: str
#     token: str
#     status: int
#     department_id: int
#     slack_id: str

# class Tasks(BaseModel):
#     task_id: int
#     user_id: int
#     title: str
#     tasks_detail: str
#     concern_desc: str
#     ticket_link: str
#     end_flag: int
#     register_date: datetime
#     end_date: datetime

# class Skills(BaseModel):
#     skill_id: int
#     skill_name: str

# class Departments(BaseModel):
#     department_id: int
#     department_name: str

# class UsersSkills(BaseModel):
#     user_skill_id: int
#     user_id: int
#     skill_id: int
    
# class TasksSkills(BaseModel):
#     task_skill_id: int
#     task_id: int
#     skill_id: int