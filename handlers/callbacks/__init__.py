from .callback_celebrity import callback_celebrity_router
from .callback_quiz import callback_quiz_router
from handlers.missed.missed_callbacks import missed_callbacks_router  # for test


__all__ = [
    'callback_celebrity_router',
    'callback_quiz_router',
    # for test
    'missed_callbacks_router',
]
