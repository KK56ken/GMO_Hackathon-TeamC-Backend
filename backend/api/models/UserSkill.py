from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class UsersSkill(Base):
    __tablename__ = 'users_skills'
    user_skill_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    skill_id = Column(Integer)
