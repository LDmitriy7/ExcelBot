from loader import dp
from . import commands
from . import purchase
from . import to_assortment
from . import to_reserve
from . import from_reserve
from . import remainder
from . import inventory
from . import ctrl_numbers


@dp.message_handler(state='*')
async def error(msg):
    await msg.answer('Ошибка, введите правильный ответ или сделайте сброс на /cancel')
