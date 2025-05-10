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
async def cmd_start(message: Message) -> None:
    """
    Обрабатывает команду запуска и отправляет пользователю приветственное сообщение с кнопками меню.

    :param message: Сообщение, содержащее информацию о команде.
    :return: None
    """
    resource = Resource(command)
    # Дожидаемся выполнения метода as_kwargs
    buttons = ['/random', '/gpt', '/talk', '/quiz', ]
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=rkb_main_menu(buttons),
    )
