from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from classes import Resource, ChatGPT, GPTMessage
from classes.states import Random
from handlers.commands import cmd_start
from keyboards.reply import rkb_main_menu

from misc import bot_thinking

from logger import logging


logging = logging.getLogger(__name__)

msg_random_router = Router()

@msg_random_router.message(Random.wait_gpt_answer, F.text == 'Хочу еще факт')
async def msg_random_next_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await state.set_state(Random.wait_gpt_answer)
        
    logging.debug(f'Fact: "{message.text}"')

    gpt_client = ChatGPT()
    await bot_thinking(message)
    resource = Resource('random')
    gpt_message = GPTMessage('random')
    buttons = ['Хочу еще факт', 'Закончить', ]
    msg_text = await gpt_client.request(gpt_message)
    logging.debug(f'Message text: "{msg_text}".')
    await message.answer_photo(
        photo=resource.photo,
        caption=msg_text,
        reply_markup=rkb_main_menu(buttons),
    )

@msg_random_router.message(Random.wait_gpt_answer, F.text == 'Закончить')
async def msg_random_end_handler(message: Message, state: FSMContext):
    await bot_thinking(message)
    await state.clear()
    await cmd_start(message)