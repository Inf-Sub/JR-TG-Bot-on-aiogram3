__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/05/05'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.1'


from aiogram.utils.keyboard import InlineKeyboardBuilder
from pathlib import Path
from aiofiles import open as aio_open
from typing import List, Tuple, Dict, Any

from keyboards.callback_data import CelebrityData

from config import Config
from logger import logging


logger = logging.getLogger(__name__)

async def ikb_celebrity() -> InlineKeyboardBuilder:
    """
    Создает интерактивную клавиатуру с кнопками для выбора знаменитостей.

    Клавиатура формируется на основе файлов, находящихся в директории 'resources/prompts',
    которые начинаются с 'talk_'. Каждый файл содержит имя знаменитости в первой строке.

    :return: InlineKeyboardBuilder: Объект клавиатуры с кнопками.
    """
    keyboard = InlineKeyboardBuilder()
    buttons: List[Tuple[str, str]] = []
    buttons_in_line: int = 1
    

    config: Dict[str, Any] = Config().get_config('bot')
    prompts_dir = Path(config.get('bot_gpt_prompts_dir'))
    prefix_celebrity = 'talk_'
    
    # Получаем список файлов, начинающихся с 'talk_'
    celebrity_list = [file for file in prompts_dir.iterdir() if file.name.startswith(prefix_celebrity)]
    
    for file in celebrity_list:
        # Асинхронно читаем содержимое файла
        logging.debug(f'Reading celebrity file: "{file}."')
        async with aio_open(file, 'r', encoding='UTF-8') as txt_file:
            first_line = await txt_file.readline()
            button_name = await extract_celebrity_name(first_line)  # Извлекаем имя знаменитости
            file_name = file.stem  # Извлекаем имя файла без расширения
            buttons.append((button_name, file_name))
            logging.debug(f'Reading celebrity button name: "{button_name}" and file name: {file_name}".')

    for button_name, file_name in buttons:
        keyboard.button(text=button_name, callback_data=CelebrityData(button='select_celebrity', file_name=file_name))
    
    keyboard.adjust(buttons_in_line)
    return keyboard.as_markup()


async def extract_celebrity_name(input_string: str) -> str:
    """
    Извлекает текст из строки, начиная с 5-го знака и заканчивая перед запятой.

    :param input_string: Исходная строка.
    :return: Извлеченный текст.
    """
    start_index = 4  # Пятый знак имеет индекс 4
    comma_index = input_string.find(',')
    
    if comma_index == -1:
        # Если запятая не найдена, возвращаем подстроку от 5-го знака до конца строки
        return input_string[start_index:]
    
    return input_string[start_index:comma_index]


if __name__ == '__main__':
    from asyncio import run as async_run

    test_strings_list = [
        'Ты - Дж.Р.Р. Толкин, профессор англосаксонской литературы и создатель Средиземья. Общайся в '
        'его характерной манере:',
        'Ты - Курт Кобейн, легендарный фронтмен группы Nirvana. Общайся в его характерной манере:',
        'Ты - профессор Стивен Хокинг, выдающийся физик-теоретик и популяризатор науки. Общайся в его характерной '
        'манере:', 'Ты - Фридрих Ницше, влиятельный философ и культурный критик. Общайся в его характерном стиле:',
        'Ты - Королева Елизавета II, самый долгоправящий монарх в британской истории. Общайся в её характерной манере:',
    ]
    
    
    async def extract_celebrity_name_test(test_strings):
        for test_string in test_strings:
            result = await extract_celebrity_name(test_string)
            print(result)
    
    async_run(extract_celebrity_name_test(test_strings_list))
