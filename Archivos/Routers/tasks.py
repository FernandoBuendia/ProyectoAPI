from fastapi import APIRouter
from fastapi import HTTPException

from ..schemas import TaskRequestModel, TaskResponseModel, TaskUpdateModel
from ..database import Task, User

router = APIRouter(prefix="/tasks")


@router.post("/", response_model=TaskResponseModel)
async def create_task(task: TaskRequestModel):

  user = User.select().where(User.username == task.user_username).first()

  if user is None:
    raise HTTPException(status_code=404, detail="User not found")
  
  new_task = Task.create(
    title = task.title,
    description = task.description,
    user = user
  )

  return new_task

@router.get("/{task_id}", response_model=TaskResponseModel)
async def get_task(task_id: int):
  
  task = Task.select().where(Task.id == task_id).first()

  if task is None:
    raise HTTPException(status_code=404, detail="Task not found")
  
  return task

@router.get("/user/{user_username}", response_model=list[TaskResponseModel])
async def get_user_tasks(user_username: str):

  user = User.select().where(User.username == user_username).first()

  if user is None:
    raise HTTPException(status_code=404, detail="User not found")
  
  return list(user.tasks)

@router.put("/user/{user_username}/tasks/{task_id}", response_model=TaskResponseModel)
async def update_task(user_username: str, task_id: int, task: TaskUpdateModel):

  user = User.select().where(User.username == user_username).first()

  if user is None:
    raise HTTPException(status_code=404, detail="User not found")

  task_to_update = Task.select().where((Task.id == task_id) & (Task.user == user)).first()

  if task_to_update is None:
    raise HTTPException(status_code=404, detail="Task not found")
  
  task_to_update.title = task.title
  task_to_update.description = task.description
  task_to_update.completed = task.completed

  task_to_update.save()

  return task_to_update
  
@router.delete("/{task_id}")
async def delete_task(task_id: int):
  
  task_to_delete = Task.select().where(Task.id == task_id).first()

  if task_to_delete is None:
    raise HTTPException(status_code=404, detail="Task not found")
  
  task_to_delete.delete_instance()
  return {"detail": "Task deleted successfully"}