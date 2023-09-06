from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Skill(Base):
    __tablename__ = 'skills'
    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(255))
