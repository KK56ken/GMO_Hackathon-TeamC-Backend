from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

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







