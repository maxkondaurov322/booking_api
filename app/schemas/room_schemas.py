from pydantic import BaseModel, Field, conint
from typing import Optional

class RoomCreate(BaseModel):
    name: str = Field(max_length=100, min_length=2)
    price: int = conint(ge=0)
    description: Optional[str] = Field(max_length=255)
    is_available: bool

class RoomRead(RoomCreate):
    id: int


    class Config:
        from_attributes = True

