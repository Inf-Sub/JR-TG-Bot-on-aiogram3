from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from classes.states import Random
from handlers.messages import msg_random_next_handler
from misc import bot_thinking

from logger import logging


logging = logging.getLogger(__name__)

cmd_random_router = Router()
command = 'random'

@cmd_random_router.message(Command(command))
# @cmd_random_router.message(Random.wait_gpt_answer, F.text == 'Хочу еще факт')
async def cmd_random(message: Message, state: FSMContext):
    await state.set_state(Random.wait_gpt_answer)
    await bot_thinking(message)
    await msg_random_next_handler(message, state)


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
# cmd_random_router = Router()
#
# @cmd_random_router.message(Command('random'))
# @cmd_random_router.message(F.text == 'Хочу еще факт')
# async def cmd_random(message: Message, bot: Bot):
#     """
#     Обрабатывает команду /random и сообщение 'Хочу еще факт'.
#
#     Отправляет пользователю заранее заготовленное изображение и делает запрос к ChatGPT с
#     заранее заготовленным промптом. Ответ ChatGPT передается пользователю. К сообщению
#     прикрепляются кнопки 'Закончить' и 'Хочу еще факт'.
#
#     :param message: Сообщение от пользователя.
#     :param bot: Экземпляр бота.
#     """
#     file_name = 'random'
#     buttons = ['Хочу еще факт', 'Закончить', ]
#     message_text = await gpt_client.random_request()
#     await send_resource_message(message, bot, file_name, keyboard=await rkb_main_menu(buttons), use_answer=True,
#         caption=message_text)
