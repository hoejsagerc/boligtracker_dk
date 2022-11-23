# Importing FastApi Modules
from fastapi import FastAPI

# Importing Controllers
from controllers.authentication import main as r_authentication
from controllers.my import main as r_my
from controllers.search import main as r_search
from controllers.system import main as r_system

# Importing Controller Models
from controllers.authentication import models as auth_models
from controllers.my import models as my_models

# Importing database config
from database import engine



# Initializing the application
app = FastAPI(
    docs_url = "/api/v1/docs",
    redoc_url = "/api/v1/redocs",
    title = "Hvorkanvibo.dk",
    description = "API for supporting the application Hvorkanvibo.dk",
    version = "1.0.0",
    openapi_url = "/api/v1/openapi.json"
)


# Initializing all the database models
auth_models.Base.metadata.create_all(bind=engine)
my_models.Base.metadata.create_all(bind=engine)


# Including the Controllers into the application
app.include_router(r_authentication.router)
app.include_router(r_my.router)
app.include_router(r_search.router)
app.include_router(r_system.router)