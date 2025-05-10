from typing import Dict

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from classes import ChatGPT, GPTMessage
from classes.enums import GPTRole
from classes.callbacks import QuizData
from classes.states import Quiz
from keyboards.inline import ikb_quiz_next

from misc import bot_thinking

from logger import logging


logging = logging.getLogger(__name__)

msg_quiz_router = Router()

@msg_quiz_router.message(Quiz.quiz_wait_for_answer)
async def msg_quiz_answer_handler(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ответ на вопрос викторины, обновляет состояние и отправляет пользователю результат.

    :param message: Сообщение, содержащее ответ пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    :return: None
    """
    await bot_thinking(message)
    await state.set_state(Quiz.quiz_wait_for_answer)
    
    current_state = await state.get_data()

    data: Dict[str, GPTMessage | QuizData | str | int] = current_state
    data['messages'].update(GPTRole.USER, message.text)

    gpt_client = ChatGPT()
    response = await gpt_client.request(data['messages'])

    data['total'] += 1
    if 'Правильно!'.lower() in response.lower() and 'неправильно!'.lower() not in response.lower():
        data['score'] += 1
        logging.debug(f'This is the correct answer! Score: {data["score"]}.')

    data['messages'].update(GPTRole.ASSISTANT, response)
    await state.update_data(data)

    print(f'msg_quiz_answer_handler:\n{message.text=}\n\n{data=}\n\n{response=}\n\n{'=' * 40}')
    
    await message.answer_photo(
        photo=data['photo'],
        caption=f'Ваш счет: {data['score']}/{data['total']}\n{response}',
        reply_markup=ikb_quiz_next(data['callback']),
        parse_mode=None
    )

    await state.set_state(Quiz.quiz_wait_press_button)
