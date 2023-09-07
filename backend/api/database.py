from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import platform

dialect = "mysql"
driver = "mysqldb"
username = "user"
password = "password"

system_name = platform.system()
if system_name == 'Windows':
	host="localhost"
elif system_name == 'Linux':
    host = "db"


database = "db"
charset_type = "utf8"
db_url = f"{dialect}+{driver}://{username}:{password}@{host}/{database}?charset={charset_type}"
Engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
