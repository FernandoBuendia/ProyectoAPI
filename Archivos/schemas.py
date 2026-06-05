from pydantic import BaseModel, ConfigDict, Field


class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ------------ User schemas ------------ #


class UserRequestModel(BaseModel):
    username: str
    password: str = Field(min_length=8, max_length=72)


class UserResponseModel(ResponseModel):
    id: int
    username: str


# ------------ Task schemas ------------ #


class TaskRequestModel(BaseModel):
    title: str
    description: str | None
    completed: bool = False


class TaskResponseModel(ResponseModel):
    id: int
    title: str
    description: str | None
    completed: bool


class TaskUpdateModel(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
