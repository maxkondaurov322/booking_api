from fastapi import FastAPI
from app.database import Base, engine
from app.routers import rooms
app = FastAPI()
app.include_router(rooms.router)

@app.post("/init-db")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {"status": "База и таблицы созданы!"}
