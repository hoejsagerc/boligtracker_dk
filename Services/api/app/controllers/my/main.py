# Importing Standard python modules and open import from top-level package
from typing import List
from datetime import datetime, timedelta
import sys
sys.path.append("...")

# Importing FastApi Modules
from fastapi import Form
from fastapi.params import Depends
from fastapi import APIRouter, status, Response, HTTPException

# Importing SQLAlchemy modules
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

# Importing controller local resources
from . import schema
from . import models
from . import crud

# Importing depencies
from dependencies import get_db
from controllers.search import models as search_models
from controllers.search import schema as search_schema


# Import authentication dependencies
from controllers.authentication.crud import get_current_user
from controllers.authentication import schema as auth_schema




# Initializing the Controller
router = APIRouter(
    prefix='/api/v1/my'
)


@router.get(
    '/houses',
    response_model=List[schema.FavouritesResponse],
    summary="List all currently tracked houses",
    tags=['My']
)
def get_tracked_houses(current_user: auth_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    my_houses = db.query(models.MyHouse).filter(models.MyHouse.userId == current_user.id).all()
    if not my_houses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="house was not found")
    
    return my_houses


@router.get(
    '/schedules',
    response_model=List[search_schema.ScheduleResponse],
    summary="List all your active search schedules",
    tags=['My']
)
def get_schedules(current_user: auth_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    schedules = db.query(search_models.Schedule).filter(search_models.Schedule.userId == current_user.id).all()
    if not schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no schedules was found")

    return schedules


@router.get(
    '/favourites',
    response_model=List[schema.FavouritesResponse],
    summary="List all my favourite houses",
    tags=['My']
)
def get_favourites(current_user: auth_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    my_houses = db.query(models.MyHouse).filter(and_(models.MyHouse.userId == current_user.id, models.MyHouse.favourite == True)).all()
    return my_houses


@router.put(
    '/favourites/add',
    response_model=schema.FavouritesResponse,
    summary="Add house to favourites",
    tags=['My']
)
def add_favourite(id: int, current_user: auth_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    my_house = db.query(models.MyHouse).filter(and_(models.MyHouse.userId == current_user.id, models.MyHouse.id == id)).first()
    if not my_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="house was not found")
    
    my_house.favourite = True
    db.commit()
    return my_house


@router.put(
    '/favourites/remove',
    response_model=schema.FavouritesResponse,
    summary="Remove house from favourites",
    tags=['My']
)
def remove_favourite(id: int, current_user: auth_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    my_house = db.query(models.MyHouse).filter(and_(models.MyHouse.userId == current_user.id, models.MyHouse.id == id)).first()
    if not my_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="house was not found")
    
    my_house.favourite = False
    db.commit()
    return my_house