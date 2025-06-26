from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.rooms import Rooms
from app.schemas.room_schemas import RoomCreate, RoomRead
from app.services.redis_cache import redis_client
import json
from fastapi.encoders import jsonable_encoder

class RoomDAO:
    @staticmethod
    async def add(session: AsyncSession, data: RoomCreate) -> Rooms:
        room = Rooms(**data.model_dump())
        session.add(room)
        await session.commit()
        await session.refresh(room)
        await redis_client.delete("rooms_all")
        return room


    @staticmethod
    async def get_all(session: AsyncSession) -> list[RoomRead]:
        cached = await redis_client.get("rooms_all")
        if cached:
            print("Получаем из кеша")
            rooms_data = json.loads(cached)
            return [RoomRead(**room) for room in rooms_data]

        print("Получаем из базы")
        result = await session.execute(select(Rooms))
        rooms = result.scalars().all()

        await redis_client.set("rooms_all", json.dumps([
            {
                "id": r.id,
                "name": r.name,
                "price": r.price,
                "description": r.description,
                "is_available": r.is_available
            }
            for r in rooms
        ]), ex=60)

        rooms_serialized = jsonable_encoder([RoomRead.model_validate(r) for r in rooms])
        await redis_client.set("rooms_all", json.dumps(rooms_serialized), ex=60)

        return [RoomRead.model_validate(r) for r in rooms]

    @staticmethod
    async def delete_room(session: AsyncSession, room_id: int) -> bool:
        # 1. ищем запись
        result = await session.execute(
            select(Rooms).where(Rooms.id == room_id)
        )
        room = result.scalar_one_or_none()

        if room is None:
            return False

        await session.delete(room)
        await session.commit()

        await redis_client.delete("rooms_all")

        return True

