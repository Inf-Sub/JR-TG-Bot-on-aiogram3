# from datetime import datetime

from logger import logging


logging = logging.getLogger(__name__)

def on_start():
    # formatted_date_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    logging.warning(f'Bot is started...')


def on_shutdown():
    # formatted_date_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    logging.warning(f'Bot is down now...')
    

