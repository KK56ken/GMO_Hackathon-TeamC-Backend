from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class TasksSkill(Base):
    __tablename__ = 'tasks_skills'
    task_skill_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer)
    skill_id = Column(Integer)
