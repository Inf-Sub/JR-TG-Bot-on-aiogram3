# from aiofiles import open as aio_open
from typing import List, Optional, AsyncIterator, Union
from pathlib import Path

from classes import ResourcePath, Extensions

from logger import logging


logging = logging.getLogger(__name__)


class Button:
    def __init__(self, *args: Union[str, None]) -> None:
        """
        Инициализирует кнопку с заданным путем и опциональным колбэком.

        :param args: Имя кнопки и колбэк, либо имя файла, для получения имени файла и считывания имени кнопки из файла.
        """
        self.name = None
        self.callback = None
        self._path = None
        path = None
        
        if len(args) == 1:
            path = args[0]
            self.callback = path
        elif len(args) == 2:
            self.name, self.callback = args
        elif len(args) > 2:
            raise ValueError("Button() принимает один или два аргумента")

        if self.name is None:
            self._path: Path = Path(ResourcePath.PROMPTS.value, f'{path}{Extensions.TXT.value}')
            self.name: Optional[str] = self.load_name()
        
        logging.debug(f'Args: {args} | Callback: {self.callback} | Name: {self.name} | Full Path: {self._path}')
    
    def load_name(self) -> Optional[str]:
        """
        Загружает имя знаменитости из текстового файла.

        :return: Имя знаменитости, если оно было загружено, иначе None.
        """
        try:
            with open(self._path, 'r', encoding='UTF-8') as txt_file:
                return self._extract_celebrity_name(txt_file.readline())
        except FileNotFoundError:
            logging.error(f"Файл не найден: {self._path}")
            return None

    @staticmethod
    def _extract_celebrity_name(input_string: str) -> Optional[str]:
        """
        Извлекает текст из строки, начиная с 6-го знака и заканчивая перед запятой.

        :param input_string: Исходная строка.
        :return: Извлеченный текст или None, если строка пустая.
        """
        if not input_string:
            return None  # Проверка на пустую строку
            
        start_index = 5  # Начинаем с 6 знака (индекс 5)
        comma_index = input_string.find(',')

        if comma_index == -1:
            # Если запятая не найдена, возвращаем подстроку от "start_index" до конца строки
            return input_string[start_index:].strip()  # Удаление лишних пробелов
        
        return input_string[start_index:comma_index].strip()  # Удаление лишних пробелов


class Buttons:
    def __init__(self, buttons: Optional[List[Button]] = None) -> None:
        """
        Инициализирует коллекцию кнопок.
        """
        self.buttons: List[Button] = self._read_buttons() if buttons is None else buttons
    
    @staticmethod
    def _read_buttons() -> List[Button]:
        """
        Загружает кнопки из файлов, начинающихся с 'talk_'.

        :return: Список загруженных кнопок.
        """
        resource_path = Path(ResourcePath.PROMPTS.value)
        # Получаем список файлов, которые начинаются с 'talk_'
        buttons_list = [file for file in resource_path.iterdir() if file.is_file() and file.name.startswith('talk_')]
        buttons = [Button(file.stem) for file in buttons_list]
        return buttons
    
    def __iter__(self) -> AsyncIterator[Button]:
        """
        Возвращает итератор для кнопок.

        :return: Итератор кнопок.
        """
        return self
    
    def __next__(self) -> Button:
        """
        Возвращает следующую кнопку.

        :return: Следующая кнопка.
        :raises StopIteration: Если кнопки закончились.
        """
        if self.buttons:
            return self.buttons.pop(0)
        raise StopIteration
