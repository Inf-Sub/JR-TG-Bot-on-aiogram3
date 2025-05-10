from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from classes.states import Random
from handlers.messages import msg_random_next_handler
from misc import bot_thinking

from logger import logging


logging = logging.getLogger(__name__)

cmd_random_router = Router()
command = 'random'

@cmd_random_router.message(Command(command))
# @cmd_random_router.message(Random.quiz_wait_for_answer, F.text == 'Хочу еще факт')
async def cmd_random(message: Message, state: FSMContext):
    await state.set_state(Random.wait_gpt_answer)
    await bot_thinking(message)
    await msg_random_next_handler(message, state)

