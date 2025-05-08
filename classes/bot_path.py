from enum import Enum
from pathlib import Path
from typing import Dict, Any

from config import Config


class BotPath(Enum):
    config: Dict[str, Any] = Config().get_config('bot')
    RESOURCES = config.get('bot_resources_dir', 'resources')
    IMAGES = Path(RESOURCES, config.get('bot_images_dir', 'images'))
    MESSAGES = Path(RESOURCES, config.get('bot_messages_dir', 'messages'))
    PROMPTS = Path(RESOURCES, config.get('bot_gpt_prompts_dir', 'prompts'))


if __name__ == '__main__':
    print(BotPath.RESOURCES)
    print(BotPath.IMAGES)
    print(BotPath.MESSAGES)
    print(BotPath.PROMPTS)

    
