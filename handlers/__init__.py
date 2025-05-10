from misc import find_routers

from .commands import *
from .callbacks import *
from .messages import *
from .missed import *

from logger import logging


logging = logging.getLogger(__name__)

# Поиск и добавление routers в список routers_list
routers_list = []
routers_list.extend(find_routers(commands))
routers_list.extend(find_routers(callbacks))
routers_list.extend(find_routers(messages))
routers_list.extend(find_routers(missed))
# for test:
# routers_list.append(missed_messages_router)

logging.debug(f'Imported {len(routers_list)} routers in "routers_list".')

__all__ = [
    'routers_list',
]
