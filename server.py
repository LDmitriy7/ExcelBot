from aiogram import executor
from handlers import dp
import middleware

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

__all__ = ['handlers', 'middleware']
