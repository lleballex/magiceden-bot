from misc import dp
from models import Parser
from states import MainStates
from keyboards import get_parsers_kb
from keyboards import parser_keyboard
from misc import ADMIN, PARSERS, DEBUG, COMMANDS as CMDS

from aiogram.types import Message
from aiogram.dispatcher import FSMContext 


@dp.message_handler(commands=['admin'], state='*')
async def admin(message: Message, state: FSMContext):
    await state.finish()

    if DEBUG or message.from_user.id == ADMIN:
        await message.answer('Выбери коллекцию или создай новую',
                             reply_markup=get_parsers_kb(PARSERS))
        await MainStates.action_wait.set()
    else:
        await message.answer('Эй, это только для админов!')


@dp.message_handler(lambda message: message.text.startswith('#'), state=MainStates.action_wait)
async def show_parser(message: Message, state: FSMContext):
    try:
        index = int(message.text.split()[0].replace('#', '')) - 1
    except ValueError:
        await message.answer('Хм... Что-то не так')
    else:
        await state.update_data(index=index)
        await message.answer(PARSERS[index].get_text(), reply_markup=parser_keyboard)
        await MainStates.parser_view.set()


@dp.message_handler(lambda message: message.text == CMDS['back'], state=MainStates.parser_view)
async def to_admin(message: Message, state: FSMContext):
    await admin(message, state)


@dp.message_handler(lambda message: message.text == CMDS['delete'], state=MainStates.parser_view)
async def delete_parser(message: Message, state: FSMContext):
    index = (await state.get_data())['index']
    Parser.get(Parser.id == PARSERS.pop(index).id).delete_instance()
    await admin(message, state)