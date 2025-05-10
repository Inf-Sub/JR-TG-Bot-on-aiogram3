from typing import List

from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_main_menu(buttons: List[str]) -> ReplyKeyboardBuilder:
    """
    Создает главное меню с кнопками.

    :param buttons: Список текстов кнопок для меню.
    :return: Объект ReplyKeyboardBuilder с настройками клавиатуры.
    """
    keyboard = ReplyKeyboardBuilder()
    for button in buttons:
        keyboard.button(
            text=button,
        )
    return keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню...',
    )
