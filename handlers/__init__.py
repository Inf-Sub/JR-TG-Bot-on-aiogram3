__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/04/27'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '1.0.1'

from handlers.commands.cmd_start import cmd_start_router
from handlers.commands.cmd_random import cmd_random_router
from handlers.commands.cmd_talk import cmd_talk_router
from handlers.commands.cmd_gpt import cmd_gpt_router

# from .entities import entities_router
from callbacks.callback_celebrity import callback_celebrity_router
# for test
from .all_messages import all_messages_router


routers_list = [
    cmd_start_router,
    cmd_random_router,
    cmd_talk_router,
    cmd_gpt_router,
    
    # entities_router,
    callback_celebrity_router,
    # for test
    all_messages_router,
]

__all__ = [
    'routers_list',
]
