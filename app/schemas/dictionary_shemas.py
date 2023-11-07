from pydantic import BaseModel

from typing import Optional
from typing import List
from datetime import datetime


class TermShema(BaseModel):
    id: Optional[int] = None
    term: str
    definition: str
    case_sensitive: Optional[bool] = False