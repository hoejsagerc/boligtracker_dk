# Importing standard python libs
import requests

# Importing FastApi Modules
from fastapi import status, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer


# Importing SQLAlchemy modules
from sqlalchemy.orm import Session

# Importing controller local resources
from . import schema
from . import models

# Importing model from my
from controllers.my import models as my_models


# Importing dependencies
from dependencies import get_db




############################
## CRUD FOR SEARCH/MANUAL ##
############################

def check_last_char(text):
    """Helper function for checking if the & sign should be added to the url"""
    last_char = text[-1]
    if last_char == "?":
        return ""
    else:
        return "&"


def generate_url(search: schema.Search):
    base_url = "https://api.prod.bs-aws-stage.com/search/cases?"

    # Adding addressTypes to the baseurl
    if not search.addressTypes:
        base_url += f'{check_last_char(base_url)}addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot'
    else:
        base_url += f'{check_last_char(base_url)}addressTypes=' + '%2C'.join(search.addressTypes)

    # Adding energyLabels to the baseurl
    if not search.energyLabels:
        base_url += f'{check_last_char(base_url)}energyLabels=A%2CB%2CC%2CD%2CE%2CF%2CG'
    else:
        base_url += f'{check_last_char(base_url)}energyLabels=' + '%2C'.join(search.energyLabels)
    
    # Adding max price to the baseurl
    if search.priceMax:
        base_url += f'{check_last_char(base_url)}priceMax={search.priceMax}'

    # Adding minimum number og rooms
    if search.minNumOfRooms:
        base_url += f'{check_last_char(base_url)}numberOfRoomsMin={search.minNumOfRooms}'

    # Adding minimum house area
    if search.minHouseArea:
        base_url += f'{check_last_char(base_url)}areaMin={search.minHouseArea}'

    # Adding minimum property area
    if search.minPropertyArea:
        base_url += f'{check_last_char(base_url)}lotAreaMin={search.minPropertyArea}'

    # Adding filter for basements
    if search.filterBasement:
        base_url += f'{check_last_char(base_url)}filterBasement={search.filterBasement}'

    # Adding filter for price drop on house
    if search.filterPriceDrop:
        base_url += f'{check_last_char(base_url)}filterPriceDrop={search.filterPriceDrop}'

    # Adding filter for open house
    if search.filterOpenHouse:
        base_url += f'{check_last_char(base_url)}highlighted={search.filterOpenHouse}'

    return base_url


def create_house_object(obj):
    try:
        caseId = f"{obj['caseID']}"
    except:
        caseId = "n/a"

    try:
        address = f"{obj['address']['roadName']}, {obj['address']['houseNumber']}, {obj['address']['zipCode']}"
    except:
        address = "n/a"

    try:
        url =  f"{obj['caseUrl']}"
    except:
        url = "n/a"
    
    try:
        realtor = f"{obj['realtor']['name']}"
    except:
        realtor = "n/a"
    
    try:
        houseArea = f"{obj['housingArea']}"
    except:
        houseArea = 0.0
    
    try:
        weightedArea = f"{obj['weightedArea']}"
    except:
        weightedArea = 0.0
    
    try:
        yearBuilt = f"{obj['yearBuilt']}"
    except:
        yearBuilt = 0
    
    try:
        propertyArea = f"{obj['lotArea']}"
    except:
        propertyArea = 0.0
    
    try:
        pricePerM2 = f"{obj['perAreaPrice']}"
    except:
        pricePerM2 = 0.0

    try:
        price = f"{obj['priceCash']}"
    except:
        price = 0.0

    try:
        priceChangeInPercent = f"{obj['priceChangePercentage']}"
    except:
        priceChangeInPercent = 0.0

    try:
        monthlyExpenses = f"{obj['monthlyExpense']}"
    except:
        monthlyExpenses = 0.0

    try:
        pageViews = f"{obj['pageViews']}"
    except:
        pageViews = 0

    try:
        totalClicks = f"{obj['totalClickCount']}"
    except:
        totalClicks = 0

    try:
        totalFavorites = f"{obj['totalFavourites']}"
    except:
        totalFavorites = 0

    try:
        numberOfRooms = f"{obj['numberOfRooms']}"
    except:
        numberOfRooms = 0

    try:
        numberOfFloors = f"{obj['numberOfFloors']}"
    except:
        numberOfFloors = 0

    try:
        energyLabel = f"{obj['energyLabel']}"
    except:
        energyLabel = "n/a"

    try:
        daysOnMarket = f"{obj['daysOnMarket']}"
    except:
        daysOnMarket = 0

    try:
        smallImageUrl = f"{obj['defaultImage']['imageSources'][1]['url']}"
    except:
        smallImageUrl = "n/a"

    try:
        largeImageUrl = f"{obj['defaultImage']['imageSources'][4]['url']}"
    except:
        largeImageUrl = "n/a"

    try:
        latitude = f"{obj['address']['coordinates']['lat']}"
    except:
        latitude = "n/a"

    try:
        longitude = f"{obj['address']['coordinates']['lon']}"
    except:
        longitude = "n/a"

    try:
        description = f"{obj['descriptionBody']}"
    except:
        description = "n/a"

    new_object = {
        "id": caseId,
        "address": address,
        "url": url,
        "realtor": realtor,
        "houseArea": float(houseArea),
        "weightedArea": float(weightedArea),
        "yearBuilt": int(yearBuilt),
        "propertyArea": float(propertyArea),
        "pricePerM2": float(pricePerM2),
        "price": float(price),
        "priceChangeInPercent": float(priceChangeInPercent),
        "monthlyExpenses": float(monthlyExpenses),
        "pageViews": int(pageViews),
        "totalClicks": int(totalClicks),
        "totalFavorites": int(totalFavorites),
        "numberOfRooms": int(numberOfRooms),
        "numberOfFloors": int(numberOfFloors),
        "energyLabel": energyLabel,
        "daysOnMarket": int(daysOnMarket),
        "smallImageUrl": smallImageUrl,
        "largeImageUrl": largeImageUrl,
        "latitude": latitude,
        "longitude": longitude,
        "description": description
    }

    return new_object


