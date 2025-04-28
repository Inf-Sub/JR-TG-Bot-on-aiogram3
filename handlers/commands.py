__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/04/27'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.2'

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


command_router = Router()

@command_router.message(Command('start'))
async def command_start(message: Message) -> None:
    await message.reply(
        test="I'm work!",
    )
   
