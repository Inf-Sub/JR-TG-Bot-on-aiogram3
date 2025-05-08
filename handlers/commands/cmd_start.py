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
from handlers.send import send_resource_message

from keyboards import rkb_main_menu

from logger import logging


logger = logging.getLogger(__name__)

cmd_start_router = Router()

@cmd_start_router.message(Command('start'))
@cmd_start_router.message(F.text == 'Закончить')
async def cmd_start(message: Message, bot: Bot):
    """
    Обрабатывает команду /start и сообщение 'Закончить'.

    Отправляет пользователю главное меню с кнопками для доступа к различным функциям бота:
    - /random: Получить рандомный факт.
    - /gpt: Начать диалог с ChatGPT.
    - /talk: Начать диалог с известной личностью.
    - /quiz: Начать викторину (если реализовано).

    :param message: Сообщение от пользователя.
    :param bot: Экземпляр бота.
    """
    file_name = 'main'
    buttons = ['/random', '/gpt', '/talk', '/quiz', ]
    await send_resource_message(message, bot, file_name, keyboard=await rkb_main_menu(buttons), use_answer=True)
