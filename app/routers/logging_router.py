from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


logging_router = APIRouter()

@logging_router.get('/logging')
async def route_registration() -> JSONResponse:
    return JSONResponse(dict({}), status_code=status.HTTP_200_OK)