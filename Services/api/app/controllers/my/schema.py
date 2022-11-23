from enum import Enum
from pydoc import describe
from pydantic import BaseModel, Field, validator
from typing import Optional, Set
from fastapi import HTTPException, status



class FavouritesResponse(BaseModel):
    id: str = Field(title="House id", description="The specific id of the house")
    address: str = Field(title="House address", description="Address of the house")
    url: str = Field(title="House realtor URL", description="The realtors url for that specific house")
    realtor: str = Field(title="Realtor name", description="The realtor company selling the house")
    houseArea: float = Field(title="Area of the house", description="The house area in square metres (m2)")
    weightedArea: float = Field(title="Weighted house area", description="The weighted area of the house in square metres (m2)")
    yearBuilt: int = Field(title="Built year", description="The year when the house was built")
    propertyArea: float = Field(title="Area of the property", description="The entire area of the property in square metres (m2)")
    pricePerM2: float = Field(title="Price per m2", description="Price per square metre in danish kr")
    price: float = Field(title="House price", description="The price of the house in danish kr")
    #priceChangeInPercent: float = Field(title="Price change in %", description="If any price changes then shown in percent")
    monthlyExpenses: float = Field(title="Monthly expenses", description="Calculated monthly expenses in danish kr")
    #pageViews: int = Field(title="Page views", description="Total page views on https://boligsiden.dk")
    #totalClicks: int = Field(title="Total clicks", description="Total number clicks on the listin on https://boligsiden.dk")
    #totalFavorites: int = Field(title="Total favorites", description="Total count of people who have favouritized the specific house")
    numberOfRooms: int = Field(title="Number of rooms", description="Total number of rooms in the house")
    numberOfFloors: int = Field(title="Number of floors", description="Total number of floors in the house")
    energyLabel: str = Field(title="The efficiency label", description="The energy label set for the house, can either be A,B,C,D,E,F or G")
    #daysOnMarket: int = Field(title="Days on the market", description="Total number of days on the market")
    smallImageUrl: str = Field(title="Image (small)", description="Small image of the house")
    largeImageUrl: str = Field(title="Image (large)", description="Large image of the house")
    latitude: str = Field(title="Position: latitude", description="Latitude coordinate for the house")
    longitude: str = Field(title="Position: longitude", description="Longitude coordinate for the house")
    description: str = Field(title="House description", description="Description of the house")
    class Config:
        orm_mode=True