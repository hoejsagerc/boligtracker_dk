from enum import Enum
from pydoc import describe
from pydantic import BaseModel, Field, validator
from typing import Optional, Set
from fastapi import HTTPException, status


##############################
## SCHEMA FOR SEARCH/MANUAL ##
##############################

class Search(BaseModel):
    zipCodes: Set[int] = Field(title="Zip Codes", 
        description="List of zip codes for the areas you want to search in")

    addressTypes: Optional[Set[str]] = Field(title="House Types", 
        description="Available Options: villa, condo, terraced+house, holiday+house, cooperative, farm, hobby+farm, full+year+plot, villa+apartment, holiday+plot")
    
    energyLabels: Optional[Set[str]] = Field(title="Energy Lables", 
        description="Available Options: A, B, C, D, E, F, G")
    
    priceMax: Optional[int] = Field(title="Maximum price", description="Should be in danish kr")
    
    minNumOfRooms: Optional[int] = Field(title="Minimum number of rooms")
    
    minHouseArea: Optional[int] = Field(title="Minimum house square metres", 
        description="Should be provided in square metres (m2)")
    
    minPropertyArea: Optional[int] = Field(title="Minimum property square metres", 
        description="Should be provided in square metres (m2)")
    
    filterPriceDrop: Optional[bool] = Field(title="Must have pricedrop",
        description="House must have a price reduction", default=False)
    
    filterBasement: Optional[bool] = Field(title="Must have basement", 
        description="House must have a basement", default=False)

    filterOpenHouse: Optional[bool] = Field(title="Must have openhouse scheduled", 
        description="Filter for houses with Open House scheduled", default=False)


    @validator('energyLabels')
    def el_match(cls, values):
        possible_values = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        for v in values:
            if v not in possible_values:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f'energyLabel value: {v} is not within allowed values')
        
        return values


    @validator('addressTypes')
    def at_match(cls, values):
        possible_values = ["villa", "condo", "terraced+house", "holiday+house", "cooperative", "farm", "hobby+farm", "full+year+plot", "villa+apartment", "holiday+plot"]
        for v in values:
            if v not in possible_values:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f'addressType value: {v} is not within allowed values')
        
        return values


    class Config:
        schema_extra = {
            "example_data": {
                "zipCodes": [
                    7100,
                    7300
                ],
                "addressTypes": [
                    "villa",
                    "farm",
                    "condo"
                ],
                "energyLabels": [
                    "A",
                    "B",
                    "C",
                    "D"
                ],
                "priceMax": 4000000,
                "minNumOfRooms": 3,
                "minHouseArea": 150,
                "minPropertyArea": 20000,
                "filterPriceDrop": True,
                "filterBasement": False
            } 
        }


class SearchResponse(BaseModel):
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
    priceChangeInPercent: float = Field(title="Price change in %", description="If any price changes then shown in percent")
    monthlyExpenses: float = Field(title="Monthly expenses", description="Calculated monthly expenses in danish kr")
    pageViews: int = Field(title="Page views", description="Total page views on https://boligsiden.dk")
    totalClicks: int = Field(title="Total clicks", description="Total number clicks on the listin on https://boligsiden.dk")
    totalFavorites: int = Field(title="Total favorites", description="Total count of people who have favouritized the specific house")
    numberOfRooms: int = Field(title="Number of rooms", description="Total number of rooms in the house")
    numberOfFloors: int = Field(title="Number of floors", description="Total number of floors in the house")
    energyLabel: str = Field(title="The efficiency label", description="The energy label set for the house, can either be A,B,C,D,E,F or G")
    daysOnMarket: int = Field(title="Days on the market", description="Total number of days on the market")
    smallImageUrl: str = Field(title="Image (small)", description="Small image of the house")
    largeImageUrl: str = Field(title="Image (large)", description="Large image of the house")
    latitude: str = Field(title="Position: latitude", description="Latitude coordinate for the house")
    longitude: str = Field(title="Position: longitude", description="Longitude coordinate for the house")
    description: str = Field(title="House description", description="Description of the house")




