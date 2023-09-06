from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Department(Base):
    __tablename__ = 'departments'
    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(255))
