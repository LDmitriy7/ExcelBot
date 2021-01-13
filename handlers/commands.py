from aiogram import types
from aiogram.dispatcher import FSMContext

import texts
from loader import dp


@dp.message_handler(commands='start')
async def send_welcome(msg: types.Message):
    await msg.answer('Приветствую', reply_markup=texts.main_kb)


@dp.message_handler(commands='get')
async def send_book(msg: types.Message):
    with open('storage/Учет закупок.xlsx', 'rb') as fp:
        await msg.answer_document(fp)


@dp.message_handler(content_types='document')
async def save_book(msg: types.Message):
    await msg.document.download('storage/Учет закупок.xlsx')
    await msg.answer('Таблица обновлена')


@dp.message_handler(commands='cancel', state='*')
async def cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer('Сброшено', reply_markup=texts.main_kb)
