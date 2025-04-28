__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/04/28'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '1.0.4.5'

from os import getenv
# from os.path import join as os_join
# from decouple import config
from dotenv import load_dotenv
from datetime import datetime as dt
import logging

load_dotenv()


class Config:
    def __init__(self):
        # Загрузка переменных окружения из файла ._env
        load_dotenv()
        self._current_date = dt.now()
        self._env = self._load_env()
    
    def _load_env(self) -> dict:
        """
        Загрузка переменных окружения из файла ._env.

        :return: Возвращает словарь с параметрами из ._env файла.
        """
        current_date = self._current_date
        try:
            return {
                'TG_TOKEN': getenv('TG_TOKEN'),
        
                # 'DB_HOST': getenv('DB_HOST'),
                # 'DB_PORT': int(getenv('DB_PORT', 3306)),
                # 'DB_USER': getenv('DB_USER'),
                # 'DB_PASSWORD': getenv('DB_PASSWORD'),
                # 'DB_NAME': getenv('DB_NAME'),
                # 'DB_COLLATE': getenv('DB_COLLATE', 'utf8_general_ci'),
                # 'DB_SCHEMAS_PATH': getenv('DB_SCHEMAS_PATH'),
                # 'DB_FILE_INIT_SCHEMA': getenv('DB_FILE_INIT_SCHEMA'),
                # 'DB_FILE_TABLE_PREFIX': getenv('DB_FILE_TABLE_PREFIX'),
                # 'DB_FILE_INIT_DATA_PREFIX': getenv('DB_FILE_INIT_DATA_PREFIX'),
                
                'LOG_DIR': current_date.strftime(getenv('LOG_DIR', r'logs\%Y\%Y.%m')),
                'LOG_FILE': current_date.strftime(getenv('LOG_FILE', 'backup_log_%Y.%m.%d.log')),
                'LOG_LEVEL_ROOT': getenv('LOG_LEVEL_ROOT', 'INFO').upper(),
                'LOG_LEVEL_CONSOLE': getenv('LOG_LEVEL_CONSOLE', 'INFO').upper(),
                'LOG_LEVEL_FILE': getenv('LOG_LEVEL_FILE', 'WARNING').upper(),
                'LOG_FORMAT_CONSOLE': getenv('LOG_FORMAT_CONSOLE').replace(r'\t', '\t').replace(r'\n', '\n'),
                'LOG_FORMAT_FILE': getenv('LOG_FORMAT_FILE').replace(r'\t', '\t').replace(r'\n', '\n'),
                'LOG_DATE_FORMAT': getenv('LOG_DATE_FORMAT', '%Y.%m.%d %H:%M:%S'),  # Default: None
                'LOG_CONSOLE_LANGUAGE': getenv('LOG_CONSOLE_LANGUAGE', 'en').lower(),
            }
        except (TypeError, ValueError) as e:
            logging.error(e)
            exit()
    
    def get_config(self, config_type: str) -> dict:
        """
        Получение конфигурации по указанному типу.

        :param config_type: Префикс для поиска переменных окружения.
        :return: Возвращает словарь с параметрами, соответствующими указанному префиксу.
        """
        return {key.lower(): self._env[key] for key in self._env.keys() if key.startswith(config_type.upper() + '_')}


if __name__ == "__main__":
    from pprint import pprint
    
    config = Config()
    tg_config = config.get_config('TG')
    log_config = config.get_config('LOG')
    
    print("TeleGram Config:")
    pprint(tg_config)
    print()
    print("Log Config:")
    pprint(log_config)
