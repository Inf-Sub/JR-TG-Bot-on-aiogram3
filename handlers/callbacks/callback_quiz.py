from typing import Dict

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from classes import Resource, ChatGPT, GPTMessage
from classes.enums import GPTRole
from classes.callbacks import QuizData
from classes.states import Quiz
from handlers.commands import cmd_start
from handlers.commands import cmd_quiz

from logger import logging
from misc import bot_thinking, pretty_print

logging = logging.getLogger(__name__)

callback_quiz_router = Router()
command = 'quiz'

@callback_quiz_router.callback_query(QuizData.filter(F.button == 'select_topic'))
async def quiz_callbacks(callback: CallbackQuery, callback_data: QuizData, state: FSMContext) -> None:
    logging.debug('quiz_callbacks')
    await callback.answer()
    # await state.clear()
    await state.set_state(Quiz.wait_gpt_answer)

    logging.debug(f'Received callback: "{callback.data}".')
    
    logging.debug(f'Callback Quiz Topic: {callback_data.topic=}')  # Resource(callback_data.file_name).photo
    photo = Resource(command).photo
    await callback.answer(
        text=f'Вы выбрали тему {callback_data.topic_name}!',
    )
    request_message = GPTMessage(command)
    request_message.update(GPTRole.USER, callback_data.topic)
    
    data: Dict[str, GPTMessage | QuizData | str | int] = {
        'messages': request_message, 'photo': photo, 'score': 0, 'callback': callback_data}
    
    gpt_client = ChatGPT()
    response = await gpt_client.request(data['messages'])
    data['messages'].update(GPTRole.ASSISTANT, response)

    # print(f'quiz_callbacks:\n{callback_data=}\n\n{request_message=}\n\n{data=}\n\n{response=}\n\n{'='*40}')

    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption=f'Ваш счет: {data['score']}\n{response}',
    )
    # await callback.bot.send_message(
    #     chat_id=callback.from_user.id,
    #     text=f'*QUIZ: Тема: {callback_data.topic_name}*\n\n{response}',
    # )
    
    await state.set_data(data)


@callback_quiz_router.callback_query(QuizData.filter(F.button == 'next_question'))
async def quiz_next_question(callback: CallbackQuery, state: FSMContext) -> None:
    logging.debug('quiz_next_question')
    await callback.answer()
    await state.set_state(Quiz.wait_gpt_answer)

    user_id = callback.from_user.id
    current_state = await state.get_data()
    if not current_state:
        logging.warning(f'State is not set. Handler will not be executed. Callback: "{callback.data}".')
        await callback.bot.send_message(
            chat_id=user_id,
            text=f'Извините, что-то пошло не так, начните Quiz сначала: /{command} или выберите другой раздел: /start',
        )
        return

    data: Dict[str, GPTMessage | QuizData | str | int] = current_state
    data['messages'].update(GPTRole.USER, 'quiz_more')

    gpt_client = ChatGPT()
    response = await gpt_client.request(data['messages'])
    data['messages'].update(GPTRole.ASSISTANT, response)
    try:
        await callback.bot.send_photo(
            chat_id=user_id,
            photo=data['photo'],
            caption=response,
            parse_mode=None
        )
    except Exception as e:
        logging.debug(f'{user_id=} | {data['photo']=} | {response=}.')
        logging.error(f'Failed to send photo: {e}')
    # pretty_print(data)

    # await callback.bot.send_message(
    #     chat_id=user_id,
    #     text=response,
    # )

    await callback.answer(
        text=f'Продолжаем тему {data['callback'].topic_name}'
    )
    await state.update_data(data)
   

@callback_quiz_router.callback_query(QuizData.filter(F.button == 'change_topic'))
async def quiz_change_topic(callback: CallbackQuery, state: FSMContext) -> None:
    logging.debug('quiz_change_topic')
    await callback.answer()
    message = callback.message
    await bot_thinking(message)
    await state.clear()
    await cmd_quiz(message)
   

@callback_quiz_router.callback_query(QuizData.filter(F.button == 'finish_quiz'))
async def quiz_change_topic(callback: CallbackQuery, state: FSMContext) -> None:
    logging.debug('quiz_change_topic')
    await callback.answer()
    message = callback.message
    await bot_thinking(message)
    await state.clear()
    await cmd_start(message)