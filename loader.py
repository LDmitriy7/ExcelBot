from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from excel_worker import ExcelBook

TOKEN = '1576619439:AAHclWhqTWpd9JSJTNgBT5Ok3Hyryl-uhA8'
bot = Bot(TOKEN, parse_mode='Html')
storage = JSONStorage('storage/storage.json')
dp = Dispatcher(bot, storage=storage)
excel_book = ExcelBook('storage/Учет закупок.xlsx')
