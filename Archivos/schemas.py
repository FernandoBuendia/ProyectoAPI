from pydantic import BaseModel, ConfigDict



class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
  

# ------------ User schemas ------------ #

class UserRequestModel(BaseModel):
    username: str
    password: str

class UserResponseModel(ResponseModel):
    id: int
    username: str

# ------------ Task schemas ------------ #

class TaskRequestModel(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    user_username: str

class TaskResponseModel(ResponseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    user_username: str

