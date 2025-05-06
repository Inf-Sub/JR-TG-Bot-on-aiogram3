__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/04/27'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.2'

from typing import Dict, Any

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiofiles import open as aio_open
from pathlib import Path

from classes import gpt_client
from handlers.handlers_state import ChatGPTRequests
from handlers.send import send_photo_and_text
from keyboards import ikb_celebrity, rkb_main_menu

from config import Config
from logger import logging


logger = logging.getLogger(__name__)

command_router = Router()

# @command_router.message(Command('start'))
# async def command_start(message: Message) -> None:
#     await message.reply(
#         test="главное меню бота",
#     )

@command_router.message(Command('start'))
@command_router.message(F.text == 'Закончить')
async def com_start(message: Message):
    config: Dict[str, Any] = Config().get_config('bot')
    images_dir = config.get('bot_images_dir')
    messages_dir = config.get('bot_messages_dir')
    file_name = 'main'
    
    photo_path = Path(f'{images_dir}/{file_name}.jpg')
    messages_path = Path(f'{messages_dir}/{file_name}.txt')
    
    photo_exists = photo_path.exists()
    text_exists = messages_path.exists()

    if photo_exists:
        photo = FSInputFile(photo_path)
    
    buttons = [
        '/random',
        '/gpt',
        '/talk',
        '/quiz',
    ]
    if text_exists:
        async with aio_open(messages_path, 'r', encoding='UTF-8') as file:
            message_text = await file.read()

        await message.answer_photo(
            photo=photo,
            caption=message_text,
            reply_markup=rkb_main_menu(buttons),
        )


@command_router.message(Command('random'))
@command_router.message(F.text == 'Хочу еще факт')
async def com_random(message: Message, bot: Bot):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    config: Dict[str, Any] = Config().get_config('bot')
    images_dir = config.get('bot_images_dir')
    messages_dir = config.get('bot_messages_dir')
    file_name = 'random'
    
    photo_path = Path(f'{images_dir}/{file_name}.jpg')
    
    photo_exists = photo_path.exists()
    
    if photo_exists:
        photo = FSInputFile(photo_path)
    
    buttons = [
        'Хочу еще факт',
        'Закончить',
    ]
    message_text = await gpt_client.random_request()
    await message.answer_photo(
        photo=photo,
        caption=message_text,
        reply_markup=rkb_main_menu(buttons),
    )

@command_router.message(Command('gpt'))
async def com_gpt(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(ChatGPTRequests.wait_for_request)
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    config: Dict[str, Any] = Config().get_config('bot')
    images_dir = config.get('bot_images_dir')
    messages_dir = config.get('bot_messages_dir')
    file_name = 'gpt'
    
    photo_path = Path(f'{images_dir}/{file_name}.jpg')
    messages_path = Path(f'{messages_dir}/{file_name}.txt')
    
    photo_exists = photo_path.exists()
    text_exists = messages_path.exists()
    
    if photo_exists:
        photo = FSInputFile(photo_path)

    if text_exists:
        async with aio_open(messages_path, 'r', encoding='UTF-8') as file:
            message_text = await file.read()

    if photo_exists and text_exists:
        await message.answer_photo(
            photo=photo,
            caption=message_text,
        )

    # await send_photo_or_text(bot, message.from_user.id, file_name)

# @command_router.message(Command('talk'))
# async def command_start(message: Message) -> None:
#     await message.reply(
#         test="поговорить с известной личностью",
#     )
#
# @command_router.message(Command('quiz'))
# async def command_start(message: Message) -> None:
#     await message.reply(
#         test="проверить свои знания",
#     )
   
