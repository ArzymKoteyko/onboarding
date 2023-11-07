from sqlalchemy import (
    Column,
    ForeignKey,
    Integer, 
    String,
    Boolean,
    TIMESTAMP
)
from .base import Base


class Tests(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    test = Column(String)
    
