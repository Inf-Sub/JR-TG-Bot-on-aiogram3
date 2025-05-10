from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_talk_end() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для завершения разговора.

    :return: Настроенная клавиатура с кнопкой для прощания.
    """
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='Попрощаться!',
    )
    return keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Задайте свой вопрос...',
        one_time_keyboard=True,
    )
