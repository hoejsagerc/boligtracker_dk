# Importing Standard python modules and open import from top-level package
from email.utils import decode_params
import sys
sys.path.append("...")

# Importing FastApi Modules
from fastapi.params import Depends
from fastapi import APIRouter, status, Response, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Importing SQLAlchemy modules
from sqlalchemy.orm import Session

# Importing controller local resources
from . import schema
from . import models
from . import crud

# Importing depencies
from dependencies import get_db
from controllers.authentication.crud import get_current_user



router = APIRouter(
    prefix='/api/v1/authentication'
)

@router.post(
    '/user', 
    response_model=schema.UserResponse, 
    summary="Sign up to use full functionality of the application",
    tags=['Authentication']
    )
def create_new_user(request: schema.User, db: Session = Depends(get_db)):
    """
    Sign up for an account
    - **username:** [required] => Enter a unique username
    - **email**: [required] => Enter unique email address. Will be used for notifications
    - **first_name**: [required] => Enter first name
    - **last_name**: [required] => Enter last name
    """
    new_user = crud.generate_user(request, db)
    return request


@router.post(
    '/login', 
    summary="Sign in to retrieve JWT for authentication",
    tags=['Authentication']
)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Sign In
    - **username:** [required] => Enter the username of a valid account
    - **password:** [required] => Enter the password for the user

    This endpoint will return a JWT token to be used for authentication with all locked routes
    """
    user = crud.check_if_user_exists(request.username, db)
    crud.verify_password(request.password, user)

    access_token = crud.generate_token(
        data = {'sub': request.username}
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.delete(
    '/user',
    summary="Delete your user account",
    tags=['Authentication']
)
def delete_user(username: str, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    """
    Delete user [Authentication Required]
    - **username:** [required] => Enter the username of a valid account

    This endpoint will return a JWT token to be used for authentication with all locked routes
    """
    if current_user.username == username:
        action = crud.delete_user(username, db)
        if action == True:
            #TODO - Create functionality for deleting all the data that the user has gathered in the database
            return {'message': f'user: {username} was deleted successfully'}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed deleting user: {username}")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"username provided does not match with your own account. You can only delete your own account.")
