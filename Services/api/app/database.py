# Importing Standard Python Modules
import os

# Import sqlalchemy modules
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Retrieving Database Values from environment variables
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')


# Generating the Database URL for the connection and creating the Database session
# FastAPI Docs on connecting to Database: https://fastapi.tiangolo.com/tutorial/sql-databases/
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_NAME

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
