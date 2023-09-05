from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

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