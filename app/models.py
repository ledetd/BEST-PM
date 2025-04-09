from typing import Optional
from sqlmodel import Field, SQLModel


class Crew(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    position: str
    location: str
   
class Project(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    customer: str
    location: str