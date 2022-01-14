from misc import dp
from models import User

from aiogram.types import Message


@dp.message_handler(state='*')
async def default_handler(message: Message):
    _, created = User.get_or_create(user_id=message.from_user.id)

    if created:
        await message.answer('Добро пожаловать')
    else:
        await message.answer('Не уверен, что я тебя понимаю')