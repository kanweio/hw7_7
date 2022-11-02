from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
from data_base.bot_db import sql_command_random
from parser.securitylab import parser


# @dp.message_handler(commands=['mem'])
async def mem_command(message: types.Message):
    mem_photo = open("../media/meme.jpg", "rb")
    await bot.send_photo(message.chat.id, mem_photo)


# @dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    await bot.send_message(message.chat.id, f"Привет {message.from_user.first_name}!")


# @dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data="button_call_1")
    markup.add(button_call_1)

    question = "Как зовут кота в мультсериале про кота и мышь?"
    answers = [
        "Джерри",
        "Барсик",
        "Гав-гав",
        "Том",
        "Малыш"
    ]

    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        open_period=5,
        reply_markup=markup
    )


async def get_random_user(message: types.Message):
    await sql_command_random(message)


async def parser_news(message: types.Message):
    articles = parser()
    for item in articles:
        await message.answer(
            f"{item['year']}\n\n"
            f"{item['day']}\n"
            f"{item['link']}\n"
            f"#Y{item['time']}\n"
            f"#{item['title']}\n"
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(mem_command, commands=['mem'])
    dp.register_message_handler(get_random_user, commands=['get'])
    dp.register_message_handler(parser_news, commands=['news'])
