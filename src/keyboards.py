from misc import COMMANDS

from aiogram.types import ReplyKeyboardMarkup


back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
back_keyboard.add(COMMANDS['back'])


parser_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
parser_keyboard.add(COMMANDS['delete'], COMMANDS['back'])


def _get_text(value, values, text=None):
    if value in values:
        return f'✅ {text or value}'
    return text or value


def get_parsers_kb(parsers):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for index, parser in enumerate(parsers):
        keyboard.insert(f'#{index + 1} {parser.collection}')
    keyboard.insert(COMMANDS['new_parser'])
    return keyboard


def get_fields_kb(fields, current_fields):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.insert(_get_text('min_price', current_fields, COMMANDS['min_price']))
    keyboard.insert(_get_text('max_price', current_fields, COMMANDS['max_price']))
    keyboard.row()

    for field in fields:
        keyboard.insert(_get_text(field, current_fields))

    keyboard.add(COMMANDS['back'], COMMANDS['save'])
    return keyboard


def get_values_kb(values, current_values):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for value in values:
        keyboard.insert(_get_text(value, current_values))
    keyboard.insert(COMMANDS['back'])
    return keyboard