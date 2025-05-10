from typing import Dict

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from classes import Resource, ChatGPT, GPTMessage
from classes.enums import GPTRole
from classes.states import ChatGPTRequests
from misc import bot_thinking


msg_gpt_router = Router()
command = 'gpt'

@msg_gpt_router.message(ChatGPTRequests.wait_gpt_answer)
async def msg_gpt_handler(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщения, ожидая ответ от ChatGPT. Устанавливает состояние ожидания и обновляет данные состояния.

    :param message: Сообщение, содержащее текст от пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    :return: None
    """
    await bot_thinking(message)
    await state.set_state(ChatGPTRequests.wait_gpt_answer)

    photo = Resource(command).photo

    current_state = await state.get_data()

    if not current_state:
        request_message = GPTMessage(command)
        data: Dict[str, GPTMessage | str] = {'messages': request_message, 'photo': photo}
    else:
        data: Dict[str, GPTMessage | str] = current_state
        data['messages'].update(GPTRole.USER, message.text)

    gpt_client = ChatGPT()
    response = await gpt_client.request(data['messages'])

    data['messages'].update(GPTRole.ASSISTANT, response)
    await state.update_data(data)

    print(f'msg_gpt_handler:\n{message.text=}\n\n{data=}\n\n{response=}\n\n{'=' * 40}')

    await message.answer_photo(
        photo=photo,
        caption=response,
    )
