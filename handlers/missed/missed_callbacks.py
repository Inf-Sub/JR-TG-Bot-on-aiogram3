__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/05/10'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '1.4.0'

from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from misc import is_admin
from logger import logging


logging = logging.getLogger(__name__)

missed_callbacks_router = Router()

@missed_callbacks_router.callback_query()
async def missed_callbacks(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    chat_id = callback.from_user.id  # or callback.message.chat.id
    if is_admin(chat_id):
        await bot.send_message(
            chat_id=chat_id,
            text=f'Привет, *{callback.from_user.full_name}*!\nЯ поймал не обработанный callback : ```callback:'
                 f' {callback.data}```',
        )
    else:
        logging.debug(f'MISSED CALLBACK: "{callback}"')

    logging.debug(f'MISSED CALLBACK DATA: "{callback.data}"')
    get_state = await state.get_state()
    logging.debug(f'MISSED CALLBACK STATE: {get_state}')