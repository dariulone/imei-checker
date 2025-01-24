from sqlalchemy import ForeignKey, String, BigInteger, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base


from settings.config import settings


# Создаем асинхронный движок для SQLite
engine = create_async_engine(settings.DB_URL, echo=True)
    
async_session = async_sessionmaker(engine)


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, unique=True)
    whitelisted = mapped_column(Boolean, default=False)  # Новый столбец для белого списка
    api_token = mapped_column(String, nullable=True)  # Хранение API токена
    service_id = mapped_column(Integer, nullable=True)


async def async_main():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Error creating schema: {e}")
