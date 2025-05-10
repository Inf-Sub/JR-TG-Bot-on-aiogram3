from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from classes import Resource
from classes.states import Quiz
from keyboards.inline import ikb_quiz_select_topic
from misc import bot_thinking

from logger import logging


logging = logging.getLogger(__name__)

cmd_quiz_router = Router()
command = 'quiz'

@cmd_quiz_router.message(Command(command))
async def cmd_quiz(message: Message, state: FSMContext):
    logging.debug('cmd_quiz')
    await state.set_state(Quiz.wait_gpt_answer)
    await bot_thinking(message)
    resource = Resource(command)
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=ikb_quiz_select_topic(),
    )


# from aiogram import Bot, Router
# from aiogram.filters import Command
# from aiogram.types import Message
# from aiogram.fsm.context import FSMContext
#
# from classes.gpt_messages import gpt_client
# from states.cmd_gpt_state import ChatGPTRequests
# from handlers.send import send_resource_message
#
# from logger import logging
#
#
# logging = logging.getLogger(__name__)
#
# cmd_gpt_router = Router()
#
# @cmd_gpt_router.message(Command('gpt'))
# async def cmd_gpt(message: Message, bot: Bot, state: FSMContext):
#     """
#     Обрабатывает команду /gpt.
#
#     Устанавливает состояние ожидания запроса от пользователя и отправляет ему заранее
#     заготовленное изображение. Ожидает текстовое сообщение от пользователя для передачи
#     его в ChatGPT.
#
#     :param message: Сообщение от пользователя.
#     :param bot: Экземпляр бота.
#     :param state: Контекст состояния для управления состоянием бота.
#     """
#     await state.set_state(ChatGPTRequests.wait_gpt_answer)
#     file_name = 'gpt'
#     await send_resource_message(message, bot, file_name, use_answer=True)
#
#
# @cmd_gpt_router.message(ChatGPTRequests.wait_gpt_answer)
# async def wait_for_gpt_handler(message: Message, bot: Bot):
#     file_name = 'gpt'
#     message_text = await gpt_client.gpt_request(message.text)
#     await send_resource_message(message, bot, file_name, use_answer=True, caption=message_text)
#
#
# @cmd_gpt_router.message()
# async def default_handler(message: Message, bot: Bot, state: FSMContext):
#     """
#     Обрабатывает все остальные сообщения от пользователя.
#
#     Если сообщение является командой (начинается с '/'), и это не команда /gpt,
#     очищает состояние и уведомляет пользователя о том, что команда не распознана.
#
#     :param message: Сообщение от пользователя.
#     :param bot: Экземпляр бота.
#     :param state: Контекст состояния для управления состоянием бота.
#     """
#     # Проверяем, является ли сообщение командой
#     if message.text.startswith('/'):
#         if message.text != '/gpt':
#             await state.clear()
#             await message.reply(f'Команда: "{message.text}" не распознана. Состояние очищено.')


#
# from aiogram import Bot, Router
# from aiogram.filters import Command
# from aiogram.types import Message
#
# from handlers.send import send_resource_message
# from keyboards import ikb_celebrity
#
# from logger import logging
#
#
# logging = logging.getLogger(__name__)
#
# cmd_talk_router = Router()
#
# @cmd_talk_router.message(Command('talk'))
# async def cmd_talk(message: Message, bot: Bot):
#     """
#     Обрабатывает команду /talk.
#
#     Отправляет пользователю заранее заготовленное изображение и предлагает выбрать из
#     нескольких известных личностей с помощью кнопок. По нажатию кнопки устанавливается
#     промпт выбранной личности для дальнейшего общения с ChatGPT.
#
#     :param message: Сообщение от пользователя.
#     :param bot: Экземпляр бота.
#     """
#     file_name = 'talk'
#     await send_resource_message(message, bot, file_name, keyboard=await ikb_celebrity(), use_answer=True)