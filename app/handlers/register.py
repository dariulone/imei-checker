from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from app.database.requests import set_user, get_user
from aiogram.filters.callback_data import CallbackData


router = Router()


class RegisterCallback(CallbackData, prefix="register"):
    action: str


async def show_api_token_request(message: Message):
    await message.answer("Добавьте свой API токен с помощью команды /set_api_token")


# Хэндлер для обработки нажатия на кнопку "Зарегистрироваться" с использованием callback_data
@router.callback_query(RegisterCallback.filter(F.action == "register"))
async def process_registration(query: CallbackQuery, callback_data: RegisterCallback):
    user_id = query.from_user.id
    await set_user(user_id)

    is_whitelisted = await get_user(user_id)

    if is_whitelisted:
        await query.message.delete()
        await query.message.answer("Вы успешно зарегистрированы и в whitelist! Добро пожаловать!")
        await show_api_token_request(query.message)
    else:
        await query.message.delete()
        await query.message.answer("Вы успешно зарегистрированы, но у вас нет доступа к функционалу.")
