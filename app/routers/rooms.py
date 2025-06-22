from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.room_dao import RoomDAO
from app.schemas.room_schemas import RoomCreate, RoomRead
from app.database import async_session

router = APIRouter(prefix='/room', tags=['Rooms'])

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

@router.post('/rooms/', response_model=RoomRead)
async def create_room(
        payload: RoomCreate,
        db: AsyncSession = Depends(get_db)  # без скобок!
):
    return await RoomDAO.add(db, payload)

@router.get('/rooms/', response_model=list[RoomRead])
async def list_rooms(db: AsyncSession = Depends(get_db)):
    return await RoomDAO.get_all(db)

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: int,
    db: AsyncSession = Depends(get_db)
):
    success = await RoomDAO.delete_room(db, room_id)
    if not success:
        raise HTTPException(status_code=404, detail="Комната не найдена")

