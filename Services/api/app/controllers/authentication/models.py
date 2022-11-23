# Importing Standard python modules and open import from top-level package
import sys
sys.path.append("...")

# Importing SQLAlchemy Modules
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Importing the Database config
from database import Base # Direct inmport since i have appended top level path

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    hashed_password = Column(String(200))
    schedules = relationship('Schedule', back_populates='user')
    my_houses = relationship('MyHouse', back_populates='user')
    house_data = relationship('HouseData', back_populates='user')