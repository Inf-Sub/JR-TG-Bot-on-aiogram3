__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/04/27'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.2'

from aiogram import Router
from aiogram.types import Message

from logger import logging


logging = logging.getLogger(__name__)

all_messages_router = Router()

@all_messages_router.message()
async def all_messages(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\nТы прислал мне сообщение: {message.text}')
    logging.debug(f'MISSED MESSAGE: {message}')
