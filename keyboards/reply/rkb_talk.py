from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_talk_end():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='Попрощаться!',
    )
    return keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Задайте свой вопрос...',
        one_time_keyboard=True,
    )
