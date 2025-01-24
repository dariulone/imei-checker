from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.database.requests import get_user, get_user_api_token
from app.keyboards.keyboards import get_inline_registration_keyboard, get_inline_command_selection_keyboard

router = Router()


# Хэндлер на команду /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    is_registered = await get_user(message.from_user.id)
    if not is_registered:
        await message.answer(
            "Вы не зарегистрированы в системе. Нажмите 'Зарегистрироваться' для завершения процесса.",
            reply_markup=get_inline_registration_keyboard()
        )
    else:
        is_whitelisted = await get_user(message.from_user.id)
        if is_whitelisted:
            api_token = await get_user_api_token(message.from_user.id)
            if api_token:
                await message.answer("Привет, у тебя есть доступ! Отправьте /send_imei для использования функционала.")
            else:
                await message.answer(
                    "Требуется добавить API токен. Пожалуйста, используйте команду /set_api_token для его добавления.")
        else:
            await message.answer("Извините, у вас нет доступа.")


@router.callback_query(lambda c: c.data and c.data.startswith('selectcommand'))
async def process_command_selection(callback_query: CallbackQuery):
    command = callback_query.data.split('selectcommand')[-1]
    await callback_query.message.answer(command)
    await callback_query.answer(callback_query.id)


@router.message(Command("help"))
async def handle_help(message: Message):
    keyboard = get_inline_command_selection_keyboard()
    await message.answer("Доступные команды:", reply_markup=keyboard)