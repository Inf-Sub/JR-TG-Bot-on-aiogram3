from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes import Buttons
from classes import TalkWithCelebrityData

from logger import logging


logging = logging.getLogger(__name__)

def ikb_talk_with_celebrity():
    keyboard = InlineKeyboardBuilder()
    buttons = Buttons()
    for button in buttons:
        logging.debug(
            f'IKB_TALK_WITH_CELEBRITY: button="select_celebrity" | text={button.name=} | file_name={button.callback=}')
        keyboard.button(
            text=button.name,
            callback_data=TalkWithCelebrityData(
                button='select_celebrity',
                file_name=button.callback,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()
