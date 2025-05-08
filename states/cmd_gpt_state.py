from aiogram.fsm.state import State, StatesGroup


class ChatGPTRequests(StatesGroup):
    wait_gpt_answer = State()


class CelebrityTalk(StatesGroup):
    wait_gpt_answer = State()


class Quiz(StatesGroup):
    wait_gpt_answer = State()
