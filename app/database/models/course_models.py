from sqlalchemy import (
    Column,
    ForeignKey,
    Integer, 
    String,
    Boolean,
    DateTime,
    Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from .base import Base
import enum

class CourseTag(enum.Enum):
    obligation = 1
    deadline = 2

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String)
    tags = Column(ARRAY(Enum(CourseTag)))
    image = Column(String, default="courses/background_1.jpg")
    created = Column(DateTime, server_default=func.now())

    partitions = relationship("Partition", back_populates="course")
    

class Partition(Base):
    __tablename__ = 'partitions'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    idx = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"))
    parent_id = Column(Integer, ForeignKey("partitions.id"), nullable=True)
    type = Column(String)
    name = Column(String)
    content = Column(String)
    created = Column(DateTime, server_default=func.now())

    course = relationship("Course", back_populates="partitions")
    parent = relationship("Partition", back_populates="partitions", remote_side=[id])
    partitions = relationship("Partition", back_populates="parent", remote_side=[parent_id])

class Container(enum.Enum):
    course = Course
    partition = Partition