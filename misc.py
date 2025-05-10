# from datetime import datetime
from pkgutil import iter_modules
from importlib import import_module
from typing import List, Dict, Any, Union
import json

from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ChatAction

from config import Config
from logger import logging


logging = logging.getLogger(__name__)

def on_start():
    # formatted_date_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    logging.warning(f'Bot is started...')


def on_shutdown():
    # formatted_date_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    logging.warning(f'Bot is down now...')


async def bot_thinking(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )


def find_routers(module: str) -> List[Router]:
    """
    Ищет и собирает все экземпляры Router в указанных модулях.

    :param module: Имя модуля, в котором будет производиться поиск маршрутизаторов.
    :return: Список всех найденных экземпляров Router.
    """
    _routers_list: List[Router] = []
    
    # Импортируем модули синхронно, так как это блокирующая операция
    for _, module_name, _ in iter_modules(module.__path__):
        full_module_name = f"{module.__name__}.{module_name}"
        imported_module = import_module(full_module_name)
        logging.debug(f'Module "{full_module_name}" imported.')
        
        # Ищем все атрибуты в модуле и добавляем только те, которые являются Router
        for attr_name in dir(imported_module):
            attr = getattr(imported_module, attr_name)
            if isinstance(attr, Router):
                _routers_list.append(attr)
    
    return _routers_list


def is_admin(user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором.

    :param user_id: Идентификатор пользователя, который необходимо проверить.
    :return: True, если пользователь является администратором; иначе False.
    """
    # Получаем конфигурацию как словарь
    config: Dict[str, Any] = Config().get_config('bot')
    admins_str: str = config.get('bot_admins_list', '')

    # Разделяем строку на список идентификаторов администраторов
    if admins_str.strip() == '':
        admins: List[int] = []
    else:
        # Преобразуем строки в целые числа и удаляем пустые значения
        admins: List[int] = [int(admin_id.strip()) for admin_id in admins_str.split(',') if admin_id.strip().isdigit()]

    # Проверяем, содержится ли user_id в списке администраторов
    admin = user_id in admins
    logging.debug(f'User "{user_id}" is admin: {admin}.')
    return admin


def pretty_print(obj: Union[Dict[str, Any], List[Any], Any], indent: int = 0) -> None:
    """
    Рекурсивно печатает объект с отступами, аналогично формату JSON.

    :param obj: Объект для печати, который может быть словарем, списком или любым другим типом.
    :param indent: Уровень отступа для форматирования вывода. По умолчанию равен 0.
    :return: None: Функция ничего не возвращает, она просто выводит отформатированный объект в стандартный вывод.
    """
    spacing = ' ' * indent
    if isinstance(obj, dict):
        print(f'{spacing}{{')
        for key, value in obj.items():
            print(f'{spacing}    {json.dumps(key)}: ', end='')
            pretty_print(value, indent + 4)
        print(f'{spacing}}}')
    elif isinstance(obj, list):
        print(f'{spacing}[')
        for item in obj:
            pretty_print(item, indent + 4)
        print(f'{spacing}]')
    else:
        print(f'{spacing}{json.dumps(obj)}')
