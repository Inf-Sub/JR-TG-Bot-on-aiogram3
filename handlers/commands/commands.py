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
# from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from classes import gpt_client
from states.cmd_gpt_state import ChatGPTRequests
from handlers.send import send_resource_message
from keyboards import ikb_celebrity, rkb_main_menu

from logger import logging


logger = logging.getLogger(__name__)

command_router = Router()

@command_router.message(Command('start'))
@command_router.message(F.text == 'Закончить')
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
    buttons = ['/random', '/gpt', '/talk', '/quiz',]
    await send_resource_message(message, bot, file_name, keyboard=rkb_main_menu(buttons), use_answer=True)


@command_router.message(Command('random'))
@command_router.message(F.text == 'Хочу еще факт')
async def cmd_random(message: Message, bot: Bot):
    """
    Обрабатывает команду /random и сообщение 'Хочу еще факт'.
    
    Отправляет пользователю заранее заготовленное изображение и делает запрос к ChatGPT с
    заранее заготовленным промптом. Ответ ChatGPT передается пользователю. К сообщению
    прикрепляются кнопки 'Закончить' и 'Хочу еще факт'.
    
    :param message: Сообщение от пользователя.
    :param bot: Экземпляр бота.
    """
    file_name = 'random'
    buttons = ['Хочу еще факт', 'Закончить',]
    message_text = await gpt_client.random_request()
    await send_resource_message(
        message, bot, file_name, keyboard=rkb_main_menu(buttons), use_answer=True, caption=message_text)


@command_router.message(Command('talk'))
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


@command_router.message(Command('gpt'))
async def cmd_gpt(message: Message, bot: Bot, state: FSMContext):
    """
    Обрабатывает команду /gpt.
    
    Устанавливает состояние ожидания запроса от пользователя и отправляет ему заранее
    заготовленное изображение. Ожидает текстовое сообщение от пользователя для передачи
    его в ChatGPT.
    
    :param message: Сообщение от пользователя.
    :param bot: Экземпляр бота.
    :param state: Контекст состояния для управления состоянием бота.
    """
    await state.set_state(ChatGPTRequests.wait_gpt_request)
    file_name = 'gpt'
    await send_resource_message(message, bot, file_name, use_answer=True)


@command_router.message(ChatGPTRequests.wait_gpt_request)
async def wait_for_gpt_handler(message: Message, bot: Bot):
    file_name = 'gpt'
    message_text = await gpt_client.gpt_request(message.text)
    await send_resource_message(message, bot, file_name, use_answer=True, caption=message_text)


@command_router.message()
async def default_handler(message: Message, bot: Bot, state: FSMContext):
    """
    Обрабатывает все остальные сообщения от пользователя.

    Если сообщение является командой (начинается с '/'), и это не команда /gpt,
    очищает состояние и уведомляет пользователя о том, что команда не распознана.

    :param message: Сообщение от пользователя.
    :param bot: Экземпляр бота.
    :param state: Контекст состояния для управления состоянием бота.
    """
    # Проверяем, является ли сообщение командой
    if message.text.startswith('/'):
        if message.text != '/gpt':
            await state.clear()
            await message.reply(f'Команда: "{message.text}" не распознана. Состояние очищено.')

