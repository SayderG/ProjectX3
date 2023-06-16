import asyncio
from aiogram import Dispatcher
from aiogram.types import Message


async def gen_map():
    await asyncio.sleep(10)
    return 'https://yandex.ru'


async def start_message(message: Message):
    my_message = await message.answer('Создаем карту')
    maps = await gen_map()
    while not maps:
        await my_message.edit_text('Создаем карту...')
        await asyncio.sleep(0.4)
        await my_message.edit_text('Создаем карту..')
        await asyncio.sleep(0.4)
        await my_message.edit_text('Создаем карту.')
        if maps:
            await message.edit_text(maps)
            return


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=["start"], state="*")
