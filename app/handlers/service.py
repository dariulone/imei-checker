from aiogram.types import CallbackQuery, Message
from app.database.requests import set_user_service_id
from app.keyboards.keyboards import get_inline_service_selection_keyboard
from app.database.requests import get_user_api_token,set_user_api_token
from aiogram import Router, F
from app.api.api import get_services_from_api
from aiogram.filters import Command
router = Router()


@router.message(Command("set_api_token"))
async def set_api_token_command(message: Message):
    command_args = message.text.split()
    if len(command_args) < 2:
        await message.answer(
            "Команда /set_api_token требует указания параметра. Например: /set_api_token e4o4aZYfKom5OXbbETkMcOCy3i8GSCGTHzWrhd4dc563b")
        return

    api_token = command_args[1]
    user_id = message.from_user.id

    await set_user_api_token(user_id, api_token)

    await message.answer(f"Ваш API_TOKEN успешно сохранен. Теперь выберите сервис для проверки IMEI.")
    await show_service_selection(message)


@router.message(Command("change_service"))
async def handle_change_service(message: Message):
    await show_service_selection(message)


async def show_service_selection(message: Message):
    user_id = message.from_user.id
    api_token = await get_user_api_token(user_id)
    services = await get_services_from_api(api_token)

    if services:
        keyboard = get_inline_service_selection_keyboard(services)
        await message.answer("Выберите сервис для проверки IMEI:", reply_markup=keyboard)
    else:
        await message.answer("Не удалось получить доступные сервисы.")


@router.callback_query(F.data.startswith("select_service_"))
async def process_service_selection(query: CallbackQuery):
    service_id = int(query.data.split('_')[-1])  # Извлекаем ID сервиса
    user_id = query.from_user.id

    # Сохраняем выбранный сервис в базе данных
    await set_user_service_id(user_id, service_id)

    await query.answer(f"Вы выбрали сервис с ID: {service_id}")
    await query.message.edit_text("Теперь вы можете отправлять запросы с командой /send_imei.")
