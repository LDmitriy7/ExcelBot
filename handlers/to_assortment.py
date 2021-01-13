from loader import dp, excel_book
from aiogram.dispatcher.filters.state import State
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts

amount = State('amount', 'to_assortment')


@dp.message_handler(text='Ушло в ассортимент')
async def to_assortment(msg: types.Message):
    await amount.set()
    await msg.answer(texts.amount_text.format('СПИСАНИЕ'))


@dp.message_handler(regexp=r'^\d+ \d+ \d+ \d+$', state=amount)
async def to_assortment_save(msg: types.Message, state: FSMContext):
    await state.update_data(amount=msg.text)

    t_data = await state.get_data()
    amount = t_data['amount']
    result = texts.form_result('Списание', amount, True, place='')
    excel_book.add_to_unlisted(result)  # запись

    await state.finish()
    await msg.answer('Готово', reply_markup=texts.main_kb)
