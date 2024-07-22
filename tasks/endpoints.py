# api/tasks/endpoints.py
from fastapi import APIRouter, HTTPException, Depends
from plotly.io._orca import status

from api.auth.dependencies import oauth2_scheme
from api.auth.service import verify_token
from api.auth.models import Task

router = APIRouter()

fake_users_db = {}

def get_user(username: str):
    return fake_users_db.get(username)

@router.post("/submit/")
async def submit_task(task: Task, token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    user["tasks"].append(task.input_data)
    return {"message": "Task submitted successfully"}

@router.get("/display/")
async def display_task(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    tasks = user.get("tasks", [])
    return {"tasks": tasks}
