from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'mysql:///localhost:3306'

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# Base = declarative_base()

dialect = "mysql"
driver = "mysqldb"
username = "user"
password = "password"
host = "db"

database = "db"
charset_type = "utf8"
db_url = f"{dialect}+{driver}://{username}:{password}@{host}/{database}?charset={charset_type}"
Engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()
