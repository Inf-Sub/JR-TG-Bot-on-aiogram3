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

