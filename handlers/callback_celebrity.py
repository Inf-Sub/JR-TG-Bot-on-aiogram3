__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/05/06'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.3'

from typing import Dict, Any

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from handlers.send import send_photo_and_text
from keyboards.callback_data import CelebrityData

from config import Config
from logger import logging


logger = logging.getLogger(__name__)

callback_celebrity_router = Router()

@callback_celebrity_router.callback_query(CelebrityData.filter(F.button == 'select_celebrity'))
async def celebrity_callbacks(callback: CallbackQuery, callback_data: CelebrityData, bot: Bot):
    config: Dict[str, Any] = Config().get_config('bot')
    prompts_dir = config.get('bot_gpt_prompts_dir')
    file_name = callback_data.file_name

    await send_photo_and_text(bot, callback.from_user.id, file_name, prompts_dir)
