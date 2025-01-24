from aiogram import Router
from aiogram.types import Message
from app.database.requests import get_user_service_id, get_user_api_token, set_user_api_token
from app.api.api import check_imei
from aiogram.filters import CommandStart, Command
router = Router()


@router.message(Command("send_imei"))
async def handle_send_command(message: Message):
    command_args = message.text.split()
    user_id = message.from_user.id

    if len(command_args) < 2:
        await message.answer("Команда /send_imei требует указания параметра \nнапример, /send_imei 356656423531580")
        return
    imei = command_args[1]  # Получаем IMEI (deviceId)
    await message.answer(f"Проверка IMEI: {imei}...")
    service_id = await get_user_service_id(user_id)
    api_token = await get_user_api_token(user_id)

    await check_imei(message, imei, service_id, api_token)


