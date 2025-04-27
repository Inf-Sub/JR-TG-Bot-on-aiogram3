import config
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
import asyncio

# @dp.message(Command('Start'))
# async def command_start(message: Message):
#     await Message.answer('start')

from random import randint

my_set = {randint(1, 50) for _ in range(10)}

for idx in enumerate(my_set):
    print(idx)

