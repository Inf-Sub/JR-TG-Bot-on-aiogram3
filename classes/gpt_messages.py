from pathlib import Path
from classes.bot_path import BotPath
from classes.gpt_roles import GPTRole


class GPTMessage:
    def __init__(self, prompt: str):
        self.prompt_file = prompt + '.txt'
        self.message_list = self._init_message()

    def _init_message(self) -> list[dict[str, str]]:
        message = {
            'role': GPTRole.SYSTEM.value,
            'content': self._load_prompt(),
        }
        return [message]

    def _load_prompt(self) -> str:
        prompt_path = Path(BotPath.PROMPTS.value, self.prompt_file)
        with open(prompt_path, 'r', encoding='UTF-8') as file:
            prompt = file.read()
        return prompt

    def update(self, role: GPTRole, message: str):
        message = {
            'role': role.value,
            'content': message,
        }
        self.message_list.append(message)
