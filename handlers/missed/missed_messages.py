__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/05/09'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.3'

from aiogram import Router
from aiogram.types import Message

from misc import is_admin
from logger import logging

logging = logging.getLogger(__name__)

missed_messages_router = Router()

@missed_messages_router.message()
async def missed_messages(message: Message):
    if is_admin(message.from_user.id):
        await message.answer(f'Привет, {message.from_user.full_name}!\nТы прислал мне сообщение: {message.text}')
    else:
        await message.answer(f'Привет, {message.from_user.full_name}!\nНажми на /start и выбери нужную команду.')
    logging.debug(f'MISSED MESSAGE: {message}')
