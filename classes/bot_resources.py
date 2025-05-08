from typing import Optional

from aiogram.types import FSInputFile
from pathlib import Path
from aiofiles import open as aio_open

from classes.bot_path import BotPath

class BotFile:
    def __init__(self, file_name: str, file_extension: str):
        self._file_name = f"{file_name}.{file_extension}" if not Path(file_name).suffix else file_name

    def get_file_path(self, path: Optional[str] = None) -> str:
        base_path = Path(__file__).parent.parent
        return str(base_path / (path or '') / self._file_name)

class BotPhoto(BotFile):
    def __init__(self, file_name: str):
        super().__init__(file_name, 'jpg')

    @property
    def photo(self) -> FSInputFile:
        return FSInputFile(self.get_file_path(BotPath.IMAGES.value))

class BotText(BotFile):
    def __init__(self, file_name: str):
        super().__init__(file_name, 'txt')

    @property
    async def text(self) -> str:
        async with aio_open(self.get_file_path(BotPath.MESSAGES.value), 'r', encoding='UTF-8') as file:
            return await file.read()

class BotPrompt(BotText):
    def __init__(self, file_name: str):
        super().__init__(file_name)

    @property
    async def text(self) -> str:
        async with aio_open(self.get_file_path(BotPath.PROMPTS.value), 'r', encoding='UTF-8') as file:
            return await file.read()


if __name__ == "__main__":
    from asyncio import run as async_run
    
    async def main_test():
        photo = BotPhoto("example_image")
        print(photo.get_file_path())
        print(photo.photo)

        text = BotText("main.txt")
        print(text.get_file_path())
        print(await text.text)

        text = BotPrompt("main.txt")
        print(text.get_file_path())
        print(await text.text)
    
    async_run(main_test())
    
