from misc import dp
from .main import admin
from core.parser import Parser
from keyboards import back_keyboard
from models import Parser as ParserModel
from misc import PARSERS, COMMANDS as CMDS
from states import MainStates, CreateParser
from keyboards import get_fields_kb, get_values_kb

import requests
from aiogram.types import Message
from aiogram.dispatcher import FSMContext


def get_fields(collection):
    response = requests.get(f'https://api-mainnet.magiceden.io/rpc/getCollectionEscrowStats/{collection}')

    if response.status_code != 200:
        return (False, response.status_code)
    if response.json() == {}:
        return (False, '"КОЛЛЕКЦИЯ НЕ НАЙДЕНА"')

    fields = {}

    for i in response.json()['results']['availableAttributes']:
        title = i['attribute']['trait_type']
        value = i['attribute']['value']

        if not fields.get(title):
            fields[title] = [i['attribute']['value']]
        else:
            fields[title].append(i['attribute']['value'])

    return (True, fields)


@dp.message_handler(lambda message: message.text == CMDS['new_parser'], state=MainStates.action_wait)
async def create_parser(message: Message):
    await message.answer('Как называется коллекция', reply_markup=back_keyboard)
    await CreateParser.collection.set()


@dp.message_handler(lambda message: message.text == CMDS['back'], state=CreateParser.collection)
@dp.message_handler(lambda message: message.text == CMDS['back'], state=CreateParser.field)
async def to_admin(message: Message, state=FSMContext):
    await admin(message, state)


@dp.message_handler(state=CreateParser.collection)
async def add_collection(message: Message, state: FSMContext):
    result = get_fields(message.text)

    if not result[0]:
        await message.answer(f'Ой-ой... Что-то пошло не так - код {result[1]}')
    else:
        await state.update_data(fields=result[1], current_fields={}, collection=message.text)
        await show_fields(message, result[1], [])


async def show_fields(message, fields, current_fields):
    await message.answer('Что дальше?', reply_markup=get_fields_kb(fields, current_fields))
    await CreateParser.field.set()


@dp.message_handler(lambda message: message.text == CMDS['save'], state=CreateParser.field)
async def save_parser(message: Message, state: FSMContext):
    data = await state.get_data()

    parser = Parser(data['collection'], data.get('current_fields', {}))
    result = parser.parse(initial=True)

    if result[0]:
        model = ParserModel.create(collection=parser.collection, filters=parser.filters)
        parser.id = model.id
        PARSERS.append(parser)
        await to_admin(message, state)
    else:
        await message.answer(f'Что-то пошло не так - код {result[1]}. Попробуй повторить попытку')


@dp.message_handler(state=CreateParser.field)
async def show_values(message: Message, state=FSMContext):
    data = await state.get_data()

    if message.text.startswith('✅ '):
        message.text = message.text[2:]

    fields = data['fields']
    current_fields = data.get('current_fields', {}).get(message.text, [])

    if fields.get(message.text):
        await state.update_data(field=message.text)
        await message.answer('Выбери значение',
                             reply_markup=get_values_kb(fields[message.text], current_fields))
        await CreateParser.value.set()
    elif message.text in [CMDS['min_price'], CMDS['max_price']]:
        await message.answer('Напиши нужную цену', reply_markup=back_keyboard)
        if message.text == CMDS['min_price']:
            await CreateParser.min_price.set()
        else:
            await CreateParser.max_price.set()
    else:
        await message.answer('Такой фильтр установить нельзя')


@dp.message_handler(lambda message: message.text == CMDS['back'], state=CreateParser.value)
@dp.message_handler(lambda message: message.text == CMDS['back'], state=CreateParser.min_price)
@dp.message_handler(lambda message: message.text == CMDS['back'], state=CreateParser.max_price)
async def to_fields(message: Message, state: FSMContext):
    data = await state.get_data()
    await show_fields(message, data['fields'], data['current_fields'])


@dp.message_handler(state=CreateParser.value)
async def set_value(message: Message, state=FSMContext):
    data = await state.get_data()

    field = data['field']
    fields = data['fields']
    current_fields = data.get('current_fields', {})

    if message.text.startswith('✅ '):
        message.text = message.text[2:]

    if not message.text in fields[field]:
        return await message.answer('Такой вариант не подойдет')

    if current_fields.get(field):
        if message.text in current_fields[field]:
            current_fields[field].remove(message.text)
            if not current_fields[field]:
                current_fields.pop(field)
        else:
            current_fields[field].append(message.text)
    else:
        current_fields[field] = [message.text]

    await state.update_data(current_fields=current_fields)
    await message.answer('Что дальше?',
                         reply_markup=get_values_kb(fields[field], current_fields.get(field, [])))


@dp.message_handler(state=CreateParser.min_price)
async def set_min_price(message: Message, state: FSMContext):
    fields = (await state.get_data()).get('current_fields', {})

    try:
        value = float(message.text)
    except ValueError:
        await message.answer('Нужно напсать число')
    else:
        if not value:
            if not fields.get('min_price', None) is None: fields.pop('min_price')
        else:
            fields['min_price'] = value
        await state.update_data(current_fields=fields)
        await to_fields(message, state)


@dp.message_handler(state=CreateParser.max_price)
async def set_max_price(message: Message, state: FSMContext):
    fields = (await state.get_data()).get('current_fields', {})

    try:
        value = float(message.text)
    except ValueError:
        await message.answer('Нужно напсать число')
    else:
        if not value:
            if not fields.get('max_price', None) is None: fields.pop('max_price')
        else:
            fields['max_price'] = value
        await state.update_data(current_fields=fields)
        await to_fields(message, state)