from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from classes import Resource
from classes.states import ChatGPTRequests
from misc import bot_thinking


cmd_gpt_router = Router()
command = 'gpt'

@cmd_gpt_router.message(Command(command))
async def cmd_gpt(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает команду для общения с ChatGPT, очищает состояние и устанавливает ожидание ответа.

    :param message: Сообщение, содержащее информацию о команде.
    :param state: Контекст состояния для управления состоянием пользователя.
    :return: None
    """
    await state.clear()
    await state.set_state(ChatGPTRequests.wait_gpt_answer)
    await bot_thinking(message)
    resource = Resource(command)
    await message.answer_photo(
        **resource.as_kwargs(),
    )
