from os import getenv
from dotenv import load_dotenv

load_dotenv()


def load_env() -> dict:
    """
    Загрузка переменных окружения из файла .env.
    """
    # Загрузка всех переменных, которые могут понадобиться в проекте
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
    }

def get_tg_config() -> dict:
    """
    Получение конфигурации для подключения к API Telegram.
    """
    env = load_env()
    return {
        'tg_token': env['TG_TOKEN'],
    }
