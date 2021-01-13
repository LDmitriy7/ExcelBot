from loader import dp, excel_book
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts


class Purchase(StatesGroup):
    amount = State()
    term = State()
    place = State()


@dp.message_handler(text='Закупка')
async def start_purchase(msg: types.Message):
    await Purchase.amount.set()
    await msg.answer(texts.amount_text.format('ЗАКУПКА'))


@dp.message_handler(regexp=r'^\d+ \d+ \d+ \d+$', state=Purchase.amount)
async def save_amount(msg: types.Message, state: FSMContext):
    await state.update_data(amount=msg.text)
    await Purchase.next()
    await msg.answer(texts.term_text, reply_markup=texts.term_kb)


@dp.message_handler(text=texts.term_buttons, state=Purchase.term)
async def save_term(msg: types.Message, state: FSMContext):
    await state.update_data(term=msg.text)
    await Purchase.next()
    await msg.answer(texts.place_text)


@dp.message_handler(state=Purchase.place)
async def save_place(msg: types.Message, state: FSMContext):
    await state.update_data(place=msg.text)

    t_data = await state.get_data()
    amount, place, term = t_data['amount'], t_data['place'], t_data['term']
    result = texts.form_result('Закупка', amount, place=place, term=term)
    excel_book.add_to_unlisted(result)  # запись

    await state.finish()
    await msg.answer('Готово', reply_markup=texts.main_kb)
