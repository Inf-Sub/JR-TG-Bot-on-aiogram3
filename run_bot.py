__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/04/27'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.2'

from typing import Dict, Any

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from asyncio import run as async_run

from config import Config
from handlers import routers_list
from misc import on_start, on_shutdown
from logger import logging


logging = logging.getLogger(__name__)

async def start_bot() -> None:
    config: Dict[str, Any] = Config().get_config('tg')
    bot = Bot(
        token=config['tg_token'], default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )
    dp = Dispatcher()

    dp.include_routers(*routers_list)

    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    
    about_bot = await bot.me()
    logging.warning(
        'Run polling for bot: @%s. ID: %d. Bot name: %r', about_bot.username, bot.id, about_bot.full_name)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        async_run(start_bot())
    except KeyboardInterrupt:
        logging.warning('Bot stopped by user')
