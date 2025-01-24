from aiogram import Router
from aiogram.types import Message
from app.database.requests import get_user_service_id, get_user_api_token, get_user, set_user_api_token
from app.api.api import check_imei
from aiogram.filters import CommandStart, Command
router = Router()


# Хэндлер на команду /profile
@router.message(Command("profile"))
async def cmd_profile(message: Message):
    user_id = message.from_user.id

    is_whitelisted = await get_user(user_id)
    api_token = await get_user_api_token(user_id)
    service_id = await get_user_service_id(user_id)

    if is_whitelisted:
        access_status = "Да" if is_whitelisted else "Нет"
        message_text = (
            f"Профиль пользователя:\n"
            f"🔹 tg_id: {user_id}\n"
            f"🔹 Доступ разрешен: {access_status}\n"
            f"🔹 API_TOKEN: {api_token if api_token else 'Не задан'}\n"
            f"🔹 service_id: {service_id if service_id else 'Не выбран'}"
        )

        await message.answer(message_text)
    else:
        await message.answer("У вас нет доступа.")

