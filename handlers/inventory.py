from loader import dp, excel_book
from aiogram import types
import texts
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class Inventory(StatesGroup):
    choice = State()
    unlisted = State()
    reserve = State()


@dp.message_handler(text='Инвентаризация')
async def inventory1(msg: types.Message):
    await Inventory.choice.set()
    await msg.answer('Выберите таблицу:', reply_markup=texts.inventory_kb)


@dp.message_handler(text=texts.inventory_buttons, state=Inventory.choice)
async def inventory2(msg: types.Message):
    if msg.text == 'Невыложенные товары':
        await Inventory.unlisted.set()
    if msg.text == 'Резерв':
        await Inventory.reserve.set()
    await msg.answer(texts.amount_text.format('ИНВЕНТАРИЗАЦИЯ'))


@dp.message_handler(regexp=r'^\d+ \d+ \d+ \d+$', state=Inventory.unlisted)
async def inv_unlisted(msg: types.Message, state: FSMContext):
    a1, a2, a3, a4 = [int(i) for i in msg.text.split()]
    b1, b2, b3, b4 = excel_book.get_unlisted('на сегодня')
    diff_amount = [str(i) for i in (a1 - b1, a2 - b2, a3 - b3, a4 - b4)]
    diff_amount = ' '.join(diff_amount)

    result = texts.form_result('Коррекция', diff_amount, place='')
    excel_book.add_to_unlisted(result)  # запись
    await state.finish()
    await msg.answer('Готово', reply_markup=texts.main_kb)


@dp.message_handler(regexp=r'^\d+ \d+ \d+ \d+$', state=Inventory.reserve)
async def inv_reserve(msg: types.Message, state: FSMContext):
    a1, a2, a3, a4 = [int(i) for i in msg.text.split()]
    b1, b2, b3, b4 = excel_book.get_reserve()
    diff_amount = [str(i) for i in (a1 - b1, a2 - b2, a3 - b3, a4 - b4)]
    diff_amount = ' '.join(diff_amount)

    result = texts.form_result('Коррекция', diff_amount)
    excel_book.add_to_reserve(result)  # запись
    await state.finish()
    await msg.answer('Готово', reply_markup=texts.main_kb)
