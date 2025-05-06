__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/04/27'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '1.0.0'

from aiogram import Router

from .commands import command_router
from .entities import entities_router
from .callback_celebrity import callback_celebrity_router
# for test
from .all_messages import all_messages_router

main_router: Router = Router()

main_router.include_routers(
    command_router,
    entities_router,
    callback_celebrity_router,
    # for test
    all_messages_router,
)

__all__ = [
    'main_router',
]
