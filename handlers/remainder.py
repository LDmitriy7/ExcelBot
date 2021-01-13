from loader import dp, excel_book
from aiogram import types
import texts


def get_ctrl_numbers(term: str):
    """term может быть = [на сегодня, на 1 неделю, на 2 недели, на 3 недели, на 4 недели]"""
    with open('storage/ctrl_numbers.txt') as fp:
        ctrl_numbers = fp.read().split()

    if term in ['на сегодня', 'в резерве']:
        factor = 1
    else:
        factor = int(term.split()[1]) + 1
    return [int(num) * factor for num in ctrl_numbers]


@dp.message_handler(text='Показать остатки')
async def remaining(msg: types.Message):
    await msg.answer('Посмотреть остатки:', reply_markup=texts.remainder_kb)


@dp.message_handler(text=texts.remainder_buttons)
async def send_remainder(msg: types.Message):
    term = msg.text.lower()
    if term == 'в резерве':
        a1, a2, a3, a4 = excel_book.get_reserve()
    else:
        a1, a2, a3, a4 = excel_book.get_unlisted(term)

    c1, c2, c3, c4 = get_ctrl_numbers(term)
    d1, d2, d3, d4 = a1 - c1, a2 - c2, a3 - c3, a4 - c4

    text = f"""
<b>Остатки {term}:</b>
База = {a1} ({d1:+})
Топ = {a2} ({d2:+})
Золото = {a3} ({d3:+})
Запонки = {a4} ({d4:+})
"""
    await msg.answer(text, reply_markup=texts.main_kb)
