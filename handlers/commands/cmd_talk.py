__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/04/27'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.3'

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from handlers.send import send_resource_message
from keyboards import ikb_celebrity

from logger import logging


logger = logging.getLogger(__name__)

cmd_talk_router = Router()

@cmd_talk_router.message(Command('talk'))
async def cmd_talk(message: Message, bot: Bot):
    """
    Обрабатывает команду /talk.

    Отправляет пользователю заранее заготовленное изображение и предлагает выбрать из
    нескольких известных личностей с помощью кнопок. По нажатию кнопки устанавливается
    промпт выбранной личности для дальнейшего общения с ChatGPT.

    :param message: Сообщение от пользователя.
    :param bot: Экземпляр бота.
    """
    file_name = 'talk'
    await send_resource_message(message, bot, file_name, keyboard=await ikb_celebrity(), use_answer=True)