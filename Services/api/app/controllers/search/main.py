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

# Importing controller local resources
from . import schema
from . import models
from . import crud

# Importing depencies
from dependencies import get_db

# Import authentication dependencies
from controllers.authentication.crud import get_current_user
from controllers.authentication import schema as auth_schema




# Initializing the Controller
router = APIRouter(
    prefix='/api/v1/search'
)



@router.post(
    '/manual', 
    response_model=List[schema.SearchResponse],
    summary="Enter search criterias to find available houses on the market",
    tags=['Search']
)
def search(request: schema.Search):
    url = crud.generate_url(request)
    found_houses = crud.sample_requests(url, request.zipCodes)
    return found_houses


@router.post(
    '/schedule',
    status_code=status.HTTP_201_CREATED,
    summary="Setup a new automated search schedule",
    tags=['Search']
)
def new_scheduled_search(request: schema.Schedule, current_user: auth_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    url = crud.generate_url(request)
    found_houses = crud.sample_requests(url, request.zipCodes)
    new_schedule = crud.save_schedule( 
        request = request,
        url = url,
        userId = current_user.id,
        db=db
    )

    for house in found_houses:
        crud.add_house_to_db(house=house, userId=current_user.id, scheduleId=new_schedule.id, db=db)

    return {'message': f'Schedule successfully created! You are now tracking #{len(found_houses)} houses'}


@router.delete(
    '/schedule',
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a schedule",
    tags=['Search']
)
def delete_schedule(id: int, current_user: auth_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == id).first()
    if schedule.userId == current_user.id:
        if not schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No schedule with id: {id} was found")

        crud.delete_my_houses(id=id, userId=current_user.id, db=db)
        crud.delete_scheduled_searches(id=id, userId=current_user.id, db=db)
        return {'message': f'Successfully deleted scheduled search: {id}, and houses tracked by that search'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No schedule with id: {id} was found")       