from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from classes import Resource
from classes.states import TalkWithCelebrity
from keyboards.inline import ikb_talk_with_celebrity
from misc import bot_thinking


cmd_talk_router = Router()
command = 'talk'

@cmd_talk_router.message(Command(command))
async def cmd_talk(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает команду общения со знаменитостью, устанавливает состояние ожидания ответа и отправляет пользователю
    сообщение с фотографией.

    :param message: Сообщение, содержащее информацию о команде.
    :param state: Контекст состояния для управления состоянием пользователя.
    :return: None
    """
    await state.set_state(TalkWithCelebrity.wait_gpt_answer)
    await bot_thinking(message)
    resource = Resource(command)
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=ikb_talk_with_celebrity(),
    )
