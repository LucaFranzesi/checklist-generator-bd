#region ------- IMPORTS -------------------------------------------------------------------------------------

from typing import List, Optional
from pydantic import BaseModel

#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- SCHEMA --------------------------------------------------------------------------------------

class Check(BaseModel):
    id: Optional[int] = None
    text: str
    parent_id: Optional[int] = None
    class ConfigDict:
        from_attributes = True

class Section(BaseModel):
    id: Optional[int] = None
    title: str
    checks: List[Check] = []

    class ConfigDict:
        from_attributes = True

class Checklist(BaseModel):
    id: Optional[int] = None
    title: str
    sections: List[Section] = []

    class ConfigDict:
        from_attributes = True

#endregion ---- SCHEMA --------------------------------------------------------------------------------------