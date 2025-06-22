from pydantic import BaseModel, Field
from typing import Optional

class RoomCreate(BaseModel):
    name: str = Field(max_length=100, min_length=2)
    price: int = Field(conint=0)
    description: Optional[str] = Field(max_length=255)

class RoomRead(RoomCreate):
    id: int

    class Config:
        from_attributes = True

