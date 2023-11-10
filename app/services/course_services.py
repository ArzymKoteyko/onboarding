from random import randint

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database.models import CourseTag, Course, Partition, Container
from .common_services import *

def compute_tag(tag: CourseTag):
    res = {
        "type": CourseTag.obligation.name
    }
    if tag == CourseTag.obligation:
        res["content"] = "Обязательно",
        res["image"] = "icons/important.jpg"
    if tag == CourseTag.deadline:
        res["content"] = f"{randint(2,3)} недели",
        res["image"] = "icons/clock.jpg"
    return res

def compute_percentage():
    return randint(0,100)

def compute_course(course: Course):
    res = partition_to_dict(course)
    res["tags"] = [compute_tag(tag) for tag in res["tags"]]
    res["percentage"] = compute_percentage()
    res["created"] = str(res["created"])
    return res

async def get_partitions_list(container: str, id: int, session: AsyncSession):
    """
    Parameters
    ----------------------------------------
    container : str 
        contanier type: ("course", "partition")
    id : int
        contanier id
    session : AsyncSession
        active async connection to db
    """   
    container = Container[container].value
    options = [selectinload(container.partitions)]
    if container == Partition: options.append(selectinload(container.parent))
    container = await session.execute(
        select(container).\
        where(container.id == id).\
        options(*options)
    )
    container = container.scalar_one_or_none()
    if container == None:
        raise KeyError
    partitions = container.partitions
    sorted(partitions, key=lambda partition: partition.idx)
    return partitions, container

async def correct_indices(container: str, partitions_list: List[Partition]):
    """
    Parameters
    ----------------------------------------
    partitions_list: List[Partition]
        list of all children partitions to be corrected
    """ 
    container = Container[container].value
    idx = 0
    for partition in partitions_list:
        if container == Course and partition.parent_id == None or container == Partition:
            partition.idx = idx
            idx += 1


async def get_partitions_json(id: int, session: AsyncSession):
    """
    Parameters
    ----------------------------------------
    id : int
        partition id
    session : AsyncSession
        active async connection to db
    """ 
    partition = await session.execute(
        select(Partition).\
        where(Partition.id == id).\
        options(selectinload(Partition.partitions), selectinload(Partition.partitions).selectinload(Partition.partitions))
    )
    partition = partition.scalar_one_or_none()
    if partition == None:
        raise KeyError
    partition_json = {
        "id": partition.id,
        "idx": partition.idx,
        "type": partition.type,
        "name": partition.name,
        "content": partition.content,
        "created": str(partition.created)
    }
    if not partition.partitions:
        return partition_json
    partition_json["partitions"] = []
    for partition in partition.partitions:
        child_partition_json = await get_partitions_json(partition.id, session)
        partition_json["partitions"].append(child_partition_json)
    return partition_json
    