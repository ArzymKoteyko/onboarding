from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


from schemas.test_schemas import TestShema
from services.test_service import *


test_router = APIRouter()

@test_router.get('/test', response_model=TestShema)
async def route_registration() -> JSONResponse:
    data = TestShema(test_param="this is test param")
    return JSONResponse(dict(data), status_code=status.HTTP_200_OK)