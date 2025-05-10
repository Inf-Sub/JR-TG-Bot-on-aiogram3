from typing import List, Dict

from classes import Resource
from classes.enums import GPTRole


class GPTMessage:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.message_list = self._init_message()

    def _init_message(self) -> List[Dict[str, str]]:
        content = Resource(self.prompt).prompt
        message = {
            'role': GPTRole.SYSTEM.value,
            'content': content,
        }
        return [message]

    def update(self, role: GPTRole, message: str):
        message = {
            'role': role.value,
            'content': message,
        }
        self.message_list.append(message)
    
    def __str__(self):
        return f'GPTMessage(prompt="{self.prompt}", messages={self.message_list})'

    def __repr__(self):
        # return f'GPTMessage(prompt="{self.prompt}", message_list={self.message_list!r})'
        messages_repr = ",\n".join(
            [f"{{'role': '{msg['role']}', 'content': '{msg['content']}'}}" for msg in self.message_list])
        return f'GPTMessage(prompt="{self.prompt}", message_list=[\n{messages_repr}\n])'
