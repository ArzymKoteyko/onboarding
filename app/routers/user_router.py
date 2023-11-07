from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


user_router = APIRouter()

@user_router.get('/user')
async def route_registration() -> JSONResponse:
    return JSONResponse(dict({}), status_code=status.HTTP_200_OK)