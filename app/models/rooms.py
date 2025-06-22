from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Numeric, Boolean
from app.database import Base

class Rooms(Base):
    __tablename__ = "rooms"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    price: Mapped[int] = mapped_column(
        nullable= False
    )
    description: Mapped[str | None] = mapped_column(
        String(255), nullable= True
    )

    is_available: Mapped[bool] = mapped_column(Boolean)

