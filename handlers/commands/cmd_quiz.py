from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from classes import Resource
from classes.states import Quiz
from keyboards.inline import ikb_quiz_select_topic
from misc import bot_thinking

from logger import logging


logging = logging.getLogger(__name__)

cmd_quiz_router = Router()
command = 'quiz'

@cmd_quiz_router.message(Command(command))
async def cmd_quiz(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает команду квиза, устанавливает состояние и отправляет пользователю сообщение с фотографией.

    :param message: Сообщение, содержащее информацию о команде.
    :param state: Контекст состояния для управления состоянием пользователя.
    :return: None
    """
    logging.debug('cmd_quiz')
    await state.set_state(Quiz.quiz_select_topic)
    await bot_thinking(message)
    resource = Resource(command)
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=ikb_quiz_select_topic(),
    )
