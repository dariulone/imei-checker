from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete, desc
from settings.config import settings
from settings.logging_config import logger


async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            user = User(tg_id=tg_id)
            session.add(user)
        logger.info(f'{tg_id} | {settings.WHITELISTED_IDS}')
        if str(tg_id) in settings.WHITELISTED_IDS:
            user.whitelisted = True

        await session.commit()


async def get_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            if user.whitelisted:
                return True
            else:
                return False
        else:
            return False


async def set_user_api_token(user_id: int, api_token: str):
    """
    Сохраняет или обновляет API токен пользователя.
    """
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(tg_id=user_id))
        user = result.scalars().first()

        if user:
            user.api_token = api_token

        await session.commit()


async def get_user_api_token(user_id: int) -> str:
    """
    Получает API токен пользователя из базы данных.
    """
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(tg_id=user_id))
        user = result.scalars().first()

        if user and user.api_token:
            return user.api_token
        return None



async def set_user_service_id(user_id: int, service_id: int):
    async with async_session() as session:
        # Проверяем, существует ли запись о сервисе для данного пользователя
        result = await session.execute(select(User).filter_by(tg_id=user_id))
        user = result.scalars().first()

        if user:
            user.service_id = service_id

        await session.commit()


# Функция для получения ID выбранного сервиса
async def get_user_service_id(user_id: int) -> int:
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(tg_id=user_id))
        user = result.scalars().first()

        return user.service_id if user else None
