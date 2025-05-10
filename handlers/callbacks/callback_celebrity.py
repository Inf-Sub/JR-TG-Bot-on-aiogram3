from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from classes import Resource, Button, GPTMessage
from classes.states import TalkWithCelebrity
from classes.callbacks import TalkWithCelebrityData

from logger import logging


logging = logging.getLogger(__name__)

callback_celebrity_router = Router()

@callback_celebrity_router.callback_query(TalkWithCelebrityData.filter(F.button == 'select_celebrity'))
async def celebrity_callbacks(callback: CallbackQuery, callback_data: TalkWithCelebrityData, bot: Bot, state: FSMContext) -> None:
    photo = Resource(callback_data.file_name).photo
    button_name = Button(callback_data.file_name).name
    await callback.answer(
        text=f'С тобой говорит {button_name}.',
    )
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption=f'С тобой говорит: {button_name}.\nЗадайте свой вопрос:',
    )
    request_message = GPTMessage(callback_data.file_name)
    await state.set_state(TalkWithCelebrity.wait_gpt_answer)
    await state.set_data({'messages': request_message, 'photo': photo})

    logging.debug(f'TALK CELEBRITY CALLBACK DATA: {callback.data} | Type: {type(callback.data)}')
    logging.debug(f'TALK CELEBRITY CALLBACK _DATA: {callback_data} | Type: {type(callback_data)}')
    get_state = await state.get_state()
    logging.debug(f'TALK CELEBRITY CALLBACK STATE: {get_state}')


# from typing import Dict, Any
#
# from aiogram import Bot, Router, F
# from aiogram.types import CallbackQuery
#
# from handlers.send import send_resource_message
# from classes.bot_callback_data import TalkWithCelebrityData
#
# from config import Config
# from logger import logging
#
#
# logging = logging.getLogger(__name__)
#
# callback_celebrity_router = Router()
#
# @callback_celebrity_router.callback_query(TalkWithCelebrityData.filter(F.button == 'select_celebrity'))
# async def callback_celebrity(callback: CallbackQuery, callback_data: TalkWithCelebrityData, bot: Bot):
#     config: Dict[str, Any] = Config().get_config('bot')
#     prompts_dir = config.get('bot_gpt_prompts_dir')
#     file_name = callback_data.file_name
#     logging.error(f'DEBUG: Used callback_celebrity: {callback.data}')
#
#     await send_resource_message(callback, bot, file_name, prompts_dir)
#
#
# # @callback_celebrity_router.callback_query_handler(text="button_click")
# # async def handle_button_click(callback_query: CallbackQuery, bot: Bot):
# #     # Обработка нажатия кнопки
# #     await bot.answer_callback_query(callback_query.id)  # Подтверждаем нажатие кнопки
