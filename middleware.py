from loader import dp
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler


class CheckID(BaseMiddleware):
    @staticmethod
    async def on_pre_process_message(msg: types.Message, *args):
        print(msg.from_user.id)
        if msg.from_user.id not in [724477101, 199585821, 333564520]:
            raise CancelHandler

    @staticmethod
    async def on_pre_process_callback_query(query: types.CallbackQuery, *args):
        if query.from_user.id not in [724477101, 199585821, 333564520]:
            raise CancelHandler


dp.setup_middleware(CheckID())
