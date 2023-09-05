from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)

