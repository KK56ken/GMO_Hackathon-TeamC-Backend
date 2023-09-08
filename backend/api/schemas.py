from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

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
    class Config():
        orm_mode = True

class TaskDetail(BaseModel):
    title: str
    user_name: str
    task_date: datetime
    skill_set: List[str]
    concern_desc: str
    task_detail: str
    ticket_link: str
    slack_id: str
    class Config():
        orm_mode = True
      
class ShowUser(BaseModel):
    user_id:int
    user_name:str
    status:int
    tasks: List[str]

    class Config():
        orm_mode = True

class CreateTask(BaseModel):
    title:str
    task_date: datetime
    skill_set:List[int]
    concern_desc: str
    task_detail: str
    ticket_link: str
    class Config():
        orm_mode = True

class DBCreateTask(BaseModel):
    user_id:int
    title:str
    task_detail: str
    concern_desc: str
    ticket_link: str
    end_flag: int
    register_date: datetime
    end_date: datetime

class ChangeProfile(BaseModel):
    user_name:str
    status:int
    department_id: int
    slack_id: int
    skill_set: List[int]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class SignUp(BaseModel):
    name: str
    email: str
    password: str
    status: int
    department_id: int
    skill_set: List[int]
    slack_id: str

class UpdateProfile(BaseModel):
    name: Optional[str] = None
    status: Optional[int] = None
    department_id: Optional[int] = None
    skill_set: Optional[List[int]] = None
    slack_id: Optional[str] = None

class UpdateTask(BaseModel):
    title: Optional[str] = None
    skill_set: Optional[List[int]] = None
    task_detail: Optional[str] = None
    concern_desc: Optional[str] = None
    ticket_link: Optional[str] = None

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