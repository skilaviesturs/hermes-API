# main.py
from fastapi import FastAPI, Depends


from . import models
from .database import engine
from .routers import computer, logs, users, auth, admin, owner

# SQLAlchemie create all tables from models
# models.Base.metadata.create_all(bind=engine)

# inicalizējam instanci
#app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app = FastAPI()

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(computer.router)
app.include_router(logs.router)
app.include_router(owner.router)
