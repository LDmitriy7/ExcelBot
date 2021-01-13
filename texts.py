from aiogram import types
from datetime import date, timedelta

main_buttons = ['Закупка',
                'Ушло в ассортимент',
                'Ушло в резерв',
                'Вернулось из резерва',
                'Показать остатки',
                'Инвентаризация',
                'Контрольные числа']
main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_kb.add(*main_buttons)

remainder_buttons = ['В резерве', 'На сегодня', 'На 1 неделю', 'На 2 недели', 'На 3 недели', 'На 4 недели']
remainder_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
remainder_kb.add(*remainder_buttons)

amount_text = """{}. Внесите количество по каждой категории:
<b>База, Топ, Золото, Запонки</b>
(4 числа через пробел)
"""

term_text = 'Выберите срок попадания в невыложенные'
term_buttons = ['Сразу', '1 неделя', '2 недели', '3 недели', '4 недели']
term_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
term_kb.add(*term_buttons)

place_text = 'Где произведена закупка?'

change_kb = types.InlineKeyboardMarkup()
change_kb.add(types.InlineKeyboardButton('Изменить', callback_data='change:ctrl_numbers'))

inventory_buttons = ['Невыложенные товары', 'Резерв']
inventory_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
inventory_kb.add(*inventory_buttons)


def form_result(article: str, amount: str, negative=False, place: str = None, term: str = None):
    """Если поле=None, то оно будет пропущено
    term может быть = [Сразу, 1 неделя, 2 недели, 3 недели, 4 недели]
    """
    today = date.today()

    if negative:
        amounts = [-int(i) for i in amount.split()]
    else:
        amounts = [int(i) for i in amount.split()]

    def get_date_from_term(term: str) -> date:
        if term == 'Сразу':
            return today
        weeks = int(term.split()[0])
        return today + timedelta(weeks=weeks)

    result = [today, article, *amounts]

    if place is not None:
        result.insert(2, place)

    if term is not None:
        result.append(get_date_from_term(term))

    return result

# def format_date(date):
#     date = str(date).split('-')
#     date = date[::-1]
#     return '.'.join(date)
