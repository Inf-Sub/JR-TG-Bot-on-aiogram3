__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/04/27'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.2'

from aiogram import Bot, Dispatcher
from asyncio import run as async_run

from config import Config
from handlers import main_router
from misk import *
from logger import logging


logging = logging.getLogger(__name__)

async def start_bot() -> None:
    env: dict = Config().get_config(config_type='tg')
    bot = Bot(token=env['tg_token'])
    dp = Dispatcher()

    dp.include_router(main_router)
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        async_run(start_bot())
    except KeyboardInterrupt:
        logging.warning('Bot stopped by user')
