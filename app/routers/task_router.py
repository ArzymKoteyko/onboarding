from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


task_router = APIRouter()

@task_router.get('/task')
async def route_registration() -> JSONResponse:
    return JSONResponse(dict({}), status_code=status.HTTP_200_OK)