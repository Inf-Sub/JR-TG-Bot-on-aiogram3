__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/05/06'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.3'


from typing import Dict, Any, Optional, Union
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.enums import ChatAction
from pathlib import Path
from aiofiles import open as aio_open

from config import Config
from logger import logging


logger = logging.getLogger(__name__)


async def send_resource_message(
        message: Union[Message, CallbackQuery], bot: Bot, file_name: str, messages_dir: str = None, images_dir: str = None,
        caption: Optional[str] = None, use_answer: bool = False, keyboard: Optional[
            Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]] = None
) -> None:
    config: Dict[str, Any] = Config().get_config('bot')
    chat_id: int = message.from_user.id
    message_text: Optional[str] = None
    
    await bot.send_chat_action(
        chat_id=chat_id,
        action=ChatAction.TYPING,
    )
    
    if messages_dir is None:
        messages_dir = config.get('bot_messages_dir')
    
    if images_dir is None:
        images_dir = config.get('bot_images_dir')
    
    photo_path = Path(f'{images_dir}/{file_name}.jpg')
    message_path = Path(f'{messages_dir}/{file_name}.txt')
    
    logging.debug(f'Chat id: {chat_id} | File paths: image="{photo_path}", text="{message_path}".')
    
    photo_exists = photo_path.exists()
    text_exists = message_path.exists()
    
    if caption:
        message_text = caption
    elif text_exists:
        async with aio_open(message_path, 'r', encoding='UTF-8') as txt_file:
            message_text = await txt_file.read()


    # Логика отправки сообщений
    if photo_exists and message_text:
        # Отправляем и фото, и текст
        photo = FSInputFile(photo_path)
        if use_answer:
            await message.answer_photo(photo=photo, caption=message_text, reply_markup=keyboard)
        else:
            await bot.send_photo(chat_id=chat_id, photo=photo, caption=message_text, reply_markup=keyboard)
    elif photo_exists:
        # Отправляем только фото
        photo = FSInputFile(photo_path)
        if use_answer:
            await message.answer_photo(photo=photo, reply_markup=keyboard)
        else:
            await bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=keyboard)
            
    elif message_text:
        # Отправляем только текст
        if use_answer:
            await message.answer_message(text=message_text, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=keyboard)
    else:
        logging.warning(f'Neither photo nor text exists for file name: "{file_name}".')
        return
    
    # Логирование отсутствующих ресурсов
    if not photo_exists:
        logging.warning(f'Photo does not exist for file name: "{file_name}".')
    
    if not text_exists and not caption:
        logging.warning(f'Text does not exist for file name: "{file_name}".')
