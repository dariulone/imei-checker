import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.handlers.start import router as start_router
from app.handlers.register import router as registration_router
from app.handlers.service import router as service_router
from app.handlers.imei import router as imei_router
from app.handlers.profile import router as profile_router
from settings.config import settings
import logging

from app.database.models import async_main

logger = logging.getLogger("aiogram")



async def main():
    bot = Bot(token=settings.TOKEN.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(registration_router)
    dp.include_router(service_router)
    dp.include_router(imei_router)
    dp.include_router(profile_router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    await async_main()
    print('Starting up...')


async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
