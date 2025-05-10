from typing import Dict, Any
from openai import AsyncOpenAI, OpenAIError
from httpx import AsyncClient, HTTPStatusError

from classes import GPTMessage
from config import Config
from logger import logging


logging = logging.getLogger(__name__)

class ChatGPT:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._initialized = True  # Устанавливаем флаг инициализации
            logging.debug('Initializing ChatGPT')

            config: Dict[str, Any] = Config().get_config('gpt', 'proxy')
            self._gpt_token: str = config.get('gpt_token', '')
            self._gpt_model: str = config.get('gpt_model', 'gpt-3.5-turbo')
            self._proxy: str = config.get('proxy_address', '')
            self._client: AsyncOpenAI = self._create_client()
    
    def _create_client(self) -> AsyncOpenAI:
        """
        Создает экземпляр AsyncOpenAI клиента.

        :return: Экземпляр AsyncOpenAI.
        :raises ValueError: Если токен или адрес прокси недействительны.
        :raises Exception: Если возникает ошибка при создании клиента.
        """
        if not self._gpt_token:
            logging.error('Недействительный токен GPT.')
            raise ValueError('Токен GPT не может быть пустым.')
        
        if not self._proxy:
            logging.warning('Адрес прокси не указан. Используется прямое соединение.')
        
        try:
            gpt_client = AsyncOpenAI(
                api_key=self._gpt_token, http_client=AsyncClient(proxy=self._proxy if self._proxy else None, ))
            logging.info('Клиент OpenAI успешно создан.')
            return gpt_client
        except Exception as e:
            logging.exception(f'Ошибка при создании клиента OpenAI: "{e}".')
            raise
    
    async def request(self, messages: GPTMessage) -> str:
        """
        Получает ответ от модели ChatGPT на основе переданных сообщений.

        :param messages: Объект GPTMessage, содержащий список сообщений.
        :return: Ответ модели ChatGPT в виде строки.
        """
        try:
            response = await self._client.chat.completions.create(
                messages=messages.message_list,
                model=self._gpt_model,
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            logging.error(f'Ошибка OpenAI: "{e}"')
            return 'Ошибка при получении ответа от ChatGPT.'
        except HTTPStatusError as e:
            logging.error(f'HTTP ошибка: "{e.response.status_code}" - "{e.response.text}"')
            return 'Ошибка в HTTP запросе.'
        except Exception as e:
            logging.exception(f'Неизвестная ошибка при запросе к ChatGPT: "{e}".')
            return "Произошла неизвестная ошибка."
