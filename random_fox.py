import aiohttp
import logging

# Настраиваем базовый логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_random_fox():
    api_fox = 'https://randomfox.ca/floof/'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_fox) as response:
                response.raise_for_status()  # Генерирует исключение для статусов HTTP ошибок
                data = await response.json()
                logger.info('Successfully retrieved fox data')
                data['id'] = data['link'].split('=')[-1]
                del data['link']
                return data
    except aiohttp.ClientResponseError as e:
        logger.error(f'HTTP error occurred: {e.status} {e.message}')
    except aiohttp.ClientConnectionError:
        logger.error('Connection error occurred')
    except aiohttp.ClientError as e:
        logger.error(f'An error occurred: {str(e)}')
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')

async def main():
    fox_data = await get_random_fox()
    if fox_data:
        logger.info(fox_data)
    else:
        logger.warning('No fox data received')


if __name__ == '__main__':
    import asyncio
    # Запускаем асинхронную функцию
    # asyncio.run(main())
    
    
    # class Base1:
    #     def describe(self):
    #         print(1000)
    #
    #
    # class Base2:
    #     def describe(self):
    #         print(2000)
    #
    #
    # class Combined(Base1, Base2):
    #     def describe(self):
    #         super().describe()
    #         Base2().describe()
    #         print(1)
    #
    #
    # obj = Combined()
    # obj.describe()


# class Base1:
#     def describe(self):
#         print(1000)
#
#
# class Base2:
#     def describe(self):
#         print(2000)
#
#
# class Combined(Base1, Base2):
#     def describe(self):
#         # Вызов метода describe от первого родительского класса
#         super().describe()  # Это вызовет Base1.describe()
#
#         # Вызов метода describe от второго родительского класса
#         Base2.describe(self)  # Здесь передаем текущий объект (self) явно
#
#         print(1)
#
#
# obj = Combined()
# obj.describe()

# class Base1:
#     def describe(self):
#         print(1000)
#
#
# class Base2:
#     def describe(self):
#         print(2000)
#
#
# class Combined(Base1, Base2):
#     def describe(self):
#         super().describe()  # Вызов метода describe от Base1
#         super(Base1, self).describe()  # Вызов метода describe от Base2
#         print(1)
#
#
# obj = Combined()
# obj.describe()