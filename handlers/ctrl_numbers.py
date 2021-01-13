from loader import dp
from aiogram.dispatcher.filters.state import State
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts

amount = State('amount', 'ctrl_numbers')


@dp.message_handler(text='Контрольные числа')
async def start_purchase(msg: types.Message):
    with open('storage/ctrl_numbers.txt') as fp:
        a1, a2, a3, a4 = fp.read().split()
    text = f'<b>Текущие числа:</b>\nБаза = {a1}\nТоп = {a2}\nЗолото = {a3}\nЗапонки = {a4}'
    await msg.answer(text, reply_markup=texts.change_kb)


@dp.callback_query_handler(text='change:ctrl_numbers')
async def save_amount1(query: types.CallbackQuery):
    await amount.set()
    await query.message.answer(texts.amount_text.format('КОНТРОЛЬНЫЕ ЧИСЛА'))


@dp.message_handler(regexp=r'^\d+ \d+ \d+ \d+$', state=amount)
async def save_amount2(msg: types.Message, state: FSMContext):
    with open('storage/ctrl_numbers.txt', 'w') as fp:
        fp.write(msg.text)
    await state.finish()
    await msg.answer('Сохранено', reply_markup=texts.main_kb)
