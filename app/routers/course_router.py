from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete
from database.db import engine

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse, Response

from typing import List
from typing import Optional
import enum

from schemas.course_shemas import CourseShema, PartitionShema
from database.models import Course, Partition
from services.common_services import *
from services.course_services import *

class Container(enum.Enum):
    course = Course
    partition = Partition

course_router = APIRouter()

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
        course = await session.execute(
            select(Course).\
            where(Course.id == id).\
            options(selectinload(Course.partitions))
        )
        course = course.scalar_one_or_none()
        if course == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        res = partition_to_dict(course)
        res = compute_course(course)
        res["partitions"] = []
        for partition in course.partitions:
            if partition.parent_id == None:
                partition_json = await get_partitions_json(partition.id, session)
                res["partitions"].append(partition_json)
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




@course_router.get('/get-partition')
async def api_get_partition(id: int):
    """
    Parameters
    ----------------------------------------
    id: int
        id of partition
    """
    # I 
    # Get partition
    return JSONResponse(PARTITION_DEMO, status_code=status.HTTP_200_OK)

@course_router.post('/append-partition')
async def api_append_partition(partition: PartitionShema, container: str, id: int):
    """
    Parameters
    ----------------------------------------
    partition : PartitionShema 
        partition data to create
    id: int
        id of course or partition in wich new partition will be appended
    container: str
        type of parent container ("course" or "partition")
    """
    async with AsyncSession(engine, expire_on_commit=False) as session:
        # I
        # Get parent container list of partitions
        partitions_list, container_entity = await get_partitions_list(container, id, session)
        # II
        # Append new partition to list
        partition = Partition(
            course_id=id if type(container_entity) == Course else container_entity.course_id,
            parent_id=None if type(container_entity) == Course else id,
            type=partition.type,
            name=partition.name,
            content=partition.content
        )
        partitions_list.append(partition)
        # III
        # Correct partitions indices
        await correct_indices(container, partitions_list)
        await session.commit()
        response = {"id": partition.id}
    return JSONResponse(response, status_code=status.HTTP_200_OK)

@course_router.post('/insert-partition')
async def api_insert_partition(partition: PartitionShema, container: str, id: int, idx: int):
    """
    Parameters
    ----------------------------------------
    partition : PartitionShema 
        partition data to create
    container: str
        type of parent container ("course" or "partition")
    id: int
        id of course or partition in wich insertion will happen
    idx: int 
        id of partition after which new partition will be inserted
    """
    # I
    # Get parent container list of partitions
    # II
    # Insert new partition to list
    # III
    # Correct partitions indices
    return JSONResponse(PARTITION_DEMO, status_code=status.HTTP_200_OK)

@course_router.post('/post-partition')
async def api_post_partition(partition: PartitionShema):
    """
    Parameters
    ----------------------------------------
    partition : PartitionShema 
        partition data to create
    """
    # I
    # Resset [idx, course_id, parent_id] to None
    # II
    # Create new partition
    return JSONResponse(PARTITION_DEMO, status_code=status.HTTP_200_OK)

@course_router.put('/put-partition')
async def api_put_partition(partition: PartitionShema):
    """
    Parameters
    ----------------------------------------
    partition : PartitionShema 
        partition data to update
    """
    # I
    # Resset [idx, course_id, parent_id] to old values
    # II
    # Update partition
    return JSONResponse(PARTITION_DEMO, status_code=status.HTTP_200_OK)

@course_router.put('/move-partition')
async def api_move_partition(pcontainer: str, pid: int, tcontainer: str, tip: int, tidx: int) -> None:
    """
    Parameters
    ----------------------------------------
    pcontainer: str
        type of parent container ("course" or "partition")
    pid : int 
        partition id 
    tcontainer: str
        type of target container ("course" or "partition")
    tip : int 
        target id (may be another partition or course) if Null act on the same partition/course
    tidx : int
        target idx after wich partition will be inserted
    """
    # I
    # Get parent container and target lists of partitions
    # II
    # Pop partition from parent list
    # III
    # Insert partition to target list
    # IV
    # Correct partitions indices
    return JSONResponse(PARTITION_DEMO, status_code=status.HTTP_200_OK)

@course_router.put('/swap-partitions')
async def api_swap_partitions(lid: int, rid: int):
    """
    Parameters
    ----------------------------------------
    lid : int 
        left partition id 
    rip : int 
        right partition id 
    """
    # I
    # Get parent container and target lists of partitions
    # II
    # Swap partitions
    # III
    # Correct partitions indices
    return JSONResponse({"left": PARTITION_DEMO, "right": PARTITION_DEMO}, status_code=status.HTTP_200_OK)

@course_router.delete('/delete-partition')
async def api_delete_partition(id: int):
    """
    Parameters
    ----------------------------------------
    id : int 
        partition id 
    """
    # I
    # Delete partition
    # II
    # Correct partitions indices
    return JSONResponse(PARTITION_DEMO, status_code=status.HTTP_200_OK)
