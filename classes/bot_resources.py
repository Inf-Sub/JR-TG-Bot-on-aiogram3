from aiogram.types import FSInputFile
# from aiofiles import open as aio_open
from typing import Optional, Dict, Union
from pathlib import Path

from classes.enums import ResourcePath, Extensions

from logger import logging


logging = logging.getLogger(__name__)


class Resource:
    """
    Класс для работы с ресурсами, такими как изображения и текстовые файлы.

    :param file_name: Имя файла, используемое для генерации путей к ресурсам.
    """
    #
    def __init__(self, file_name: str) -> None:
        self._file_name = file_name
    
    def _get_path(self, resource_type: str, extension: str) -> Path:
        """
        Получает путь к ресурсу.

        :param resource_type: Тип ресурса (например, 'images' или 'messages').
        :param extension: Расширение файла (например, '.jpg' или '.txt').
        :return: Путь к ресурсу.
        """
        return Path(resource_type, f'{self._file_name}{extension}')
    
    @property
    def photo(self) -> Optional[FSInputFile]:
        """
        Получает объект изображения, если он существует.

        :return: Объект изображения или None, если файл не найден.
        """
        photo_path = self._get_path(ResourcePath.IMAGES.value, Extensions.JPG.value)
        logging.debug(f'Photo path: "{photo_path}". Photo exists: {photo_path.exists()}')
        return FSInputFile(photo_path) if photo_path.exists() else None
    
    @property
    def text(self) -> Optional[str]:
        """
        Асинхронно получает текст из файла, если он существует.

        :return: Содержимое текстового файла или None, если файл не найден.
        """
        return self._read_file(ResourcePath.MESSAGES.value, Extensions.TXT.value)
    
    @property
    def prompt(self) -> Optional[str]:
        """
        Асинхронно получает текст из файла-промпта, если он существует.

        :return: Содержимое текстового файла-промпта или None, если файл не найден.
        """
        return self._read_file(ResourcePath.PROMPTS.value, Extensions.TXT.value)
    
    def _read_file(self, resource_type: str, extension: str) -> Optional[str]:
        """
        Асинхронно читает содержимое файла.

        :param resource_type: Тип ресурса, используемыйдля построения пути.
        :param extension: Расширение файла.
        :return: Содержимое файла или None, если файл не найден.
        """
        file_path = self._get_path(resource_type, extension)
        if file_path.exists():
            with open(file_path, 'r', encoding='UTF-8') as file:
                return file.read()
        return None
    
    def as_kwargs(self) -> Dict[str, Union[FSInputFile, Optional[str]]]:
        """
        Возвращает словарь с ресурсами в виде ключей и значений.

        :return: Словарь с изображением и текстом.
        """
        return {'photo': self.photo, 'caption': self.text, }
