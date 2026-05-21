from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends

from fastapi.security import OAuth2PasswordRequestForm

from .database import BaseDeDatos as connection
from .database import User, Task

from .Routers import user_router, task_router


@asynccontextmanager
async def lifespan(_app):
  if connection.is_closed():
    connection.connect()
  
  connection.create_tables([User, Task], safe = True)

  yield

  if not connection.is_closed():
    connection.close()
  

app = FastAPI(lifespan=lifespan,
              title="ToDo List API",
              description="API para gestionar tareas en una aplicación de lista de tareas",
              version="1.0.0")

api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(user_router)
api_v1.include_router(task_router)


@api_v1.post("/auth")
async def auth(data: OAuth2PasswordRequestForm = Depends()):
  return {
    "username": data.username,
    "password": data.password
  }

app.include_router(api_v1)

@app.get("/about")
async def about():
  return {"message": "Esta es una API para gestionar tareas en una aplicación de lista de tareas."}