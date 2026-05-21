from fastapi import APIRouter
from fastapi import HTTPException

from ..schemas import UserRequestModel, UserResponseModel
from ..database import User

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

  if User.select().where(User.username == user.username).exists():
    raise HTTPException(status_code=400, detail="Username already exists")
  
  new_user = User.create(
    username = user.username,
    password = User.generate_password(user.password)
  )

  return new_user

@router.get("/{id}", response_model=UserResponseModel)
async def get_user(id: int):

  user = User.select().where(User.id == id).first()

  if user is None:
    raise HTTPException(status_code=404, detail="User not found")
  
  return user

@router.delete("/{id}")
async def delete_user(id: int):

  user_to_delete = User.select().where(User.id == id).first()

  if user_to_delete is None:
    raise HTTPException(status_code=404, detail="User not found")
  
  user_to_delete.delete_instance()
  
  return {"detail": "User deleted successfully"}