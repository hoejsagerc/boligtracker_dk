# Importing Standard python modules and open import from top-level package
from ast import For
from email.policy import default
import sys
from xmlrpc.client import Boolean
sys.path.append("...")

# Importing SQLAlchemy Modules
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# Importing the Database config
from database import Base # Direct inmport since i have appended top level path



class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='schedules')
    my_houses = relationship('MyHouse', back_populates='schedules')
    name = Column(String(100))
    description = Column(String(300))
    zipCodes = Column(String(200))
    addressTypes = Column(String(100))
    energyLabels = Column(String(50))
    priceMax = Column(Integer)
    minNumOfRooms = Column(Integer)
    minHouseArea = Column(Integer)
    minPropertyArea = Column(Integer)
    filterPriceDrop = Column(Boolean, default=False)
    filterBasement = Column(Boolean, default=False)
    filterOpenHouse = Column(Boolean, default=False)
    url = Column(String(400))
