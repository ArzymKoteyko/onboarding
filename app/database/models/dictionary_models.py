from sqlalchemy import (
    Column,
    ForeignKey,
    Integer, 
    String,
    Boolean,
    TIMESTAMP
)
from .base import Base


class Term(Base):
    __tablename__ = 'terms'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    term = Column(String, unique=True)
    definition = Column(String)
    case_sensitive = Column(Boolean, default = False)
    
