from aiogram import types, Dispatcher
from config import bot, ADMINS
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_base.bot_db import sql_command_all, sql_command_delete


async def pin(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in ADMINS:
            await message.answer("Ты не мой босс!")
        elif not message.reply_to_message:
            await message.answer("Команда должна быть ответом на сообщение!")
        else:
            await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
            await message.answer(f"{message.from_user.first_name} закрепил(а) сообщение "
                                 f"{message.reply_to_message.from_user.full_name}")



async def delete_data(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Ты не мой босс!")
    else:
        users = await sql_command_all()
        for user in users:
            await bot.send_message(message.from_user.id, f"{user[2]},{user[3]}, {user[4]}, {user[5]} "
                                         f"{user[6]}\n\n{user[1]}",
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(f"delete {user[0]}",
                                                          callback_data=f"delete {user[1]}")
                                 ))


async def complete_delete(call: types.CallbackQuery):
    await sql_command_delete(call.data.replace('delete ', ''))
    await call.answer(text='Удалено с БД', show_alert=True)
    await bot.delete_message(call.from_user.id, call.message.message_id)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!/')
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith('delete'))