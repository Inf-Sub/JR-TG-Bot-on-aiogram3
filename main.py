import logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold
from aiogram.utils.markdown import hide_link

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from typing import Dict, Any, Optional

from datetime import datetime, timedelta
from random import randint
import re

from config import get_tg_config
from random_fox import get_random_fox

dp = Dispatcher()

scheduler = AsyncIOScheduler()


@dp.message(Command("help"))
@dp.message(CommandStart(deep_link=True, magic=F.args == "help"))
async def cmd_start_help(message: Message):
    await message.answer("Это сообщение со справкой")


@dp.message(CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'book_(\d+)'))))

@dp.message(F.text, Command('start'))
async def command_start(message: Message):
    await message.reply('Hello, bro!')
    
    
@dp.message(F.text, Command("hello"))
async def cmd_hello(message: Message):
    content = Text(
        "Hello, ",
        Bold(message.from_user.full_name)
    )
    await message.reply(
        **content.as_kwargs()
    )


@dp.message(F.text, F.new_chat_members)
async def somebody_added(message: Message):
    for user in message.new_chat_members:
        # проперти full_name берёт сразу имя И фамилию
        # (на скриншоте выше у юзеров нет фамилии)
        await message.reply(f"Привет, {user.full_name}")


@dp.message(F.text, Command("hidden_link"))
async def cmd_hidden_link(message: Message):
    image_fox = await get_random_fox()
    await message.answer(
        f"{hide_link(image_fox['image'])}"
        f"Длинное сообщение с картинкой, но лимит на подписи к медиафайлам составляет всего 1024 символа против 4096 "
        f"у обычного текстового!"
    )


@dp.message(F.text, Command('fox'))
async def command_fox(message: Message, command: Optional[CommandObject] = None):
    if command.args is None or not command.args.isdigit():
        count = 1
    else:
        count = int(command.args)
    
    unique_image = set()
    index = 1
    while index <= count:
        date = datetime.now() + timedelta(seconds=randint(1, 10))
        
        dict_image_fox = await get_random_fox()
        if dict_image_fox['id'] in unique_image:
            continue
        
        fox_number = f' #{index}' if count > 1 else ''
        msg = await message.reply(f'Бегаем по лесу, ищем и фотографируем для Вас лису{fox_number}, ожидайте.')

        unique_image.add(dict_image_fox['id'])
        logger.info(f'{dict_image_fox=}')
        
        # options = LinkPreviewOptions(
        #     url=dict_image_fox['image'],
        #     prefer_large_media=True
        # )

        scheduler.add_job(
            edit_msg_fox, 'date', run_date=date, kwargs={
                'message': msg, 'image': dict_image_fox, 'index': index})
        
        # await edit_msg_fox(message=msg, image=dict_image_fox, index=index)

        index += 1
        
        # await message.answer_photo(
        # await message.reply_photo(
        #     photo=image_fox['image'],
        #     caption=f'Fox {index}: {image_fox['link'].split('=')[-1]}')


async def edit_msg_fox(message: Message, image: [str, str], index: int):
    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f'Image date: {formatted_datetime=}')
    
    await message.edit_text(
        f'{hide_link(image['image'])}'
        f'<b>Fox: {index}</b>\n'
        # f'<b>id: {image['link'].split('=')[1]}</b>\n\n'
        f'<b>id: {image['id']}</b>\n\n'
        f'<i>Фото сделано в: {formatted_datetime}</i>'
    )


async def main() -> None:
    env: Dict[str, Any] = get_tg_config()
    
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=env['tg_token'], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    scheduler.start()
    
    # And the run events dispatching
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    asyncio.run(main())
