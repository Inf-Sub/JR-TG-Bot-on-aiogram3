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

@msg_quiz_router.message(Quiz.wait_gpt_answer)
async def msg_quiz_answer_handler(message: Message, state: FSMContext):
    logging.debug('msg_quiz_answer_handler')
    await bot_thinking(message)
    await state.set_state(Quiz.wait_gpt_answer)
    
    user_id = message.from_user.id
    current_state = await state.get_data()
    if not current_state:
        logging.warning(f'State is not set. Handler will not be executed.')
        await message.bot.send_message(
            chat_id=user_id,
            text='Выберите тему в меню выше 👆 или начните тестирование снова: /quiz.\n'
                 'Или воспользуйтесь меню по команде:\n/start',
            # text='Извините, что-то пошло не так, начните проверку снова: /quiz или выберите другой раздел: /start',
        )
        await state.clear()
        return

    data: Dict[str, GPTMessage | QuizData | str | int] = current_state
    data['messages'].update(GPTRole.USER, message.text)

    gpt_client = ChatGPT()
    response = await gpt_client.request(data['messages'])

    logging.debug(f'{response=}')
    if 'Правильно!'.lower() in response.lower():
        data['score'] += 1
        logging.debug(f'This is the correct answer! Score: {data["score"]}.')

    data['messages'].update(GPTRole.ASSISTANT, response)
    await state.update_data(data)

    # print(f'msg_quiz_answer_handler:\n{message.text=}\n\n{data=}\n\n{response=}\n\n{'=' * 40}')
    
    await message.answer_photo(
        photo=data['photo'],
        caption=f'Ваш счет: {data['score']}\n{response}',
        reply_markup=ikb_quiz_next(data['callback']),
        parse_mode=None
    )