class Schedule(BaseModel):
    name: str = Field(title="Name of the schedule")

    description: str = Field(title="Description of the scheduled search")

    zipCodes: Set[int] = Field(title="Zip Codes", 
        description="List of zip codes for the areas you want to search in")

    addressTypes: Optional[Set[str]] = Field(title="House Types", 
        description="Available Options: villa, condo, terraced+house, holiday+house, cooperative, farm, hobby+farm, full+year+plot, villa+apartment, holiday+plot")
    
    energyLabels: Optional[Set[str]] = Field(title="Energy Lables", 
        description="Available Options: A, B, C, D, E, F, G")
    
    priceMax: Optional[int] = Field(title="Maximum price", description="Should be in danish kr")
    
    minNumOfRooms: Optional[int] = Field(title="Minimum number of rooms")
    
    minHouseArea: Optional[int] = Field(title="Minimum house square metres", 
        description="Should be provided in square metres (m2)")
    
    minPropertyArea: Optional[int] = Field(title="Minimum property square metres", 
        description="Should be provided in square metres (m2)")
    
    filterPriceDrop: Optional[bool] = Field(title="Must have pricedrop",
        description="House must have a price reduction", default=False)
    
    filterBasement: Optional[bool] = Field(title="Must have basement", 
        description="House must have a basement", default=False)

    filterOpenHouse: Optional[bool] = Field(title="Must have openhouse scheduled", 
        description="Filter for houses with Open House scheduled", default=False)


    @validator('energyLabels')
    def el_match(cls, values):
        possible_values = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        for v in values:
            if v not in possible_values:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f'energyLabel value: {v} is not within allowed values')
        
        return values


    @validator('addressTypes')
    def at_match(cls, values):
        possible_values = ["villa", "condo", "terraced+house", "holiday+house", "cooperative", "farm", "hobby+farm", "full+year+plot", "villa+apartment", "holiday+plot"]
        for v in values:
            if v not in possible_values:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f'addressType value: {v} is not within allowed values')
        
        return values


    class Config:
        schema_extra = {
            "example_data": {
                "zipCodes": [
                    7100,
                    7300
                ],
                "addressTypes": [
                    "villa",
                    "farm",
                    "condo"
                ],
                "energyLabels": [
                    "A",
                    "B",
                    "C",
                    "D"
                ],
                "priceMax": 4000000,
                "minNumOfRooms": 3,
                "minHouseArea": 150,
                "minPropertyArea": 20000,
                "filterPriceDrop": True,
                "filterBasement": False
            } 
        }


class ScheduleResponse(BaseModel):
    id: int = Field(title="Schedule id", description="The identifiable id of the schedule")
    #userId: int = Field(title="User Id", description="The id of the user")
    name: str = Field(title="Schedule Title", description="The title of the schedule")
    description: str = Field(title="Schedule description", description="Description of the scheduled search")
    zipCodes: str = Field(title="Zip Codes", description="List of zip codes for the areas you want to search in")
    addressTypes: str = Field(title="House Types", description="Available Options: villa, condo, terraced+house, holiday+house, cooperative, farm, hobby+farm, full+year+plot, villa+apartment, holiday+plot")
    energyLabels: str = Field(title="Energy Lables", description="Available Options: A, B, C, D, E, F, G")
    priceMax: int = Field(title="Maximum price", description="Provided in danish kr")
    minNumOfRooms: int = Field(title="Minimum number of rooms")
    minHouseArea: int = Field(title="Minimum house square metres", description="Provided in square metres (m2)")
    minPropertyArea: int = Field(title="Minimum property square metres", description="Should be provided in square metres (m2)")
    filterPriceDrop: bool = Field(title="Must have pricedrop", description="House must have a price reduction", default=False)
    filterBasement: bool = Field(title="Must have basement", description="House must have a basement", default=False)
    filterOpenHouse: bool = Field(title="Must have openhouse scheduled", description="Filter for houses with Open House scheduled", default=False)
    #url: str = Field(title="Backend api url", description="Nonusable url")
    class Config:
        orm_mode=True