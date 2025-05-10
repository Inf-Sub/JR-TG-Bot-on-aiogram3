from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from classes import Resource
from keyboards.reply import rkb_main_menu

from logger import logging


logging = logging.getLogger(__name__)

cmd_start_router = Router()
command = 'main'

@cmd_start_router.message(Command('start'))
@cmd_start_router.message(Command('help'))
# @cmd_start_router.message(F.text == 'Закончить')
# @cmd_start_router.message(F.text == 'Попрощаться!')
async def cmd_start(message: Message):
    resource = Resource(command)
    # Дожидаемся выполнения метода as_kwargs
    buttons = ['/random', '/gpt', '/talk', '/quiz', ]
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=rkb_main_menu(buttons),
    )


# from aiogram import Bot, Router, F
# from aiogram.filters import Command
# from aiogram.types import Message
#
# from classes import gpt_client
# from handlers.send import send_resource_message
# from keyboards import rkb_main_menu
#
# from logger import logging
#
#
# logging = logging.getLogger(__name__)
#
# cmd_start_router = Router()
#
# @cmd_start_router.message(Command('start'))
# @cmd_start_router.message(F.text == 'Закончить')
# async def cmd_start(message: Message, bot: Bot):
#     """
#     Обрабатывает команду /start и сообщение 'Закончить'.
#
#     Отправляет пользователю главное меню с кнопками для доступа к различным функциям бота:
#     - /random: Получить рандомный факт.
#     - /gpt: Начать диалог с ChatGPT.
#     - /talk: Начать диалог с известной личностью.
#     - /quiz: Начать викторину (если реализовано).
#
#     :param message: Сообщение от пользователя.
#     :param bot: Экземпляр бота.
#     """
#     file_name = 'main'
#     buttons = ['/random', '/gpt', '/talk', '/quiz', ]
#     await send_resource_message(message, bot, file_name, keyboard=await rkb_main_menu(buttons), use_answer=True)
