from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from aiogram.filters.callback_data import CallbackData


class RegisterCallback(CallbackData, prefix="register"):
    action: str


def get_inline_registration_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Зарегистрироваться",
                    callback_data=RegisterCallback(action="register").pack()
                )
            ]
        ]
    )

    # Возвращаем клавиатуру
    return keyboard

def get_inline_keyboard_with_token(api_token: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Текущий API_TOKEN: {api_token}",
                    callback_data="show_token"
                )
            ]
        ]
    )

    return keyboard


def get_inline_service_selection_keyboard(services):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=service["title"],  # Отображаем название сервиса
                    callback_data=f"select_service_{service['id']}",  # Передаем ID сервиса в callback_data
                    # При необходимости, можно добавить параметры для увеличения кнопок
                    # Например, делаем кнопки более крупными, увеличив размер текста
                    # На практике это ограничено длиной текста и используемым шрифтом
                    # text=service["title"].ljust(20, " ")  # Пример для увеличения размера текста
                )
            ] for service in services
        ]
    )

    return keyboard


# Функция для создания инлайн клавиатуры с командами
def get_inline_command_selection_keyboard():
    # Список доступных команд
    commands = [
        {"command": "/start", "description": "start"},
        {"command": "/help", "description": "help"},
        {"command": "/profile", "description": "profile"},
        {"command": "/set_api_token", "description": "set api token"},
        {"command": "/change_service", "description": "change service"},
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{command['command']}: {command['description']}",
                    callback_data=f"selectcommand{command['command']}",
                )
            ] for command in commands
        ]
    )

    return keyboard
