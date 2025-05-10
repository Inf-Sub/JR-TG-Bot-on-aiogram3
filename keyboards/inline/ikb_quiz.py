from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.bot_bottons import Button, Buttons
from classes.callbacks.bot_callback_data import QuizData, TalkWithCelebrityData

from logger import logging


logging = logging.getLogger(__name__)

def ikb_quiz_select_topic() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для выбора темы викторины.

    :return: Настроенная клавиатура с кнопками выбора тем.
    """
    logging.debug('ikb_quiz_select_topic')
    keyboard = InlineKeyboardBuilder()
    buttons_quiz_themes: List[Button] = [
        Button('Язык Python', 'quiz_prog'),
        Button('Математика', 'quiz_math'),
        Button('Биология', 'quiz_biology'),
    ]
    buttons = Buttons(buttons_quiz_themes)
    
    for button in buttons:
        logging.debug(
            f'IKB_QUIZ_SELECT_TOPIC: text={button.name=} | button="select_topic" | topic={button.callback=} | topic_name={button.name=}')
        keyboard.button(
            text=button.name,
            callback_data=QuizData(
                button='select_topic',
                topic=button.callback,
                topic_name=button.name,
            )
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_quiz_next(current_topic: QuizData) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для перехода к следующему вопросу викторины.

    :param current_topic: Данные о текущей теме викторины.
    :return: Настроенная клавиатура с действиями для викторины.
    """
    logging.debug('ikb_quiz_next')
    keyboard = InlineKeyboardBuilder()
    buttons_quiz_actions = [
        Button('Дальше', 'next_question'),
        Button('Сменить тему', 'change_topic'),
        Button('Закончить', 'finish_quiz'),
    ]
    buttons_quiz_actions = Buttons(buttons_quiz_actions)
    
    for button in buttons_quiz_actions:
        logging.debug(
            f'IKB_QUIZ_NEXT: text={button.name=} | button="select_topic" | topic={button.callback=} | topic_name={button.name=}')
        keyboard.button(
            text=button.name,
            callback_data=QuizData(
                button=button.callback,
                topic=current_topic.topic,
                topic_name=current_topic.topic_name
            ),
        )
    keyboard.adjust(2, 1)
    return keyboard.as_markup()
