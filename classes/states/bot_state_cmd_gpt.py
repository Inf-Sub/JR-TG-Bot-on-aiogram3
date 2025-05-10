from aiogram.fsm.state import State, StatesGroup


class ChatGPTRequests(StatesGroup):
    wait_gpt_answer = State()


class Random(StatesGroup):
    wait_gpt_answer = State()


class TalkWithCelebrity(StatesGroup):
    wait_gpt_answer = State()


class Quiz(StatesGroup):
    quiz_select_topic = State()
    quiz_wait_for_answer = State()
    quiz_wait_press_button = State()
