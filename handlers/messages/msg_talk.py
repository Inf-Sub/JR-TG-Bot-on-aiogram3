from typing import Dict

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from classes import ChatGPT, GPTMessage
from classes.enums import GPTRole
from classes.states import TalkWithCelebrity
from handlers.commands import cmd_start
from keyboards.reply import rkb_talk_end

from misc import bot_thinking

from logger import logging


logging = logging.getLogger(__name__)

msg_talk_router = Router()

@msg_talk_router.message(TalkWithCelebrity.wait_gpt_answer, F.text != 'Попрощаться!')
async def msg_talk_handler(message: Message, state: FSMContext):
    await bot_thinking(message)

    user_id = message.from_user.id
    current_state = await state.get_data()
    if not current_state:
        logging.warning(f'State is not set. Handler will not be executed.')
        await message.bot.send_message(
            chat_id=user_id,
            text='Выберите личность в меню выше 👆 или начните разговор снова: /talk.\n'
                 'Или воспользуйтесь меню по команде:\n/start',
        )
        await state.clear()
        return

    data: Dict[str, GPTMessage | str] = await state.get_data()
    data['messages'].update(GPTRole.USER, message.text)

    gpt_client = ChatGPT()
    response = await gpt_client.request(data['messages'])

    data['messages'].update(GPTRole.ASSISTANT, response)
    await state.update_data(data)
    
    print(f'msg_talk_handler:\n{message.text=}\n\n{data=}\n\n{response=}\n\n{'=' * 40}')
    
    await message.answer_photo(
        photo=data['photo'],
        caption=response,
        reply_markup=rkb_talk_end(),
    )

@msg_talk_router.message(TalkWithCelebrity.wait_gpt_answer, F.text == 'Попрощаться!')
async def msg_talk_end_handler(message: Message, state: FSMContext):
    await bot_thinking(message)
    await state.clear()
    await cmd_start(message)
