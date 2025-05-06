__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/05/05'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Production'  # 'Production / Development'
__version__ = '1.0.0'

from os.path import join as os_join
from pathlib import Path
from datetime import datetime as dt
from typing import Optional, Dict, Any

from aiofiles import open as aio_open

from config import Config
from logger import logging

logger = logging.getLogger(__name__)


class AsyncFileSaver:
    """
    Класс для асинхронного сохранения вопросов и ответов к ChatGPT.

    :ivar _folder_path (Path): Путь к папке, где будут сохраняться файлы.
    :ivar _file_name (str): Имя файла, в который будут сохраняться данные.
    :ivar _separator (str): Разделитель между вопросами и ответами.
    """
    
    def __init__(self, folder_name: Optional[str] = None, file_name: Optional[str] = None) -> None:
        """
        Инициализирует AsyncFileSaver с указанными параметрами пути к папке и имени файла.

        :param folder_name: Имя папки для сохранения файлов.
        :param file_name: Имя файла для сохранения данных.
        """
        config: Dict[str, Any] = Config().get_config('save')
        
        self._folder_path = None
        self._folder_name: str = folder_name if folder_name else config.get('save_dir', r'SAVE_GPT_QA\%Y\%m')
        self._file_name: str = file_name if file_name else config.get('save_file', 'GPT_QA_%Y.%m.%d_%H.%M.%S.txt')
        self._separator: str = f'\n\n{"=" * 50}\n\n'
    
    async def _ensure_folder_exists(self) -> bool:
        """
        Проверяет существование папки и создаёт её, если она не существует.
        """
        try:
            if self._folder_name.exists() and not self._folder_name.is_dir():
                raise NotADirectoryError(f'Path exists but is not a directory: {self._folder_name}')
            self._folder_name.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f'Failed to create directory: {e}')
        return False
    
    async def _save_qa_pair(self, question: str, answer: str) -> None:
        """
        Сохраняет пару вопрос-ответ в файл.

        :param question: Вопрос для сохранения.
        :param answer: Ответ для сохранения.
        """
        file_path = os_join(self._folder_name, self._file_name)
        formatted_file_path = dt.now().strftime(file_path)
        self._folder_path: Path = Path(formatted_file_path)
        self._folder_name: Path = self._folder_path.parent
        
        # Убедитесь, что папка существует перед сохранением
        if await self._ensure_folder_exists():
            async with aio_open(formatted_file_path, 'a', encoding='utf-8') as file:
                # Проверяем, если файл пустой, то записываем вопрос и разделитель
                if self._folder_path.stat().st_size == 0:
                    await file.write(question)
                    await file.write(self._separator)
                await file.write(answer)
            
            logger.info(f'Содержимое переменных "question" и "answer" сохранено в файл: {formatted_file_path}')

    async def save(self, question: str, answer: str) -> None:
        """
        Сохраняет вопрос и ответ, если они не пустые.

        :param question: Вопрос для сохранения.
        :param answer: Ответ для сохранения.
        """
        if question and answer:
            await self._save_qa_pair(question, answer)
        else:
            logger.warning('Вопрос или ответ пусты. Сохранение не выполнено.')


if __name__ == '__main__':
    from asyncio import run as async_run, sleep as aio_sleep
    
    async def saver_main_test():
        file_saver = AsyncFileSaver()
        await file_saver.save('question 1', 'answer 1')
        await aio_sleep(1)
        await file_saver.save('question 2', 'answer 2')
        await aio_sleep(1)
        await file_saver.save('question 3', '')
        await aio_sleep(1)
        await file_saver.save('', 'answer 4')
        await aio_sleep(1)
        await file_saver.save('', '')
    
    async_run(saver_main_test())