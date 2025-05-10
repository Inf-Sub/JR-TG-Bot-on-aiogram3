from .states import ChatGPTRequests, Random, TalkWithCelebrity, Quiz
from .callbacks import TalkWithCelebrityData, QuizData
from .enums import ResourcePath, Extensions, GPTRole
from .bot_resources import Resource
from .gpt_messages import GPTMessage
from .gpt_openai import ChatGPT
from .bot_bottons import Button, Buttons


# gpt_client = ChatGPT()

__all__ = [
    'ChatGPTRequests',
    'Random',
    'TalkWithCelebrity',
    'Quiz', 'TalkWithCelebrityData',
    'QuizData',
    'ResourcePath',
    'Extensions',
    'GPTRole',
    'Resource',
    'GPTMessage',
    'ChatGPT',
    'Button',
    'Buttons',
]
