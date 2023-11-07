from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

material_router = APIRouter()

@material_router.get('/material')
async def route_registration() -> JSONResponse:
    return JSONResponse(dict({}), status_code=status.HTTP_200_OK)