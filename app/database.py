from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# 👇 Адрес подключения к базе
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/booking"

# 👇 Движок подключения
engine = create_async_engine(DATABASE_URL, echo=True)

# 👇 Создатель сессий
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 👇 Декларативная база
class Base(DeclarativeBase):
    pass
