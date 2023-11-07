import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

from routers import course_router, dictionary_router, user_router, task_router, logging_router
from database.db import db_create


app: FastAPI = FastAPI()

@app.on_event('startup')
async def startup():
    db_create()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(
    task_router,
    prefix='/api',
    tags=['task']
)

app.include_router(
    course_router,
    prefix='/api',
    tags=['course']
)

app.include_router(
    dictionary_router,
    prefix='/api',
    tags=['dictionary']
)

app.include_router(
    user_router,
    prefix='/api',
    tags=['user']
)

app.include_router(
    logging_router,
    prefix='/api',
    tags=['logging']
)

@app.get("/images/{image}")
async def get_image(image):
    image_path = Path(f"images/{image}")
    if not image_path.is_file():
        return {"error": "Image not found on the server"}
    return FileResponse(image_path)

@app.get("/images/courses/{image}")
async def get_course_background(image):
    image_path = Path(f"images/courses/{image}")
    if not image_path.is_file():
        return {"error": "Image not found on the server"}
    return FileResponse(image_path)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5678)
