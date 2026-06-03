from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordRequestForm

from .database import BaseDeDatos as connection
from .database import User, Task

from .routers import user_router, task_router

from common import create_access_token

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


@api_v1.post("/authentication")
async def auth(data: OAuth2PasswordRequestForm = Depends()):
  
  user = User.authenticate(data.username, data.password)
  
  if user:
    return {
      "access_token": create_access_token(user),
      "token_type": "bearer"
    }
  
  else:
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "Credenciales inválidas",
      headers = {"WWW-Authenticate": "Bearer"})

app.include_router(api_v1)

@app.get("/about")
async def about():
  return {"message": "Esta es una API para gestionar tareas en una aplicación de lista de tareas."}