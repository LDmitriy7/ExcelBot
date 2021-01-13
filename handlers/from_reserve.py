from loader import dp, excel_book
from aiogram.dispatcher.filters.state import State
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts

amount = State('amount', 'from_reserve')


@dp.message_handler(text='Вернулось из резерва')
async def to_assortment(msg: types.Message):
    await amount.set()
    await msg.answer(texts.amount_text.format('ИЗ РЕЗЕРВА'))


@dp.message_handler(regexp=r'^\d+ \d+ \d+ \d+$', state=amount)
async def to_assortment_save(msg: types.Message, state: FSMContext):
    await state.update_data(amount=msg.text)

    t_data = await state.get_data()
    amount = t_data['amount']

    result = texts.form_result('Из резерва', amount, place='', term='Сразу')
    excel_book.add_to_unlisted(result)  # запись

    result = texts.form_result('Уход', amount, True)
    excel_book.add_to_reserve(result)  # запись

    await state.finish()
    await msg.answer('Готово', reply_markup=texts.main_kb)
