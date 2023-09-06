from database import Base, Engine
from sqlalchemy import Column, Integer, String, ForeignKey

class Department(Base):
    __tablename__ = 'departments'
    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(255))

class Skill(Base):
    __tablename__ = 'skills'
    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(255))

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title = Column(String(255))
    tasks_detail = Column(String(255))
    concern_desc = Column(String(255))
    ticket_link = Column(String(255))
    end_flag = Column(Integer)
    register_date = Column(String(255))
    end_date = Column(String(255))

class TasksSkill(Base):
    __tablename__ = 'tasks_skills'
    task_skill_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer)
    skill_id = Column(Integer)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    token = Column(String(255))
    status = Column(Integer)
    department_id = Column(Integer)
    slack_id = Column(String(255))

class UsersSkill(Base):
    __tablename__ = 'users_skills'
    user_skill_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    skill_id = Column(Integer)

def main():
    # テーブルが存在しなければ、テーブルを作成
    Base.metadata.create_all(bind=Engine)
    print("テーブル作成完了")

if __name__ == "__main__":
    main()