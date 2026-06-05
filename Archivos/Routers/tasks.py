from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from ..schemas import TaskRequestModel, TaskResponseModel, TaskUpdateModel
from ..database import Task, User

from common import get_current_user

router = APIRouter(prefix="/tasks")


@router.post("/", response_model=TaskResponseModel)
async def create_task(task: TaskRequestModel, user: User = Depends(get_current_user)):

    new_task = Task.create(
        title=task.title, description=task.description, user_id=user.id
    )

    return new_task


@router.get("/{task_id}", response_model=TaskResponseModel)
async def get_task(task_id: int, user: User = Depends(get_current_user)):

    task = Task.select().where((Task.id == task_id) & (Task.user_id == user.id)).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get("/user_tasks", response_model=list[TaskResponseModel])
async def get_user_tasks(user: User = Depends(get_current_user)):

    return [user_task for user_task in user.tasks]


@router.put("/user_tasks/{task_id}", response_model=TaskResponseModel)
async def update_task(
    task_id: int, task_update: TaskUpdateModel, user: User = Depends(get_current_user)
):

    task_to_update = (
        Task.select().where((Task.id == task_id) & (Task.user_id == user.id)).first()
    )

    if task_to_update is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_update.title is not None:
        task_to_update.title = task_update.title

    if task_update.description is not None:
        task_to_update.description = task_update.description

    if task_update.completed is not None:
        task_to_update.completed = task_update.completed

    task_to_update.save()

    return task_to_update


@router.delete("/{task_id}")
async def delete_task(task_id: int, user: User = Depends(get_current_user)):

    task_to_delete = (
        Task.select().where((Task.id == task_id) & (Task.user_id == user.id)).first()
    )

    if task_to_delete is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_to_delete.delete_instance()
    return {"detail": "Task deleted successfully"}
