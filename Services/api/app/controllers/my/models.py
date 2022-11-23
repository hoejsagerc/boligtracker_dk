# Importing Standard python modules and open import from top-level package
from email.policy import default
import sys
from xmlrpc.client import Boolean
sys.path.append("...")

# Importing SQLAlchemy Modules
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

# Importing the Database config
from database import Base # Direct inmport since i have appended top level path


class MyHouse(Base):
    __tablename__ = "my_houses"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='my_houses')
    scheduleId = Column(Integer, ForeignKey('schedules.id'))
    schedules = relationship('Schedule', back_populates='my_houses')
    houseId = Column(Integer)
    address = Column(String(200))
    url = Column(String(400))
    realtor = Column(String(200))
    houseArea = Column(Float)
    weightedArea = Column(Float)
    yearBuilt = Column(Integer)
    propertyArea = Column(Float)
    pricePerM2 = Column(Float)
    price = Column(Float)
    monthlyExpenses = Column(Float)
    numberOfRooms = Column(Integer)
    numberOfFloors = Column(Integer)
    energyLabel = Column(String(20))
    smallImageUrl = Column(String(400))
    largeImageUrl = Column(String(400))
    latitude = Column(String(200))
    longitude = Column(String(200))
    description = Column(String(5000))
    favourite = Column(Boolean)


class HouseData(Base):
    __tablename__ = "house_data"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='house_data')
    scheduleId = Column(Integer, ForeignKey('schedules.id'))
    #schedule = relationship('Schedule', back_populates='my_houses')
    houseId = Column(Integer)
    address = Column(String(200))
    url = Column(String(400))
    realtor = Column(String(200))
    houseArea = Column(Float)
    weightedArea = Column(Float)
    yearBuilt = Column(Integer)
    propertyArea = Column(Float)
    pricePerM2 = Column(Float)
    price = Column(Float)
    priceChangeInPercent = Column(Float)
    monthlyExpenses = Column(Float)
    numberOfRooms = Column(Integer)
    numberOfFloors = Column(Integer)
    energyLabel = Column(String(20))
    pageViews = Column(Integer)
    totalClicks = Column(Integer)
    totalFavorites = Column(Integer)
    daysOnMarket = Column(Integer)
    smallImageUrl = Column(String(400))
    largeImageUrl = Column(String(400))
    latitude = Column(String(200))
    longitude = Column(String(200))
    description = Column(String(5000))
    favourite = Column(Boolean)
    