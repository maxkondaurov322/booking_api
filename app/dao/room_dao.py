from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.rooms import Rooms
from app.schemas.room_schemas import RoomCreate

class RoomDAO:
    @staticmethod
    async def add(session: AsyncSession, data: RoomCreate) -> Rooms:
        room = Rooms(**data.model_dump())  # создаём экземпляр
        session.add(room)
        await session.commit()
        await session.refresh(room)
        return room


    @staticmethod
    async def get_all(session: AsyncSession) -> list[Rooms]:
        result = await session.execute(select(Rooms))
        return result.scalars().all()

    @staticmethod
    async def delete_room(session: AsyncSession, room_id: int) -> bool:
        # 1. ищем запись
        result = await session.execute(
            select(Rooms).where(Rooms.id == room_id)
        )
        room = result.scalar_one_or_none()   # ← SELECT всегда даёт строки

        if room is None:        # ничего не нашли
            return False

        await session.delete(room)  # 2. удаляем найденный объект
        await session.commit()
        return True
