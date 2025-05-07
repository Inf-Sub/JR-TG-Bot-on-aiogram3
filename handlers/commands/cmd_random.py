__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/04/27'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.3'

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message

from classes import gpt_client
from handlers.send import send_resource_message
from keyboards import rkb_main_menu

from logger import logging


logger = logging.getLogger(__name__)

cmd_random_router = Router()

@cmd_random_router.message(Command('random'))
@cmd_random_router.message(F.text == 'Хочу еще факт')
async def cmd_random(message: Message, bot: Bot):
    """
    Обрабатывает команду /random и сообщение 'Хочу еще факт'.

    Отправляет пользователю заранее заготовленное изображение и делает запрос к ChatGPT с
    заранее заготовленным промптом. Ответ ChatGPT передается пользователю. К сообщению
    прикрепляются кнопки 'Закончить' и 'Хочу еще факт'.

    :param message: Сообщение от пользователя.
    :param bot: Экземпляр бота.
    """
    file_name = 'random'
    buttons = ['Хочу еще факт', 'Закончить', ]
    message_text = await gpt_client.random_request()
    await send_resource_message(message, bot, file_name, keyboard=rkb_main_menu(buttons), use_answer=True,
        caption=message_text)
