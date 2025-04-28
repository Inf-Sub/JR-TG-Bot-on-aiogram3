__author__ = 'InfSub'
__contact__ = 'https:/t.me/InfSub'
__copyright__ = 'Copyright (C) 2025, [LegioNTeaM] InfSub'
__date__ = '2025/04/27'
__deprecated__ = False
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '0.0.2'

from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import MessageEntityType

from logger import logging


logging = logging.getLogger(__name__)

entities_router = Router()

@entities_router.message(F.entities)
async def catch_entities(message: Message):
    entity_dict = {}
    logging.debug(f'MESSAGE ENTITIES: {message}')
    
    for entity in message.entities:
        logging.debug(f'ENTITY: {entity}')
        
        entity_text = message.text[entity.offset:entity.offset + entity.length]
        entity_type = entity.type
        
        if entity.type in (
                MessageEntityType.EMAIL, MessageEntityType.PHONE_NUMBER, MessageEntityType.HASHTAG,
                MessageEntityType.CASHTAG
        ):
            # Инициализируем множество для этого типа, если его еще нет
            if entity_type not in entity_dict:
                entity_dict[entity_type] = set()
            # Добавляем текст сущности в соответствующее множество
            entity_dict[entity_type].add(entity_text)
            
            # Если есть найденные сущности, отправляем ответ
        if entity_dict:
            response_text = ', '.join(
                f"{entity_type.lower()}: {', '.join(texts)}" for entity_type, texts in entity_dict.items())
            await message.answer(text=f'Вы отправили: {response_text}!')


# @entities_router.message(F.entities)
# async def catch_entities(message: Message):
#     entity_text = ''
#     logging.debug(f'MESSAGE ENTITIES: {message}')
#
#     for entity in message.entities:
#         logging.debug(f'ENTITY: {entity}')
#
#         entity_type = entity.type.upper()
#         entity_dict = dict()
#
#         if entity.type == MessageEntityType.EMAIL:
#             entity_dict[entity_type] = message.text[entity.offset:entity.offset + entity.length]
#             # await message.answer(text=f'Вы отправили EMAIL: {email}!', )
#
#         if entity.type == MessageEntityType.PHONE_NUMBER:
#             entity_dict[entity_type] = message.text[entity.offset:entity.offset + entity.length]
#             # await message.answer(text=f'Вы отправили PHONE_NUMBER: {phone_number}!', )
#
#         if entity.type == MessageEntityType.HASHTAG:
#             entity_dict[entity_type] = message.text[entity.offset:entity.offset + entity.length]
#             # await message.answer(text=f'Вы отправили HASHTAG: {hash_tag}!', )
#
#         if entity.type == MessageEntityType.CASHTAG:
#             entity_dict[entity_type] = message.text[entity.offset:entity.offset + entity.length]
#             # await message.answer(text=f'Вы отправили CASHTAG: {cash_tag}!', )
#
#     await message.answer(text=f'Вы отправили {entity_dict}!', )
