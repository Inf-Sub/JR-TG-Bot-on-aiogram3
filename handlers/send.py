__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/05/06'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.3'


from typing import Dict, Any, Optional
from aiogram import Bot
from aiogram.types import FSInputFile
from pathlib import Path
from aiofiles import open as aio_open

from config import Config
from logger import logging


logger = logging.getLogger(__name__)

async def send_photo_and_text(
        bot: Bot, chat_id: int, file_name: str, messages_dir: str = None, images_dir: str = None) -> None:
    config: Dict[str, Any] = Config().get_config('bot')

    if messages_dir is None:
        messages_dir = config.get('bot_messages_dir')
    
    if images_dir is None:
        images_dir = config.get('bot_images_dir')

    photo_path = Path(f'{images_dir}/{file_name}.jpg')
    message_path = Path(f'{messages_dir}/{file_name}.txt')

    logging.debug(f'Chat id: {chat_id} | File paths: image="{photo_path}", text="{message_path}".')

    photo_exists = photo_path.exists()
    text_exists = message_path.exists()

    if not photo_exists and not text_exists:
        logging.warning(f'Neither photo nor text exists for file name: "{file_name}".')
        return

    message_text: Optional[str] = None
    if text_exists:
        async with aio_open(message_path, 'r', encoding='UTF-8') as txt_file:
            message_text = await txt_file.read()

    if photo_exists:
        photo = FSInputFile(photo_path)
        await bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=message_text if message_text else None,
        )
        if not message_text:
            logging.warning(f'Sent photo without text for file name: "{file_name}".')
    elif message_text:
        await bot.send_message(
            chat_id=chat_id,
            text=message_text,
        )
        logging.warning(f'Sent text without photo for file name: "{file_name}".')

    if not photo_exists:
        logging.warning(f'Photo does not exist for file name: "{file_name}".')

    if not text_exists:
        logging.warning(f'Text does not exist for file name: "{file_name}".')