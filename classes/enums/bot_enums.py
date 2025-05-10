from enum import Enum
from pathlib import Path
from typing import Dict, Any
from config import Config


class ResourcePath(Enum):
    _config: Dict[str, Any] = Config().get_config('folders')
    RESOURCES = Path(_config.get('bot_resources_dir', 'resources'))
    IMAGES = Path(RESOURCES, _config.get('bot_images_dir', 'images'))
    MESSAGES = Path(RESOURCES, _config.get('bot_messages_dir', 'messages'))
    PROMPTS = Path(RESOURCES, _config.get('bot_prompts_dir', 'prompts'))


class GPTRole(Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'


class Extensions(Enum):
    JPG = '.jpg'
    TXT = '.txt'
