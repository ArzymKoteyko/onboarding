from pydantic import BaseModel

from typing import Optional
from typing import List
from datetime import datetime
from database.models import CourseTag   

class CourseTagShema(BaseModel):
    type: str
    content: Optional[str] = None
    image: Optional[str] = None


class CourseShema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    tags: Optional[List[CourseTagShema]] = None
    percentage: Optional[int] = 0
    image: Optional[str] = None
    created: Optional[str] = None

class PartitionShema(BaseModel):
    id: Optional[int] = None
    idx: Optional[int] = None
    course_id: Optional[int] = None
    parent_id: Optional[int] = None
    type: str
    name: str
    content: str
    created: Optional[int] = None  