def sample_requests(base_url: str, zipCodes: list):
    all_houses = []
    for zip in zipCodes:
        page_number = 1
        per_page = 50
        url = base_url + f"&zipCodes={zip}&per_page={per_page}&page={page_number}&sortAscending=true&sortBy=timeOnMarket"
        req = requests.get(url)
        while req.json()['cases']:
            for case in req.json()['cases']:
                house_obj = create_house_object(case)
                all_houses.append(house_obj)
            
            page_number += 1
            url = base_url + f"&zipCodes={zip}&per_page={per_page}&page={page_number}&sortAscending=true&sortBy=timeOnMarket"
            req = requests.get(url)
    
    return all_houses



def save_schedule(request: schema.Schedule, url: str, userId: int, db: Session):
    if request.zipCodes:
        string_ints = [str(int) for int in list(request.zipCodes)]
        zipCodesString = ",".join(string_ints)
        print(zipCodesString)
    else:
        zipCodesString = ""

    if request.addressTypes:
        addressTypesString = ",".join(list(request.addressTypes))
    else:
        addressTypesString = ""

    if request.energyLabels:
        energyLabelsString = ",".join(list(request.energyLabels))
    else:
        energyLabelsString = ""
    
    new_schedule = models.Schedule(
        userId = userId,
        name = request.name,
        description = request.description,
        zipCodes = zipCodesString,
        addressTypes = addressTypesString,
        energyLabels = energyLabelsString,
        priceMax = request.priceMax,
        minNumOfRooms = request.minNumOfRooms,
        minHouseArea = request.minHouseArea,
        minPropertyArea = request.minPropertyArea,
        filterPriceDrop = request.filterPriceDrop,
        filterBasement = request.filterBasement,
        filterOpenHouse = request.filterOpenHouse,
        url = url
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule


def add_house_to_db(house: schema.SearchResponse, userId: int, scheduleId: int, db: Session):
    new_house = my_models.MyHouse(
        userId = userId,
        scheduleId = scheduleId,
        address = house['address'],
        url = house['url'],
        realtor = house['realtor'],
        houseArea = house['houseArea'],
        weightedArea = house['weightedArea'],
        yearBuilt = house['yearBuilt'],
        propertyArea = house['propertyArea'],
        pricePerM2 = house['pricePerM2'],
        price = house['price'],
        monthlyExpenses = house['monthlyExpenses'],
        numberOfRooms = house['numberOfRooms'],
        numberOfFloors = house['numberOfFloors'],
        energyLabel = house['energyLabel'],
        smallImageUrl = house['smallImageUrl'],
        largeImageUrl = house['largeImageUrl'],
        latitude = house['latitude'],
        longitude = house['longitude'],
        description = house['description'],
        favourite = False
    )
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return new_house


def delete_my_houses(id: int, userId: int, db: Session):
    try:
        db.query(my_models.MyHouse).filter(my_models.MyHouse.userId == userId and my_models.MyHouse.id == id).delete(synchronize_session=False)
        db.commit()
        return True
    except:
        return False


def delete_scheduled_searches(id: int, userId: int, db: Session):
    try:
        db.query(models.Schedule).filter(models.Schedule.id == id).delete(synchronize_session=False)
        db.commit()
        return True
    except:
        return False