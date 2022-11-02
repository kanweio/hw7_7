import aioschedule
from aiogram import types, Dispatcher
from config import bot
import asyncio


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await message.answer("OK!")


async def watering_plants():
    await bot.send_message(chat_id=chat_id, text="Цветочки хотят пить:(")


async def visit_grandma():
    await bot.send_message(chat_id=chat_id, text="Пора навестить бабулю!)")


async def scheduler():
    aioschedule.every(3).days.at('18:00').do(watering_plants)
    aioschedule.every().saturday.at('09:30').do(visit_grandma)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


def register_handlers_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id,
                                lambda word: 'Напомни' in word.text)
