from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot, ADMINS
from keyboards.client_kb import submit_markup, cancel_markup
from data_base.bot_db import sql_command_insert


# FSM - Finite State Machine

class FSMAdmin(StatesGroup):
    imya = State()
    id = State()
    age = State()
    direction = State()
    grupa = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id not in ADMINS:
            await message.answer("Ты не мой босс!")
        else:
            await FSMAdmin.imya.set()
            await message.answer(
                f"Привет {message.from_user.full_name}, "
                f"Имя ментора: ",
                reply_markup=cancel_markup
            )
    else:
        await message.answer('Напишите в ЛС')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['imya'] = message.text
    await FSMAdmin.next()
    await message.answer('id ментора: ')


async def load_id(message: types.Message, state: FSMContext):
    try:
        if not 1 < int(message.text) < 10000000:
            await message.answer('Введите ID!')
            return

        async with state.proxy() as data:
            data['id'] = int(message.text)
        await FSMAdmin.next()
        await message.answer('Возраст ментора: ')
    except:
        await message.answer('Используйте числа')


async def load_age(message: types.Message, state: FSMContext):
    try:
        if not 16 < int(message.text) < 100:
            await message.answer('Ментор должен быть старше 16!')
        else:
            async with state.proxy() as data:
                data['age'] = int(message.text)
            await FSMAdmin.next()
            await message.answer('Направление ментора?')
    except:
        await message.answer('Пиши числа!')


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
        await FSMAdmin.next()
        await message.answer('Группа: ')


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['grupa'] = message.text
        await bot.send_message(message.from_user.id,
                               f"Имя: {data['imya']},  ID: {data['id']}, Возраст: {data['age']},"
                               f"Направление: {data['direction']},"
                               f"Группа: {data['grupa']}\n")
    await FSMAdmin.next()
    await message.answer('Все верно?', reply_markup=submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await sql_command_insert(state)
        await state.finish()
        await message.answer('Регистрация завершена')
    elif message.text.lower() == 'нет':
        await state.finish()
        await message.answer('Отменено')
    else:
        await message.answer('Ошибка')


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено')


def register_handlers_fsm_anketa(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True),
                                state='*')


    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.imya)
    dp.register_message_handler(load_id, state=FSMAdmin.id)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_group, state=FSMAdmin.grupa)
    dp.register_message_handler(submit, state=FSMAdmin.submit)
