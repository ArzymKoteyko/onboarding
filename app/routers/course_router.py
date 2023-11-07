from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select, delete
from database.db import engine

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse, Response

from typing import List
from typing import Optional

from schemas.course_shemas import CourseShema
from database.models import Course
from services.common_services import *
from services.course_services import *

course_router = APIRouter()

COURSE_DEMO = {
    "id": 0,
    "title": "Социализация: учимся общаться и адаптироваться в обществе",
    "percentage": 54,
    "image": "courses/background_1.jpg",
    "tags": [
        {
            "icon": "dummy",
            "text": "2 недели"
        },
        {
            "icon": "dummy",
            "text": "Обязательно"
        }
    ],
    "partitions": [
        {
            "id": 0,
            "type": "text",
            "name": "partition 1",
            "partitions": [
                {
                    "id": 5,
                    "type": "video",
                    "name": "partition 1.1",
                },
                {
                    "id": 6,
                    "type": "video",
                    "name": "partition 1.2",
                }
            ]
        },
        {
            "id": 1,
            "type": "text",
            "name": "partition 2",
        },
        {
            "id": 2,
            "type": "test",
            "name": "partition 3",
        },
        {
            "id": 3,
            "type": "text",
            "name": "partition 4",
        },
        {
            "id": 4,
            "type": "test",
            "name": "partition 5",
        }
    ] 
}

PARTITION_DEMO = {
    "id": 1,
    "type": "text",
    "name": "partition 2",
    "content": """### This is beautiful title
##### Not so beautiful title

![Alt text](http://95.165.137.33:5678/images/courses/background_2.jpg "a title")

Lorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века.

* list item 1
* list item 2
* list item 3

A table:

| a | b |
| - | - |
| some stuff | some other stuff |

Lorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века.

![Alt text](http://95.165.137.33:5678/images/courses/background_1.jpg "a title")


> A block quote with ~strikethrough~ and a URL: https://reactjs.org.

* Lists
* [ ] todo
* [x] done
"""
}

# если лимит равен 0 возращает все возможные курсы
@course_router.get('/courses', response_model=List[CourseShema])
async def get_courses(limit: int = 0) -> List[CourseShema]:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        if limit == 0:
            partitions = await session.execute(
                select(Course)
            )  
        else:
            partitions = await session.execute(
                select(Course).\
                limit(limit)
            )
        partitions = partitions.scalars()
        res = [compute_course(partition) for partition in partitions]
        return JSONResponse(res, status_code=status.HTTP_200_OK)
    



@course_router.get('/course', response_model=CourseShema)
async def get_course(id: int) -> CourseShema:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        partition = await session.execute(
            select(Course).\
            where(Course.id == id)
        )
        partition = partition.scalar_one_or_none()
        if partition == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        res = partition_to_dict(partition)
        res = compute_course(partition)
    return JSONResponse(res, status_code=status.HTTP_200_OK)

@course_router.post('/course', response_model=CourseShema)
async def post_course(course: CourseShema) -> CourseShema:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        partition = Course(
            title = course.title,
            image = course.image,
            tags = [CourseTag[tag.type] for tag in course.tags]
        )
        session.add(partition)
        await session.commit()
        res = compute_course(partition)
    return JSONResponse(res, status_code=status.HTTP_200_OK)

@course_router.put('/course', response_model=CourseShema)
async def put_course(course: CourseShema) -> CourseShema:
    return JSONResponse(dict({}), status_code=status.HTTP_200_OK)

@course_router.delete('/course')
async def delete_course(id: int) -> CourseShema:
    async with AsyncSession(engine) as session:
        await session.execute(
            delete(Course).\
            where(Course.id == id)
        )
        await session.commit()
    return JSONResponse({}, status_code=status.HTTP_200_OK)




@course_router.get('/partition')
async def get_partition(id: int):
    return JSONResponse(PARTITION_DEMO, status_code=status.HTTP_200_OK)

@course_router.post('/partition')
async def get_partition():
    return JSONResponse(PARTITION_DEMO, status_code=status.HTTP_200_OK)

@course_router.put('/partition')
async def get_partition():
    return JSONResponse(PARTITION_DEMO, status_code=status.HTTP_200_OK)

@course_router.delete('/partition')
async def get_partition():
    return JSONResponse(PARTITION_DEMO, status_code=status.HTTP_200_OK)
